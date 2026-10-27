import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "aggregate_results", Path(__file__).parents[1] / "tools" / "aggregate_results.py"
)
aggregate_results = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aggregate_results)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n")


class AggregateResultsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "results"
        self.root.mkdir()
        self.output = self.root / "derived_summary"

    def tearDown(self):
        self.temp.cleanup()

    def run_aggregate(self):
        summary = aggregate_results.aggregate(self.root, self.output)
        aggregate_results.write_outputs(summary, self.output)
        return summary

    def add_training(self):
        folder = self.root / "raw" / "study" / "experiment"
        write_json(folder / "training_state.json", {
            "iteration": 9, "effective_updates": 9, "skipped_updates": 1,
            "elapsed_seconds": 5.0, "max_vram_bytes": 2048,
            "target_steps": 10, "complete": True, "stopped_for_budget": False,
        })
        rows = [
            {"iteration": 8, "effective_updates": 9, "skipped_updates": 0,
             "optimizer_step_applied": True, "elapsed_seconds": 1.0,
             "max_vram_bytes": 1024, "loss": 0.5, "PSNR": 999},
            {"iteration": 9, "effective_updates": 9, "skipped_updates": 1,
             "optimizer_step_applied": False, "elapsed_seconds": 2.0,
             "max_vram_bytes": 2048, "loss": 0.4},
        ]
        (folder / "training.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))

    def add_official(self):
        path = self.root / "derived" / "experiment" / "metrics.csv"
        path.parent.mkdir(parents=True)
        with path.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["view", *aggregate_results.OFFICIAL])
            writer.writerow([0, 20, .8, .2, .5, .4, .3, .2, .1, .05])
            writer.writerow(["mean", 21, .81, .19, .51, .41, .31, .21, .11, .06])

    def test_complete_result_and_train_test_separation(self):
        self.add_training()
        self.add_official()
        write_json(self.root / "a0" / "geometry.json", {
            "mean_pred_to_gt": .01, "mean_gt_to_pred": .02,
            "chamfer_l1_symmetric": .03, "rmse_pred_to_gt": .015,
            "rmse_gt_to_pred": .025, "precision@0.01": .7,
            "completeness@0.01": .6, "fscore@0.01": .646,
        })
        write_json(self.root / "a1" / "floor.json", {
            "mean_abs_distance": .02, "rmse_distance": .03,
            "p95_abs_distance": .04, "inlier_fraction": .8,
            "selector": {"instance_id": 2},
        })
        write_json(self.root / "a2" / "regularization.json", {
            "selector": {"instance_id": 2},
            "before_mean_abs_distance": .02, "before_rmse_distance": .03,
            "before_p95_abs_distance": .04, "after_mean_abs_distance": 0.001,
            "after_rmse_distance": .002, "after_p95_abs_distance": .003,
            "ransac_inlier_fraction": .8,
        })
        write_json(self.root / "floor_selection.json", {
            "status": "selected", "instance_id": 2,
            "evidence_type": "geometric_heuristic", "semantic_ground_truth": False,
        })
        write_json(self.root / "a1" / "instances.json", {"instances": [{"instance_id": 2}],
                                                           "exported_faces": 4, "boundary_faces": 1,
                                                           "face_coverage": .8})
        write_json(self.root / "a1" / "gazebo_validation.json", {
            "condition": "A1", "gates": {"G0": {"status": "PASS"},
                                             "G1": {"status": "NOT_EXECUTED"},
                                             "G2": {"status": "NOT_EXECUTED"},
                                             "G3": {"status": "NOT_APPLICABLE"},
                                             "G4": {"status": "NOT_APPLICABLE"}},
        })
        write_json(self.root / "colmap" / "baseline_run.json", {"status": "ok", "fused": "fused.ply", "stages": []})

        summary = self.run_aggregate()
        self.assertEqual(summary["training"]["scope"], "train")
        self.assertEqual(summary["test_evaluation"]["scope"], "test")
        self.assertEqual(summary["training"]["metrics"]["amp_skips"]["value"], 1)
        self.assertEqual(summary["test_evaluation"]["rendering"]["PSNR"]["value"], 21)
        self.assertNotIn("PSNR", summary["training"]["metrics"])
        self.assertEqual(summary["geometry"]["records"][0]["condition"], "A0")
        self.assertEqual(summary["gazebo"]["conditions"]["A1"]["G0"]["value"], "PASS")
        self.assertEqual(summary["baseline"]["status"], "AVAILABLE")
        self.assertTrue(all(len(source["sha256"]) == 64 for source in summary["sources"]))
        for filename in ("summary.json", "summary.csv", "tables.md", "results_status.md"):
            self.assertTrue((self.output / filename).is_file())

    def test_partial_and_missing_are_explicit(self):
        self.add_training()
        summary = self.run_aggregate()
        self.assertEqual(summary["test_evaluation"]["rendering"]["PSNR"]["status"], "PENDING")
        self.assertIsNone(summary["test_evaluation"]["rendering"]["PSNR"]["value"])
        self.assertEqual(summary["baseline"]["status"], "NOT_EXECUTED")
        self.assertEqual(summary["gazebo"]["conditions"]["A0"]["G2"]["status"], "NOT_APPLICABLE")
        self.assertIn("PENDING", (self.output / "results_status.md").read_text())

    def test_empty_directory_produces_pending_not_zero(self):
        summary = self.run_aggregate()
        self.assertEqual(summary["training"]["status"], "PENDING")
        self.assertIsNone(summary["training"]["metrics"]["final_iteration"]["value"])
        text = (self.output / "summary.json").read_text()
        self.assertNotIn("NaN", text)

    def test_invalid_nan_is_rejected(self):
        path = self.root / "derived" / "experiment" / "metrics.csv"
        path.parent.mkdir(parents=True)
        path.write_text("view,PSNR,SSIM,LPIPS,AP50,AP75,AP80,AP85,AP90,AP95\n"
                        "0,1,1,1,1,1,1,1,1,1\nmean,nan,1,1,1,1,1,1,1,1\n")
        with self.assertRaisesRegex(ValueError, "PSNR"):
            aggregate_results.aggregate(self.root, self.output)

    def test_invalid_finite_metric_is_rejected(self):
        self.add_official()
        path = self.root / "derived" / "experiment" / "metrics.csv"
        text = path.read_text().replace(".06", "1.06")
        path.write_text(text)
        with self.assertRaisesRegex(ValueError, "AP95"):
            aggregate_results.aggregate(self.root, self.output)

    def test_outputs_are_deterministic(self):
        self.add_training()
        self.add_official()
        self.run_aggregate()
        first = {path.name: path.read_bytes() for path in self.output.iterdir()}
        self.run_aggregate()
        second = {path.name: path.read_bytes() for path in self.output.iterdir()}
        self.assertEqual(first, second)

    def test_identical_gpu_models_remain_separate(self):
        path = self.root / "20261008-gpu.csv"
        path.write_text(
            "timestamp, name, memory.used [MiB], utilization.gpu [%]\n"
            "t0, Tesla T4, 6000 MiB, 95 %\n"
            "t0, Tesla T4, 10 MiB, 0 %\n"
            "t1, Tesla T4, 6100 MiB, 90 %\n"
            "t1, Tesla T4, 10 MiB, 0 %\n"
        )
        summary = self.run_aggregate()
        telemetry = summary["training"]["gpu_telemetry"]
        self.assertEqual([row["gpu_ordinal"] for row in telemetry], [0, 1])
        self.assertEqual(telemetry[0]["peak_memory_mib"], 6100)
        self.assertEqual(telemetry[1]["mean_utilization_percent"], 0)
        self.assertEqual(summary["training"]["metrics"]["peak_gpu_memory_mib"]["value"], 6100)


if __name__ == "__main__":
    unittest.main()
