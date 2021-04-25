from argparse import ArgumentParser
import xgboost as xgb
import mlflow
import mlflow.xgboost
import time
import GPUtil
from rich import traceback, print

from mlf_core.mlf_core import MLFCore
from data_loading.data_loader import load_train_test_data


def start_training():
    parser = ArgumentParser(description='XGBoost Example')
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
        # Enable the logging of all parameters, metrics and models to mlflow
        mlflow.autolog(1)

        # Log hardware and software
        MLFCore.log_sys_intel_conda_env()

        # Fetch and prepare data
        dtrain, dtest = load_train_test_data()

        # TODO MLF-CORE: Enable input data logging
        # MLFCore.log_input_data('data/')

        # Set XGBoost parameters
        param = {'objective': 'multi:softmax',
                 'num_class': 8,
                 'single_precision_histogram': True if dict_args['single_precision_histogram'] == 'True' else False,
                 'subsample': 0.5,
                 'colsample_bytree': 0.5,
                 'colsample_bylevel': 0.5}

        # Set random seeds
        MLFCore.set_general_random_seeds(dict_args["general_seed"])
        MLFCore.set_xgboost_random_seeds(dict_args["xgboost_seed"], param)

        # Set CPU or GPU as training device
        if use_cuda:
            param['tree_method'] = 'gpu_hist'
        else:
            param['tree_method'] = 'hist'

        # Train on the chosen device
        results = {}
        runtime = time.time()
        xgb.train(param, dtrain, dict_args['max_epochs'], evals=[(dtest, 'test')], evals_result=results)
        device = 'GPU' if use_cuda else 'CPU'
        if use_cuda:
            print(f'[bold green]{device} Run Time: {str(time.time() - runtime)} seconds')


if __name__ == '__main__':
    traceback.install()
    start_training()
