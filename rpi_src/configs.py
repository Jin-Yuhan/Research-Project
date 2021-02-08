'''
author: Jin Yuhan
date: 2021-01-25 19:14:37
lastTime: 2021-02-08 14:50:17
'''



BATCH_SIZE = 15
LAYER_DIMS = [15, 20, 20, 20, 20, 20, 20, 20, 8]
REGULARIZATION_RATE = 0.000001
MOVING_AVERAGE_DECAY = 0.99
LEARNING_RATE_BASE = 0.1
LEARNING_RATE_DECAY = 0.99
TRAINING_STEPS = 3000001
MODEL_SAVE_PATH = "./model_data/model.ckpt"
TRAIN_DATA_SAVE_PATH = "./train_data/train_data.json"