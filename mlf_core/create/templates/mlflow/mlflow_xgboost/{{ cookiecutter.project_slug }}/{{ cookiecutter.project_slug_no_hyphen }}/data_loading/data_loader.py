import xgboost as xgb

from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split


def load_train_test_data():
    # Fetch dataset using sklearn
    dataset = fetch_covtype()
    X = dataset.data
    y = dataset.target

    # Create 0.75/0.25 train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=0)

    # Convert input data from numpy to XGBoost format
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    return dtrain, dtest
