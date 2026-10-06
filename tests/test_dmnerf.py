import json
import os
from pathlib import Path
import random
import sys
import tempfile
from types import SimpleNamespace
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/dmnerf'))
from prepare import extract_scene

class Infrastructure(unittest.TestCase):
    def test_select_scene(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with zipfile.ZipFile(root/'data.zip','w') as z:
                z.writestr('dmsr/study/a.txt','study'); z.writestr('dmsr/office/a.txt','office')
            extract_scene(root/'data.zip',root/'out')
            self.assertEqual((root/'out/dmsr/study/a.txt').read_text(),'study')
            self.assertFalse((root/'out/dmsr/office').exists())
    def test_refuse_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with zipfile.ZipFile(root/'data.zip','w') as z:
                z.writestr('dmsr/study/../../../escape','bad')
            with self.assertRaises(ValueError): extract_scene(root/'data.zip',root/'out')
    def test_notebook_cells_compile(self):
        paths=list((ROOT/'notebooks').glob('DMNeRF_*.ipynb'))
        self.assertEqual(len(paths),4)
        for path in paths:
            book=json.loads(path.read_text())
            for cell in book['cells']:
                if cell['cell_type']=='code': compile(''.join(cell['source']),str(path),'exec')
    def test_resume_exact_cpu(self):
        import numpy as np
        import torch
        import runtime_control as control
        original=dict(os.environ)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                os.environ.update(DMNERF_STEPS='6',DMNERF_SECONDS='99999')
                args=SimpleNamespace(basedir=tmp,expname='study',log_time='smoke',i_save=3)
                folder=Path(tmp)/'study/smoke'; folder.mkdir(parents=True)
                def models():
                    a,b=torch.nn.Linear(2,2),torch.nn.Linear(2,2)
                    return a,b,torch.optim.Adam(list(a.parameters())+list(b.parameters()),lr=.001)
                def step(i,a,b,opt):
                    x=torch.rand(4,2)+float(np.random.rand())+random.random()
                    loss=(b(a(x))**2).mean(); opt.zero_grad(); loss.backward(); opt.step()
                    control.finish_step(i,a,b,opt,args,loss)
                control.seed(); a,b,opt=models()
                for i in range(3): step(i,a,b,opt)
                copy=folder/'resume.tar'; copy.write_bytes((folder/'latest.tar').read_bytes())
                for i in range(3,6): step(i,a,b,opt)
                expected=[p.detach().clone() for p in list(a.parameters())+list(b.parameters())]
                a,b,opt=models(); os.environ['DMNERF_RESUME']=str(copy)
                start=control.load_resume(a,b,opt); self.assertEqual(start,3)
                for i in range(start,6): step(i,a,b,opt)
                for want,got in zip(expected,list(a.parameters())+list(b.parameters())):
                    self.assertTrue(torch.equal(want,got))
        finally:
            os.environ.clear(); os.environ.update(original)

@unittest.skipUnless(os.environ.get('DMNERF_UPSTREAM'),'Set DMNERF_UPSTREAM for synthetic mesh test')
class MeshContract(unittest.TestCase):
    def test_positive_surface_preserves_ids(self):
        import numpy as np
        import torch
        import trimesh
        from patch_upstream import apply
        upstream=Path(os.environ['DMNERF_UPSTREAM']).resolve(); apply(upstream); apply(upstream)
        sys.path.insert(0,str(upstream))
        from tools import mesh_generator as mesh
        cwd=Path.cwd(); render_before=mesh.dm_nerf; grid_before=os.environ.get('DMNERF_GRID_DIM')
        try:
            os.chdir(upstream); os.environ['DMNERF_GRID_DIM']='32'
            class Embedder:
                def embed(self,points): return points
            def sphere(points):
                result=torch.zeros((len(points),8))
                result[:,3]=30*(1-torch.linalg.norm(points[:,:3],dim=-1)); return result
            def render(rays,*unused):
                result=torch.zeros((rays.shape[1],3)); result[:,2]=1
                return {'ins_fine':result}
            mesh.dm_nerf=render
            args=SimpleNamespace(datadir='./data/dmsr/study',expname='study',N_test=256,device='cpu',near=4.,far=15.,N_importance=128,N_samples=64)
            palette=np.array([[255,0,0],[0,255,0],[0,0,255]],dtype=np.uint8)
            with tempfile.TemporaryDirectory() as tmp,torch.no_grad():
                mesh.mesh_main(Embedder(),Embedder(),None,sphere,args,trimesh.creation.box(),palette,tmp,{'2':0})
                labels=np.load(Path(tmp)/'instance_labels.npz')
                exported=trimesh.load(Path(tmp)/'mesh_instances.ply',process=False)
                self.assertGreater(len(exported.vertices),0)
                self.assertEqual(len(exported.vertices),len(labels['vertex_instance_id']))
                self.assertTrue((labels['vertex_instance_id']==2).all())
                np.testing.assert_allclose(exported.vertices,labels['vertices'],atol=1e-6)
        finally:
            os.chdir(cwd); mesh.dm_nerf=render_before
            if grid_before is None: os.environ.pop('DMNERF_GRID_DIM',None)
            else: os.environ['DMNERF_GRID_DIM']=grid_before
if __name__=='__main__': unittest.main()
