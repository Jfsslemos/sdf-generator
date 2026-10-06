#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import numpy as np
import trimesh


def parse_rgb(s):
    vals=tuple(int(v) for v in s.split(','))
    if len(vals)!=3 or any(v<0 or v>255 for v in vals):
        raise argparse.ArgumentTypeError('use R,G,B with values in 0..255')
    return vals


def fit_plane_svd(points):
    center=points.mean(axis=0)
    _,_,vh=np.linalg.svd(points-center, full_matrices=False)
    n=vh[-1]
    n=n/np.linalg.norm(n)
    d=-float(np.dot(n,center))
    return n,d


def ransac_plane(points, threshold=0.02, iterations=1000, seed=42):
    rng=np.random.default_rng(seed)
    best=None
    npts=len(points)
    if npts<3: raise ValueError('menos de 3 pontos')
    for _ in range(iterations):
        p=points[rng.choice(npts,3,replace=False)]
        n=np.cross(p[1]-p[0],p[2]-p[0])
        norm=np.linalg.norm(n)
        if norm<1e-9: continue
        n=n/norm; d=-float(np.dot(n,p[0]))
        dist=np.abs(points@n+d)
        mask=dist<=threshold
        count=int(mask.sum())
        if best is None or count>best[0]: best=(count,mask)
    if best is None: raise RuntimeError('RANSAC falhou')
    n,d=fit_plane_svd(points[best[1]])
    return n,d,best[1]


def selection_mask(mesh, rgb=None, labels=None, instance_id=None):
    if labels is not None:
        data=np.load(labels)
        ids=np.asarray(data['vertex_instance_id']).reshape(-1)
        if len(ids)!=len(mesh.vertices):
            raise ValueError('labels/mesh vertex count mismatch')
        return ids==instance_id, {'instance_id':int(instance_id),'labels':str(labels)}
    colors=np.asarray(mesh.visual.vertex_colors)
    if colors.ndim!=2 or colors.shape[1]<3:
        raise ValueError('mesh has no vertex colors')
    return np.all(colors[:,:3].astype(np.uint8)==np.array(rgb,dtype=np.uint8),axis=1), {'rgb':list(rgb)}


def main():
    ap=argparse.ArgumentParser(description='Mede planaridade de um subconjunto de vértices do piso.')
    ap.add_argument('mesh',type=Path)
    sel=ap.add_mutually_exclusive_group(required=True)
    sel.add_argument('--rgb',type=parse_rgb,help='legacy selector R,G,B')
    sel.add_argument('--instance-id',type=int,help='preferred selector: explicit exported instance id')
    ap.add_argument('--labels',type=Path,help='instance_labels.npz; required with --instance-id')
    ap.add_argument('--threshold',type=float,default=0.02)
    ap.add_argument('--iterations',type=int,default=1000)
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    if (args.instance_id is None)!=(args.labels is None):
        ap.error('--instance-id and --labels must be provided together')
    mesh=trimesh.load(args.mesh,process=False)
    mask,selector=selection_mask(mesh,args.rgb,args.labels,args.instance_id)
    pts=np.asarray(mesh.vertices)[mask]
    if len(pts)<3:
        raise ValueError(f'selection contains only {len(pts)} vertices')
    n,d,inliers=ransac_plane(pts,args.threshold,args.iterations,args.seed)
    residual=np.abs(pts@n+d)
    result={
        'mesh':str(args.mesh),'selector':selector,'vertices':int(len(pts)),
        'plane_normal':n.tolist(),'plane_d':float(d),
        'ransac_threshold':args.threshold,'inlier_fraction':float(inliers.mean()),
        'mean_abs_distance':float(residual.mean()),
        'rmse_distance':float(np.sqrt(np.mean(residual**2))),
        'p95_abs_distance':float(np.percentile(residual,95)),
        'max_abs_distance':float(residual.max()),
    }
    s=json.dumps(result,indent=2); print(s)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(s,encoding='utf-8')


if __name__=='__main__':
    main()
