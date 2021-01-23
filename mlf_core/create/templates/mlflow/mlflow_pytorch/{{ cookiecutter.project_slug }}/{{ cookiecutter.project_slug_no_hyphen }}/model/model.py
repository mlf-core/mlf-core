from torch.autograd import Variable
import pytorch_lightning as pl
import torch
from argparse import ArgumentParser
from pytorch_lightning.metrics.functional import accuracy
from torch.nn import functional as F


class LightningMNISTClassifier(pl.LightningModule):
    def __init__(self, len_test_set: int, **kwargs):
        """
        Initializes the network
        """
        super(LightningMNISTClassifier, self).__init__()

        # mnist images are (1, 28, 28) (channels, width, height)
        self.optimizer = None
        self.conv1 = torch.nn.Conv2d(1, 32, 3, 1)
        self.conv2 = torch.nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = torch.nn.Dropout2d(0.25)
        self.fc1 = torch.nn.Linear(9216, 128)
        self.dropout2 = torch.nn.Dropout2d(0.25)
        self.fc2 = torch.nn.Linear(128, 10)
        self.args = kwargs
        self.len_test_set = len_test_set

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)

        parser.add_argument(
            "--num_workers",
            type=int,
            default=3,
            metavar="N",
            help="number of workers (default: 3)",
        )
        parser.add_argument(
            "--lr", type=float, default=0.01, help="learning rate (default: 0.01)",
        )
        parser.add_argument('--training-batch-size', type=int, default=64, help='Input batch size for training')

        parser.add_argument('--test-batch-size', type=int, default=1000, help='Input batch size for testing')

        return parser

    def forward(self, x):
        """
        :param x: Input data

        :return: output - mnist digit label for the input image
        """
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = torch.flatten(self.dropout1(x), 1)
        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)

        return output

    def cross_entropy_loss(self, logits, labels):
        """
        Initializes the loss function

        :return: output - Initialized cross entropy loss function
        """
        return F.nll_loss(logits, labels)

    def training_step(self, train_batch, batch_idx):
        """
        Training the data as batches and returns training loss on each batch

        :param train_batch: Batch data
        :param batch_idx: Batch indices

        :return: output - Training loss
        """
        x, y = train_batch
        logits = self.forward(x)
        loss = self.cross_entropy_loss(logits, y)
        return {"loss": loss}

    def training_epoch_end(self, training_step_outputs):
        """
        Bla
        """
        train_avg_loss = torch.stack([x["loss"] for x in training_step_outputs]).mean()
        self.log("train_loss", train_avg_loss)

    # do something with preds

    def test_step(self, test_batch, batch_idx):
        """
        Performs test and computes the accuracy of the model

        :param test_batch: Batch data
        :param batch_idx: Batch indices

        :return: output - Testing accuracy
        """

        x, y = test_batch
        output = self.forward(x)
        _, y_hat = torch.max(output, dim=1)
        test_acc = accuracy(y_hat.cpu(), y.cpu())
        # sum up batch loss
        data, target = Variable(x), Variable(y)
        test_loss = F.nll_loss(output, target, reduction='sum').data.item()
        # get the index of the max log-probability
        pred = output.data.max(1)[1]
        correct = pred.eq(target.data).cpu().sum().item()
        return {"test_acc": test_acc, "test_loss": test_loss, "correct": correct}

    def test_epoch_end(self, outputs):
        """
        Computes average test accuracy score

        :param outputs: outputs after every epoch end

        :return: output - average test loss
        """
        avg_test_acc = torch.stack([x["test_acc"] for x in outputs]).mean()
        avg_test_loss = sum([x["test_loss"] for x in outputs])/self.len_test_set
        test_correct = sum([x["correct"] for x in outputs])
        self.log("avg_test_acc", avg_test_acc, sync_dist=True)
        self.log("avg_test_loss", avg_test_loss, sync_dist=True)
        self.log("test_correct", test_correct, sync_dist=True)

    def prepare_data(self):
        """
        Prepares the data for training and prediction
        """
        return {}

    def configure_optimizers(self):
        """
        Initializes the optimizer and learning rate scheduler

        :return: output - Initialized optimizer and scheduler
        """
        self.optimizer = torch.optim.Adam(self.parameters())
        return [self.optimizer]
