from lane_bridge import *
from train_dqn import *

from config import (BATCH_SIZE, CLIP_REWARD, DISCOUNT_FACTOR,
                    EVAL_LENGTH, STEPS_BETWEEN_EVAL, INPUT_SHAPE,
                    LEARNING_RATE, LOAD_FROM, LOAD_REPLAY_BUFFER,
                    MAX_EPISODE_LENGTH, MEM_SIZE,
                    MIN_REPLAY_BUFFER_SIZE, PRIORITY_SCALE, SAVE_PATH,
                    TENSORBOARD_DIR, TOTAL_STEPS, UPDATE_FREQ, UPDATE_TARGET_FREQ, USE_PER,
                    WRITE_TENSORBOARD)


env = gym_env_generator(episode_timeout=200)
print("The environment has the following {} actions".format(env.action_space.n))
# Build main and target networks
MAIN_DQN = build_q_network(env.action_space.n, False, LEARNING_RATE, input_shape=INPUT_SHAPE)
TARGET_DQN = build_q_network(env.action_space.n, True, LEARNING_RATE, input_shape=INPUT_SHAPE)
replay_buffer = ReplayBuffer(size=MEM_SIZE, input_shape=INPUT_SHAPE, use_per=USE_PER)
agent = Agent(MAIN_DQN, TARGET_DQN, replay_buffer, env.action_space.n, input_shape=INPUT_SHAPE, batch_size=BATCH_SIZE, use_per=USE_PER)
#agent.replay_buffer.load("/Users/tomyaacov/university/BPLivenessRL/test_folder")
s = np.load("/Users/tomyaacov/university/BPLivenessRL/test_folder" + '/states.npy')
a = np.load("/Users/tomyaacov/university/BPLivenessRL/test_folder" + '/actions.npy')
r = np.load("/Users/tomyaacov/university/BPLivenessRL/test_folder" + '/rewards.npy')
t = np.load("/Users/tomyaacov/university/BPLivenessRL/test_folder" + '/terminal_flags.npy')
i = np.load("/Users/tomyaacov/university/BPLivenessRL/test_folder" + '/is_last.npy')

for j in range(s.shape[0]):
    agent.replay_buffer.add_experience(a[j],s[j,:],r[j],t[j],i[j])
agent.replay_buffer.add_experience(0,np.array([0,0,0]),0,False,True)
state = np.array([1.0, 3.0, 0.0])
print(agent.DQN.predict(state.reshape((-1, agent.input_shape[0])))[0] )
for j in range(100000):
    l, e = agent.learn(32,1,j)
    #print(j, l, np.abs(e).mean())
    if j%10 == 9:
        print(j, l, np.abs(e).mean())
        agent.update_target_network()
states = np.array([1.0, 3.0, 0.0])
print(agent.DQN.predict(states.reshape((-1, agent.input_shape[0])))[0] )
new_states = np.array([2.0,2.5,0.0])
states = states.reshape((-1, agent.input_shape[0]))
new_states = new_states.reshape((-1, agent.input_shape[0]))
terminal_flags = np.array([False])
rewards = np.array([0.0])
actions = np.array([1.0])
# Main DQN estimates best action in new states
arg_q_max = agent.DQN.predict(new_states.reshape((-1, agent.input_shape[0]))).argmax(axis=1)
print("arg_q_max", arg_q_max)
# Target DQN estimates q-vals for new states
future_q_vals = agent.target_dqn.predict(new_states.reshape((-1, agent.input_shape[0])))
print("future_q_vals", future_q_vals)
double_q = future_q_vals[[0], arg_q_max]
print("double_q", double_q)
# Calculate targets (bellman equation)
target_q = rewards + (DISCOUNT_FACTOR*double_q * (1-terminal_flags))#TODO:
print("target_q", target_q)
# # Use targets to calculate loss (and use loss to calculate gradients)
with tf.GradientTape() as tape:
    q_values = agent.DQN(states)
    print("q_values", q_values)
    one_hot_actions = tf.keras.utils.to_categorical(actions, agent.n_actions, dtype=np.float32)  # using tf.one_hot causes strange errors
    print("one_hot_actions", one_hot_actions)
    Q = tf.reduce_sum(tf.multiply(q_values, one_hot_actions), axis=1)
    print("Q", Q)
    error = Q - target_q
    print("error", error)
    loss = tf.keras.losses.Huber()(target_q, Q)
    print("loss", loss)

model_gradients = tape.gradient(loss, agent.DQN.trainable_variables)
print("model_gradients", model_gradients)
train_step = agent.DQN.optimizer.apply_gradients(zip(model_gradients, agent.DQN.trainable_variables))
print("train_step", train_step)




