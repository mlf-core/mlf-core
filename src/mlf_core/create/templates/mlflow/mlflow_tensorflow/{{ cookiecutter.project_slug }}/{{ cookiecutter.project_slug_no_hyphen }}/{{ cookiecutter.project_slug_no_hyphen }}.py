from argparse import ArgumentParser
import tensorflow as tf
import mlflow
import mlflow.tensorflow
import os
import time
from rich import traceback, print

from mlf_core.mlf_core import MLFCore
from data_loading.data_loader import load_train_test_data
from model.model import create_model
from training.train import train, test


def start_training():
    parser = ArgumentParser(description='Tensorflow example')
    parser.add_argument(
        '--cuda',
        type=bool,
        default=True,
        help='Enable or disable CUDA support',
    )
    parser.add_argument(
        '--max_epochs',
        type=int,
        default=10,
        help='Number of epochs to train',
    )
    parser.add_argument(
        '--general-seed',
        type=int,
        default=0,
        help='General Python, Python random and Numpy seed.',
    )
    parser.add_argument(
        '--tensorflow-seed',
        type=int,
        default=0,
        help='Tensorflow specific random seed.',
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=64,
        help='Input batch size for training and testing',
    )
    parser.add_argument(
        '--buffer-size',
        type=int,
        default=10000,
        help='Buffer size for Mirrored Training',
    )
    parser.add_argument(
        '--lr',
        type=float,
        default=0.01,
        help='Learning rate',
    )
    args = parser.parse_args()
    dict_args = vars(args)
    # Disable GPU support if no GPUs are supposed to be used
    if not dict_args['cuda']:
        tf.config.set_visible_devices([], 'GPU')

    with mlflow.start_run():
        # Enable the logging of all parameters, metrics and models to mlflow and Tensorboard
        mlflow.autolog(1)

        # Log hardware and software
        MLFCore.log_sys_intel_conda_env()

        # Fix all random seeds and Tensorflow specific reproducibility settings
        MLFCore.set_general_random_seeds(dict_args["general_seed"])
        MLFCore.set_tensorflow_random_seeds(dict_args["tensorflow_seed"])

        # Use Mirrored Strategy for multi GPU support
        strategy = tf.distribute.MirroredStrategy()
        print(f'[bold blue]Number of devices: {strategy.num_replicas_in_sync}')

        # Fetch and prepare dataset
        train_dataset, eval_dataset = load_train_test_data(strategy, dict_args['batch_size'], dict_args['buffer_size'], dict_args['tensorflow_seed'])

        # TODO MLF-CORE: Enable input data logging
        # MLFCore.log_input_data('data/')

        with strategy.scope():
            # Define model and compile model
            model = create_model(input_shape=(28, 28, 1))
            model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          optimizer=tf.keras.optimizers.Adam(learning_rate=dict_args['lr']),
                          metrics=['accuracy'])

            # Train and evaluate the trained model
            runtime = time.time()
            train(model, dict_args['max_epochs'], train_dataset)
            eval_loss, eval_acc = test(model, eval_dataset)
            print(f'Test loss: {eval_loss}, Test Accuracy: {eval_acc}')

            device = 'GPU' if dict_args['cuda'] else 'CPU'
            print(f'[bold green]{device} Run Time: {str(time.time() - runtime)} seconds')

            print(f'[bold blue]\nLaunch TensorBoard with:\ntensorboard --logdir={os.path.join(mlflow.get_artifact_uri(), "tensorboard_logs", "train")}')


if __name__ == '__main__':
    traceback.install()
    print(f'Num GPUs Available: {len(tf.config.experimental.list_physical_devices("GPU"))}')

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Filtering out any Warnings messages

    start_training()
