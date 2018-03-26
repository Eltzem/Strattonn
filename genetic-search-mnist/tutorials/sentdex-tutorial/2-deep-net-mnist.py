import tensorflow as tf
# import MNIST handwritten images tutorial dataset (28 x 28 resolution)
from tensorflow.examples.tutorials.mnist import input_data

# 10 classes, 0-9
# one_hot == one pixel or element is ON, rest are OFF
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

'''
Feed Forward Neural Network

input > weight > hidden layer 1 (activation function) > weight > hidden layer 2 (activation function)
> repeat layers > weight > output layer

compare output to intended output w/ cost or loss function
optimization function (optimizer)  > minimize cost (AdamOptimizer...SGB, AdaGrad, many options)
    back propogation manipulation of weights

feed forward + back propogation = epoch
'''

# hidden layer sizes
n_nodes_hl1 = 1500
n_nodes_hl2 = 1000
n_nodes_hl3 = 500

n_classes = 10

# go through 100 features at a time
batch_size = 32

# Define starting data and size & shape of 'x' placeholder
# height x width of image = 28 * 28 = 784, don't need a matrix
    # use a 1-dimmensional array for simplicity
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def neural_network_model (data):
    '''
    Build computation graph / neural network model.
    '''

    # weights are tf Variables w/ random starting values
    # weights have shape 784 * n_nodes_hl1
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784, n_nodes_hl1])), 
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])), 
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])), 
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])), 
                      'biases': tf.Variable(tf.random_normal([n_classes]))}

    # (input_data & weights) + bias
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    # Rectified Linear activation function
    l1 = tf.nn.relu(l1)
    
    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    # Rectified Linear activation function
    l2 = tf.nn.relu(l2)
    
    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    # Rectified Linear activation function
    l3 = tf.nn.relu(l3)
    
    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

    return output

def train_neural_network (x, y):
    # get neural network output (one_hot array)
    prediction = neural_network_model(x)
    
    # cross entropy w/ logits as clst function
    # get cost (difference) of prediction to actual output data
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = y))

    # use AdamOptimizer
    # learning_rate = 0.001 default
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # number of epochs to do (cycles of feed forward + back prop)
    n_epochs = int(input("number epochs: "))

    # run session
    sess = tf.Session()
    # init variables
    sess.run(tf.global_variables_initializer())

    # Train Network w/ training data

    for epoch in range(n_epochs):
        epoch_loss = 0

        # total num samples / batch_size = number of runs in each epoch
        for run in range(int(mnist.train.num_examples / batch_size)):
            # gets input and output in batch_size (nice pre-build magic function to get data)
            epoch_x, epoch_y = mnist.train.next_batch(batch_size)

            # run through data with optimizer, cost
            # pass in data (x, y) = (input, output)
            # tensorflow 'magically' knows it can modify weights and biases
            run, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y: epoch_y})

            # keep track of total loss this epoch
            epoch_loss += c

        print("Epoch ", epoch, " completed out of ", n_epochs, " with loss ", epoch_loss)

        # Test Network

        # tf.argmax returns index of maximum value in array
        # compares this index of predicted outputs and actual output data
        # hope they are the same
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        # get model accuracy expressed as a float value
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        # test accuracy of model against testing data
        # images -> labels w/ another magic function from Google
        print("Accuracy: ", accuracy.eval({x:mnist.test.images, y: mnist.test.labels}, session = sess))



    # Test Network

    # tf.argmax returns index of maximum value in array
    # compares this index of predicted outputs and actual output data
    # hope they are the same
    correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

    # get model accuracy expressed as a float value
    accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

    # test accuracy of model against testing data
        # images -> labels w/ another magic function from Google
    print("Accuracy: ", accuracy.eval({x:mnist.test.images, y: mnist.test.labels}, session = sess))

    sess.close()


train_neural_network(x, y)


