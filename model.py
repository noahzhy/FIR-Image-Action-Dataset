from keras.optimizers import *
from keras.metrics import *
from keras.models import *
from keras.layers import *
from keras.losses import *


def model_3dcnn():
    model = Sequential()
    model.add(Conv3D(32, kernel_size=(3, 3, 3), input_shape=(32, 24, 8, 1), padding='same'))
    model.add(Conv3D(32, kernel_size=(3, 3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), padding='same'))
    model.add(Dropout(0.25))

    model.add(Conv3D(64, kernel_size=(3, 3, 3), padding='same'))
    model.add(Conv3D(64, kernel_size=(3, 3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), padding='same'))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(8, activation='softmax'))

    model.compile(loss=CategoricalCrossentropy(), optimizer=Adam(), metrics=['accuracy'])
    model.summary()
    return model


def model_cnn_lstm():
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
    model.add(Dense(8, activation='softmax'))
    model.summary()
    model.compile(loss=CategoricalCrossentropy(), optimizer=Adam(), metrics=['accuracy'])
    return model


if __name__ == "__main__":
    model = model_cnn_lstm()
    model = model_3dcnn()
