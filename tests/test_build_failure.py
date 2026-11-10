import pandas as pd,pytest
from scripts.generate_build_dataset import generate_dataset
from src.build_failure.model import FEATURES,train_model,predict_build
def test_dataset_reproducible():pd.testing.assert_frame_equal(generate_dataset(100,7),generate_dataset(100,7))
def test_model_metrics():
 r=train_model(generate_dataset(300,9));assert set(r["metrics"])=={"accuracy","precision","recall","f1","roc_auc"};assert set(r["feature_importance"])==set(FEATURES)
def test_prediction_requires_all_features():
 r=train_model(generate_dataset(200,3))
 with pytest.raises(ValueError,match="missing features"):predict_build(r["model"],{"changed_files":2})
def test_prediction_probability():
 r=train_model(generate_dataset(300,5));f={"changed_files":8,"lines_added":250,"lines_deleted":50,"test_count":40,"previous_failures":2,"dependency_changed":1,"avg_test_duration_sec":45.0};p=predict_build(r["model"],f);assert p["prediction"] in {"SUCCESS","FAILURE"} and 0<=p["failure_probability"]<=1
