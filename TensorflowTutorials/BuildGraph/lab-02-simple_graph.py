import tensorflow as tf
import sys

# Build very simple graph
node1 = tf.constant(10.4, tf.float32)
node2 = tf.constant(5.6, tf.float32)
node3 = tf.add(node1, node2)
print('Node1:', node1)
print('Node2:', node2)
print('Node3:', node3)

# Launch graph
sess = tf.Session()
print('sess.run(node1, node2):', sess.run([node1, node2]))
print('sess.run(node3):', sess.run(node3))
