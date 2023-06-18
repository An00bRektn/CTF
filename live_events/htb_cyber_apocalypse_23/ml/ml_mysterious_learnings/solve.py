#!/usr/bin/env python3
import tensorflow as tf
from tensorflow import keras

new_model = tf.keras.models.load_model(filepath='./alien.h5')
print(new_model.summary())
print(new_model.get_layer('uZDNyc3Q0bmR9'))
