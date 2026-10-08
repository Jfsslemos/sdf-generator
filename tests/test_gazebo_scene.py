"""CPU evidence for portable scene export; never asserts Gazebo runtime success."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from export_gazebo_scene import export_scene, validate_world, digest


class GazeboExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.vertices = np.array([[0,0,0], [1,0,0], [0,1,0], [2,0,1], [3,0,1], [2,1,1]], dtype=float)
        self.faces = np.array([[0,1,2], [3,4,5], [0,1,3]])
        self.mesh = self.root / 'mesh_geometry.ply'
        trimesh.Trimesh(self.vertices, self.faces, process=False).export(self.mesh)
        self.labels = self.root / 'instance_labels.npz'
        np.savez(self.labels, vertices=self.vertices, triangles=self.faces,
                 vertex_instance_id=[2,2,2,7,7,7])

    def tearDown(self):
        self.temp.cleanup()

    def test_split_portable_scale_and_static_gates(self):
        out = self.root / 'a1'
        result = export_scene(self.mesh, self.labels, out, 'A1', 'y')
        self.assertEqual([r['instance_id'] for r in result['objects']], [2,7])
        self.assertEqual(result['gates']['G1']['status'], 'NOT_EXECUTED')
        self.assertTrue(any('boundary' in w for w in result['warnings']))
        world = ET.parse(out/'scene.world')
        self.assertEqual([m.get('name') for m in world.findall('./world/model')], ['instance_002', 'instance_007'])
        self.assertTrue(all(s.text == '1 1 1' for s in world.findall('.//scale')))
        self.assertTrue(all(s.text == 'true' for s in world.findall('.//static')))
        manifest = json.loads((out/'manifest.json').read_text())
        self.assertEqual([r['model_name'] for r in manifest['objects']],
                         ['instance_002', 'instance_007'])
        self.assertEqual([r['uri'] for r in manifest['objects']],
                         ['meshes/instance_002.obj', 'meshes/instance_007.obj'])
        self.assertTrue(all(len(r['sha256']) == 64 for r in manifest['objects']))
        moved = self.root / 'relocated'
        shutil.copytree(out, moved)
        shutil.rmtree(out)
        self.assertEqual(validate_world(moved/'scene.world')['status'], 'PASS')
        self.assertNotIn('/home/joao', (moved/'scene.world').read_text())

    def test_raw_keeps_boundary_faces_and_deterministic_world(self):
        a, b = self.root/'a', self.root/'b'
        export_scene(self.mesh, self.labels, a, 'A0', 'z')
        export_scene(self.mesh, self.labels, b, 'A0', 'z')
        self.assertEqual((a/'scene.world').read_bytes(), (b/'scene.world').read_bytes())
        raw = trimesh.load(a/'meshes/scene_raw.obj', process=False)
        self.assertEqual(len(raw.faces), 3)
        with self.assertRaises(ValueError):
            export_scene(self.mesh, self.labels, a, 'A0', 'z')

    def test_a2_provenance_and_displaced_vertices(self):
        changed = self.root/'regularized.ply'
        verts = self.vertices.copy(); verts[:3, 2] = 0.2
        trimesh.Trimesh(verts, self.faces, process=False).export(changed)
        provenance = self.root/'floor.json'
        provenance.write_text(json.dumps({'instance_id':2, 'source':'geometric_heuristic', 'ground_truth':False, 'source_sha256':digest(self.labels)}))
        with self.assertRaises(ValueError):
            export_scene(changed, self.labels, self.root/'missing', 'A2', 'z')
        result = export_scene(changed, self.labels, self.root/'a2', 'A2', 'z', provenance)
        self.assertFalse(result['floor_provenance']['ground_truth'])
        obj = trimesh.load(self.root/'a2/meshes/instance_002.obj', process=False)
        np.testing.assert_allclose(obj.vertices[:,2], .2)
        with self.assertRaises(ValueError):
            export_scene(changed, self.labels, self.root/'bad_a1', 'A1', 'z')

    def test_g0_rejects_missing_relative_asset_and_scale(self):
        out = self.root/'a0'
        export_scene(self.mesh, self.labels, out, 'A0', 'z')
        path = out/'scene.world'
        tree = ET.parse(path)
        tree.find('.//uri').text = 'meshes/missing.obj'
        tree.write(path)
        with self.assertRaises(ValueError): validate_world(path)
        tree.find('.//uri').text = 'meshes/scene_raw.obj'
        tree.find('.//scale').text = 'nan 1 1'
        tree.write(path)
        with self.assertRaises(ValueError): validate_world(path)

    def test_g0_rejects_invalid_xml_duplicate_names_and_reference_mismatch(self):
        malformed = self.root/'malformed.world'
        malformed.write_text('<sdf><world>')
        with self.assertRaises(ET.ParseError):
            validate_world(malformed)

        out = self.root/'a1'
        export_scene(self.mesh, self.labels, out, 'A1', 'z')
        path = out/'scene.world'
        tree = ET.parse(path)
        models = tree.findall('./world/model')
        models[1].set('name', models[0].get('name'))
        tree.write(path)
        with self.assertRaisesRegex(ValueError, 'unique'):
            validate_world(path)

        tree = ET.parse(self.root/'a1/scene.world')
        # Restore uniqueness while retaining two existing, valid local assets.
        models = tree.findall('./world/model')
        models[1].set('name', 'instance_007')
        models[0].find('link/collision/geometry/mesh/uri').text = 'meshes/instance_007.obj'
        tree.write(path)
        with self.assertRaisesRegex(ValueError, 'differ'):
            validate_world(path)

    def test_large_repeated_ids_are_stable_and_negative_ids_fail(self):
        labels = self.root/'unusual_ids.npz'
        np.savez(labels, vertices=self.vertices, triangles=self.faces,
                 vertex_instance_id=[1007,1007,1007,0,0,0])
        first = export_scene(self.mesh, labels, self.root/'unusual_a', 'A1', 'z')
        second = export_scene(self.mesh, labels, self.root/'unusual_b', 'A1', 'z')
        expected = ['instance_000', 'instance_1007']
        self.assertEqual([item['model_name'] for item in first['objects']], expected)
        self.assertEqual([item['model_name'] for item in second['objects']], expected)
        self.assertEqual((self.root/'unusual_a/scene.world').read_bytes(),
                         (self.root/'unusual_b/scene.world').read_bytes())

        invalid = self.root/'negative_id.npz'
        np.savez(invalid, vertices=self.vertices, triangles=self.faces,
                 vertex_instance_id=[-1,-1,-1,0,0,0])
        with self.assertRaisesRegex(ValueError, 'nonnegative'):
            export_scene(self.mesh, invalid, self.root/'invalid', 'A1', 'z')


if __name__ == '__main__':
    unittest.main()
