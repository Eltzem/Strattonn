

from keras.layers import *
from keras.models import Sequential

import numpy as np

import csv
from random import randint

f = csv.reader(open('amd.csv'))
x_train = []
y_train = []
x_test = []
y_test = []
for row in f:
    if row[0] == 'timestamp':
        continue

    if randint(1, 10) <= 9:
        x_train.append(np.array([float(row[1]), float(row[2]), float(row[3])]))
        '''
        newY = np.zeros(100, dtype=np.int)
        newY[int(float(row[4]))] = 1
        y_train.append(newY)
        '''
        y_train.append(int(float(row[4])))
    else:
        print("adding to test")
        '''
        x_test.append(np.array([float(row[1]), float(row[2]), float(row[3])]))
        newY = np.zeros(100, dtype=np.int)
        newY[int(float(row[4]))] = 1
        y_test.append(newY)
        '''
        y_test.append(int(float(row[4])))

print(x_train[randint(1,3000)])
print(y_train[randint(1,3000)])

input('hit enter to continue')

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)



model = Sequential()
model.add(Dense(30, input_shape=(3,), activation='relu'))
model.add(Dense(30, activation='relu'))
#model.add(Dropout(0))
model.add(Dense(1, activation='relu'))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

model.fit(x=x_train, y=y_train, epochs=20, batch_size=10, verbose=1)

scores = model.evaluate(x_test, y_test)
print(scores)
