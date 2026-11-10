import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
FEATURES=["changed_files","lines_added","lines_deleted","test_count","previous_failures","dependency_changed","avg_test_duration_sec"]
TARGET="build_failed"
def train_model(data:pd.DataFrame,random_state:int=42)->dict:
 missing=set(FEATURES+[TARGET])-set(data.columns)
 if missing:raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
 if data.empty or data[TARGET].nunique()!=2:raise ValueError("Training data must contain successful and failed builds")
 labels=data[TARGET].astype(int);xtr,xte,ytr,yte=train_test_split(data[FEATURES],labels,test_size=.25,random_state=random_state,stratify=labels)
 model=RandomForestClassifier(n_estimators=250,max_depth=9,min_samples_leaf=3,class_weight="balanced",random_state=random_state,n_jobs=-1);model.fit(xtr,ytr)
 pred=model.predict(xte);probs=model.predict_proba(xte)[:,1]
 metrics={"accuracy":float(accuracy_score(yte,pred)),"precision":float(precision_score(yte,pred,zero_division=0)),"recall":float(recall_score(yte,pred,zero_division=0)),"f1":float(f1_score(yte,pred,zero_division=0)),"roc_auc":float(roc_auc_score(yte,probs))}
 importance=dict(sorted(zip(FEATURES,model.feature_importances_.tolist()),key=lambda x:x[1],reverse=True))
 return {"model":model,"metrics":metrics,"feature_importance":importance}
def predict_build(model,features:dict)->dict:
 missing=set(FEATURES)-set(features)
 if missing:raise ValueError(f"Prediction is missing features: {', '.join(sorted(missing))}")
 row=pd.DataFrame([{k:features[k] for k in FEATURES}],columns=FEATURES);prob=float(model.predict_proba(row)[0][1])
 return {"failure_probability":prob,"prediction":"FAILURE" if prob>=.5 else "SUCCESS"}
