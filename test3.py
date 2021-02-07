import tensorflow as tf
from tensorflow.keras.initializers import VarianceScaling
from tensorflow.keras.layers import (Add, Conv2D, Dense, Flatten, Input,
                                     Lambda, Subtract)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras import initializers
import numpy as np
from train_dqn import *
tf.enable_eager_execution()
sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()

batch_size = 32
all_states = np.load("lane-bridge/save-00001500/replay-buffer/states.npy")
#new_states = np.load("lane-bridge/save-00001500/replay-buffer/states.npy")
all_actions = np.load("lane-bridge/save-00001500/replay-buffer/actions.npy")
all_rewards = np.load("lane-bridge/save-00001500/replay-buffer/rewards.npy")
all_terminal_flags = np.load("lane-bridge/save-00001500/replay-buffer/terminal_flags.npy")

def get_minibatch(batch_size=32, priority_scale=0.0):
    """Returns a minibatch of self.batch_size = 32 transitions
    Arguments:
        batch_size: How many samples to return
        priority_scale: How much to weight priorities. 0 = completely random, 1 = completely based on priority
    Returns:
        A tuple of states, actions, rewards, new_states, and terminals
        If use_per is True:
            An array describing the importance of transition. Used for scaling gradient steps.
            An array of each index that was sampled
    """
    # Get sampling probabilities from priority list
    indices = []
    for i in range(batch_size):
        while True:
            index = random.randint(0, all_states.shape[0] - 1)
            if not all_terminal_flags[index]:
                indices.append(index)
                break
    # Retrieve states from memory
    old_states = []
    new_states = []
    for idx in indices:
        old_states.append(all_states[idx, ...])
        new_states.append(all_states[idx+1, ...])
    #states = np.transpose(np.asarray(states), axes=(0, 2, 3, 1))
    #new_states = np.transpose(np.asarray(new_states), axes=(0, 2, 3, 1))
    old_states = np.asarray(old_states)
    new_states = np.asarray(new_states)
    
    return old_states, all_actions[indices], all_rewards[indices], new_states, all_terminal_flags[indices]

OPTIMIZER = Adam(0.1)
LOSS_FUNCTION = tf.keras.losses.Huber()

MAIN_DQN = tf.keras.models.Sequential()
MAIN_DQN.add(tf.keras.Input(shape=(2,)))
MAIN_DQN.add(tf.keras.layers.Dense((2,)[0], activation='relu', kernel_initializer=initializers.Zeros(), bias_initializer=initializers.Zeros()))
MAIN_DQN.add(tf.keras.layers.Dense(2, kernel_initializer=initializers.Zeros(), bias_initializer=initializers.Zeros()))
MAIN_DQN.compile(OPTIMIZER, loss=LOSS_FUNCTION)

TARGET_DQN = tf.keras.models.Sequential()
TARGET_DQN.add(tf.keras.Input(shape=(2,)))
TARGET_DQN.add(tf.keras.layers.Dense((2,)[0], activation='relu', kernel_initializer=initializers.Zeros(), bias_initializer=initializers.Zeros()))
TARGET_DQN.add(tf.keras.layers.Dense(2, kernel_initializer=initializers.Zeros(), bias_initializer=initializers.Zeros()))
TARGET_DQN.compile(OPTIMIZER, loss=LOSS_FUNCTION)

# print(tf.global_variables())
# init = tf.global_variables_initializer()
# sess.run(init)
# sess.run(tf.variables_initializer(OPTIMIZER.variables()))

state = np.array([1.0, 5.0])
print(state.reshape((-1, 2)))
q_vals = MAIN_DQN.predict(state.reshape((-1, 2)))[0]
print("q_vals", q_vals)

for step in range(30000):
    states, actions, rewards, new_states, terminal_flags = get_minibatch(batch_size=batch_size)
    arg_q_max = MAIN_DQN.predict(new_states).argmax(axis=1)

    # Target DQN estimates q-vals for new states
    future_q_vals = TARGET_DQN.predict(new_states)
    double_q = future_q_vals[range(batch_size), arg_q_max]

    # Calculate targets (bellman equation)
    target_q = rewards + (0.99*double_q * (1-terminal_flags))#TODO:

    # Open a GradientTape.
    with tf.GradientTape() as tape:
        q_values = MAIN_DQN(states)
        one_hot_actions = tf.keras.utils.to_categorical(actions, 2, dtype=np.float32)  # using tf.one_hot causes strange errors
        Q = tf.reduce_sum(tf.multiply(q_values, one_hot_actions), axis=1)
        error = Q - target_q
        loss = tf.keras.losses.Huber()(target_q, Q)

    model_gradients = tape.gradient(loss, MAIN_DQN.trainable_variables)
    train_step = MAIN_DQN.optimizer.apply_gradients(zip(model_gradients, MAIN_DQN.trainable_variables))
    # sess.run(train_step)
    # Logging.
    if step % 100 == 0:
        print("Step:", step, "Loss:", float(loss.numpy()))
        TARGET_DQN.set_weights(MAIN_DQN.get_weights())

state = np.array([1.0, 5.0])
print(state.reshape((-1, 2)))
q_vals = MAIN_DQN.predict(state.reshape((-1, 2)))[0]
print("q_vals", q_vals)



