#!/usr/bin/env python3
"""Select a low, broad planar instance geometrically; never assign semantic GT."""
import argparse
import json
from pathlib import Path
import numpy as np
from mesh_contract import load_labels, sha256

def select_floor(labels, up=(0,1,0), min_area=0.5, min_horizontal=0.85,
                 max_tilt_degrees=15., max_rmse=0.03, lower_fraction=0.20,
                 ambiguity_ratio=0.8, mesh_file=None):
    v,f,ids=load_labels(labels,mesh_file=mesh_file)
    up=np.asarray(up,dtype=float)
    if up.shape!=(3,) or not np.isfinite(up).all() or np.linalg.norm(up)==0: raise ValueError('invalid up vector')
    up=up/np.linalg.norm(up)
    if not (min_area>0 and 0<min_horizontal<=1 and 0<max_tilt_degrees<90 and max_rmse>0 and 0<lower_fraction<1 and 0<ambiguity_ratio<=1): raise ValueError('invalid thresholds')
    height=v@up; span=float(np.ptp(height))
    low=float(np.quantile(height,0.01)); limit=low+lower_fraction*span
    records=[]
    for iid in np.unique(ids):
        faces=f[np.all(ids[f]==iid,axis=1)]
        if not len(faces): continue
        tri=v[faces]; cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); area=np.linalg.norm(cross,axis=1)/2
        valid=area>1e-12;tri=tri[valid];area=area[valid];cross=cross[valid]
        if not len(area):continue
        centers=tri.mean(axis=1);center=np.average(centers,weights=area,axis=0)
        # Area-weighted triangle vertices; invariant to face winding, deterministic.
        pts=tri.reshape(-1,3);weights=np.repeat(area/3,3);delta=pts-center
        covariance=(delta*weights[:,None]).T@delta/weights.sum()
        eig,axes=np.linalg.eigh(covariance); normal=axes[:,0]
        if normal@up<0:normal=-normal
        horizontal=np.abs(cross@up)/(2*area)>=np.cos(np.deg2rad(max_tilt_degrees))
        fraction=float(area[horizontal].sum()/area.sum());rmse=float(np.sqrt(max(0,eig[0])))
        level=float(center@up)
        accepted=bool(area.sum()>=min_area and fraction>=min_horizontal and normal@up>=np.cos(np.deg2rad(max_tilt_degrees)) and rmse<=max_rmse and level<=limit)
        records.append(dict(instance_id=int(iid),area=float(area.sum()),horizontal_fraction=fraction,
                            area_weighted_height=level,plane_normal=normal.tolist(),plane_d=float(-normal@center),rmse=rmse,eligible=accepted))
    eligible=sorted((r for r in records if r['eligible']),key=lambda r:(-r['area'],r['instance_id']))
    ambiguous=len(eligible)>1 and eligible[1]['area']>=eligible[0]['area']*ambiguity_ratio
    chosen=eligible[0]['instance_id'] if eligible and not ambiguous else None
    return dict(schema_version=1,status='selected' if chosen is not None else 'ambiguous' if ambiguous else 'not_identified',
                evidence_type='geometric_heuristic',semantic_ground_truth=False,instance_id=chosen,
                source_sha256=sha256(labels),source=Path(labels).name,
                mesh_sha256=sha256(mesh_file) if mesh_file else None,
                parameters=dict(up=up.tolist(),min_area=min_area,min_horizontal=min_horizontal,max_tilt_degrees=max_tilt_degrees,max_rmse=max_rmse,lower_fraction=lower_fraction,ambiguity_ratio=ambiguity_ratio),
                lower_height_limit=limit,candidates=records,
                limitations=['May select a low rug/platform; geometry does not prove semantic floor.',
                             'Fragmented or merged floor IDs can cause abstention; do not force an ID.'])

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('labels',type=Path);p.add_argument('--mesh',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--up',type=float,nargs=3,default=(0,1,0))
    a=p.parse_args();r=select_floor(a.labels,a.up,mesh_file=a.mesh);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
