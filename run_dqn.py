from config import (BATCH_SIZE, CLIP_REWARD, DISCOUNT_FACTOR,
                    EVAL_LENGTH, STEPS_BETWEEN_EVAL, INPUT_SHAPE,
                    LEARNING_RATE, LOAD_FROM, LOAD_REPLAY_BUFFER,
                    MAX_EPISODE_LENGTH, MEM_SIZE,
                    MIN_REPLAY_BUFFER_SIZE, PRIORITY_SCALE, SAVE_PATH,
                    TENSORBOARD_DIR, TOTAL_STEPS, UPDATE_FREQ, USE_PER,
                    WRITE_TENSORBOARD)
from train_dqn import *
from lane_bridge import *
import pygame

# Create environment
if __name__ == "__main__":
    #pygame_settings["display"] = True
    pygame.init()  
    env = gym_env_generator(episode_timeout=15)
    print("The environment has the following {} actions".format(env.action_space.n))

    # Build main and target networks
    MAIN_DQN = build_q_network(env.action_space.n, LEARNING_RATE, input_shape=INPUT_SHAPE)
    TARGET_DQN = build_q_network(env.action_space.n, input_shape=INPUT_SHAPE)

    replay_buffer = ReplayBuffer(size=MEM_SIZE, input_shape=INPUT_SHAPE, use_per=USE_PER)
    agent = Agent(MAIN_DQN, TARGET_DQN, replay_buffer, env.action_space.n, input_shape=INPUT_SHAPE, batch_size=BATCH_SIZE, use_per=USE_PER)
    print('Loading from', LOAD_FROM)
    meta = agent.load("/Users/tomyaacov/university/BPLivenessRL/lane-bridge/save-00100005", False)
    MAIN_DQN.compile(Adam(LEARNING_RATE), loss=tf.keras.losses.Huber())
    TARGET_DQN.compile(Adam(LEARNING_RATE), loss=tf.keras.losses.Huber())
    total_rewards = 0
    state = np.array([3., 4., 1.])
    print(agent.target_dqn.predict(state.reshape((-1, agent.input_shape[0])))[0] )
    print(agent.DQN.predict(state.reshape((-1, agent.input_shape[0])))[0] )
    # for i in range(1):
    #     observation = env.reset()
    #     print(type(observation))
    #     reward_sum = 0
    #     counter = 0
    #     while True:
    #         # env.render()
    #         action = agent.get_action(counter, 15, observation, env, True)
    #         observation, reward, done, info = env.step(action)
    #         if reward == 1:
    #             done = True
    #         reward_sum += reward
    #         counter += 1
    #         print(action, observation, reward, done, info)
    #         if done:
    #             break
    #     print(reward_sum)
    #     total_rewards += reward_sum
    # print(1+(total_rewards/1000))
    # env.close()
    # pygame.quit()