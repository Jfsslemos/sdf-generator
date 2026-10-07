"""Strict correspondence between exported vertex IDs, topology and geometry."""
from pathlib import Path
import hashlib
import numpy as np

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def load_labels(path, mesh_file=None, allow_vertex_change=False):
    with np.load(path,allow_pickle=False) as data:
        v=np.asarray(data['vertices'],dtype=float)
        f=np.asarray(data['triangles'])
        ids=np.asarray(data['vertex_instance_id'])
    if v.ndim!=2 or v.shape[1]!=3 or not len(v) or not np.isfinite(v).all():
        raise ValueError('vertices must be finite nonempty Nx3')
    if f.ndim!=2 or f.shape[1]!=3 or not np.issubdtype(f.dtype,np.integer):
        raise ValueError('triangles must be integer Nx3')
    if len(f) and (f.min()<0 or f.max()>=len(v)):
        raise ValueError('triangle index out of bounds')
    if ids.ndim!=1 or len(ids)!=len(v) or not np.issubdtype(ids.dtype,np.integer) or (ids<0).any():
        raise ValueError('instance IDs must be nonnegative integer vector, one per vertex')
    if mesh_file is not None:
        import trimesh
        mesh=trimesh.load(mesh_file,process=False)
        if not isinstance(mesh,trimesh.Trimesh) or not np.array_equal(mesh.faces,f) or mesh.vertices.shape!=v.shape:
            raise ValueError('mesh topology/order differs from labels')
        if not np.isfinite(mesh.vertices).all(): raise ValueError('non-finite mesh')
        if not allow_vertex_change and not np.allclose(mesh.vertices,v,atol=1e-6,rtol=0):
            raise ValueError('mesh coordinates/order differ from labels')
        v=np.asarray(mesh.vertices)
    return v,f.astype(np.int64),ids.astype(np.int64)
