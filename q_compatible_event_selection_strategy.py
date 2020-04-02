from bppy import *


class QCompatibleEventSelectionStrategy(SimpleEventSelectionStrategy):

    def __init__(self, Q):
        SimpleEventSelectionStrategy.__init__(self)
        self.Q = Q

    def selectable_events(self, statements):
        # TODO: change to be Q compatible
        possible_events = SimpleEventSelectionStrategy.selectable_events(self, statements)
        if possible_events.__len__() > 1:
            possible_events.discard(BEvent("I"))
        return possible_events

