from keras.layers import *
from keras.models import *


model_cnlst = Sequential()
model_cnlst.add(TimeDistributed(Conv2D(64, (3, 3), strides=(1,1), activation='relu'), input_shape=(8, 32, 24, 1)))
model_cnlst.add(TimeDistributed(Conv2D(64, (3, 3), strides=(1,1), activation='relu')))
model_cnlst.add(TimeDistributed(MaxPooling2D(2,2)))
model_cnlst.add(TimeDistributed(Conv2D(128, (3, 3), strides=(1,1), activation='relu')))
model_cnlst.add(TimeDistributed(Conv2D(128, (3, 3), strides=(1,1), activation='relu')))
model_cnlst.add(TimeDistributed(MaxPooling2D(2,2)))
model_cnlst.add(TimeDistributed(BatchNormalization()))
model_cnlst.add(TimeDistributed(Flatten()))
model_cnlst.add(Dropout(0.2))

model_cnlst.add(LSTM(32, return_sequences=False, dropout=0.2)) # used 32 units

model_cnlst.add(Dense(32, activation='relu'))
model_cnlst.add(Dropout(0.2))
model_cnlst.add(Dense(1, activation='sigmoid'))
model_cnlst.summary()