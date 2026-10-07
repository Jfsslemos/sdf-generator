import json
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from select_floor import select_floor
from mesh_contract import load_labels

class FloorSelection(unittest.TestCase):
    def scene(self,root,tie=False):
        v=[];f=[];ids=[]
        for iid,y,size in [(7,0,4),(8,1,1),(9,3,4)]+([(10,0,4)] if tie else []):
            n=len(v);v.extend([[0,y,0],[size,y,0],[size,y,size],[0,y,size]])
            f.extend([[n,n+1,n+2],[n,n+2,n+3]]);ids.extend([iid]*4)
        path=root/'labels.npz';np.savez(path,vertices=v,triangles=f,vertex_instance_id=ids);return path
    def test_floor_not_table_or_ceiling_and_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=self.scene(Path(tmp));a=select_floor(p);b=select_floor(p)
            self.assertEqual(a,b);self.assertEqual(a['instance_id'],7)
            self.assertFalse(a['semantic_ground_truth']);self.assertEqual(a['evidence_type'],'geometric_heuristic')
    def test_ambiguity_abstains(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=select_floor(self.scene(Path(tmp),True));self.assertIsNone(r['instance_id']);self.assertEqual(r['status'],'ambiguous')
    def test_no_large_plane_abstains(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=select_floor(self.scene(Path(tmp)),min_area=100);self.assertEqual(r['status'],'not_identified')
    def test_invalid_ids_and_indices_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.npz';np.savez(p,vertices=np.zeros((3,3)),triangles=[[0,1,-1]],vertex_instance_id=[1,1,1])
            with self.assertRaises(ValueError):load_labels(p)
            np.savez(p,vertices=np.zeros((3,3)),triangles=[[0,1,2]],vertex_instance_id=[1.,1.,1.])
            with self.assertRaises(ValueError):load_labels(p)
    def test_geometry_pair_matches_and_mismatch_rejected(self):
        import trimesh
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=self.scene(root);v,f,ids=load_labels(p)
            mesh=root/'mesh_geometry.ply';trimesh.Trimesh(v,f,process=False).export(mesh)
            self.assertEqual(select_floor(p,mesh_file=mesh)['instance_id'],7)
            trimesh.Trimesh(v+1,f,process=False).export(mesh)
            with self.assertRaisesRegex(ValueError,'coordinates'):select_floor(p,mesh_file=mesh)
            trimesh.Trimesh(v,f[::-1],process=False).export(mesh)
            with self.assertRaisesRegex(ValueError,'topology'):select_floor(p,mesh_file=mesh)
    def test_all_instances_diagnosed_and_no_faces_abstains(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'labels.npz';np.savez(p,vertices=[[0,0,0],[1,0,0],[0,0,1]],triangles=[[0,1,2]],vertex_instance_id=[1,2,3])
            r=select_floor(p);self.assertEqual(len(r['candidates']),3)
            self.assertIsNone(r['instance_id']);self.assertTrue(all(c['rejection_reasons'] for c in r['candidates']))
    def test_bad_up_and_nonfinite_vertices_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=self.scene(Path(tmp))
            with self.assertRaises(ValueError):select_floor(p,up=(0,0,0))
            v,f,ids=load_labels(p);v[0,0]=float('nan');np.savez(p,vertices=v,triangles=f,vertex_instance_id=ids)
            with self.assertRaises(ValueError):select_floor(p)
    def test_winding_and_colors_do_not_control_selection(self):
        import trimesh
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=self.scene(root);v,f,ids=load_labels(p);f=f[:,::-1]
            np.savez(p,vertices=v,triangles=f,vertex_instance_id=ids)
            mesh=trimesh.Trimesh(v,f,process=False);mesh.visual.vertex_colors=np.full((len(v),4),255,dtype=np.uint8)
            target=root/'mesh.ply';mesh.export(target)
            self.assertEqual(select_floor(p,mesh_file=target)['instance_id'],7)
if __name__=='__main__':unittest.main()
