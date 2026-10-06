"""Fail-closed adaptations of the pinned upstream; keep the resulting diff."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def replace(text, old, new, count=1):
    if text.count(old) != count:
        raise ValueError('Unexpected upstream content: ' + old[:70])
    return text.replace(old, new)

def apply(upstream):
    upstream = Path(upstream)
    stamp = upstream / 'session-patch.json'
    identity = {'patcher':digest(__file__), 'runtime':digest(Path(__file__).with_name('runtime_control.py'))}
    if stamp.exists():
        saved = json.loads(stamp.read_text())
        diff = subprocess.check_output(['git','diff'], cwd=upstream)
        if saved['identity'] != identity or saved['diff_sha256'] != hashlib.sha256(diff).hexdigest():
            raise RuntimeError('Modified upstream workspace; use a new work directory')
        if digest(upstream / 'runtime_control.py') != identity['runtime']:
            raise RuntimeError('Modified runtime controls')
        return
    if subprocess.check_output(['git','diff'], cwd=upstream):
        raise RuntimeError('Refusing to patch a dirty upstream checkout')
    f = upstream / 'train_dmsr.py'; s = f.read_text()
    s = replace(s, 'import os\n', 'import os\nimport runtime_control as control\n')
    s = replace(s, 'N_iters = 500000 + 1', 'N_iters = int(os.environ["DMNERF_STEPS"])')
    s = replace(s, 'range(0, N_iters)', 'range(start_iteration, N_iters)')
    a = s.index('        if i % args.i_save == 0:')
    b = s.index("\n\nif __name__ == '__main__':", a)
    s = s[:a] + '''        # Separate evaluation avoids rendering at iteration zero and is recorded as a protocol adaptation.
        if control.finish_step(i, model_coarse, model_fine, optimizer, args, total_loss):
            return
''' + s[b:]
    s = replace(s, '    # Create nerf model', '    control.seed()\n    # Create nerf model')
    s = replace(s, '    # move data to gpu', '    start_iteration = control.load_resume(model_coarse, model_fine, optimizer)\n\n    # move data to gpu')
    f.write_text(s)
    f = upstream / 'datasets/loader_dmsr.py'
    f.write_text(replace(f.read_text(), 'skip = 1', 'skip = int(os.environ.get("DMNERF_TRAIN_SKIP", "1"))', 2))
    f = upstream / 'networks/tester.py'
    f.write_text(replace(f.read_text(), 'multichannel=True', 'channel_axis=-1'))
    # Torch 2.x can expose a device mismatch in upstream AP evaluation: the
    # module-level `device` becomes CUDA while IoU/confidence tensors are CPU.
    # AP is a small bookkeeping computation, so keep it explicitly on CPU.
    f = upstream / 'networks/evaluator.py'; s = f.read_text()
    s = replace(s,
        '    if confidence is not None:\n        column_max_index = torch.argsort(confidence, descending=True)\n        column_max_value = IoUs_Metrics[column_max_index]\n',
        '    IoUs_Metrics = IoUs_Metrics.detach().cpu()\n    if confidence is not None:\n        confidence = confidence.detach().cpu()\n        column_max_index = torch.argsort(confidence, descending=True)\n        column_max_value = IoUs_Metrics[column_max_index]\n')
    s = replace(s, '        tp_list = tp_list.to(device=device)', '        tp_list = tp_list.cpu()')
    f.write_text(s)
    f = upstream / 'tools/visualizer.py'; s = f.read_text()
    s = replace(s, 'astype(np.float)', 'astype(float)')
    f.write_text(replace(s, 'steps=dim)', 'steps=dim, device="cpu")'))
    f = upstream / 'tools/mesh_generator.py'; s = f.read_text()
    s = replace(s, 'grid_dim = 256', 'grid_dim = int(os.environ.get("DMNERF_GRID_DIM", "256"))')
    s = replace(s, 'grid_query_pts.cuda().reshape(-1, 3)', 'grid_query_pts.cpu().reshape(-1, 3)')
    s = replace(s, 'raw = None', 'raw = []')
    s = replace(s, 'in_pcd = grid_query_pts[step:step + N_test]', 'in_pcd = grid_query_pts[step:step + N_test].to(args.device)')
    a = s.index('        if raw is None:'); b = s.index('    def occupancy_activation', a)
    s = s[:a] + '''        raw.append(raw_fine[:, 3].detach().cpu())

    alpha = torch.cat(raw)
    del raw

''' + s[b:]
    s = replace(s, '    vertices, faces, vertex_normals, _ = ski_measure.marching_cubes', '''    if not occupancy_grid.min() < level < occupancy_grid.max():
        with open(os.path.join(save_dir, 'mesh_status.json'), 'w') as f:
            json.dump({'status': 'no_surface', 'level': level,
                       'min': float(occupancy_grid.min()), 'max': float(occupancy_grid.max())}, f)
        print('No surface at the official threshold; checkpoint needs more training.')
        return
    vertices, faces, vertex_normals, _ = ski_measure.marching_cubes''')
    s = replace(s, '    selected_mesh = o3d_mesh_canonical_clean', '''    if N_vertices == 0:
        with open(os.path.join(save_dir, 'mesh_status.json'), 'w') as f:
            json.dump({'status': 'empty_after_cleaning'}, f)
        return
    selected_mesh = o3d_mesh_canonical_clean''')
    s = replace(s, '    ins_color = render_label2world(pred_label, ins_rgbs, color_dict, ins_map)', '''    # IDs from a new training run need not match the dataset's fixed ins_map.
    labels = pred_label.detach().cpu().numpy()
    np.savez_compressed(os.path.join(save_dir, 'instance_labels.npz'),
                        vertex_instance_id=labels,
                        vertices=np.asarray(o3d_mesh_canonical_clean.vertices),
                        triangles=np.asarray(o3d_mesh_canonical_clean.triangles))
    o3d.io.write_triangle_mesh(os.path.join(save_dir, 'mesh_geometry.ply'), o3d_mesh_canonical_clean)
    o3d_mesh_canonical_clean.vertex_colors = o3d.utility.Vector3dVector(ins_rgbs[labels][:, [2, 1, 0]] / 255.0)
    o3d.io.write_triangle_mesh(os.path.join(save_dir, 'mesh_instances.ply'), o3d_mesh_canonical_clean)
    ins_color = render_label2world(pred_label, ins_rgbs, color_dict, ins_map)''')
    f.write_text(s)
    shutil.copy2(Path(__file__).with_name('runtime_control.py'), upstream / 'runtime_control.py')
    diff = subprocess.check_output(['git','diff'], cwd=upstream)
    (upstream / 'session.patch').write_bytes(diff)
    stamp.write_text(json.dumps({'identity':identity,'diff_sha256':hashlib.sha256(diff).hexdigest()}, indent=2))
