import os

import tensorflow as tf # 텐서플로우
import numpy as np

FLAGS = None
_ = None


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
                    tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                              batch_input_shape=[batch_size, None]),
                    tf.keras.layers.GRU(rnn_units,
                                        return_sequences=True,
                                        stateful=True,
                                        recurrent_initializer='glorot_uniform'),
                    tf.keras.layers.Dense(vocab_size)
                    ])
    return model


def generate_text(model, start_string, num_generate=1000):
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    text_generated = list()

    temperature = 1.0

    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)

        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))


def main():
    predict_model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)

    predict_model.load_weights(tf.train.latest_checkpoint(FLAGS.model))

    predict_model.build(tf.TensorShape([1, None]))

    predict_model.summary()

    while True:
        try:
            user_str = input('\x1B[38;5;2m테스트 입력: \x1B[38;5;6m').strip()
            user_cnt = int(input('\x1B[38;5;2m생성할 단어 개수: \x1B[38;5;6m').strip())
            if user_str == '':
                continue
            print(generate_text(predict_model, start_string=user_str, num_generate=user_cnt))
        except KeyboardInterrupt:
            print(('\x1B[38;5;1m'
                   'Catch a Ctrl+C! Program is shutting down'
                   '\x1B[0m'))
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str,
                        default='./7th_training_checkpoints_ko')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.model = os.path.abspath(os.path.expanduser(FLAGS.model))

    main()
