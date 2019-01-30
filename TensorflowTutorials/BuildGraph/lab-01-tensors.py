# TensorFlow 버전과 Python 3 버전을 확인
import tensorflow as tf
print('TensorFlow version:', tf.__version__)
import sys
print('Python version:', sys.version)

# Tensors
hello = tf.constant('Hello, TensorFlow!')
print(hello)

# 생성한 그래프는 Session에서 run해주어야 함!
sess = tf.Session()
print(sess.run(hello))
