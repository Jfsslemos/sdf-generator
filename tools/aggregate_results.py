#!/usr/bin/env python3
"""Build deterministic, provenance-backed dissertation result summaries.

The input is one result directory. Missing artifacts remain explicit PENDING
values; malformed, non-finite, or ambiguous evidence aborts aggregation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import defaultdict
from pathlib import Path

STATUSES = ("AVAILABLE", "PENDING", "NOT_EXECUTED", "NOT_APPLICABLE")
OFFICIAL = ("PSNR", "SSIM", "LPIPS", "AP50", "AP75", "AP80", "AP85", "AP90", "AP95")
RENDER = OFFICIAL[:3]
DECOMPOSITION = OFFICIAL[3:]
DISTANCES = (
    "mean_pred_to_gt", "mean_gt_to_pred", "chamfer_l1_symmetric",
    "rmse_pred_to_gt", "rmse_gt_to_pred",
)
FLOOR_METRICS = ("mean_abs_distance", "rmse_distance", "p95_abs_distance", "inlier_fraction")
EXCLUDED_RUN_MARKERS = {"smoke", "pilot", "amp_pilot", "benchmark"}


def _reject_constant(value):
    raise ValueError(f"Non-finite JSON constant: {value}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def require_number(value, label, *, nonnegative=False):
    if not finite_number(value) or (nonnegative and value < 0):
        raise ValueError(f"Invalid finite numeric value for {label}: {value!r}")
    return value


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cell(value=None, status=None, sources=(), unit=None, note=None):
    if status is None:
        status = "AVAILABLE" if value is not None else "PENDING"
    if status not in STATUSES:
        raise ValueError(f"Invalid result status: {status}")
    result = {"status": status, "value": value, "sources": sorted(set(sources))}
    if unit is not None:
        result["unit"] = unit
    if note is not None:
        result["note"] = note
    return result


class Sources:
    def __init__(self, root: Path):
        self.root = root
        self.records = {}

    def add(self, path: Path, role: str):
        path = path.resolve()
        try:
            relative = path.relative_to(self.root).as_posix()
        except ValueError as exc:
            raise ValueError(f"Source outside result directory: {path}") from exc
        record = self.records.setdefault(relative, {
            "path": relative, "sha256": sha256(path), "bytes": path.stat().st_size, "roles": [],
        })
        if role not in record["roles"]:
            record["roles"].append(role)
            record["roles"].sort()
        return relative

    def sorted(self):
        return [self.records[key] for key in sorted(self.records)]


def discover(root: Path, output: Path, basename: str):
    found = []
    for path in root.rglob(basename):
        if not path.is_file():
            continue
        try:
            path.resolve().relative_to(output)
            continue
        except ValueError:
            pass
        found.append(path.resolve())
    return sorted(found, key=lambda item: item.relative_to(root).as_posix())


def scientific(paths, root):
    paths = [path for path in paths if not EXCLUDED_RUN_MARKERS.intersection(
        part.lower() for part in path.relative_to(root).parts
    )]
    experiment = [path for path in paths if "experiment" in (part.lower() for part in path.relative_to(root).parts)]
    return experiment or paths


def select_single(paths, role, root, *, allow_identical=True):
    if not paths:
        return None
    by_hash = defaultdict(list)
    for path in paths:
        by_hash[sha256(path)].append(path)
    if len(by_hash) > 1:
        names = ", ".join(path.relative_to(root).as_posix() for path in paths)
        raise ValueError(f"Ambiguous {role}: multiple different candidates: {names}")
    if not allow_identical and len(paths) > 1:
        raise ValueError(f"Ambiguous {role}: multiple candidates")
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())[0]


def parse_official(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["view", *OFFICIAL]:
            raise ValueError(f"Unexpected official metrics header in {path}")
        rows = list(reader)
    means = [row for row in rows if row["view"].strip().lower() == "mean"]
    views = [row for row in rows if row["view"].strip().lower() != "mean"]
    if len(means) != 1 or not views:
        raise ValueError("Official evaluator CSV requires view rows and exactly one mean row")
    values = {}
    for key in OFFICIAL:
        try:
            value = float(means[0][key])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid official metric {key}") from exc
        values[key] = require_number(value, key)
    return values, len(views)


def parse_jsonl(path: Path):
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line, parse_constant=_reject_constant))
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"Invalid JSONL {path}:{line_number}: {exc}") from exc
    return rows


def training_from_logs(paths, source_paths):
    unique = {}
    for path, source in zip(paths, source_paths):
        unique.setdefault(sha256(path), (path, source))
    logs = [(path, source, parse_jsonl(path)) for path, source in unique.values()]
    # Reject overlapping snapshots rather than counting replayed copies twice.
    seen = set()
    segments = []
    all_rows = []
    for path, source, rows in sorted(logs, key=lambda item: item[1]):
        current = []
        for row in rows:
            signature = json.dumps(row, sort_keys=True, allow_nan=False)
            if signature in seen:
                raise ValueError(f"Overlapping training logs include the same row: {source}")
            seen.add(signature)
            for key in ("iteration", "elapsed_seconds", "effective_updates", "skipped_updates", "max_vram_bytes"):
                require_number(row.get(key), f"training.{key}", nonnegative=True)
            if not isinstance(row.get("optimizer_step_applied"), bool):
                raise ValueError("Training row lacks boolean optimizer_step_applied")
            if current and (row["elapsed_seconds"] < current[-1]["elapsed_seconds"] or
                            row["iteration"] <= current[-1]["iteration"]):
                segments.append((source, current))
                current = []
            if current:
                previous = current[-1]
                if row["iteration"] != previous["iteration"] + 1:
                    raise ValueError("Training log has an iteration gap inside a process segment")
                if row["effective_updates"] - previous["effective_updates"] != int(row["optimizer_step_applied"]):
                    raise ValueError("Inconsistent effective_updates counter")
                if row["skipped_updates"] - previous["skipped_updates"] != int(not row["optimizer_step_applied"]):
                    raise ValueError("Inconsistent skipped_updates counter")
            current.append(row)
            all_rows.append(row)
        if current:
            segments.append((source, current))
    if not all_rows:
        return None
    elapsed = sum(rows[-1]["elapsed_seconds"] for _, rows in segments)
    require_number(elapsed, "training elapsed", nonnegative=True)
    observed = len(all_rows)
    return {
        "observed_iterations": observed,
        "observed_process_segments": len(segments),
        "training_time_seconds": elapsed,
        "iterations_per_second": observed / elapsed if elapsed > 0 else None,
        "seconds_per_iteration": elapsed / observed,
        "observed_updates": sum(int(row["optimizer_step_applied"]) for row in all_rows),
        "observed_skips": sum(int(not row["optimizer_step_applied"]) for row in all_rows),
        "peak_pytorch_vram_bytes": max(row["max_vram_bytes"] for row in all_rows),
    }


def parse_gpu_csv(paths, registry):
    per_gpu = defaultdict(lambda: {"memory": [], "utilization": [], "sources": set()})
    for path in paths:
        source = registry.add(path, "gpu_telemetry")
        with path.open(newline="", encoding="utf-8", errors="replace") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise ValueError(f"GPU telemetry has no header: {source}")
            fields = {name.strip(): name for name in reader.fieldnames}
            name_field = next((raw for clean, raw in fields.items() if clean == "name"), None)
            memory_field = next((raw for clean, raw in fields.items() if clean.startswith("memory.used")), None)
            utilization_field = next((raw for clean, raw in fields.items() if clean.startswith("utilization.gpu")), None)
            if not (name_field and memory_field and utilization_field):
                raise ValueError(f"Unexpected GPU telemetry header: {source}")
            for row in reader:
                name = row[name_field].strip()
                if not name:
                    raise ValueError(f"GPU telemetry row lacks name: {source}")
                def number(raw, label):
                    match = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", raw or "")
                    if not match:
                        raise ValueError(f"Invalid GPU {label}: {raw!r}")
                    return require_number(float(match.group()), f"gpu.{label}", nonnegative=True)
                per_gpu[name]["memory"].append(number(row[memory_field], "memory_mib"))
                per_gpu[name]["utilization"].append(number(row[utilization_field], "utilization_percent"))
                per_gpu[name]["sources"].add(source)
    return [{
        "gpu_name": name,
        "samples": len(values["memory"]),
        "peak_memory_mib": max(values["memory"]),
        "mean_utilization_percent": sum(values["utilization"]) / len(values["utilization"]),
        "sources": sorted(values["sources"]),
    } for name, values in sorted(per_gpu.items())]


def condition_from_path(path: Path, root: Path):
    tokens = re.split(r"[^a-z0-9]+", path.relative_to(root).as_posix().lower())
    for condition in ("a0", "a1", "a2"):
        if condition in tokens:
            return condition.upper()
    if "colmap" in tokens or "baseline" in tokens:
        return "baseline"
    return "unassigned"


def section_status(items):
    return "AVAILABLE" if items else "PENDING"


def aggregate(input_dir: Path, output_dir: Path):
    root = input_dir.resolve()
    output = output_dir.resolve()
    if not root.is_dir():
        raise ValueError(f"Input result directory does not exist: {input_dir}")
    registry = Sources(root)

    state_candidates = scientific(discover(root, output, "training_state.json"), root)
    states = []
    for path in state_candidates:
        data = load_json(path)
        for key in ("iteration", "effective_updates", "skipped_updates", "elapsed_seconds", "max_vram_bytes"):
            require_number(data.get(key), f"training_state.{key}", nonnegative=True)
        states.append((data["iteration"], path, data))
    final_state = max(states, key=lambda item: (item[0], item[1].relative_to(root).as_posix())) if states else None
    if len([item for item in states if item[0] == final_state[0]]) > 1 if final_state else False:
        peers = [item for item in states if item[0] == final_state[0]]
        canonical = {json.dumps(item[2], sort_keys=True) for item in peers}
        if len(canonical) > 1:
            raise ValueError("Conflicting training_state.json files for the final iteration")

    log_paths = scientific(discover(root, output, "training.jsonl"), root)
    log_sources = [registry.add(path, "training_log") for path in log_paths]
    log_metrics = training_from_logs(log_paths, log_sources) if log_paths else None
    state_source = registry.add(final_state[1], "training_state") if final_state else None
    training_sources = sorted(set(log_sources + ([state_source] if state_source else [])))
    state = final_state[2] if final_state else {}
    training_values = {
        "final_iteration": state.get("iteration"),
        "target_iterations": state.get("target_steps"),
        "effective_updates": state.get("effective_updates"),
        "amp_skips": state.get("skipped_updates"),
        "amp_skip_fraction": (state["skipped_updates"] / (state["effective_updates"] + state["skipped_updates"]))
            if state.get("effective_updates") is not None and state.get("skipped_updates") is not None and
               state["effective_updates"] + state["skipped_updates"] > 0 else None,
        "training_time_seconds": log_metrics.get("training_time_seconds") if log_metrics else None,
        "iterations_per_second": log_metrics.get("iterations_per_second") if log_metrics else None,
        "seconds_per_iteration": log_metrics.get("seconds_per_iteration") if log_metrics else None,
        "peak_pytorch_vram_bytes": max(
            [value for value in (state.get("max_vram_bytes"),
                                 log_metrics.get("peak_pytorch_vram_bytes") if log_metrics else None)
             if value is not None], default=None),
    }
    units = {
        "training_time_seconds": "s", "iterations_per_second": "iteration/s",
        "seconds_per_iteration": "s/iteration", "peak_pytorch_vram_bytes": "byte",
        "amp_skip_fraction": "fraction",
    }
    training = {
        "status": "AVAILABLE" if training_sources else "PENDING",
        "scope": "train",
        "complete": cell(state.get("complete"), sources=[state_source] if state_source else []),
        "stopped_for_budget": cell(state.get("stopped_for_budget"), sources=[state_source] if state_source else []),
        "metrics": {key: cell(value, sources=training_sources, unit=units.get(key))
                    for key, value in training_values.items()},
        "observed_log": log_metrics,
    }

    gpu_paths = [path for path in root.rglob("*-gpu.csv") if path.is_file()]
    gpu_paths = scientific(sorted(gpu_paths), root)
    gpu = parse_gpu_csv(gpu_paths, registry) if gpu_paths else []
    peak_gpu = max((record["peak_memory_mib"] for record in gpu), default=None)
    training["metrics"]["peak_gpu_memory_mib"] = cell(
        peak_gpu, sources=sorted({source for record in gpu for source in record["sources"]}), unit="MiB"
    )
    training["gpu_telemetry"] = gpu

    stage_paths = scientific(discover(root, output, "stages.jsonl"), root)
    stage_records = []
    stage_seen = set()
    for path in stage_paths:
        source = registry.add(path, "stage_log")
        for record in parse_jsonl(path):
            require_number(record.get("elapsed_seconds"), "stage.elapsed_seconds", nonnegative=True)
            identity = (record.get("started_utc"), record.get("stage"), record.get("log"))
            if identity in stage_seen:
                continue
            stage_seen.add(identity)
            stage_records.append({
                "stage": record.get("stage"), "status": record.get("status"),
                "elapsed_seconds": record["elapsed_seconds"], "source": source,
            })
    training["stages"] = sorted(stage_records, key=lambda row: (str(row["source"]), str(row["stage"])))

    official_paths = [path for path in root.rglob("metrics.csv")
                      if path.is_file() and tuple(part.lower() for part in path.parts[-3:]) == ("derived", "experiment", "metrics.csv")]
    official_path = select_single(sorted(official_paths), "official evaluator metrics", root)
    official_source = registry.add(official_path, "official_test_metrics") if official_path else None
    official_values, official_views = parse_official(official_path) if official_path else ({}, None)
    evaluation = {
        "status": "AVAILABLE" if official_path else "PENDING", "scope": "test",
        "views": cell(official_views, sources=[official_source] if official_source else []),
        "rendering": {key: cell(official_values.get(key), sources=[official_source] if official_source else []) for key in RENDER},
        "decomposition": {key: cell(official_values.get(key), sources=[official_source] if official_source else []) for key in DECOMPOSITION},
    }

    geometry_records = []
    for path in sorted(root.rglob("*.json")):
        if not path.is_file():
            continue
        try:
            path.resolve().relative_to(output)
            continue
        except ValueError:
            pass
        data = load_json(path)
        keys = set(data) if isinstance(data, dict) else set()
        metric_keys = sorted(key for key in keys if key in DISTANCES or key.startswith(("precision@", "completeness@", "fscore@")))
        if not metric_keys:
            continue
        source = registry.add(path, "geometry_metrics")
        metrics = {}
        for key in metric_keys:
            metrics[key] = require_number(data[key], f"geometry.{key}", nonnegative=True)
        geometry_records.append({
            "condition": condition_from_path(path, root), "status": "AVAILABLE",
            "metrics": metrics, "prediction": data.get("prediction"),
            "ground_truth": data.get("ground_truth"), "source": source,
        })
    geometry = {"status": section_status(geometry_records), "scope": "test", "records": geometry_records}

    planarity_records = []
    regularization_records = []
    for path in sorted(root.rglob("*.json")):
        if not path.is_file():
            continue
        try:
            path.resolve().relative_to(output)
            continue
        except ValueError:
            pass
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        if all(key in data for key in ("mean_abs_distance", "rmse_distance", "p95_abs_distance", "inlier_fraction")):
            source = registry.add(path, "floor_planarity")
            metrics = {key: require_number(data[key], f"floor.{key}", nonnegative=True) for key in FLOOR_METRICS}
            planarity_records.append({"condition": condition_from_path(path, root), "status": "AVAILABLE",
                                      "selector": data.get("selector"), "metrics": metrics, "source": source})
        before_after = [f"{phase}_{key}" for phase in ("before", "after")
                        for key in ("mean_abs_distance", "rmse_distance", "p95_abs_distance")]
        if all(key in data for key in before_after):
            source = registry.add(path, "floor_regularization")
            metrics = {key: require_number(data[key], f"regularization.{key}", nonnegative=True) for key in before_after}
            inlier = data.get("ransac_inlier_fraction")
            if inlier is not None:
                metrics["before_inlier_fraction"] = require_number(inlier, "regularization.ransac_inlier_fraction", nonnegative=True)
            regularization_records.append({"status": "AVAILABLE", "selector": data.get("selector"),
                                           "metrics": metrics, "source": source})

    floor_selection_paths = discover(root, output, "floor_selection.json")
    floor_selection_path = select_single(floor_selection_paths, "floor selection", root)
    if floor_selection_path:
        selection_data = load_json(floor_selection_path)
        selection_source = registry.add(floor_selection_path, "floor_selection")
        floor_selection = {
            "status": "AVAILABLE", "selection_status": selection_data.get("status"),
            "instance_id": cell(selection_data.get("instance_id"), sources=[selection_source],
                                note="Geometric heuristic; never semantic ground truth."),
            "evidence_type": selection_data.get("evidence_type"),
            "semantic_ground_truth": selection_data.get("semantic_ground_truth"),
            "source": selection_source,
        }
    else:
        floor_selection = {"status": "PENDING", "selection_status": None,
                           "instance_id": cell(), "evidence_type": None,
                           "semantic_ground_truth": None, "source": None}
    floor = {"status": "AVAILABLE" if planarity_records or regularization_records or floor_selection_path else "PENDING",
             "selection": floor_selection, "planarity": planarity_records,
             "regularization": regularization_records}

    instances = []
    for path in discover(root, output, "instances.json"):
        data = load_json(path)
        if not isinstance(data, dict) or "instances" not in data:
            raise ValueError(f"Invalid instances.json: {path.relative_to(root)}")
        source = registry.add(path, "instance_manifest")
        instances.append({
            "condition": condition_from_path(path, root), "status": "AVAILABLE",
            "instance_count": len(data["instances"]), "exported_faces": data.get("exported_faces"),
            "boundary_faces": data.get("boundary_faces"), "face_coverage": data.get("face_coverage"),
            "source": source,
        })
    decomposition_structure = {"status": section_status(instances), "records": instances}

    applicability = {
        "A0": {"G0": True, "G1": True, "G2": False, "G3": False, "G4": False},
        "A1": {"G0": True, "G1": True, "G2": True, "G3": False, "G4": False},
        "A2": {"G0": True, "G1": True, "G2": True, "G3": True, "G4": True},
    }
    gazebo = {condition: {gate: cell(status="PENDING" if applies else "NOT_APPLICABLE")
                          for gate, applies in gates.items()} for condition, gates in applicability.items()}
    gazebo_sources = []
    for path in discover(root, output, "gazebo_validation.json"):
        data = load_json(path)
        condition = str(data.get("condition", condition_from_path(path, root))).upper()
        if condition not in gazebo:
            raise ValueError(f"Gazebo condition must be A0/A1/A2: {condition}")
        source = registry.add(path, "gazebo_validation")
        gazebo_sources.append(source)
        for gate in applicability[condition]:
            raw = data.get("gates", {}).get(gate)
            if raw is None:
                continue
            status = raw.get("status") if isinstance(raw, dict) else raw
            if status in ("PASS", "FAIL"):
                gazebo[condition][gate] = cell(status, status="AVAILABLE", sources=[source])
            elif status == "NOT_EXECUTED":
                gazebo[condition][gate] = cell(status="NOT_EXECUTED", sources=[source])
            elif status == "NOT_APPLICABLE":
                gazebo[condition][gate] = cell(status="NOT_APPLICABLE", sources=[source])
            else:
                raise ValueError(f"Invalid Gazebo gate status {condition}/{gate}: {status!r}")
    gazebo_section = {"status": "AVAILABLE" if gazebo_sources else "PENDING", "conditions": gazebo}

    baseline_paths = discover(root, output, "baseline_run.json")
    baseline_path = select_single(baseline_paths, "COLMAP baseline report", root)
    if baseline_path:
        data = load_json(baseline_path)
        source = registry.add(baseline_path, "colmap_baseline")
        if data.get("status") != "ok":
            baseline_status = "NOT_EXECUTED"
        else:
            baseline_status = "AVAILABLE"
        baseline = {"status": baseline_status, "method": "COLMAP", "run": data, "source": source}
    else:
        baseline = {"status": "NOT_EXECUTED", "method": "COLMAP", "run": None, "source": None}

    return {
        "schema_version": 1,
        "input_root": ".",
        "generator": {"path": "tools/aggregate_results.py", "sha256": sha256(Path(__file__))},
        "training": training,
        "test_evaluation": evaluation,
        "geometry": geometry,
        "ablation": {"conditions": ["A0", "A1", "A2"], "floor": floor,
                     "instance_structure": decomposition_structure},
        "gazebo": gazebo_section,
        "baseline": baseline,
        "sources": registry.sorted(),
    }


def flatten_cells(value, prefix="", context=None):
    context = dict(context or {})
    rows = []
    if isinstance(value, dict) and set(("status", "value", "sources")).issubset(value):
        rows.append({
            **context, "field": prefix, "status": value["status"], "value": value["value"],
            "unit": value.get("unit"), "sources": ";".join(value.get("sources", [])),
        })
    elif isinstance(value, dict):
        for key in sorted(value):
            rows.extend(flatten_cells(value[key], f"{prefix}.{key}" if prefix else key, context))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            item_context = dict(context)
            if isinstance(item, dict):
                for key in ("condition", "source", "gpu_name", "stage"):
                    if key in item and not isinstance(item[key], (dict, list)):
                        item_context[key] = item[key]
            rows.extend(flatten_cells(item, f"{prefix}[{index}]", item_context))
    return rows


def metric_rows(summary):
    rows = flatten_cells(summary)
    # Add dynamic scientific metrics that are plain numeric mappings.
    for index, record in enumerate(summary["geometry"]["records"]):
        for metric, value in sorted(record["metrics"].items()):
            rows.append({"condition": record["condition"], "field": f"geometry.records[{index}].{metric}",
                         "status": "AVAILABLE", "value": value, "unit": None,
                         "sources": record["source"]})
    for family in ("planarity", "regularization"):
        for index, record in enumerate(summary["ablation"]["floor"][family]):
            for metric, value in sorted(record["metrics"].items()):
                rows.append({"condition": record.get("condition"),
                             "field": f"ablation.floor.{family}[{index}].{metric}",
                             "status": "AVAILABLE", "value": value, "unit": None,
                             "sources": record["source"]})
    return sorted(rows, key=lambda row: (row["field"], str(row.get("condition", ""))))


def format_value(entry):
    if entry["status"] != "AVAILABLE" or entry["value"] is None:
        return "—"
    value = entry["value"]
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def render_tables(summary):
    training = summary["training"]["metrics"]
    evaluation = summary["test_evaluation"]
    chunks = ["# Tabelas derivadas dos resultados rastreáveis", "",
              "Ausências aparecem como `—`; o status detalhado está em `results_status.md`.", "",
              "## Custo de treinamento", "",
              markdown_table(["Métrica", "Valor", "Unidade"], [
                  [key, format_value(value), value.get("unit", "—")] for key, value in training.items()
              ]), "", "## Avaliação oficial — conjunto de teste", "",
              markdown_table(["Família", "Métrica", "Valor"],
                             [[family, key, format_value(value)]
                              for family, metrics in (("renderização", evaluation["rendering"]),
                                                      ("decomposição", evaluation["decomposition"]))
                              for key, value in metrics.items()]),
              "", "## Geometria", ""]
    geometry_rows = []
    for record in summary["geometry"]["records"]:
        geometry_rows.extend([[record["condition"], key, f"{value:.6g}", record["source"]]
                              for key, value in sorted(record["metrics"].items())])
    chunks.append(markdown_table(["Condição", "Métrica", "Valor", "Fonte"], geometry_rows or [["—", "—", "—", "—"]]))
    chunks += ["", "## Piso — A1/A2", ""]
    floor_rows = []
    for family in ("planarity", "regularization"):
        for record in summary["ablation"]["floor"][family]:
            condition = record.get("condition", "pareado")
            floor_rows.extend([[condition, key, f"{value:.6g}", record["source"]]
                               for key, value in sorted(record["metrics"].items())])
    chunks.append(markdown_table(["Condição", "Métrica", "Valor", "Fonte"], floor_rows or [["—", "—", "—", "—"]]))
    chunks += ["", "## Gazebo Classic", ""]
    chunks.append(markdown_table(["Condição", "G0", "G1", "G2", "G3", "G4"], [
        [condition, *[gates[gate]["value"] if gates[gate]["status"] == "AVAILABLE" else gates[gate]["status"]
                     for gate in ("G0", "G1", "G2", "G3", "G4")]]
        for condition, gates in summary["gazebo"]["conditions"].items()
    ]))
    chunks += ["", "## Baseline externo", "",
               markdown_table(["Método", "Status", "Fonte"], [["COLMAP", summary["baseline"]["status"],
                                                                summary["baseline"]["source"] or "—"]]), ""]
    return "\n".join(chunks)


def render_status(summary, rows):
    counts = {status: sum(row["status"] == status for row in rows) for status in STATUSES}
    lines = ["# Estado dos resultados", "",
             "Estados são derivados somente dos artefatos encontrados; ausência nunca vira zero.", "",
             markdown_table(["Status", "Campos"], [[status, counts[status]] for status in STATUSES]), "",
             "## Campos", "",
             markdown_table(["Campo", "Status", "Fonte"], [
                 [row["field"], row["status"], row["sources"] or "—"] for row in rows
             ]), ""]
    return "\n".join(lines)


def write_outputs(summary, output_dir: Path):
    rows = metric_rows(summary)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    fields = ["field", "status", "value", "unit", "condition", "source", "gpu_name", "stage", "sources"]
    with (output_dir / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    (output_dir / "tables.md").write_text(render_tables(summary), encoding="utf-8")
    (output_dir / "results_status.md").write_text(render_status(summary, rows), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="directory containing raw and derived experiment artifacts")
    parser.add_argument("--output", type=Path, required=True, help="empty or reusable derived output directory")
    args = parser.parse_args()
    summary = aggregate(args.results, args.output)
    write_outputs(summary, args.output)
    print(json.dumps({"output": str(args.output), "sources": len(summary["sources"])}, sort_keys=True))


if __name__ == "__main__":
    main()
