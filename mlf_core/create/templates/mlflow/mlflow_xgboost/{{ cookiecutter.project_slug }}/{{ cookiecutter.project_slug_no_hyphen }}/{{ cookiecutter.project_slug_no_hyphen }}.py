import click
import xgboost as xgb
import mlflow
import mlflow.xgboost
import time


from mlf_core.mlf_core import log_sys_intel_conda_env, set_general_random_seeds
from data_loading.data_loader import load_train_test_data


@click.command()
@click.option('--epochs', type=int, default=5, help='Number of epochs to train')
@click.option('--general-seed', type=int, default=0, help='General Python, Python random and Numpy seed.')
@click.option('--xgboost-seed', type=int, default=0, help='XGBoost specific random seed.')
@click.option('--cuda', type=click.Choice(['True', 'False']), help='Enable or disable CUDA support.')
@click.option('--single-precision-histogram', default=True, help='Enable or disable single precision histogram calculation.')
def start_training(epochs, general_seed, xgboost_seed, cuda, single_precision_histogram):
    use_cuda = True if cuda == 'True' else False

    with mlflow.start_run():
        # Fetch and prepare data
        dtrain, dtest = load_train_test_data()

        # Enable the logging of all parameters, metrics and models to mlflow
        mlflow.xgboost.autolog()

        # Set XGBoost parameters
        param = {
            'objective': 'multi:softmax',
            'num_class': 8,
        }
        param['single_precision_histogram'] = True if single_precision_histogram == 'True' else False
        param['subsample'] = 0.5
        param['colsample_bytree'] = 0.5
        param['colsample_bylevel'] = 0.5

        # Set random seeds
        set_general_random_seeds(general_seed)
        set_xgboost_random_seeds(xgboost_seed, param)

        # Set CPU or GPU as training device
        if not use_cuda:
            param['tree_method'] = 'hist'
        else:
            param['tree_method'] = 'gpu_hist'

        # Train on the chosen device
        results = {}
        runtime = time.time()
        xgb.train(param, dtrain, epochs, evals=[(dtest, 'test')], evals_result=results)
        device = 'GPU' if use_cuda else 'CPU'
        if use_cuda:
            click.echo(click.style(f'{device} Run Time: {str(time.time() - runtime)} seconds', fg='green'))

        # Log hardware and software
        log_sys_intel_conda_env('{{ cookiecutter.project_slug_no_hyphen }}')


def set_xgboost_random_seeds(seed, param):
    param['seed'] = seed


if __name__ == '__main__':
    start_training()