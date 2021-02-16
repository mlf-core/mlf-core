from argparse import ArgumentParser
import xgboost as xgb
import time
import mlflow
import GPUtil
import mlflow.xgboost
from rich import traceback, print
from dask_cuda import LocalCUDACluster
from dask.distributed import LocalCluster, Client
from dask import array as da
from xgboost.dask import DaskDMatrix
from sklearn.datasets import fetch_covtype
from dask_ml.model_selection import train_test_split

from mlf_core.mlf_core import MLFCore


def start_training():
    parser = ArgumentParser(description='XGBoost Dask example')
    parser.add_argument(
        '--max_epochs',
        type=int,
        default=25,
        help='Number of epochs to train',
    )
    parser.add_argument(
        '--general-seed',
        type=int,
        default=0,
        help='General Python, Python random and Numpy seed.',
    )
    parser.add_argument(
        '--xgboost-seed',
        type=int,
        default=0,
        help='XGBoost specific random seed.',
    )
    parser.add_argument(
        '--cuda',
        type=bool,
        default=True,
        help='Enable or disable CUDA support.',
    )
    parser.add_argument(
        '--n-workers',
        type=int,
        default=2,
        help='Number of workers. Equivalent to number of GPUs.',
    )
    parser.add_argument(
        '--single-precision-histogram',
        type=bool,
        default=True,
        help='Enable or disable single precision histogram calculation.',
    )
    avail_gpus = GPUtil.getGPUs()
    args = parser.parse_args()
    dict_args = vars(args)
    use_cuda = True if dict_args['cuda'] and len(avail_gpus) > 0 else False
    if use_cuda:
        print(f'[bold blue]Using {len(avail_gpus)} GPUs!')
    else:
        print('[bold blue]No GPUs detected. Running on the CPU')

    with mlflow.start_run():
        # Enable the logging of all parameters, metrics and models to mlflow and Tensorboard
        mlflow.autolog(1)

        # Setup a Dask cluster to facilitate multiCPU/multiGPU training
        if use_cuda:
            cluster = LocalCUDACluster(n_workers=dict_args['n_workers'], threads_per_worker=1)
        else:
            cluster = LocalCluster(n_workers=dict_args['n_workers'], threads_per_worker=1)
        with cluster as cluster:
            with Client(cluster) as client:
                # Fetch and prepare data
                dtrain, dtest = load_train_test_data(client)

                # Set XGBoost parameters
                param = {'objective': 'multi:softmax',
                         'num_class': 8,
                         'single_precision_histogram': True if dict_args['single_precision_histogram'] == 'True' else False,
                         'subsample': 0.5,
                         'colsample_bytree': 0.5,
                         'colsample_bylevel': 0.5,
                         'verbosity': 2}

                # Set random seeds
                MLFCore.set_general_random_seeds(dict_args["general_seed"])
                MLFCore.set_xgboost_dask_random_seeds(dict_args["xgboost_seed"], param)

                # Set CPU or GPU as training device
                if use_cuda:
                    param['tree_method'] = 'gpu_hist'
                else:
                    param['tree_method'] = 'hist'

                runtime = time.time()
                trained_xgboost_model = xgb.dask.train(client,
                                                       param,
                                                       dtrain,
                                                       num_boost_round=dict_args['max_epochs'],
                                                       evals=[(dtest, 'test')])
                mlflow.xgboost.log_model(trained_xgboost_model['booster'], 'model')
                mlflow.log_metric('test mlogloss', trained_xgboost_model['history']['test']['mlogloss'][-1])
                print(trained_xgboost_model['history'])

                device = 'GPU' if use_cuda else 'CPU'
                if use_cuda:
                    print(f'[bold green]{device} Run Time: {str(time.time() - runtime)} seconds')

                # Log hardware and software
                MLFCore.log_sys_intel_conda_env()


def load_train_test_data(client):
    dataset = fetch_covtype()

    # TODO MLF-CORE: Enable input data logging
    # MLFCore.log_input_data('data/')

    # Rechunking is required for the covertype dataset
    X = da.from_array(dataset.data, chunks=1000)
    y = da.from_array(dataset.target, chunks=1000)

    # Create 0.75/0.25 train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=0)

    dtrain = DaskDMatrix(client, X_train, y_train)
    dtest = DaskDMatrix(client, X_test, y_test)

    return dtrain, dtest


if __name__ == '__main__':
    traceback.install()
    start_training()
