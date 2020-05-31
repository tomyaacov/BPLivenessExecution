import numpy as np
import random
from collections import deque
import progressbar

import gym

from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam


#enviroment = gym.make("Taxi-v3").env
#enviroment.render()

enviroment = gym.make("CartPole-v1").env

print('Number of states: {}'.format(enviroment.observation_space))
print('Number of actions: {}'.format(enviroment.action_space.n))


class Agent:
    def __init__(self, enviroment, optimizer):

        # Initialize atributes
        #self._state_size = enviroment.observation_space.n
        self._action_size = enviroment.action_space.n
        self._optimizer = optimizer
        self._enviroment = enviroment

        self.expirience_replay = deque(maxlen=2000)

        # Initialize discount and exploration rate
        self.gamma = 0.9
        self.epsilon = 0.5

        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.align_target_model()

    def store(self, state, action, reward, next_state, terminated):
        self.expirience_replay.append((state, action, reward, next_state, terminated))

    def _build_compile_model(self):
        # model = Sequential()
        # model.add(Embedding(self._state_size, 10, input_length=1))
        # model.add(Reshape((10,)))
        # #model.add(Dense(50, activation='relu'))
        # model.add(Dense(50, activation='relu'))
        # model.add(Dense(self._action_size, activation='linear'))
        #
        # model.compile(loss='mse', optimizer=self._optimizer)

        model = Sequential()
        model.add(Dense(24, input_shape=(self._enviroment.observation_space.shape[0],), activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self._action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))


        return model

    def align_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return enviroment.action_space.sample()

        q_values = self.q_network.predict(state)
        return np.argmax(q_values[0])

    def retrain(self, batch_size):
        minibatch = random.sample(self.expirience_replay, batch_size)

        states = np.zeros((32, self._enviroment.observation_space.shape[0]), dtype="float32")
        targets = np.zeros((32, self._action_size), dtype="float32")
        counter = 0

        for state, action, reward, next_state, terminated in minibatch:

            target = self.q_network.predict(state)

            if terminated:
                target[0][action] = reward
            else:
                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)

            states[counter] = state[0]
            targets[counter] = target
            counter += 1

        self.q_network.fit(states, targets, epochs=1, verbose=0)

    # def retrain(self, batch_size):
    #     minibatch = random.sample(self.expirience_replay, batch_size)
    #
    #     for state, action, reward, next_state, terminated in minibatch:
    #
    #         target = self.q_network.predict(state)
    #
    #         if terminated:
    #             target[0][action] = reward
    #         else:
    #             t = self.target_network.predict(next_state)
    #             target[0][action] = reward + self.gamma * np.amax(t)
    #
    #         self.q_network.fit(state, target, epochs=1, verbose=0)


optimizer = Adam(learning_rate=0.01)
agent = Agent(enviroment, optimizer)

batch_size = 32
num_of_episodes = 1000
timesteps_per_episode = 10^8
agent.q_network.summary()

for e in range(0, num_of_episodes):
    # Reset the enviroment
    state = enviroment.reset()
    state = np.reshape(state, [1, 4])

    # Initialize variables
    reward = 0
    terminated = False

    # bar = progressbar.ProgressBar(maxval=timesteps_per_episode,
    #                               widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    # bar.start()

    for timestep in range(timesteps_per_episode):
        # Run Action
        action = agent.act(state)

        # Take action
        next_state, reward, terminated, info = enviroment.step(action)
        next_state = np.reshape(next_state, [1, 4])
        agent.store(state, action, reward, next_state, terminated)

        state = next_state

        if terminated:
            agent.align_target_model()
            break

        if len(agent.expirience_replay) > batch_size:
            agent.retrain(batch_size)

    #     bar.update(timestep)
    #
    # bar.finish()
    print("**********************************")
    print("Episode: {}".format(e + 1))
    print("**********************************")




agent.epsilon = 0
# Initialize variables
reward = 0
terminated = False

for i_episode in range(20):
    state = enviroment.reset()
    state = np.reshape(state, [1, 4])
    for t in range(100):
        enviroment.render()
        print(state)
        action = agent.act(state)
        # Take action
        next_state, reward, terminated, info = enviroment.step(action)
        next_state = np.reshape(next_state, [1, 4])
        state = next_state
        if terminated:
            print("Episode finished after {} timesteps".format(t+1))
            break
enviroment.close()