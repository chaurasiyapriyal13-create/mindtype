"""Generate reproducible tabular EDA and an exportable feature figure."""
from pathlib import Path
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.analytics import FEATURES
p=argparse.ArgumentParser();p.add_argument('--data',default='data/sessions.csv');args=p.parse_args()
df=pd.read_csv(args.data);out=Path('reports');out.mkdir(exist_ok=True)
df[FEATURES+['self_report_strain']].describe().to_csv(out/'descriptive_statistics.csv')
df[FEATURES+['self_report_strain']].corr(method='spearman').to_csv(out/'spearman_correlations.csv')
fig,axes=plt.subplots(2,3,figsize=(12,7));fig.patch.set_facecolor('#f7f6f0')
for ax,col in zip(axes.ravel(),FEATURES):
    ax.scatter(df[col],df.self_report_strain,s=15,alpha=.45,color='#708968');ax.set_xlabel(col.replace('_',' '));ax.set_ylabel('Self-report (0–10)');ax.spines[['top','right']].set_visible(False)
fig.suptitle('MindType · exploratory associations (not causal evidence)');fig.tight_layout();fig.savefig(out/'feature_associations.png',dpi=160)
print('EDA exports written to reports/. Inspect participant and device confounding before interpretation.')
