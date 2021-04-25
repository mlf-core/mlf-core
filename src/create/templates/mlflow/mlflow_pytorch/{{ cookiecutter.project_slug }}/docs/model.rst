
Model
======

TODO MLF-CORE: Write your model documentation here.

Overview
~~~~~~~~~~

The trained model classifies images of handwritten digits into the written number.

Training and test data
~~~~~~~~~~~~~~~~~~~~~~~~

The training data origins from the classical machine learning benchmark dataset `mnist <http://yann.lecun.com/exdb/mnist/>`_.
60000 images are part of the training dataset and a further 10000 can be used for testing.
For more details visit the `mnist website <http://yann.lecun.com/exdb/mnist/>`_.

Model architecture
~~~~~~~~~~~~~~~~~~~~~~

The model is based on `Pytorch <https://pytorch.org/>`_ and `Pytorch Lightning <https://github.com/PyTorchLightning/pytorch-lightning>`_.
On a high level the model can be summarized as follows:
1. 1x convolutional layer
2. 1x rectified linear activation function
3. 1x convolutional layer
4. 1x rectified linear activation function
5. 1x 2D max pooling layer
6. 1x 0.25 dropout layer
7. 1x flatten layer
8. 1x fully connected layer
9. 1x rectified linear activation function
10. 1x 0.25 dropout layer
11. 1x fully connected layer
12. log softmax generating the final output

Evaluation
~~~~~~~~~~~~~

The model was evaluated on 20% (10000 images) of unseen test data. The loss origins from the test data.
The full training history is viewable by running the mlflow user interface inside the root directory of this project:
``mlflow ui``.

Hyperparameter selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hyperparameters were chosen on widely known strong defaults.

1. ``Adam optimizer`` was chosen for strong, general performance.
