import json
import math
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/baselines'))
sys.path.insert(0,str(ROOT/'tools'))

from prepare_colmap_dmsr import prepare, OPENGL_TO_COLMAP
from postprocess_instances import split_instances


class ColmapPreparation(unittest.TestCase):
    def test_known_pose_model_and_source_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            scene=root/'study'
            rgb=scene/'train/rgbs'; rgb.mkdir(parents=True)
            Image.new('RGB',(4,4),(1,2,3)).save(rgb/'000.png')
            Image.new('RGB',(4,4),(4,5,6)).save(rgb/'001.png')
            p0=np.eye(4)
            p1=np.eye(4); p1[0,3]=1.0
            (scene/'train/transforms.json').write_text(json.dumps({
                'camera_angle_x':math.pi/2,
                'frames':[{'transform_matrix':p0.tolist()},{'transform_matrix':p1.tolist()}],
            }))
            manifest=prepare(scene,root/'baseline',source_count=1)
            self.assertEqual(manifest['images'],2)
            self.assertAlmostEqual(manifest['fx'],2.0,places=7)
            self.assertEqual(manifest['source_pairs'][0]['sources'],['001.png'])
            self.assertEqual(manifest['source_pairs'][1]['sources'],['000.png'])
            lines=[x for x in (root/'baseline/sparse/images.txt').read_text().splitlines()
                   if x and not x.startswith('#')]
            self.assertEqual(len(lines),2)
            # Identity NeRF c2w maps COLMAP +z to NeRF -z and preserves camera center.
            converted=p0@OPENGL_TO_COLMAP
            self.assertTrue(np.allclose(converted[:3,2],[0,0,-1]))
            self.assertTrue(np.allclose(manifest['records'][1]['center'],[1,0,0]))

    def test_rejects_pose_count_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); scene=root/'study'; rgb=scene/'train/rgbs'; rgb.mkdir(parents=True)
            Image.new('RGB',(4,4)).save(rgb/'000.png')
            (scene/'train/transforms.json').write_text(json.dumps({
                'camera_angle_x':math.pi/2,'frames':[]
            }))
            with self.assertRaisesRegex(ValueError,'count mismatch'):
                prepare(scene,root/'baseline')


class InstanceSplitting(unittest.TestCase):
    def test_explicit_ids_create_independent_meshes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            vertices=np.array([[0,0,0],[1,0,0],[0,1,0],[2,0,0],[3,0,0],[2,1,0]],float)
            triangles=np.array([[0,1,2],[3,4,5]],int)
            labels=np.array([1,1,1,2,2,2],int)
            np.savez_compressed(root/'labels.npz',vertices=vertices,triangles=triangles,
                                vertex_instance_id=labels)
            report=split_instances(root/'labels.npz',root/'out')
            self.assertEqual(len(report['instances']),2)
            self.assertEqual(report['boundary_faces'],0)
            self.assertEqual(report['face_coverage'],1.0)
            self.assertTrue((root/'out/instance_001.ply').is_file())
            self.assertTrue((root/'out/instance_002.obj').is_file())

    def test_boundary_faces_are_not_silently_assigned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            vertices=np.array([[0,0,0],[1,0,0],[0,1,0]],float)
            triangles=np.array([[0,1,2]],int)
            labels=np.array([1,1,2],int)
            np.savez_compressed(root/'labels.npz',vertices=vertices,triangles=triangles,
                                vertex_instance_id=labels)
            report=split_instances(root/'labels.npz',root/'out')
            self.assertEqual(report['boundary_faces'],1)
            self.assertEqual(report['face_coverage'],0.0)


if __name__=='__main__':
    unittest.main()
