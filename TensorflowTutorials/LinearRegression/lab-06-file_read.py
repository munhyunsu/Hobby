import tensorflow as tf
import pandas as pd
tf.set_random_seed(6292)  # 난수 고정!

# data
xy = pd.read_csv('data/lab-06-crime-data.csv')
x_data = xy.values[:, 0:-1]
y_data = xy.values[:, [-1]]

# X and Y
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# W, b
W = tf.Variable(tf.random_normal([1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

# WX + b
hypothesis = W * X + b

# cost / loss function
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# Minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-3)
train = optimizer.minimize(cost)

# Launch the graph
sess = tf.Session()

# Initializes global variables
sess.run(tf.global_variables_initializer())

# Fitting
for step in range(10001):
    cost_val,  _ = sess.run([cost, train],
                                         feed_dict={X: x_data,
                                                    Y: y_data})
    if step % 1000 == 0:
        print('Step:', step, 'Cost:', cost_val)
