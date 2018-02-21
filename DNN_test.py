from DNN import DNN

# tests the DNN class

model = DNN()

# add layers
model.add_dense(32, 'relu', _inputs=5)
model.add_dense(100, 'softmax', _dropoutRate=0.1)
model.add_dense(1, 'elu')

model.compile('adam', 'mean_squared_error', ['accuracy'])



# create some fake data
inputs = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7], [1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
outputs = [[1],[2],[3],[1],[2],[3]]

model.train(inputs, outputs, 10, 1)
test_inputs = [[0,1,2,3,4], [1,2,3,4,5]]
test_outputs = [[0], [1]]
print(model.evaluate(test_inputs, test_outputs))

prediction_inputs = [[2,3,4,5,6]]
prediction_outputs = [[2]]
print(model.predict(prediction_inputs))


if model.get_layers()[0].get_config()['batch_input_shape'] == (None, 5):
    print('input shape test passed')
else:
    print('FAILED: input shape test')

if model.get_layers()[1].get_config()['units'] == 100:
    print('perceptron count test passed')
else:
    print('FAILED: perceptron count test')

if model.get_layers()[2].get_config()['activation'] == 'elu':
    print('activation function test passed')
else:
    print('FAILED: activation function test')

model.close()
