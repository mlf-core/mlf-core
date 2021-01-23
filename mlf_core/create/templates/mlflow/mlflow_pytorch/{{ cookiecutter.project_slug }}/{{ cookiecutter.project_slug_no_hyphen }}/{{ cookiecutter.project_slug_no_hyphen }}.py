#
# Trains an MNIST digit recognizer using PyTorch Lightning,
# and uses Mlflow to log metrics, params and artifacts
# NOTE: This example requires you to first install
# pytorch-lightning (using pip install pytorch-lightning)
#       and mlflow (using pip install mlflow).
#
# pylint: disable=arguments-differ
# pylint: disable=unused-argument
# pylint: disable=abstract-method
import pytorch_lightning as pl
import torch
from argparse import ArgumentParser
from pytorch_lightning.callbacks import ModelCheckpoint
import mlflow
from data_loading.data_loader import MNISTDataModule
from model.model import LightningMNISTClassifier
from mlf_core.mlf_core import log_sys_intel_conda_env, set_pytorch_random_seeds, set_general_random_seeds
import os
from rich import print


if __name__ == "__main__":
    parser = ArgumentParser(description="PyTorch Autolog Mnist Example")
    parser.add_argument(
        "--general-seed",
        type=int,
        default=0,
        help="number of workers (default: 3)",
    )
    parser.add_argument(
        "--pytorch-seed",
        type=int,
        default=0,
        help="number of workers (default: 3)",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=100,
        help="log interval (default: 100)",
    )

    # Set GPU settings
    # click option cuda
    use_cuda = (True if 'True' == 'True' else False) and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    if use_cuda and torch.cuda.device_count() > 0:
        print(f'[bold blue]Using {torch.cuda.device_count()} GPUs!')

    parser = pl.Trainer.add_argparse_args(parent_parser=parser)
    parser = LightningMNISTClassifier.add_model_specific_args(parent_parser=parser)

    mlflow.pytorch.autolog()
    # log conda env and system information
    log_sys_intel_conda_env()
    # parse cli arguments
    args = parser.parse_args()
    dict_args = vars(args)

    set_general_random_seeds(dict_args['general_seed'])
    set_pytorch_random_seeds(dict_args['pytorch_seed'], True)

    if "accelerator" in dict_args:
        if dict_args["accelerator"] == "None":
            dict_args["accelerator"] = None

    dm = MNISTDataModule(**dict_args)

    dm.prepare_data()
    dm.setup(stage="fit")
    model = LightningMNISTClassifier(len_test_set=len(dm.df_test), **dict_args)
    model.log_every_n_steps = dict_args['log_interval']

    checkpoint_callback = ModelCheckpoint(
        filepath=os.getcwd(), save_top_k=1, verbose=True, monitor="train_loss", mode="min", prefix="",
    )

    trainer = pl.Trainer.from_argparse_args(
        args, checkpoint_callback=checkpoint_callback
    )
    trainer.deterministic = True
    trainer.benchmark = False
    trainer.log_every_n_steps = dict_args['log_interval']
    trainer.fit(model, dm)
    trainer.test()
