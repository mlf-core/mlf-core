import os
import mlflow
import mlflow.pytorch
import click
import torch
import torch.optim as optim
import time
import tempfile

from tensorboardX import SummaryWriter
from rich import traceback

from mlf_core.mlf_core import log_sys_intel_conda_env, set_general_random_seeds
from model.model import create_model, create_parallel_model
from training.train import train, test
from data_loading.data_loader import load_train_test_data


@click.command()
@click.option('--cuda', type=click.Choice(['True', 'False']), default='True', help='Enable or disable CUDA support.')
@click.option('--epochs', type=int, default=5, help='Number of epochs to train')
@click.option('--general-seed', type=int, default=0, help='General Python, Python random and Numpy seed.')
@click.option('--pytorch-seed', type=int, default=0, help='Pytorch specific random seed.')
@click.option('--log-interval', type=int, default=100, help='Number of batches before logging training status')
@click.option('--training-batch-size', type=int, default=64, help='Input batch size for training')
@click.option('--test-batch-size', type=int, default=1000, help='Input batch size for testing')
@click.option('--learning-rate', type=float, default=0.01, help='Learning rate')
def start_training(cuda, epochs, general_seed, pytorch_seed, log_interval,
                   training_batch_size, test_batch_size, learning_rate):
    # Set GPU settings
    use_cuda = (True if cuda == 'True' else False) and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    if use_cuda and torch.cuda.device_count() > 0:
        click.echo(click.style(f'Using {torch.cuda.device_count()} GPUs!', fg='blue'))

    # Set all random seeds and possibly turn of GPU non determinism
    set_general_random_seeds(general_seed)
    set_pytorch_random_seeds(pytorch_seed, use_cuda=use_cuda)

    # Load training and testing data
    train_loader, test_loader = load_train_test_data(training_batch_size, test_batch_size)

    # Define model, device and optimizer
    if torch.cuda.device_count() > 1:
        model = create_parallel_model()
    else:
        model = create_model()
    model.to(device)
    optimizer = optim.Adam(model.parameters())
    optimizer.step()

    with mlflow.start_run():
        # Create a SummaryWriter to write TensorBoard events locally
        events_output_dir = tempfile.mkdtemp()
        writer = SummaryWriter(events_output_dir)
        click.echo(click.style(f'Writing TensorBoard events locally to {events_output_dir}\n', fg='blue'))

        # Start training
        runtime = time.time()
        for epoch in range(1, epochs + 1):
            train(use_cuda, model, epoch, optimizer, log_interval, train_loader, writer)
            test(use_cuda, model, epoch, test_loader, writer)
        device = 'GPU' if use_cuda else 'CPU'
        click.echo(click.style(f'{device} Run Time: {str(time.time() - runtime)} seconds', fg='green'))

        # Closing writer to allow for the model to be logged
        writer.close()

        # Log the model to mlflow
        click.echo(click.style('Logging model to mlflow...', fg='blue'))
        mlflow.pytorch.log_model(model, 'models')

        # Log hardware and software
        log_sys_intel_conda_env()

        # Upload the TensorBoard event logs as a run artifact
        click.echo(click.style('Uploading TensorBoard events as a run artifact...', fg='blue'))
        mlflow.log_artifacts(events_output_dir, artifact_path='events')
        click.echo(click.style(f'\nLaunch TensorBoard with:\ntensorboard --logdir={os.path.join(mlflow.get_artifact_uri(), "events")}', fg='blue'))


def set_pytorch_random_seeds(seed, use_cuda):
    torch.manual_seed(seed)
    if use_cuda:
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # For multiGPU
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


if __name__ == '__main__':
    traceback.install()
    click.echo(click.style(f'Num GPUs Available: {torch.cuda.device_count()}', fg='blue'))

    start_training()
