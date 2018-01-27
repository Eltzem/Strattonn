from keras.layers import Dense
from keras.models import Sequential
from keras import metrics

import numpy as np
import random

from keras.datasets import mnist

size_hl1 = 500
size_hl2 = 500
size_hl3 = 500

n_inputs = 28 * 28
n_classes = 10

batch_size = 32

n_epochs = int(input("num epochs:"))

def create_neural_network_model ():

    model = Sequential()
    model.add(Dense(size_hl1, input_shape=(n_inputs,), activation='relu'))
    model.add(Dense(size_hl2, activation='relu'))
    model.add(Dense(size_hl3, activation='relu'))
    model.add(Dense(n_classes, activation='relu'))

    return model

def train_neural_network_model (model, x, y):
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=[metrics.mae, metrics.categorical_accuracy])
    model.fit(x=x, y=y, epochs=n_epochs, batch_size=batch_size, verbose=1)

def test_neural_network_model (model, x, y):
    scores = model.evaluate(x, y)
    print(scores)

def flatten_images (images_array):
    images_flat = []

    for image in images_array:
        image_flat = []
        for row in image:
            for column in row:
                #image_flat.append(column)
                if column > 50:
                    #print(column)
                    #print(1)
                    image_flat.append(1)
                else:
                    #print(0)
                    image_flat.append(0)
                
        images_flat.append(np.array(image_flat))

    return np.array(images_flat)

def expand_outputs (outputs):
    expanded_outputs = []
    for output in outputs:
        array = np.zeros(n_classes)
        array[output] = 1
        expanded_outputs.append(np.array(array))

    return np.array(expanded_outputs)

(x_train, y_train), (x_test, y_test) = mnist.load_data()
#print(x_train[101])




train = list(zip(x_train, y_train))
test = list(zip(x_test, y_test))

random.shuffle(train)
random.shuffle(test)

x_train, y_train = zip(*train)
x_test, y_test = zip(*test)


x_train = flatten_images(x_train)
x_test = flatten_images(x_test)

y_train = expand_outputs(y_train)
y_test = expand_outputs(y_test)

'''
train = []
test = []

for i in range(len(x_train)):
    train.append([x_train[i], y_train[i]])

for i in range(len(x_test)):
    test.append([x_test[i], y_test[i]])

random.shuffle(train)
random.shuffle(test)

x_train = []
y_train = []
for i in range(len(train)):
    x_train.append(train[0])
    y_train.append(train[1])
x_train = np.array(x_train)
y_train = np.array(y_train)

print(x_train[3])

x_test = []
y_test = []
for i in range(len(test)):
    x_test.append(test[0])
    y_test.append(test[1])
x_test = np.array(x_test)
y_test = np.array(y_test)
'''


#print(x_train.shape)
#print(y_train.shape)

#print(x_train[101])
#print(y_train[101])


model = create_neural_network_model()
train_neural_network_model (model, x_train, y_train)
test_neural_network_model(model, x_test, y_test)

