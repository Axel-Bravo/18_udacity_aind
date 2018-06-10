import numpy as np
import re

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
import keras


# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    # create X and y
    for i in range(0, len(series) - window_size):
        X.append(series[i:(window_size + i)])
        y.append(series[window_size + i])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y


def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(units=5, input_shape=(window_size,1)))
    model.add(Dense(1))
    return model


def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    pattern = re.compile('[^a-z0-9!,.:;?\\s]')
    text = pattern.sub('', text)
    text = text.replace(u'\xa0', u' ')

    return text


def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    # create inputs and outputs
    for i in range(0, len(text) - window_size, step_size):
        inputs.append(text[i:(window_size + i)])
        outputs.append(text[window_size + i])

    # reshape each
    inputs = np.asarray(inputs)
    inputs.shape = (np.shape(inputs)[0:2])
    outputs = np.asarray(outputs)
    outputs.shape = (len(outputs))

    return inputs,outputs


# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(units=200, input_shape=(window_size, num_chars)))
    model.add(Dense(units=num_chars))
    model.add(Activation('softmax'))

    return model
