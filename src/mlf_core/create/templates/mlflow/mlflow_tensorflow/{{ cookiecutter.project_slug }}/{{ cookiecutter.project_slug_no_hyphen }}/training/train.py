import tensorflow as tf
import os


def train(model, epochs, train_dataset):
    # Define the checkpoint directory to store the checkpoints
    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir='./logs'),
        tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix, save_weights_only=True)
    ]

    model.fit(train_dataset, epochs=epochs, callbacks=callbacks)
    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))


def test(model, eval_dataset):
    eval_loss, eval_acc = model.evaluate(eval_dataset)

    return eval_loss, eval_acc
