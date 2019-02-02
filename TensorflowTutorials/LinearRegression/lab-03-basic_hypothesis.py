import tensorflow as tf
tf.set_random_seed(6292)  # 난수 고정!

# X and Y data
x_train = [1, 2, 3]
y_train = [1, 2, 3]

# W, b
W = tf.Variable(tf.random_normal([1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

# WX + b
hypothesis = W * x_train+ b

# cost / loss function
cost = tf.reduce_mean(tf.square(hypothesis - y_train))

# Minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train = optimizer.minimize(cost)

# Launch the graph
sess = tf.Session()

# Initializes global variables
sess.run(tf.global_variables_initializer())

# Fitting
for step in range(2001):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(cost), sess.run(W), sess.run(b))
