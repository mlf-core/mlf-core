import tensorflow as tf
import tensorflow_datasets as tfds


def load_train_test_data(strategy, batch_size, buffer_size, tensorflow_seed):
    # Fetch dataset with corresponding information and separate dataset
    datasets, info = tfds.load(name='mnist', with_info=True, as_supervised=True)
    mnist_train, mnist_test = datasets['train'], datasets['test']

    # Distribute data to devices and scale images
    BATCH_SIZE_PER_REPLICA = batch_size
    BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync

    def scale(image, label):
        image = tf.cast(image, tf.float32)
        image /= 255

        return image, label

    # Ensure that seeds are set and reshuffle_each_iteration is False!
    # https://github.com/tensorflow/tensorflow/issues/38197
    train_dataset = mnist_train.map(scale).cache().shuffle(buffer_size, seed=tensorflow_seed, reshuffle_each_iteration=False).batch(BATCH_SIZE)
    eval_dataset = mnist_test.map(scale).batch(BATCH_SIZE)

    return train_dataset, eval_dataset
