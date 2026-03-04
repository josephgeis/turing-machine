from enum import Enum
from typing import Dict, List


class Tape:
    class Direction(Enum):
        LEFT = 'L'
        RIGHT = 'R'

    LEFT = Direction.LEFT
    RIGHT = Direction.RIGHT

    def __init__(self, init=None):
        self._left = []
        self._right = []
        if init:
            self.load_tape(init)

    @property
    def head(self):
        if len(self._right) == 0:
            return None
        else:
            return self._right[0]

    def _trim(self):
        while self._left[:1] == [None]:
            self._left.pop(0)
        while self._right[-1:] == [None]:
            self._right.pop(-1)

    def backward(self):
        if len(self._right) == 0 and len(self._left) == 0:
            pass
        elif len(self._right) > 0 and len(self._left) == 0:
            self._right.insert(0, None)
        else:
            self._right.insert(0, self._left.pop(-1))
        self._trim()

    def forward(self):
        if len(self._right) == 0 and len(self._left) == 0:
            pass
        elif len(self._right) == 0 and len(self._left) > 0:
            self._left.append(None)
        else:
            self._left.append(self._right.pop(0))
        self._trim()

    def write(self, value):
        if len(self._right) == 0:
            if value is not None:
                self._right.insert(0, value)
        elif len(self._right) == 1 and value is None:
            self._right.pop(0)
        else:
            self._right[0] = value

    def clear(self):
        self.write(None)

    @property
    def right(self):
        return self._right[:]

    @property
    def left(self):
        return self._left[:]

    def load_tape(self, string):
        esc_null = lambda c: None if c == "\x00" else c
        chars = [esc_null(c) for c in string]
        self._right = chars + self._right[len(chars):]
        self._trim()


class State:
    def __init__(self, name):
        self.rules = []
        self.name = name

    def add_rule(self, read, write, direction, next_state):
        self.rules.append((read, write, direction, next_state))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}, {len(self.rules)}>"

    def cycle(self, head):
        for read, write, direction, next_state in self.rules:
            if head == read:
                return write, direction, next_state
        return None


class TuringMachine:
    def __init__(self, initial_tape=None):
        self._tape = Tape(initial_tape)
        self.states = set()
        self.state = None
        self.accept_state = None
        self.reject_state = None

    def add_state(self, state):
        self.states.add(state)

    def new_state(self):
        state = State(f"q{len(self.states)}")
        self.states.add(state)
        return state

    def set_state(self, state):
        if state and state not in self.states:
            raise ValueError("State not added to machine")

        self.state = state

    def set_accept(self, state):
        if state and state not in self.states:
            raise ValueError("State not added to machine")

        self.accept_state = state

    def set_reject(self, state):
        if state and state not in self.states:
            raise ValueError("State not added to machine")

        self.reject_state = state

    @property
    def accept(self):
        return self.state is self.accept_state

    @property
    def reject(self):
        return self.state is self.reject_state

    def load_tape(self, tape):
        self.tape.load_tape(tape)

    def cycle(self):
        if self.state is None:
            raise RuntimeError("Current state is None.")

        res = self.state.cycle(self.tape.head)

        if res:
            write, direction, next_state = res
        else:
            raise RuntimeError("Machine crashed.")

        self.tape.write(write)
        match direction:
            case Tape.LEFT:
                self.tape.backward()
            case Tape.RIGHT:
                self.tape.forward()
        if next_state not in self.states:
            raise RuntimeError("State not added to machine.")
        self.state = next_state

    def run(self):
        while not (self.accept or self.reject):
            self.cycle()

    def __str__(self):
        parts = [f"state='{self.state}'"]
        if self.accept:
            parts.append("ACCEPT")
        if self.reject:
            parts.append("REJECT")
        return " ".join(parts)

    @property
    def tape(self):
        return self._tape


class MachineBuilder:
    def __init__(self):
        self.unresolved_states: dict = dict()
        self.current_state = None
        self.accept_state = None
        self.reject_state = None
        self.start_state = None
        self.init_tape = None

    def read_line(self, line: str):
        command, *args = line.split() or ["PASS"]
        match command:
            case "STATE":
                if len(args) != 1:
                    raise RuntimeError(f"Invalid state definition: '{line.rstrip('\n')}'")
                self.current_state = self.unresolved_states.setdefault(args[0], [])
            case "RULE":
                if self.current_state is None:
                    raise RuntimeError("No state defined.")
                elif len(args) != 5:
                    raise RuntimeError(f"Invalid rule definition: '{line.rstrip('\n')}'")
                read, caret, write, direction, destination = args
                if caret != ":=" or (direction != "L" and direction != "R"):
                    raise RuntimeError(f"Invalid rule definition: '{line.rstrip('\n')}'")
                self.current_state.append((read, write, Tape.Direction(direction), destination))
            case "ACCEPT":
                if len(args) != 1:
                    raise RuntimeError(f"Invalid accept definition: '{line.rstrip('\n')}'")
                self.accept_state = args[0]
            case "REJECT":
                if len(args) != 1:
                    raise RuntimeError(f"Invalid reject definition: '{line.rstrip('\n')}'")
                self.reject_state = args[0]
            case "START":
                if len(args) != 1:
                    raise RuntimeError(f"Invalid start definition: '{line.rstrip('\n')}'")
                self.start_state = args[0]
            case "LOAD":
                if len(args) != 1:
                    raise RuntimeError(f"Invalid load definition: '{line.rstrip('\n')}'")
                self.init_tape = args[0].replace(r"\0", "\x00")
            case "PASS":
                pass
            case _:
                raise RuntimeError(f"Invalid statement: '{line.rstrip('\n')}'")


    def build(self):
        esc = lambda x: None if x == r"\0" else x
        machine = TuringMachine()
        states: Dict[str, State] = {}
        for state in self.unresolved_states.keys():
            states[state] = State(state)
            machine.add_state(states[state])

        for state, rules in self.unresolved_states.items():
            for read, write, direction, next_state in rules:
                if next_state not in states:
                    raise RuntimeError(f"Unresolved state '{next_state}' in rule '{read} := {write} {direction} {next_state}' on '{state}'")
                states[state].add_rule(esc(read), esc(write), direction, states[next_state])

        machine.set_state(self.start_state and states[self.start_state])
        machine.set_accept(self.accept_state and states[self.accept_state])
        machine.set_reject(self.reject_state and states[self.reject_state])
        if self.init_tape:
            machine.load_tape(self.init_tape)

        return machine


if __name__ == '__main__':
    import sys
    assert len(sys.argv) > 1
    builder = MachineBuilder()
    with open(sys.argv[1]) as fd:
        for line in fd:
            builder.read_line(line)

    machine = builder.build()
    machine.run()
    print(machine)
    print('right:', ''.join([r'\0' if x is None else x for x in machine.tape.right]))
