import random


def glie_3(i, num_episodes):
    if i >= num_episodes-100:
        return 0
    return 1

def glie_10(i, num_episodes):
    if i >= num_episodes-100:
        return 0
    return 1-(i/num_episodes)


def epsilon_greedy_online(bprogram, Q, s_t, epsilon, reward_sum):
    if random.random() > epsilon:
        if s_t in Q:
            try:
                a_t_hash = random.choice([key for key in Q[s_t].keys() if reward_sum + Q[s_t][key] > -1])
            except IndexError:
                return bprogram.next_event()  # TODO: not sure it's the right approach
            # a_t_hash = max(Q[s_t], key=Q[s_t].get)
            for a in bprogram.event_selection_strategy.selectable_events(bprogram.tickets):
                if a_t_hash == a.__hash__():
                    return a
        else:
            return bprogram.next_event()  # TODO: not sure it's the right approach
    else:
        try:
            return random.choice(tuple(bprogram.event_selection_strategy.selectable_events(bprogram.tickets)))  # TODO: not sure it's the right approach
            # return bprogram.next_event()  # TODO: not sure it's the right approach
        except IndexError:
            return None


def must_finish(bprogram):
    return [x.get('must_finish', False) for x in bprogram.tickets]


def qlearning(bprogram_generator, num_episodes, alpha, gamma, testing, seed, glie, episode_timeout=None):
    random.seed(seed)
    Q = dict()
    test_results = []
    tested_episodes = []
    mean_reward = []
    for i in range(num_episodes):
        bprogram = bprogram_generator()
        done = False
        bprogram.setup()
        steps_counter = 0
        reward_sum = 0
        s_t = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
        hot_states = [False] * len(bprogram.tickets)
        #print(s_t)
        if s_t not in Q:
            Q[s_t] = {i.__hash__(): 0 for i in bprogram.event_selection_strategy.selectable_events(bprogram.tickets)}
        epsilon = glie(i, num_episodes)
        a_t = epsilon_greedy_online(bprogram, Q, s_t, epsilon, reward_sum)
        while not done:
            bprogram.advance_bthreads(a_t)
            s_t_1 = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
            r_t = 0
            hot_states_1 = must_finish(bprogram)
            for j in range(len(hot_states)):
                if hot_states[j] and not hot_states_1[j]:
                    r_t += 1
                if not hot_states[j] and hot_states_1[j]:
                    r_t += -1
            #print(a_t.name, s_t_1, r_t)
            reward_sum += r_t
            bprogram_done = bprogram.event_selection_strategy.selectable_events(bprogram.tickets).__len__() == 0
            a_t_1 = epsilon_greedy_online(bprogram, Q, s_t_1, epsilon, reward_sum)
            if s_t_1 not in Q:
                if bprogram_done:
                    Q[s_t_1] = {0: 0}
                else:
                    Q[s_t_1] = {i.__hash__(): 0 for i in bprogram.event_selection_strategy.selectable_events(bprogram.tickets)}

            Q[s_t][a_t.__hash__()] = Q[s_t][a_t.__hash__()] + alpha * (
                        r_t + gamma * max(Q[s_t_1].values()) - Q[s_t][a_t.__hash__()])

            s_t, a_t, hot_states = s_t_1, a_t_1, hot_states_1
            timeout = steps_counter == episode_timeout
            done = bprogram_done or timeout
            steps_counter += 1
        if testing:
            test_results.append(reward_sum)
            tested_episodes.append(i)
            mean_reward.append(sum(test_results[-100:])/len(test_results[-100:]))
            print(f"Round {i} ended with {mean_reward[-1]} mean reward")
    return Q, test_results, tested_episodes, mean_reward


