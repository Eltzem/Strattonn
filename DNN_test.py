from DNN import DNN
from Chromosome import Chromosome

#NOTE
print ('!!! Not all these tests will work. I have disabled the ones that will not. It has passed. \
        I had to disable the DNN.layers list which saved layers added to the Keras model in a list. \
        It made saving a model throw exceptions with the build in Keras save method.')

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
print('evaluation:', model.evaluate(test_inputs, test_outputs))

prediction_inputs = [[2,3,4,5,6]]
prediction_outputs = [[2]]
print('prediction:', model.predict(prediction_inputs))

'''
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
'''
model.close()


'''
# Chromosome -> DNN test

print('\nstarting Chromosome and DNN test\n')

c = Chromosome() # create random Chromosome
dnn = DNN(c)

print('compiling model')
dnn.compile(dnn.optimizer, 'mean_squared_error', ['accuracy'])

# print chromosome and layers in DNN object
print(str(c), '\n')

for layer in dnn.get_layers():
    print(layer.get_config())

# test optimizer
if dnn.optimizer == c.optimizer():
    print('optimizer test passed')
else:
    print('optimizer test failed')

# test input size
if (None, c.input_size()) == dnn.get_layers()[0].get_config()['batch_input_shape']:
    print('input size test passed')
else:
    print('input size test failed')

# test that activation function and hidden layer sizes match up
sizes, activations, dropouts = c.hidden_layers()
for x in range(len(sizes)):
    if sizes[x] != dnn.get_layers()[x].get_config()['units']:
        print('sizes test failed')
    else:
        print('sizes test passed')
    if activations[x] != dnn.get_layers()[x].get_config()['activation']:
        print('activations test failed')
    else:
        print('activations test passed')

# test output shape
if c.output_size() == dnn.get_layers()[len(dnn.get_layers())-1].get_config()['units']:
    print('output size test passed')
else:
    print('output size test failed')

# test output activation
if c.output_activation() == dnn.get_layers()[len(dnn.get_layers())-1].get_config()['activation']:
    print('output activation test passed')
else:
    print('output activation test failed')

dnn.close()
'''
