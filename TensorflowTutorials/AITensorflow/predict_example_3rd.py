import os
import re
import string

import tensorflow as tf # 텐서플로우
import numpy as np

FLAGS = None
_ = None

def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
    return tf.strings.regex_replace(stripped_html,
                                    '[%s]' % re.escape(string.punctuation),
                                    '')


def main():
    class_names = ['Negative', 'Positive']

    max_features = 1000*10
    sequence_length = 50*5
    vectorize_layer = tf.keras.layers.experimental.preprocessing.TextVectorization(
            standardize=custom_standardization,
            max_tokens=max_features,
            output_mode='int',
            output_sequence_length=sequence_length,
            ngrams=(1, 2, 3))
    
    embedding_dim = 4*5

    model = tf.keras.Sequential([
            tf.keras.layers.Embedding(max_features+1, embedding_dim, mask_zero=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1)])

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), 
                  optimizer=tf.keras.optimizers.Adam(), 
                  metrics=tf.metrics.BinaryAccuracy(threshold=0.0))
    
    export_model = tf.keras.Sequential([
            vectorize_layer,
            model,
            tf.keras.layers.Activation('sigmoid')
    ])

    export_model.compile(
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
    )
    
    export_model.load_weights(FLAGS.model)
    
    while True:
        try:
            user_str = input('\x1B[38;5;2m테스트 입력: \x1B[38;5;6m').strip()
            if user_str == '':
                continue
            predicted = export_model.predict(tf.expand_dims(user_str, -1))[0][0]
            print((f'\x1B[38;5;3m'
                   f'예측 결과: {class_names[int(round(predicted))]} '
                   f'({predicted:0.4f})'
                   f'\x1B[0m'))
        except KeyboardInterrupt:
            print(('\x1B[38;5;1m'
                   'Catch a Ctrl+C! Program is shutting down'
                   '\x1B[0m'))
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str,
                        default='./3rd_model/my_model')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.model = os.path.abspath(os.path.expanduser(FLAGS.model))

    main()
