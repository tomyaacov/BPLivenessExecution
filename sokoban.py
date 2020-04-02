from bppy import *
import itertools
from q_learning import *
import matplotlib.pyplot as plt


must_finish = "must_finish"
state = "state"


def action_to_new_location(action, i, j):
    if action == "Up":
        return i - 1, j
    if action == "Down":
        return i + 1, j
    if action == "Left":
        return i, j - 1
    if action == "Right":
        return i, j + 1


def event_to_new_location(event):
    return action_to_new_location(action=event.name, **event.data)


def event_to_2_steps_trajectory(event):
    i, j = event_to_new_location(event)
    return event_to_new_location(BEvent(event.name, {"i": i, "j": j}))


def new_location_to_events(i, j):
    return [BEvent("Up", {"i": i+1, "j": j}),
            BEvent("Down", {"i": i-1, "j": j}),
            BEvent("Left", {"i": i, "j": j+1}),
            BEvent("Right", {"i": i, "j": j-1})]


def is_adjacent(l1, l2):
    terms = list()
    terms.append(l1[0] == l2[0] and l1[1] == l2[1]+1)
    terms.append(l1[0] == l2[0] and l1[1] == l2[1]-1)
    terms.append(l1[0] == l2[0]+1 and l1[1] == l2[1])
    terms.append(l1[0] == l2[0]-1 and l1[1] == l2[1])
    return sum(terms) == 1


def find_adjacent_objects(list_1, list_2):
    return [(l1, l2) for l1 in list_1 for l2 in list_2 if is_adjacent(l1, l2)]


def block_action(event, neighbors_list):
    neighbors_list = neighbors_list["neighbors_list"]
    p1 = event_to_new_location(event)
    p2 = event_to_2_steps_trajectory(event)
    return (p1, p2) in neighbors_list or (p2, p1) in neighbors_list


@b_thread
def player(i, j):
    directions = ["Up", "Down", "Left", "Right"]
    while True:
        e = yield {request: [BEvent(d, {"i": i, "j": j}) for d in directions], state: str(i)+"_"+str(j)}
        i, j = event_to_new_location(e)


@b_thread
def wall(walls_list):
    block_list = list(itertools.chain(*[new_location_to_events(i, j) for i, j in walls_list]))  # use event_to_new_location(e)
    yield {block: block_list}


@b_thread
def box(box_list, walls_list):  # walls list should be global const
    while True:
        neighbors_list = find_adjacent_objects(box_list, walls_list) + \
                         find_adjacent_objects(box_list, box_list)
        double_object_movement = EventSet(block_action, neighbors_list=neighbors_list)
        box_list_state = "_".join([str(i) for b in box_list for i in b])
        e = yield {block: double_object_movement, waitFor: All(), state: box_list_state}
        new_player_location = event_to_new_location(e)
        if new_player_location in box_list:
            new_box_location = event_to_2_steps_trajectory(e)
            box_list.remove(new_player_location)
            box_list.append(new_box_location)


# def block_action(n_list): change to gera's option
#     def predicate():
#           pass
#     return predicate
#


@b_thread
def target(i, j, full):
    e = yield {waitFor: All(), state: 1}
    while True:
        new_player_location = event_to_new_location(e)
        if new_player_location == (i, j):
            full = false
        elif new_player_location in box_list:
            new_box_location = event_to_2_steps_trajectory(e)
            if (i, j) == new_box_location:
                full = true
        if full:
            e = yield {block: All(), must_finish: not full}
        else:
            e = yield {waitFor: All(), must_finish: not full, state: 2}


@b_thread
def map_printer(map):
    while True:
        #print("\n".join(map))
        #print()
        e = yield {waitFor: All()}
        map = ",".join(map).replace("a", " ").split(",")
        map = ",".join(map).replace("A", "t").split(",")
        i, j = event_to_new_location(e)
        if map[i][j] == "b" or map[i][j] == "B":
            i2, j2 = event_to_2_steps_trajectory(e)
            if map[i2][j2] == "t":
                map[i2] = map[i2][:j2] + "B" + map[i2][j2 + 1:]
            else:
                map[i2] = map[i2][:j2] + "b" + map[i2][j2 + 1:]
            if map[i][j] == "b":
                map[i] = map[i][:j] + "a" + map[i][j+1:]
            else:
                map[i] = map[i][:j] + "A" + map[i][j + 1:]
        elif map[i][j] == "t":
            map[i] = map[i][:j] + "A" + map[i][j + 1:]
        else:
            map[i] = map[i][:j] + "a" + map[i][j + 1:]


# run
def find(map, ch):
    return [(i, j) for i, row in enumerate(map) for j, c in enumerate(row) if c == ch]

map = [
    "  XXXXX ",
    "XXX   X ",
    "X b X XX",
    "X X  t X",
    "X    X X",
    "XX X   X",
    " Xa  XXX",
    " XXXXX  "
]

# map = [
#     "XXXXXX",
#     "Xa   X",
#     "X   bX",
#     "X   tX",
#     "XXXXXX"
#        ]


def init_bprogram():
    walls_list = find(map, "X")
    box_list = find(map, "b") + find(map, "B")
    empty_target_list = find(map, "t") + find(map, "A")
    full_target_list = find(map, "B")
    player_locations = find(map, "a") + find(map, "A")

    bthreads_list = [player(*l) for l in player_locations] + \
                    [target(*l, false) for l in empty_target_list] + \
                    [target(*l, true) for l in full_target_list] + \
                    [wall(walls_list), box(box_list, walls_list), map_printer(map)]
    return BProgram(bthreads=bthreads_list,
                     event_selection_strategy=SimpleEventSelectionStrategy())


Q, results, episodes, mean_reward = qlearning(init_bprogram=init_bprogram,
                                              num_episodes=100000,
                                              episode_timeout=100,
                                              alpha=0.1,
                                              gamma=0.99,
                                              testing=True,
                                              seed=1,
                                              glie=glie_10)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
# event_runs = []
# for i in range(100):
#     reward, event_run = run_optimal(b_program, Q, i)
#     if event_run not in event_runs:
#         event_runs.append(event_run)
# print(event_runs)
print(Q_test_optimal(b_program, Q, 1000, 2))


