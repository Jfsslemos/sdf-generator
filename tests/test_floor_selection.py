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
if __name__=='__main__':unittest.main()
