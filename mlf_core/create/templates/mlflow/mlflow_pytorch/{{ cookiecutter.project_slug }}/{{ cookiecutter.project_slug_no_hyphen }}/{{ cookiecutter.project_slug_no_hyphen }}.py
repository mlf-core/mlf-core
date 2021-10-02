import os
from argparse import ArgumentParser

import mlflow
import pytorch_lightning as pl
from data_loading.data_loader import MNISTDataModule
from model.model import LightningMNISTClassifier
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
from rich import print

from mlf_core.mlf_core import MLFCore

if __name__ == "__main__":
    parser = ArgumentParser(description='PyTorch Autolog Mnist Example')
    parser.add_argument(
        '--general-seed',
        type=int,
        default=0,
        help='General random seed',
    )
    parser.add_argument(
        '--pytorch-seed',
        type=int,
        default=0,
        help='Random seed of all Pytorch functions',
    )
    parser.add_argument(
        '--log-interval',
        type=int,
        default=100,
        help='log interval of stdout',
    )
    parser = pl.Trainer.add_argparse_args(parent_parser=parser)
    parser = LightningMNISTClassifier.add_model_specific_args(parent_parser=parser)

    mlflow.autolog(1)
    # log conda env and system information
    MLFCore.log_sys_intel_conda_env()
    # parse cli arguments
    args = parser.parse_args()
    dict_args = vars(args)
    # store seed and number of gpus to make linter bit less restrict in terms of naming
    general_seed = dict_args['general_seed']
    pytorch_seed = dict_args['pytorch_seed']
    num_of_gpus = dict_args['gpus']
    MLFCore.set_general_random_seeds(general_seed)
    MLFCore.set_pytorch_random_seeds(pytorch_seed, num_of_gpus)

    if 'accelerator' in dict_args:
        if dict_args['accelerator'] == 'None':
            dict_args['accelerator'] = None
        elif dict_args['accelerator'] != 'ddp':
            print(f'[bold red]{dict_args["accelerator"]}[bold blue] currently not supported. Switching to [bold green]ddp!')
            dict_args['accelerator'] = 'ddp'

    dm = MNISTDataModule(**dict_args)

    # TODO MLF-CORE: Enable input data logging
    # MLFCore.log_input_data('data/')

    dm.prepare_data()
    dm.setup(stage='fit')
    model = LightningMNISTClassifier(len_test_set=len(dm.df_test), hparams=parser.parse_args(), **dict_args)
    model.log_every_n_steps = dict_args['log_interval']

    # check, whether the run is inside a Docker container or not
    if 'MLF_CORE_DOCKER_RUN' in os.environ:
        checkpoint_callback = ModelCheckpoint(filepath='/mlflow/tmp/mlruns', save_top_k=1, verbose=True, monitor='train_avg_loss', mode='min', prefix='',)
        trainer = pl.Trainer.from_argparse_args(args, checkpoint_callback=checkpoint_callback, default_root_dir='/data', logger=TensorBoardLogger('/data'))
        tensorboard_output_path = f'data/default/version_{trainer.logger.version}'
    else:
        checkpoint_callback = ModelCheckpoint(filepath=os.getcwd(), save_top_k=1, verbose=True, monitor='train_avg_loss', mode='min', prefix='',)
        trainer = pl.Trainer.from_argparse_args(args, checkpoint_callback=checkpoint_callback)
        tensorboard_output_path = f'{os.getcwd()}/lightning_logs/version_{trainer.logger.version}'

    trainer.deterministic = True
    trainer.benchmark = False
    trainer.log_every_n_steps = dict_args['log_interval']
    trainer.fit(model, dm)
    trainer.test()
    print(f'\n[bold blue]For tensorboard log, call [bold green]tensorboard --logdir={tensorboard_output_path}')
