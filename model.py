from keras.models import Model, Sequential
from keras.optimizers import *
from keras.metrics import *
from keras.layers import *
from keras.losses import *


def model():
    model = Sequential()
    model.add(TimeDistributed(Conv2D(64, (3, 3), activation='relu'), input_shape=(8, 32, 24, 1)))
    model.add(TimeDistributed(Conv2D(64, (3, 3), activation='relu')))
    model.add(TimeDistributed(MaxPooling2D(2,2)))
    model.add(TimeDistributed(Conv2D(128, (3, 3), activation='relu')))
    model.add(TimeDistributed(Conv2D(128, (3, 3), activation='relu')))
    model.add(TimeDistributed(MaxPooling2D(2,2)))
    model.add(TimeDistributed(BatchNormalization()))
    model.add(TimeDistributed(Flatten()))
    model.add(Dropout(0.2))

    model.add(LSTM(32, return_sequences=False, dropout=0.2)) # used 32 units

    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.summary()
    return model


if __name__ == "__main__":
    model = model()