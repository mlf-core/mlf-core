import pytorch_lightning as pl
import torch
from argparse import ArgumentParser
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
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
        elif dict_args["accelerator"] != "ddp":
            print(f"[bold red]{dict_args['accelerator']}[bold blue] currently not supported. Switching to [bold green]ddp!")

    dm = MNISTDataModule(**dict_args)

    dm.prepare_data()
    dm.setup(stage="fit")
    model = LightningMNISTClassifier(len_test_set=len(dm.df_test), **dict_args)
    model.log_every_n_steps = dict_args['log_interval']

    # check, whether the run is inside a Docker container or not
    if 'MLF_CORE_DOCKER_RUN' in os.environ:
        checkpoint_callback = ModelCheckpoint(
            filepath='/mlflow/tmp/mlruns', save_top_k=1, verbose=True, monitor="train_loss", mode="min", prefix="",
        )
        trainer = pl.Trainer.from_argparse_args(args, checkpoint_callback=checkpoint_callback, default_root_dir='/data', logger=TensorBoardLogger('/data'))
        tensorboard_output_path = f'data/default/version_{trainer.logger.version}'
    else:
        checkpoint_callback = ModelCheckpoint(
            filepath=os.getcwd(), save_top_k=1, verbose=True, monitor="train_loss", mode="min", prefix="",
        )
        trainer = pl.Trainer.from_argparse_args(args, checkpoint_callback=checkpoint_callback)
        tensorboard_output_path = f'{os.getcwd()}/lightning_logs/version_{trainer.logger.version}'

    trainer.deterministic = True
    trainer.benchmark = False
    trainer.log_every_n_steps = dict_args['log_interval']
    trainer.fit(model, dm)
    trainer.test()
    print(f'\n[bold blue]For tensorboard log, call [bold green]tensorboard --logdir={tensorboard_output_path}')

