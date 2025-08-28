# IArtProj2

This project focuses on the supervised classification of mushrooms as edible or poisonous, based on morphological and ecological features. It was developed as part of an academic assignment and follows the **CRISP-DM methodology**, structured into five phases.

## Project Structure

Each phase of the CRISP-DM cycle is documented in a dedicated file:

- **[0. Business Understanding](0.BusinessUnderstanding.md)** — Defines the goals, context, and motivation for the project.
- **[1. Data Understanding](1.DataUnderstanding.ipynb)** — Exploratory data analysis and initial insights.
- **[2. Data Preparation](2.DataPreparation.ipynb)** — Feature engineering, encoding, handling missing values, and preprocessing.
- **[3. Modeling and Evaluation](3.ModelingAndEvaluation.ipynb)** — Training and evaluation of multiple models, feature selection, PCA, hyperparameter tuning.
- **[4. Deployment](4.Deployment.ipynb)** — Final model training on full data and submission to Kaggle.

## How to Run

To run this project:

1. Ensure you have Python 3.8+ and Jupyter Notebook installed.
2. Clone or download the repository.
3. Ensure you have the following files in you data directory (test.csv, train.csv)
4. Rerun the notebooks if you don't have the following files in your data directory (processed_train.csv, processed_train_full.csv, submission.csv)
5. Open files 1–4 in Jupyter Notebook or your preferred IDE.
6. Run all cells in order.

> The notebooks are mostly self-contained and include code, outputs, and comments for reproducibility and understanding. Make sure you have the required files to run each notebook.

## Requirements

You will need the following Python libraries:

- `pandas`
- `numpy`
- `scikit-learn`
- `xgboost`
- `optuna`
- `matplotlib`
- `seaborn`
- `scipy`

You can install them via:
```bash
pip install -r requirements.txt
```

## Dataset

The dataset is a synthetic yet realistic mushroom dataset provided for a kaggle competition. It contains 3.1M samples with 18 categorical features and 3 numerical features.

## Results

The final model (XGBoost) was tuned using Optuna and trained on the full dataset. It achieved **competitive performance**, with accuracy ≈ **0.9911** and **ROC AUC ≈ 0.9969**, ranking **~0.1–0.2% below the top 1** on the Kaggle leaderboard.

---

For further details, refer to each notebook and the accompanying plots and comments.