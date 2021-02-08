'''
author: Jin Yuhan
date: 2021-01-25 18:10:05
lastTime: 2021-01-27 22:39:34
'''

import tensorflow as tf

def get_regularization_losses():
    return tf.add_n(tf.compat.v1.get_collection("losses"))

def get_weights(shape, dtype, regularizer):
    weights = tf.compat.v1.get_variable("weights", shape, dtype, initializer=tf.truncated_normal_initializer(stddev=0.1), trainable=True)
    
    if regularizer:
        tf.compat.v1.add_to_collection("losses", regularizer(weights))
    return weights

def inference(layer_dims, in_tensor, regularizer):
    in_layer_dim = layer_dims[0]

    for i in range(1, len(layer_dims)):
        out_layer_dim = layer_dims[i]
        
        with tf.compat.v1.variable_scope("layer" + str(i)):
            weights = get_weights([in_layer_dim, out_layer_dim], tf.float32, regularizer)
            bias = tf.compat.v1.get_variable("bias", [out_layer_dim], tf.float32, initializer=tf.constant_initializer(0.0))
            in_tensor = tf.matmul(in_tensor, weights) + bias
            in_layer_dim = out_layer_dim

        if i < len(layer_dims) - 1:
            in_tensor = tf.nn.relu(in_tensor)
            
    return in_tensor
