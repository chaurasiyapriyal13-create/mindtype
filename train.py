"""Participant-separated model comparison for self-reported strain regression."""
from pathlib import Path
import argparse, json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.analytics import FEATURES
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',default=str(ROOT/'data'/'sessions.csv'));p.add_argument('--source',choices=['real','synthetic'],required=True);args=p.parse_args()
    df=pd.read_csv(args.data)
    required=['participant_id','self_report_strain',*FEATURES]
    if not set(required)<=set(df.columns): raise ValueError('Dataset is missing required columns.')
    if df[required].isna().any().any(): raise ValueError('Dataset contains missing values; inspect and clean before training.')
    if not np.isfinite(df[['self_report_strain',*FEATURES]].to_numpy(dtype=float)).all(): raise ValueError('Non-finite values in dataset.')
    if not df.self_report_strain.between(0,10).all(): raise ValueError('Ratings must be 0–10.')
    if df.participant_id.nunique()<10: raise ValueError('Collect at least 10 participants to exercise this split. This minimum does not establish statistical adequacy.')
    train,test=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(df,groups=df.participant_id))
    X=df[FEATURES];y=df.self_report_strain;groups=df.participant_id
    candidates={'mean_baseline':DummyRegressor(),'ridge':make_pipeline(StandardScaler(),Ridge(alpha=10)),'random_forest':RandomForestRegressor(n_estimators=150,max_depth=5,min_samples_leaf=4,random_state=42,n_jobs=-1)}
    cv=GroupKFold(n_splits=min(5,groups.iloc[train].nunique()))
    scores={}
    for name,model in candidates.items():
        mae=-cross_val_score(model,X.iloc[train],y.iloc[train],groups=groups.iloc[train],cv=cv,scoring='neg_mean_absolute_error').mean()
        scores[name]={'training_group_cv_mae':round(float(mae),4)}
    best=min(scores,key=lambda n:scores[n]['training_group_cv_mae'])
    model=candidates[best].fit(X.iloc[train],y.iloc[train]);pred=model.predict(X.iloc[test])
    metrics={'source':args.source,'target':'self-reported current strain (0–10), not diagnosis','selected_model':best,'selection':'group cross-validation on training participants only','candidates':scores,'held_out_mae':float(mean_absolute_error(y.iloc[test],pred)),'held_out_rmse':float(np.sqrt(mean_squared_error(y.iloc[test],pred))),'train_participants':int(groups.iloc[train].nunique()),'test_participants':int(groups.iloc[test].nunique()),'participant_overlap':len(set(groups.iloc[train])&set(groups.iloc[test])),'sessions':len(df),'limitations':'Exploratory performance on this dataset; no clinical validation. Small datasets produce unstable estimates.'}
    # Synthetic smoke tests are saved separately and never loaded by the live app.
    out=ROOT/'models'/('synthetic_demo' if args.source=='synthetic' else '');out.mkdir(parents=True,exist_ok=True)
    joblib.dump({'model':model,'source':args.source,'features':FEATURES},out/'regressor.joblib')
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2))
    print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
