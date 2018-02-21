from keras.models import Sequential
from keras.layers import *
from keras import backend as KerasBackend

import numpy as np

class DNN:

    def __init__ (self):
        self.model = Sequential() # blank model
        self.layers = []

    def close (self):
        self.model = None
        self.layers = None
        KerasBackend.clear_session()

    def add_dense (self, _perceptrons, _activation, _inputs=None, _dropoutRate=0):
        print("adding dense perceptron layer")

        newLayer = Dense(_perceptrons, activation=_activation, input_shape=(_inputs,))

        self.model.add(newLayer)
        self.layers.append(newLayer)

        # add Dropout to layer, if any
        if _dropoutRate > 0:
            self.addDropout(_dropoutRate)

    def add_dropout (self, _dropoutRate):
        print("adding dropout")

        # dropout of a layer functions as a layer in Keras
        newLayer = Dropout(_dropoutRate)
        self.model.add(newLayer)
        self.model.layers.append(newLayer)

    # configure the learning process before training
    def compile (self, _optimizer, _loss, _metrics):
        print("compiling model")

        self.model.compile(optimizer=_optimizer, loss=_loss, metrics=_metrics)

    # fit model, I called it train
    def train (self, _inputs, _outputs, _epochs, _batchSize):
        print("training model")

        # make sure inputs and ouputs are numpy.array (s)
        _inputs = np.array(_inputs)
        _outputs = np.array(_outputs)

        self.model.fit(x=_inputs, y=_outputs, epochs=_epochs, batch_size=_batchSize, verbose=2)

    # test the model
    def evaluate (self, _inputs, _outputs):
        # make sure inputs and outputs are numpy.array (s)
        _inputs = np.array(_inputs)
        _outputs = np.array(_outputs)

        return self.model.evaluate(x=_inputs, y=_outputs)

    def predict (self, _inputs):
        # make sure inputs are numpy.array (s)
        _inputs = np.array(_inputs)

        return self.model.predict(x=_inputs)

    def get_layers(self):
        return self.layers
