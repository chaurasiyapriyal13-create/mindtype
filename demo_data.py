"""Synthetic pipeline test, never evidence of real-world strain prediction."""
from pathlib import Path
import numpy as np
import pandas as pd
rng=np.random.default_rng(42)
rows=[]
for person in range(30):
    personal=rng.normal(180,35)
    for session in range(8):
        rating=float(rng.uniform(0,10))
        rows.append({'participant_id':f'demo_{person:03}','session_id':f'{person}_{session}','self_report_strain':round(rating,2),'median_interval_ms':max(30,personal+rating*8+rng.normal(0,25)),'interval_variability':max(.01,.4+rating*.025+rng.normal(0,.12)),'median_dwell_ms':max(15,80+rng.normal(0,20)),'pause_rate':float(np.clip(.025+rating*.007+rng.normal(0,.025),0,1)),'backspace_rate':float(np.clip(.03+rating*.006+rng.normal(0,.03),0,1)),'error_rate':float(np.clip(.02+rating*.003+rng.normal(0,.02),0,1))})
path=Path(__file__).resolve().parents[1]/'data'/'synthetic_demo.csv';pd.DataFrame(rows).to_csv(path,index=False);print(path)
