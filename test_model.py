from keras.optimizers import *
from keras.metrics import *
from keras.models import *
from keras.layers import *
from keras.losses import *


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
