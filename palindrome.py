from turing import TuringMachine, Tape

def run_palindrome_machine():
    machine = TuringMachine()

    q0 = machine.new_state()
    q1 = machine.new_state()
    q2 = machine.new_state()
    q3 = machine.new_state()
    q4 = machine.new_state()
    q5 = machine.new_state()
    q6 = machine.new_state()
    q7 = machine.new_state()
    q8 = machine.new_state()

    q0.add_rule('a', '*', Tape.RIGHT, q1)
    q0.add_rule('b', '#', Tape.RIGHT, q5)
    q0.add_rule(None, None, Tape.LEFT, q7)

    q1.add_rule('a', 'a', Tape.RIGHT, q1)
    q1.add_rule('b', 'b', Tape.RIGHT, q1)
    q1.add_rule(None, None, Tape.RIGHT, q2)

    q2.add_rule('a', 'a', Tape.RIGHT, q2)
    q2.add_rule('b', 'b', Tape.RIGHT, q2)
    q2.add_rule(None, 'a', Tape.LEFT, q3)

    q3.add_rule('a', 'a', Tape.LEFT, q3)
    q3.add_rule('b', 'b', Tape.LEFT, q3)
    q3.add_rule(None, None, Tape.LEFT, q4)

    q4.add_rule('a', 'a', Tape.LEFT, q4)
    q4.add_rule('b', 'b', Tape.LEFT, q4)
    q4.add_rule('*', 'a', Tape.RIGHT, q0)
    q4.add_rule('#', 'b', Tape.RIGHT, q0)

    q5.add_rule('a', 'a', Tape.RIGHT, q5)
    q5.add_rule('b', 'b', Tape.RIGHT, q5)
    q5.add_rule(None, None, Tape.RIGHT, q6)

    q6.add_rule('a', 'a', Tape.RIGHT, q6)
    q6.add_rule('b', 'b', Tape.RIGHT, q6)
    q6.add_rule(None, 'b', Tape.LEFT, q3)

    q7.add_rule('a', 'a', Tape.LEFT, q7)
    q7.add_rule('b', 'b', Tape.LEFT, q7)
    q7.add_rule(None, None, Tape.RIGHT, q8)

    machine.set_accept(q8)
    machine.set_state(q0)
    machine.load_tape("abbbaa")

    machine.run()
    print(machine)
    print('right:', ''.join([r'\0' if x is None else x for x in machine.tape.right]))

if __name__ == '__main__':
    run_palindrome_machine()