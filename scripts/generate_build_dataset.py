import argparse
from pathlib import Path
import numpy as np,pandas as pd
def generate_dataset(rows:int=800,seed:int=42)->pd.DataFrame:
 rng=np.random.default_rng(seed);changed=rng.poisson(5,rows).clip(0,35);added=(changed*rng.uniform(8,45,rows)).astype(int);deleted=(changed*rng.uniform(2,25,rows)).astype(int);tests=rng.integers(5,180,rows);previous=rng.poisson(.7,rows).clip(0,6);dependency=rng.binomial(1,.14,rows);duration=rng.gamma(2.2,18,rows).clip(2,180).round(2)
 score=-3.2+.13*changed+.006*added+.95*previous+1.8*dependency+.028*duration-.009*tests;prob=1/(1+np.exp(-score));failed=rng.binomial(1,prob)
 return pd.DataFrame({"build_id":[f"BUILD-{i:04d}" for i in range(1,rows+1)],"changed_files":changed,"lines_added":added,"lines_deleted":deleted,"test_count":tests,"previous_failures":previous,"dependency_changed":dependency,"avg_test_duration_sec":duration,"build_failed":failed})
def main():
 p=argparse.ArgumentParser();p.add_argument("--rows",type=int,default=800);p.add_argument("--seed",type=int,default=42);p.add_argument("--output",type=Path,default=Path("data/build_history.csv"));a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);generate_dataset(a.rows,a.seed).to_csv(a.output,index=False);print(f"Generated {a.rows} synthetic build records at {a.output}")
if __name__=="__main__":main()
