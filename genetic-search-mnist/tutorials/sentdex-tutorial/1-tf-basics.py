import tensorflow as tf

# build computation graph

x1 = tf.constant([5, 3], tf.int32)
x2 = tf.constant([6, 4], tf.int32)

#result = x1 * x2

result = tf.multiply(x1, x2)

print(result)



# run session

sess = tf.Session()
output = sess.run(result)
sess.close()

print(output)