def run(bprogram, Q, seed, episode_timeout):
    random.seed(seed)
    done = False
    bprogram.setup()
    run = ""
    hot_states_history = []
    reward_sum = 0
    s_t = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
    hot_states = [False] * len(bprogram.tickets)
    if s_t in Q:
        choices = [key for key in Q[s_t].keys() if Q[s_t][key] + reward_sum > -1]
        #print(choices)
        try:
            a_t_hash = random.choice(choices)
            for a in bprogram.event_selection_strategy.selectable_events(bprogram.tickets):
                if a_t_hash == a.__hash__():
                    a_t = a
                    break
        except IndexError:
            a_t = bprogram.next_event()
    else:
        a_t = bprogram.next_event()
    run += a_t.name
    steps_counter = 0
    while True:
        bprogram.advance_bthreads(a_t)
        s_t_1 = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
        r_t = 0
        hot_states_1 = must_finish(bprogram)
        for j in range(len(hot_states)):
            if hot_states[j] and not hot_states_1[j]:
                r_t += 1
            if not hot_states[j] and hot_states_1[j]:
                r_t += -1
        #print(a_t.name, s_t_1, r_t)
        reward_sum += r_t
        done = bprogram.event_selection_strategy.selectable_events(bprogram.tickets).__len__() == 0
        if done:
            break
        if s_t_1 in Q:
            choices = [key for key in Q[s_t_1].keys() if reward_sum + Q[s_t_1][key] > -1]
            #print(choices)
            try:
                a_t_hash = random.choice(choices)
                for a in bprogram.event_selection_strategy.selectable_events(bprogram.tickets):
                    if a_t_hash == a.__hash__():
                        a_t_1 = a
                        break
            except IndexError:
                a_t_1 = bprogram.next_event()
        else:
            a_t_1 = bprogram.next_event()
        s_t, a_t, hot_states = s_t_1, a_t_1, hot_states_1   
        run += a_t.name
        if steps_counter == episode_timeout:
            break
        steps_counter += 1
    return reward_sum, run


def Q_test(bprogram_generator, Q, rounds, seed, episode_timeout):
    total_reward = 0
    success = 0
    for i in range(rounds):
        print(i)
        bprogram = bprogram_generator()
        r, s = run(bprogram, Q, seed+i, episode_timeout)
        total_reward += r
        if r==0:
            success += 1
    print(success/rounds)
    return total_reward/rounds


def run_optimal(bprogram, Q, seed, episode_timeout):
    random.seed(seed)
    done = False
    bprogram.setup()
    run = ""
    hot_states_history = []
    reward_sum = 0
    s_t = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
    hot_states = [False] * len(bprogram.tickets)
    if s_t in Q:
        choices = [key for key in Q[s_t].keys() if Q[s_t][key] == max(Q[s_t].values())]
        #print(choices)
        try:
            a_t_hash = random.choice(choices)
            for a in bprogram.event_selection_strategy.selectable_events(bprogram.tickets):
                if a_t_hash == a.__hash__():
                    a_t = a
                    break
        except IndexError:
            a_t = bprogram.next_event()
    else:
        a_t = bprogram.next_event()
    run += a_t.name
    steps_counter = 0
    while True:
        bprogram.advance_bthreads(a_t)
        s_t_1 = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
        r_t = 0
        hot_states_1 = must_finish(bprogram)
        for j in range(len(hot_states)):
            if hot_states[j] and not hot_states_1[j]:
                r_t += 1
            if not hot_states[j] and hot_states_1[j]:
                r_t += -1
        #print(a_t.name, s_t_1, r_t)
        reward_sum += r_t
        done = bprogram.event_selection_strategy.selectable_events(bprogram.tickets).__len__() == 0
        if done:
            break
        if s_t_1 in Q:
            choices = [key for key in Q[s_t_1].keys() if Q[s_t_1][key] == max(Q[s_t_1].values())]
            #print(choices)
            try:
                a_t_hash = random.choice(choices)
                for a in bprogram.event_selection_strategy.selectable_events(bprogram.tickets):
                    if a_t_hash == a.__hash__():
                        a_t_1 = a
                        break
            except IndexError:
                a_t_1 = bprogram.next_event()
        else:
            a_t_1 = bprogram.next_event()
        s_t, a_t, hot_states = s_t_1, a_t_1, hot_states_1
        run += a_t.name
        if steps_counter == episode_timeout:
            break
        steps_counter += 1
    return reward_sum, run


def Q_test_optimal(bprogram_generator, Q, rounds, seed, episode_timeout):
    total_reward = 0
    success = 0
    for i in range(rounds):
        bprogram = bprogram_generator()
        r, s = run_optimal(bprogram, Q, seed+i, episode_timeout)
        total_reward += r
        if r==0:
            success += 1
    print(success/rounds)
    return total_reward/rounds

