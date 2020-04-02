from bppy import *

@b_thread
def a():
    yield {request: BEvent("a"), block: AllExcept([BEvent("a")])}
@b_thread
def b():
    yield {request: BEvent("b")}
    yield {request: BEvent("b")}
    yield {request: BEvent("b")}
    yield {request: BEvent("b")}


bprogram = BProgram(bthreads=[a(), b()],
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=PrintBProgramRunnerListener())
bprogram.run()
