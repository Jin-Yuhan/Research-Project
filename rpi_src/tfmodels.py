# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-09 20:30:49
lastTime: 2021-02-16 18:02:59
'''

import tensorflow as tf
import numpy as np

class TFModel(object):
    def __init__(self, **kwargs):
        self._layers = kwargs.get("layers")
        self._activate_funcs = kwargs.get("activate_funcs")
        self._moving_average_decay = kwargs.get("moving_average_decay")
        self._model_dir = kwargs.get("model_dir")
    
    def inference(self, in_tensor, regularizer):
        in_layer = self._layers[0]

        for i in range(1, len(self._layers)):
            out_layer = self._layers[i]
            with tf.variable_scope("layer" + str(i)):
                weights = TFModel._get_weights([in_layer, out_layer], tf.float32, regularizer)
                bias = TFModel._get_bias([out_layer], tf.float32)
                in_tensor = tf.matmul(in_tensor, weights) + bias
                in_tensor = TFModel._activate(in_tensor, self._activate_funcs[i - 1])
            in_layer = out_layer

        return in_tensor

    def run(self, arg):
        pass

    @staticmethod
    def _get_regularization_losses():
        return tf.add_n(tf.get_collection("losses"))

    @staticmethod
    def _get_weights(shape, dtype, regularizer):
        weights = tf.get_variable("weights", shape, dtype, 
            initializer=tf.truncated_normal_initializer(stddev=0.1), trainable=True)
            
        if regularizer:
            tf.add_to_collection("losses", regularizer(weights))
        return weights

    @staticmethod
    def _get_bias(shape, dtype):
        return tf.get_variable("bias", shape, dtype, initializer=tf.constant_initializer(0.0))

    @staticmethod
    def _activate(tensor, activate_func):
        func = eval(activate_func)
        return func(tensor) if func else tensor


class TrainModel(TFModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._batch_size = kwargs.get("batch_size")
        self._training_steps = kwargs.get("training_steps")
        self._regularizer = eval(kwargs.get("regularizer"))
        self._regularization_rate = kwargs.get("regularization_rate")
        self._learning_rate_base = kwargs.get("learning_rate_base")
        self._learning_rate_decay = kwargs.get("learning_rate_decay")
        self._staircase = kwargs.get("staircase")
        self._optimizer = eval(kwargs.get("optimizer"))
        self._model_save_path = kwargs.get("model_save_path")
        
    def run(self, get_batch):
        x = tf.placeholder(tf.float32, [None, self._layers[0]], name="x-input")
        y = tf.placeholder(tf.float32, [None, self._layers[-1]], name="y-input")

        regularizer = self._regularizer(self._regularization_rate)
        z = tf.nn.softmax(self.inference(x, regularizer)) # 前向传播
        cross_entropy = -tf.reduce_mean(y * tf.math.log(tf.clip_by_value(z, 1e-10, 1.0)))
        loss = tf.reduce_mean(cross_entropy) + TFModel._get_regularization_losses()

        global_step = tf.Variable(0, trainable=False)
        variable_averages = tf.train.ExponentialMovingAverage(self._moving_average_decay, global_step)
        variable_averages_op = variable_averages.apply(tf.trainable_variables())

        learning_rate = tf.train.exponential_decay(self._learning_rate_base, 
            global_step, 3000, self._learning_rate_decay, staircase=self._staircase)
        
        train_step = self._optimizer(learning_rate).minimize(loss, global_step=global_step)
        train_op = tf.group(train_step, variable_averages_op)
        saver = tf.train.Saver()

        with tf.Session() as sess:
            tf.global_variables_initializer().run()

            for i in range(self._training_steps):
                xs, ys = get_batch(self._batch_size)
                _, loss_value, step, lr = sess.run([train_op, loss, global_step, learning_rate], 
                    feed_dict={x: xs, y: ys})

                if i % 1000 == 0:
                    with tf.variable_scope("", reuse=True):
                        print(sess.run(tf.get_variable("layer1/bias")))
                    print("After %d training step(s), loss on training batch is %g, learning rate is %g." % (step, loss_value, lr))
                    saver.save(sess, self._model_save_path, global_step=global_step)


class TestModel(TFModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, get_batch):
        ckpt = tf.train.get_checkpoint_state(self._model_dir)
        if ckpt and ckpt.model_checkpoint_path:
            with tf.Graph().as_default():
                x = tf.placeholder(tf.float32, [None, self._layers[0]], name="x-input")
                y = tf.placeholder(tf.float32, [None, self._layers[-1]], name="y-input")

                z = self.inference(x, None)
                correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(z, 1))
                accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

                variable_averages = tf.train.ExponentialMovingAverage(self._moving_average_decay)
                variables_to_restore = variable_averages.variables_to_restore()
                saver = tf.train.Saver(variables_to_restore)

                with tf.Session() as sess:
                    saver.restore(sess, ckpt.model_checkpoint_path)

                    xs, ys = get_batch()
                    global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    accuracy_score = sess.run(accuracy, feed_dict={x:xs, y:ys})
                    print("After %s training step(s), validation accuracy=%g" % (global_step, accuracy_score))
        else:
            print("No checkpoint file found")

class RuntimeModel(TFModel):
    DIRECTION_MAP = {
        0: [0, 0, 0],
        1: [1, 0, 0],
        2: [1 / np.sqrt(2), 0, -1 / np.sqrt(2)],
        3: [0, 0, -1],
        4: [-1 / np.sqrt(2), 0, -1 / np.sqrt(2)],
        5: [-1, 0, 0],
        6: [-1 / np.sqrt(2), 0, 1 / np.sqrt(2)],
        7: [0, 0, 1],
        8: [1 / np.sqrt(2), 0, 1 / np.sqrt(2)]
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ckpt = tf.train.get_checkpoint_state(self._model_dir)
        if ckpt and ckpt.model_checkpoint_path:
            self._x = tf.placeholder(tf.float32, [1, self._layers[0]], name="x-input")
            self._result = tf.nn.softmax(self.inference(self._x, None))
            self._session = tf.Session()

            variable_averages = tf.train.ExponentialMovingAverage(self._moving_average_decay)
            variables_to_restore = variable_averages.variables_to_restore()
            saver = tf.train.Saver(variables_to_restore)
            saver.restore(self._session, ckpt.model_checkpoint_path)
        else:
            print("No checkpoint file found")

    def close(self):
        self._session.close()

    def run(self, x):
        result = self._session.run(self._result, feed_dict={self._x: x})[0]
        index = np.argmax(result)
        return RuntimeModel.DIRECTION_MAP[index], 10 * result[index]