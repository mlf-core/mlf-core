import click
import xgboost as xgb
import time
import mlflow
import GPUtil
import mlflow.xgboost

from dask_cuda import LocalCUDACluster
from dask.distributed import LocalCluster, Client
from dask import array as da
from xgboost.dask import DaskDMatrix
from sklearn.datasets import fetch_covtype, load_boston
from dask_ml.model_selection import train_test_split
from mlf_core.mlf_core import log_sys_intel_conda_env, set_general_random_seeds

from rich import traceback


@click.command()
@click.option('--cuda', type=click.Choice(['True', 'False']), default=True, help='Enable or disable CUDA support.')
@click.option('--n-workers', type=int, default=2, help='Number of workers. Equivalent to number of GPUs.')
@click.option('--epochs', type=int, default=5, help='Number of epochs to train')
@click.option('--general-seed', type=int, default=0, help='General Python, Python random and Numpy seed.')
@click.option('--xgboost-seed', type=int, default=0, help='XGBoost specific random seed.')
@click.option('--single-precision-histogram', default=True, help='Enable or disable single precision histogram calculation.')
def start_training(cuda, n_workers, epochs, general_seed, xgboost_seed, single_precision_histogram):
    avail_gpus = GPUtil.getGPUs()
    use_cuda = True if cuda == 'True' and len(avail_gpus) > 0 else False
    if use_cuda:
        click.echo(click.style(f'Using {len(avail_gpus)} GPUs!', fg='blue'))
    else:
        click.echo(click.style('No GPUs detected. Running on the CPU', fg='blue'))

    with mlflow.start_run():
        # Enable the logging of all parameters, metrics and models to mlflow and Tensorboard
        mlflow.xgboost.autolog()

        # Setup a Dask cluster to facilitate multiCPU/multiGPU training
        if use_cuda:
            cluster = LocalCUDACluster(n_workers=n_workers, threads_per_worker=1)
        else:
            cluster = LocalCluster(n_workers=n_workers, threads_per_worker=1)
        with cluster as cluster:
            with Client(cluster) as client:
                # Fetch and prepare data
                dtrain, dtest = load_train_test_data(client)

                # Set XGBoost parameters
                param = {'objective': 'multi:softmax',
                         'num_class': 8,
                         'single_precision_histogram': True if single_precision_histogram == 'True' else False,
                         'subsample': 0.5,
                         'colsample_bytree': 0.5,
                         'colsample_bylevel': 0.5,
                         'verbosity': 2}

                # Set random seeds
                set_general_random_seeds(general_seed)
                set_xgboost_dask_random_seeds(xgboost_seed, param)

                # Set CPU or GPU as training device
                if use_cuda:
                    param['tree_method'] = 'gpu_hist'
                else:
                    param['tree_method'] = 'hist'

                runtime = time.time()
                trained_xgboost_model = xgb.dask.train(client,
                                                       param,
                                                       dtrain,
                                                       num_boost_round=epochs,
                                                       evals=[(dtest, 'test')])
                mlflow.xgboost.log_model(trained_xgboost_model['booster'], 'model')
                mlflow.log_metric('test merror', trained_xgboost_model['history']['test']['merror'][-1])
                click.echo(trained_xgboost_model['history'])

                device = 'GPU' if use_cuda else 'CPU'
                if use_cuda:
                    click.echo(click.style(f'{device} Run Time: {str(time.time() - runtime)} seconds', fg='green'))

                # Log hardware and software
                log_sys_intel_conda_env()


def load_train_test_data(client):
    dataset = fetch_covtype()

    # Rechunking is required for the covertype dataset
    X = da.from_array(dataset.data, chunks=1000)
    y = da.from_array(dataset.target, chunks=1000)

    # Create 0.75/0.25 train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=0)

    dtrain = DaskDMatrix(client, X_train, y_train)
    dtest = DaskDMatrix(client, X_test, y_test)

    return dtrain, dtest


def set_xgboost_dask_random_seeds(seed, param):
    param['seed'] = seed


if __name__ == '__main__':
    traceback.install()
    start_training()
