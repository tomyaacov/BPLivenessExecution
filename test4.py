import os
import gym
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
env = gym.make("CartPole-v0").env
env.reset()
n_actions = env.action_space.n
state_dim = env.observation_space.shape


from tensorflow import keras
import random
from tensorflow.keras import layers as L
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()


network = keras.models.Sequential()
network.add(L.InputLayer(state_dim))

# let's create a network for approximate q-learning following guidelines above
network.add(L.Dense(5, activation='elu'))
network.add(L.Dense(5, activation='relu'))
network.add(L.Dense(n_actions, activation='linear'))

s = env.reset()

# Create placeholders for the <s, a, r, s'> tuple and a special indicator for game end (is_done = True)
states_ph = keras.backend.placeholder(dtype='float32', shape=(None,) + state_dim)
actions_ph = keras.backend.placeholder(dtype='int32', shape=[None])
rewards_ph = keras.backend.placeholder(dtype='float32', shape=[None])
next_states_ph = keras.backend.placeholder(dtype='float32', shape=(None,) + state_dim)
is_done_ph = keras.backend.placeholder(dtype='bool', shape=[None])

#get q-values for all actions in current states
predicted_qvalues = network(states_ph)

#select q-values for chosen actions
predicted_qvalues_for_actions = tf.reduce_sum(predicted_qvalues * tf.one_hot(actions_ph, n_actions),
                                              axis=1)

gamma = 0.99

# compute q-values for all actions in next states
predicted_next_qvalues = network(next_states_ph)

# compute V*(next_states) using predicted next q-values
next_state_values = tf.math.reduce_max(predicted_next_qvalues, axis=1)

# compute "target q-values" for loss - it's what's inside square parentheses in the above formula.
target_qvalues_for_actions = rewards_ph + tf.constant(gamma) * next_state_values

# at the last state we shall use simplified formula: Q(s,a) = r(s,a) since s' doesn't exist
target_qvalues_for_actions = tf.where(is_done_ph, rewards_ph, target_qvalues_for_actions)

#mean squared error loss to minimize
loss = (predicted_qvalues_for_actions - tf.stop_gradient(target_qvalues_for_actions)) ** 2
loss = tf.reduce_mean(loss)

# training function that resembles agent.update(state, action, reward, next_state) from tabular agent
train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(loss)

a = 0
next_s, r, done, _ = env.step(a)

init = tf.global_variables_initializer()
sess.run(init)
sess.run(train_step, {
            states_ph: [s], actions_ph: [a], rewards_ph: [r],
            next_states_ph: [next_s], is_done_ph: [done]
        })