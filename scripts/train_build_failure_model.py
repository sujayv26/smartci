from pathlib import Path
import joblib,pandas as pd
from src.build_failure.model import train_model
from scripts.generate_build_dataset import generate_dataset
def main():
 path=Path("data/build_history.csv")
 if not path.exists():path.parent.mkdir(parents=True,exist_ok=True);generate_dataset(800,42).to_csv(path,index=False);print("Generated reproducible synthetic dataset")
 result=train_model(pd.read_csv(path));out=Path("artifacts/build_failure_model.joblib");out.parent.mkdir(parents=True,exist_ok=True);joblib.dump(result["model"],out)
 print("Held-out metrics:");[print(f"{k}: {v:.3f}") for k,v in result["metrics"].items()];print("Feature importance:");[print(f"{k}: {v:.3f}") for k,v in result["feature_importance"].items()];print(f"Model saved to {out}")
if __name__=="__main__":main()
