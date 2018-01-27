import tensorflow as tf
import numpy as np
import os
# preprocesses data
from create_sentiment_featuresets import create_feature_sets_and_labels

'''
Feed Forward Neural Network

input > weight > hidden layer 1 (activation function) > weight > hidden layer 2 (activation function)
> repeat layers > weight > output layer

compare output to intended output w/ cost or loss function
optimization function (optimizer)  > minimize cost (AdamOptimizer...SGB, AdaGrad, many options)
    back propogation manipulation of weights

feed forward + back propogation = epoch
'''

# get & preprocess data
train_x, train_y, test_x, test_y = create_feature_sets_and_labels('pos.txt', 'neg.txt')

# hidden layer sizes
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 2

# go through 100 features at a time
batch_size = 1

# Define starting data and size & shape of 'x' placeholder
# height x width of image = 28 * 28 = 784, don't need a matrix
    # use a 1-dimmensional array for simplicity
x = tf.placeholder('float', [None, len(train_x[0])])
y = tf.placeholder('float')

def neural_network_model (data):
    '''
    Build computation graph / neural network model.
    '''

    # weights are tf Variables w/ random starting values
    # weights have shape 784 * n_nodes_hl1
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([len(train_x[0]), n_nodes_hl1])), 
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
    
    # saver to save model
    saver = tf.train.Saver()

    # Train Network w/ training data

    for epoch in range(n_epochs):
        epoch_loss = 0

        # restore from saved model

        #if epoch > 0:
            #saver.restore(sess, 'model.ckpt')


        # split each epoch into batch sizes to limit memory usage (although it doesn't really)
        # just feeds data at neural network in small batches
        i = 0
        while i < len(train_x):
            start = i
            end = i + batch_size

            batch_x = np.array(train_x[start:end])
            batch_y = np.array(train_y[start:end])

            # run through data with optimizer, cost
            # pass in data (x, y) = (input, output)
            # tensorflow 'magically' knows it can modify weights and biases
            run, c = sess.run([optimizer, cost], feed_dict = {x: batch_x, y: batch_y})

            # keep track of total loss this epoch
            epoch_loss += c

            i += batch_size

        # save model
        #saver.save(sess, 'model.ckpt')

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
        print("Accuracy: ", accuracy.eval({x: test_x, y: test_y}, session = sess))



    # Test Network

    # tf.argmax returns index of maximum value in array
    # compares this index of predicted outputs and actual output data
    # hope they are the same
    correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

    # get model accuracy expressed as a float value
    accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

    # test accuracy of model against testing data
        # images -> labels w/ another magic function from Google
    print("Accuracy: ", accuracy.eval({x: test_x, y: test_y}, session = sess))

    sess.close()


train_neural_network(x, y)


