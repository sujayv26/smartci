import argparse
from pathlib import Path
import joblib
from src.build_failure.model import predict_build
def main():
 p=argparse.ArgumentParser();p.add_argument("--changed-files",type=int,required=True);p.add_argument("--lines-added",type=int,required=True);p.add_argument("--lines-deleted",type=int,required=True);p.add_argument("--test-count",type=int,required=True);p.add_argument("--previous-failures",type=int,required=True);p.add_argument("--dependency-changed",type=int,choices=[0,1],required=True);p.add_argument("--avg-test-duration-sec",type=float,required=True);a=p.parse_args();path=Path("artifacts/build_failure_model.joblib")
 if not path.exists():raise SystemExit("Model not found. Run: python -m scripts.train_build_failure_model")
 features={"changed_files":a.changed_files,"lines_added":a.lines_added,"lines_deleted":a.lines_deleted,"test_count":a.test_count,"previous_failures":a.previous_failures,"dependency_changed":a.dependency_changed,"avg_test_duration_sec":a.avg_test_duration_sec};result=predict_build(joblib.load(path),features);print(f"Prediction: {result['prediction']}");print(f"Failure probability: {result['failure_probability']:.1%}")
if __name__=="__main__":main()
