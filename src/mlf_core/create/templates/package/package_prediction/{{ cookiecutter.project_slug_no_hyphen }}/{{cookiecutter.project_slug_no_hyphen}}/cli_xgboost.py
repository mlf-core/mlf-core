import os
import sys
from dataclasses import dataclass

import click
import numpy as np
import xgboost as xgb

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
        model = get_xgboost_model(f'{WD}/models/xgboost_test_model.xgb')
    else:
        model = get_xgboost_model(model)
    if cuda:
        model.set_param({'predictor': 'gpu_predictor'})
    print('[bold blue] Parsing data')
    data_to_predict = parse_data_to_predict(input)
    print('[bold blue] Performing predictions')
    predictions = np.round(model.predict(data_to_predict.DM))
    print(predictions)
    if output:
        print(f'[bold blue]Writing predictions to {output}')
        write_results(predictions, output)


@dataclass
class Dataset:
    X: np.ndarray
    y: list
    DM: xgb.DMatrix
    gene_names: list
    sample_names: list


def parse_data_to_predict(path_to_data_to_predict: str) -> Dataset:
    """
    Parses the data to predict and returns a full Dataset include the DMatrix
    :param path_to_data_to_predict: Path to the data on which predictions should be performed on
    """
    X = []
    y = []
    gene_names = []
    sample_names = []
    with open(path_to_data_to_predict, "r") as file:
        all_runs_info = next(file).split("\n")[0].split("\t")[2:]
        for run_info in all_runs_info:
            split_info = run_info.split("_")
            y.append(int(split_info[0]))
            sample_names.append(split_info[1])
        for line in file:
            split = line.split("\n")[0].split("\t")
            X.append([float(x) for x in split[2:]])
            gene_names.append(split[:2])

    X = [list(i) for i in zip(*X)]

    X_np = np.array(X)
    DM = xgb.DMatrix(X_np, label=y)

    return Dataset(X_np, y, DM, gene_names, sample_names)


def write_results(predictions: np.ndarray, path_to_write_to) -> None:
    """
    Writes the predictions into a human readable file.
    :param predictions: Predictions as a numpy array
    :param path_to_write_to: Path to write the predictions to
    """
    np.savetxt(path_to_write_to, predictions, delimiter=',')


def get_xgboost_model(path_to_xgboost_model: str):
    """
    Fetches the model of choice and creates a booster from it.
    :param path_to_xgboost_model: Path to the xgboost model1
    """
    model = xgb.Booster()
    model.load_model(os.path.abspath(path_to_xgboost_model))

    return model


if __name__ == "__main__":
    traceback.install()
    sys.exit(main())  # pragma: no cover
