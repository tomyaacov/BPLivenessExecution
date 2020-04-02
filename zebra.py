from bppy import *
from q_compatible_event_selection_strategy import RLEventSelectionStrategy
from q_learning import *
import matplotlib.pyplot as plt

must_finish = "must_finish"
state = "state"

House = EventSet(lambda e: e.name in ["House1", "House2", "House3", "House4", "House5"])
Color = EventSet(lambda e: e.name in ['Yellow', 'Blue', 'Red', 'Ivory', 'Green'])
Nationality = EventSet(lambda e: e.name in ['Norwegian', 'Ukrainian', 'Englishman', 'Spaniard', 'Japanese'])
Drink = EventSet(lambda e: e.name in ['Water', 'Tea', 'Milk', 'OrangeJuice', 'Coffee'])
Smoke = EventSet(lambda e: e.name in ['Kools', 'Chesterfield', 'OldGold', 'LuckyStrike', 'Parliament'])
Pet = EventSet(lambda e: e.name in ['Fox', 'Horse', 'Snails', 'Dog', 'Zebra'])


def five_houses():
    # There are five houses
    yield {block: AllExcept(BEvent(name="House1")), request: BEvent(name="House1"), state: 1, must_finish: True}
    for i in range(2, 6):
        yield {request: BEvent(name="House"+str(i)), state: i, must_finish: True}


def englishman_red():
    # The Englishman lives in the red house
    events = {BEvent("Red"), BEvent("Englishman")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def spaniard_dog():
    # The Spaniard owns the dog
    events = {BEvent("Dog"), BEvent("Spaniard")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def coffee_green():
    # The Spaniard owns the dog
    events = {BEvent("Coffee"), BEvent("Green")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def ukrainian_tea():
    # The Ukrainian drinks tea
    events = {BEvent("Ukrainian"), BEvent("Tea")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def green_after_ivory():
    # The green house is immediately after the ivory house
    yield {request: BEvent("Ivory"), state: 1, must_finish: True}
    yield {waitFor: House, state: 2, must_finish: True}
    yield {request: BEvent("Green"), block: House, state: 3, must_finish: True}


def old_god_snails():
    # The Old Gold smoker owns snails
    events = {BEvent("OldGold"), BEvent("Snails")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def kools_yellow():
    # Kools are smoked in the yellow house
    events = {BEvent("Kools"), BEvent("Yellow")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def milk_middle_house():
    # Milk is drunk in the middle house
    count = 0
    e = yield {waitFor: House, state: count, must_finish: True}
    while e in House:
        e = yield {waitFor: House, request: BEvent("Milk"), state: count+1, must_finish: True}
        count += 1

    for i in range(count-1):
        yield {waitFor: House, state: count+i+3, must_finish: True}

    yield {block: House, state: count*2+1}

def norwegian_first_house():
    # The Norwegian lives in the first house
    yield {waitFor: BEvent(name="House1"), state: 1, must_finish: True}
    yield {request: BEvent("Norwegian"), block: House, state: 2, must_finish: True}


def chesterfield_neighbor_fox():
    # The man who smokes Chesterfield is a neighbor of the man with the fox.
    events = {BEvent("Chesterfield"), BEvent("Fox")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {waitFor: House, state: 2, must_finish: True}
    yield {request: events - {e}, block: House, state: 3, must_finish: True}


def kools_neighbor_horse():
    # The man who smokes Kools is a neighbor of the man with the horse.
    events = {BEvent("Kools"), BEvent("Horse")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {waitFor: House, state: 2, must_finish: True}
    yield {request: events - {e}, block: House, state: 3, must_finish: True}


def orangejuice_luckystrike():
    # The Lucky Strike smoker drinks orange juice
    events = {BEvent("OrangeJuice"), BEvent("LuckyStrike")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def japanese_parliament():
    # The Japanese smokes Parliament
    events = {BEvent("Parliament"), BEvent("Japanese")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {request: events - {e}, block: House, state: 2, must_finish: True}


def norwegian_neighbors_blue():
    # The Norwegian neighbors the blue house.
    events = {BEvent("Norwegian"), BEvent("Blue")}
    e = yield {request: events, state: 1, must_finish: True}
    yield {waitFor: House, state: 2, must_finish: True}
    yield {request: events - {e}, block: House, state: 3, must_finish: True}


def water():
    # Now, who drinks water?
    yield {request: BEvent("Water"), state: 1, must_finish: True}


def zebra():
    # Who owns the zebra?
    yield {request: BEvent("Zebra"), state: 1, must_finish: True}


def different_attributes():
    # In the interest of clarity, it must be added that each of the five
    # houses is painted a different color, and their inhabitants are of
    # different national extractions, own different pets, drink different
    # beverages and smoke different brands of American cigarets [sic]
    s = set()
    while True:
        e = yield {waitFor: All(), block: s, state: s.__len__()}
        if e != BEvent(name="I"):
            s.add(e)


def one_color():
    yield {waitFor: House, state: 1}
    while True:
        yield {waitFor: Color, block: House, state: 2}
        yield {waitFor: House, block: Color, state: 3}


def one_nationality():
    yield {waitFor: House, state: 1}
    while True:
        yield {waitFor: Nationality, block: House, state: 2}
        yield {waitFor: House, block: Nationality, state: 3}


def one_drink():
    yield {waitFor: House, state: 1}
    while True:
        yield {waitFor: Drink, block: House, state: 2}
        yield {waitFor: House, block: Drink, state: 3}


def one_smoke():
    yield {waitFor: House, state: 1}
    while True:
        yield {waitFor: Smoke, block: House, state: 2}
        yield {waitFor: House, block: Smoke, state: 3}


def one_pet():
    yield {waitFor: House, state: 1}
    while True:
        yield {waitFor: Pet, block: House, state: 2}
        yield {waitFor: House, block: Pet, state: 3}


def idle():
    yield {request: BEvent(name="I"), state: 0, must_finish: False}
    yield {waitFor: BEvent(name="A"), state: 0}


b_program = BProgram(source_name="zebra",
                     event_selection_strategy=RLEventSelectionStrategy(),
                     listener=PrintBProgramRunnerListener())
b_program.run()
Q, results, episodes, mean_reward = qlearning(b_program, 200000, 0.1, 0.99, True, 5, glie_10)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
event_runs = []
for i in range(100):
    reward, event_run = run(b_program, Q, i)
    if event_run not in event_runs:
        event_runs.append(event_run)
print(event_runs)
print(Q_test(b_program, Q, 1000, 2))

