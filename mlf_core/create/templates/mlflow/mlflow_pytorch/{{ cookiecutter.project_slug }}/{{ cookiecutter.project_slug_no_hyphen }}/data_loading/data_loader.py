import pytorch_lightning as pl
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, **kwargs):
        """
        Initialization of the data module with a train and test dataset, as well as a loader for each.
        The dataset is th example MNIST dataset
        """
        super(MNISTDataModule, self).__init__()
        self.df_train = None
        self.df_test = None
        self.train_data_loader = None
        self.test_data_loader = None
        self.args = kwargs

        # transforms for images
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    def setup(self, stage=None):
        """
        Downloads the data, parse it and split the data into train, test, validation data
        :param stage: Stage - training or testing
        """
        self.df_train = datasets.MNIST('dataset', download=True, train=True, transform=self.transform)
        self.df_test = datasets.MNIST('dataset', download=True, train=False, transform=self.transform)

    def train_dataloader(self):
        """
        :return: output - Train data loader for the given input
        """
        return DataLoader(self.df_train, batch_size=self.args['training_batch_size'], num_workers=self.args['num_workers'], shuffle=True)

    def test_dataloader(self):
        """
        :return: output - Test data loader for the given input
        """
        return DataLoader(self.df_test, batch_size=self.args['test_batch_size'], num_workers=self.args['num_workers'], shuffle=False)
