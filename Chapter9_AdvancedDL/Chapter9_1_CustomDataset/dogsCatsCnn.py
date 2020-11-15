import os
import random

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from dogsCatsData import DOGSCATS


np.random.seed(0)
tf.random.set_seed(0)

data = DOGSCATS()
data.data_augmentation(augment_size=5_000)
data.data_preprocessing(preprocess_mode="MinMax")
(x_train_, x_val, y_train_, y_val) = data.get_splitted_train_validation_set()
x_train, y_train = data.get_train_set()
x_test, y_test = data.get_test_set()
num_classes = data.num_classes


LOGS_DIR = os.path.abspath("C:/Users/Jan/Dropbox/_Programmieren/UdemyTF/logs/")
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)


def build_model(
    optimizer: tf.keras.optimizers.Optimizer,
    learning_rate: float,
    filter_block1: int,
    kernel_size_block1: int,
    filter_block2: int,
    kernel_size_block2: int,
    filter_block3: int,
    kernel_size_block3: int,
    dense_layer_size: int,
) -> Model:
    # Input
    input_img = Input(shape=x_train.shape[1:])
    # Conv Block 1
    x = Conv2D(filters=filter_block1, kernel_size=kernel_size_block1, padding='same')(input_img)
    x = Activation("relu")(x)
    x = Conv2D(filters=filter_block1, kernel_size=kernel_size_block1, padding='same')(x)
    x = Activation("relu")(x)
    x = MaxPool2D()(x)
    # Conv Block 2
    x = Conv2D(filters=filter_block2, kernel_size=kernel_size_block2, padding='same')(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=filter_block2, kernel_size=kernel_size_block2, padding='same')(x)
    x = Activation("relu")(x)
    x = MaxPool2D()(x)
    # Conv Block 3
    x = Conv2D(filters=filter_block3, kernel_size=kernel_size_block3, padding='same')(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=filter_block3, kernel_size=kernel_size_block3, padding='same')(x)
    x = Activation("relu")(x)
    x = MaxPool2D()(x)
    # Dense Part
    x = Flatten()(x)
    x = Dense(units=dense_layer_size)(x)
    x = Activation("relu")(x)
    x = Dense(units=num_classes)(x)
    y_pred = Activation("softmax")(x)

    # Build the model
    model = Model(
        inputs=[input_img],
        outputs=[y_pred]
    )
    opt = optimizer(learning_rate=learning_rate)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=opt,
        metrics=["accuracy"]
    )
    return model


# Global params
epochs = 20
batch_size = 256

optimizer = Adam
learning_rate = 0.001
filter_block1 = 32
kernel_size_block1 = 3
filter_block2 = 64
kernel_size_block2 = 3
filter_block3 = 128
kernel_size_block3 = 3
dense_layer_size = 512

rand_model = build_model(
    optimizer,
    learning_rate,
    filter_block1,
    kernel_size_block1,
    filter_block2,
    kernel_size_block2,
    filter_block3,
    kernel_size_block3,
    dense_layer_size,
)
model_log_dir = os.path.join(LOGS_DIR, "modelCatsDogsStart")

tb_callback = TensorBoard(
    log_dir=model_log_dir
)

rand_model.fit(
    x=x_train_,
    y=y_train_,
    verbose=1,
    batch_size=batch_size,
    epochs=epochs,
    callbacks=[tb_callback],
    validation_data=(x_val, y_val),
)

score = rand_model.evaluate(
    x=x_test,
    y=y_test,
    verbose=0,
    batch_size=batch_size
)
print(f"Test performance: {score}")
