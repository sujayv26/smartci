# SMART CI — ASSIGNMENT 4

## A4_5: Build-Failure Prediction

**Name:** Sujay V | **USN:** 24BTRAO041  
**GitHub Repository:** https://github.com/sujayv26/smartci

### 1. Aim
To develop a machine-learning model that predicts whether a software build is likely to succeed or fail using historical build characteristics such as code changes, test activity, previous failures, dependency changes, and test execution duration.

### 2. Introduction
Build pipelines compile code and execute automated tests. Unexpected failures delay development and deployment. A predictive model can estimate failure risk and help developers prioritize inspection. This assignment implements supervised binary classification using a reproducible synthetic historical dataset. The dataset demonstrates the ML workflow and is not represented as real production CI history.

### 3. Tools and Technologies
- Python 3.12
- Pandas and NumPy for dataset preparation
- Scikit-learn for model training and evaluation
- Random Forest Classifier for binary classification
- Joblib for local model persistence
- pytest for automated testing
- Git and GitHub

### 4. Implementation
**4.1 Dataset generation — `scripts/generate_build_dataset.py`**  
A reproducible dataset of 800 synthetic build records is generated using a fixed random seed. Each row contains changed files, lines added, lines deleted, test count, previous failure count, dependency-change indicator, average test duration, and target `build_failed`. The dataset is saved as `data/build_history.csv`.

**4.2 Feature selection — `src/build_failure/model.py`**  
Seven input features are used: `changed_files`, `lines_added`, `lines_deleted`, `test_count`, `previous_failures`, `dependency_changed`, and `avg_test_duration_sec`. The target is `build_failed`, where 1 represents failure and 0 represents success.

**4.3 Model training**  
The data is divided into training and testing subsets using a stratified 75:25 split and fixed random state. A Random Forest Classifier with 250 trees, maximum depth 9, balanced class weights, and a fixed seed is trained.

**4.4 Evaluation**  
The held-out test subset is evaluated using accuracy, precision, recall, F1-score, and ROC-AUC. Feature importance is extracted to show which variables contributed most to the fitted model.

**4.5 Prediction**  
The `predict_build()` function accepts the seven build features and returns `SUCCESS` or `FAILURE` with estimated failure probability. The CLI loads the saved model and accepts feature values as arguments.

### 5. Execution and Workflow Configuration
Install:
```bash
python -m pip install -r requirements.txt
```
Generate data:
```bash
python -m scripts.generate_build_dataset --rows 800 --seed 42
```
Train and evaluate:
```bash
python -m scripts.train_build_failure_model
```
Predict a sample build:
```bash
python -m scripts.predict_build --changed-files 8 --lines-added 250 --lines-deleted 50 --test-count 40 --previous-failures 2 --dependency-changed 1 --avg-test-duration-sec 45
```
The trained model is saved to `artifacts/build_failure_model.joblib`. The artifact is excluded from Git and can be recreated by running the training command. If the CSV is absent, the training script creates the default synthetic dataset.

### 6. Experiments and Observations
**Experiment 1 — Dataset generation:** The generator creates 800 records with seed 42. Re-running with the same row count and seed produces the same dataset.

**Experiment 2 — Model evaluation:** The verified local held-out metrics were:

| Metric | Result |
|---|---:|
| Accuracy | 0.750 |
| Precision | 0.697 |
| Recall | 0.662 |
| F1-score | 0.679 |
| ROC-AUC | 0.808 |

**Experiment 3 — Feature importance:** Average test duration, test count, and lines added were the three highest-importance features in this run. Feature importance describes the fitted model and does not establish causation.

**Experiment 4 — Sample prediction:** For 8 changed files, 250 lines added, 50 lines deleted, 40 tests, 2 previous failures, dependency change enabled, and 45-second average test duration, the verified local run predicted `FAILURE` with an 87.9% estimated failure probability.

### 7. Screenshots and Results
Add actual screenshots from your local run:
- Figure 1. Dataset generation showing 800 synthetic records.
- Figure 2. Model training metrics and feature importance.
- Figure 3. CLI prediction and failure probability.
- Figure 4. Successful pytest output for build-failure prediction tests.

### 8. Learning Outcomes
- Understood supervised binary classification.
- Generated and inspected tabular data using Pandas and NumPy.
- Learned feature selection, target labels, and stratified train-test splitting.
- Implemented a Random Forest classifier using Scikit-learn.
- Evaluated a classifier with accuracy, precision, recall, F1-score, and ROC-AUC.
- Interpreted feature importance and used a saved model for new predictions.
- Understood why synthetic-data results are not production performance evidence.

### 9. Conclusion
A build-failure prediction baseline was implemented using a Random Forest classifier trained on 800 reproducible synthetic build records. The verified held-out evaluation achieved 0.750 accuracy and 0.808 ROC-AUC. The system saves the trained model locally and predicts the outcome and estimated failure probability for a new build. Real historical CI data would be required for production validation.

### 10. GitHub Repository
https://github.com/sujayv26/smartci
