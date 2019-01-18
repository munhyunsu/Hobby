import tensorflow as tf
import pandas as pd
import numpy as np


def main():
    # prepare data
    xy = pd.read_csv('/tmp/deep_rps.csv')
    #xy = xy.drop('userid', 1)
    x_data = xy.values[:, :-1]
    y_data = xy.values[:, [-1]]

    # const
    nb_classes = 3 # {'Rock': 1, 'Paper': 2, 'Scissors': 3}

    # placeholder for a tensor
    X = tf.placeholder(tf.float32, [None, x_data.shape[1]])
    Y = tf.placeholder(tf.int32, [None, 1])
    Y_one_hot = tf.one_hot(Y, nb_classes)
    Y_one_hot = tf.reshape(Y_one_hot, [-1, nb_classes])

    # variables for hypothesis
    W = tf.Variable(tf.random_normal([x_data.shape[1], nb_classes]), 
                    name='weight')
    b = tf.Variable(tf.random_normal([nb_classes]), 
                    name='bias')

    # softmax for logistic regression
    logits = tf.matmul(X, W) + b
    hypothesis = tf.nn.softmax(logits)

    # Cross entropy
    cost_i = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits,
                                                        labels=Y_one_hot)
    cost = tf.reduce_mean(cost_i)
    optimizer = tf.train.GradientDescentOptimizer(
                                        learning_rate=1e-2).minimize(cost)

    prediction = tf.argmax(hypothesis, 1)
    correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Launch graph
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for step in range(2001):
            sess.run(optimizer, feed_dict={X: x_data, Y: y_data})
            if step%100 == 0:
                loss, acc = sess.run([cost, accuracy], 
                                     feed_dict={X: x_data, Y: y_data})
                print('Step: {0:5d}   Loss: {1:.3f}   Acc: {2:.2%}'.format(
                        step, loss, acc))

        pred = sess.run(prediction, 
                        feed_dict={X: x_data})
        hands = set()
        for p, y in zip(pred, y_data.flatten()):
            hands.add(p)
        print('Predicted hands: {0}'.format(hands))


if __name__ == '__main__':
    main()
