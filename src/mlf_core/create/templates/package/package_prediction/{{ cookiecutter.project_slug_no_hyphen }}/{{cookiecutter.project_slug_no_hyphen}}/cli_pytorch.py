import os
import sys

import click
import numpy as np
import torch

from rich import traceback, print

WD = os.path.dirname(__file__)


@click.command()
@click.option('-i', '--input', required=True, type=str, help='Path to data file to predict.')
@click.option('-m', '--model', type=str, help='Path to an already trained XGBoost model. If not passed a default model will be loaded.')
@click.option('-c/-nc', '--cuda/--no-cuda', type=bool, default=False, help='Whether to enable cuda or not')
@click.option('-o', '--output', type=str, help='Path to write the output to')
def main(input: str, model: str, cuda: bool, output: str):
    """Command-line interface for {{ cookiecutter.project_name }}"""

    print(r"""[bold blue]
        {{ cookiecutter.project_name }}
        """)

    print('[bold blue]Run [green]{{ cookiecutter.project_name }} --help [blue]for an overview of all commands\n')
    if not model:
        model = get_pytorch_model(f'{WD}/models/pytorch_test_model')
    else:
        model = get_pytorch_model(model)
    if cuda:
        model.cuda()
    print('[bold blue] Parsing data')
    data_to_predict = read_data_to_predict(input)
    print('[bold blue] Performing predictions')
    predictions = np.round(model.predict(data_to_predict))
    print(predictions)
    if output:
        print(f'[bold blue]Writing predictions to {output}')
        write_results(predictions, output)


def read_data_to_predict(path_to_data_to_predict: str):
    """
    Parses the data to predict and returns a full Dataset include the DMatrix
    :param path_to_data_to_predict: Path to the data on which predictions should be performed on
    """
    return


def write_results(predictions: np.ndarray, path_to_write_to) -> None:
    """
    Writes the predictions into a human readable file.
    :param predictions: Predictions as a numpy array
    :param path_to_write_to: Path to write the predictions to
    """
    pass


def get_pytorch_model(path_to_pytorch_model: str):
    """
    Fetches the model of choice and creates a booster from it.
    :param path_to_pytorch_model: Path to the xgboost model1
    """
    model = torch.load(path_to_pytorch_model)
    return model


if __name__ == "__main__":
    traceback.install()
    sys.exit(main())  # pragma: no cover
