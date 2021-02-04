'''
author: Jin Yuhan
date: 2021-01-27 19:56:51
lastTime: 2021-01-27 22:23:16
'''

import tensorflow as tf
import train_data as td
import configs
import inference

def evaluate(data):
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32, [None, configs.LAYER_DIMS[0]], name="x-input")
        y = tf.placeholder(tf.float32, [None, configs.LAYER_DIMS[-1]], name="y-input")
        xs, ys = td.get_batch(data, len(data))

        result = inference.inference(configs.LAYER_DIMS, x, None)
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(result, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        variable_averages = tf.train.ExponentialMovingAverage(configs.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state('./model_data')

            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                accuracy_score = sess.run(accuracy, feed_dict={x:xs, y:ys})
                print("After %s training step(s), validation accuracy=%g" % (global_step, accuracy_score))
            else:
                print("No checkpoint file found")

if __name__ == "__main__":
    data = td.load_at_path(configs.TRAIN_DATA_SAVE_PATH)

    if data:
        print("load %d train data" % len(data))
        # random.shuffle(data)  # 随机排序一次
        evaluate(data[configs.BATCH_SIZE:])
    else:
        print("No train data!")
