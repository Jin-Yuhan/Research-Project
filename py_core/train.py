'''
author: Jin Yuhan
date: 2021-01-25 19:14:14
lastTime: 2021-01-27 22:28:15
'''

import tensorflow as tf # 1.15
import train_data as td
import configs
import inference
import random

def train(data):
    x = tf.compat.v1.placeholder(tf.float32, [None, configs.LAYER_DIMS[0]], name="x-input")
    y = tf.compat.v1.placeholder(tf.float32, [None, configs.LAYER_DIMS[-1]], name="y-input")

    regularizer = tf.contrib.layers.l2_regularizer(configs.REGULARIZATION_RATE)
    result = inference.inference(configs.LAYER_DIMS, x, regularizer) # 前向传播

    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(configs.MOVING_AVERAGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(tf.compat.v1.trainable_variables())

    sm = tf.nn.softmax(result)
    cross_entropy = -tf.reduce_mean(y * tf.math.log(tf.clip_by_value(sm, 1e-10, 1.0)))
    loss = tf.reduce_mean(cross_entropy) + inference.get_regularization_losses()
    learning_rate = tf.compat.v1.train.exponential_decay(configs.LEARNING_RATE_BASE, global_step, 3000, configs.LEARNING_RATE_DECAY, staircase=True)
    
    train_step = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
    train_op = tf.group(train_step, variable_averages_op)

    saver = tf.compat.v1.train.Saver()

    with tf.compat.v1.Session() as sess:
        tf.compat.v1.global_variables_initializer().run()

        for i in range(configs.TRAINING_STEPS):
            xs, ys = td.get_batch(data, configs.BATCH_SIZE)
            _, loss_value, step, lr = sess.run([train_op, loss, global_step, learning_rate], feed_dict={x: xs, y: ys})

            if i % 1000 == 0:
                with tf.compat.v1.variable_scope("", reuse=True):
                    print(sess.run(tf.compat.v1.get_variable("layer1/bias")))
                print("After %d training step(s), loss on training batch is %g, learning rate is %g." % (step, loss_value, lr))
                saver.save(sess, configs.MODEL_SAVE_PATH, global_step=global_step)

def main():
    data = td.load_at_path(configs.TRAIN_DATA_SAVE_PATH)

    if data:
        print("load %d train data" % len(data))
        random.shuffle(data)  # 随机排序一次
        train(data)
    else:
        print("No train data!")

if __name__ == "__main__":
    main()
