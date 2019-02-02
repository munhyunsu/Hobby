import tensorflow as tf
tf.set_random_seed(6292)  # 난수 고정!

# xy_data
x_data = [[1, 2],
          [2, 3],
          [3, 4]]
y_data = [[0],
          [1],
          [2]]

# X and Y data
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
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.2)
train = optimizer.minimize(cost)

# Launch the graph
sess = tf.Session()

# Initializes global variables
sess.run(tf.global_variables_initializer())

# Fitting
for step in range(2001):
    cost_val, W_val, b_val, _ = sess.run([cost, W, b, train],
                                         feed_dict={X: [1, 2, 3],
                                                    Y: [1, 2, 3]})
    if step % 20 == 0:
        print(step, cost_val, W_val, b_val)
