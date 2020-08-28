Model
======

Overview
~~~~~~~~~~

The trained model predicts the forest covertype from cartographic variables only.

Training and test data
~~~~~~~~~~~~~~~~~~~~~~~~

The training data origins from the `covertype dataset <https://archive.ics.uci.edu/ml/datasets/covertype>`_, which contains 581012 instances of 54 attributes.

Model architecture
~~~~~~~~~~~~~~~~~~~~~~

The model is based on `XGBoost <https://xgboost.readthedocs.io/en/latest/>`_.

Evaluation
~~~~~~~~~~~~~

The model was evaluated on 20% of unseen test data. The reported root mean squared error origins from the test data.
The full training history is viewable by running the mlflow user interface inside the root directory of this project:
``mlflow ui``.

Hyperparameter selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

No sophisticated Hyperparameter selection was conducted due to time constraints.

1. ``single-precision-histogram`` was enabled for faster training.
2. ``subsample`` was set to 0.5 for arbitrary reasons.
3. ``colsample_bytree`` was set to 0.5 for arbitrary reasons.
4. ``colsample_bylevel`` was set to 0.5 for arbitrary reasons.
