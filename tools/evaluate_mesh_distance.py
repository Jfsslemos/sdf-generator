#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import numpy as np
import trimesh
from scipy.spatial import cKDTree


def load_points(path: Path, samples: int, seed: int):
    obj=trimesh.load(path, process=False)
    if isinstance(obj, trimesh.Trimesh):
        if len(obj.faces):
            state = np.random.get_state()
            np.random.seed(seed)
            try:
                pts,_=trimesh.sample.sample_surface(obj, samples)
            finally:
                np.random.set_state(state)
            return np.asarray(pts)
        return np.asarray(obj.vertices)
    if isinstance(obj, trimesh.points.PointCloud):
        return np.asarray(obj.vertices)
    raise TypeError(f'Formato não suportado: {type(obj)}')


def metrics(pred, gt, thresholds):
    t_gt=cKDTree(gt); t_pred=cKDTree(pred)
    d_pred,_=t_gt.query(pred,k=1)
    d_gt,_=t_pred.query(gt,k=1)
    out={
        'mean_pred_to_gt':float(d_pred.mean()),
        'mean_gt_to_pred':float(d_gt.mean()),
        'chamfer_l1_symmetric':float(d_pred.mean()+d_gt.mean()),
        'rmse_pred_to_gt':float(np.sqrt(np.mean(d_pred**2))),
        'rmse_gt_to_pred':float(np.sqrt(np.mean(d_gt**2))),
    }
    for th in thresholds:
        precision=float(np.mean(d_pred <= th))
        completeness=float(np.mean(d_gt <= th))
        f=0.0 if precision+completeness==0 else 2*precision*completeness/(precision+completeness)
        out[f'precision@{th:g}']=precision
        out[f'completeness@{th:g}']=completeness
        out[f'fscore@{th:g}']=f
    return out


def main():
    ap=argparse.ArgumentParser(description='Compara mesh/nuvem reconstruída com referência usando distâncias NN.')
    ap.add_argument('prediction', type=Path)
    ap.add_argument('ground_truth', type=Path)
    ap.add_argument('--samples', type=int, default=200000)
    ap.add_argument('--thresholds', type=float, nargs='+', default=[0.01,0.02,0.05])
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--out', type=Path)
    args=ap.parse_args()
    pred=load_points(args.prediction,args.samples,args.seed)
    gt=load_points(args.ground_truth,args.samples,args.seed)
    out=metrics(pred,gt,args.thresholds)
    out.update({'prediction':str(args.prediction),'ground_truth':str(args.ground_truth),'n_prediction':len(pred),'n_ground_truth':len(gt)})
    s=json.dumps(out,indent=2)
    print(s)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(s,encoding='utf-8')

if __name__=='__main__':
    main()
