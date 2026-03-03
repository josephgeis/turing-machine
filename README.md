# turing-machine

A Python implementation of a Turing machine computing model with infinite tape.

## Usage

### Using a machine_def file

The easiest way is probably using the machine_def format defined below:

- `STATE [name]`: defines a new state
  - `name`: name of the state
- `RULE [read] := [write] [shift] [next]`: defines a rule on the state
  - *Note:* `RULE` directives must follow a `STATE` directive; 
    a file is invalid if there is a `RULE` directive with no `STATE` directive above it. 
  - `read`: character to read off the tape
  - `write`: character to write onto the tape
  - `shift`: `L` or `R` to shift left or right on the tape
  - `next`: state to move to
- `ACCEPT [name]`: sets the accept state
  - `name`: name of accept state
- `REJECT [name]`: sets the reject state
  - `name`: name of reject state
- `START [name]`: sets the starting state
  - `name`: name of the start state
- `LOAD [string]`: loads the give string onto the tape
  - `string`: string to load
- `PASS`: does nothing; a blank line is the same as a `PASS` directive

`\0` can be used to represent a blank value. Spaces are not a valid character.

**To run the machine:** `python -m turing [file]` where `[file]` is the path of your machine_def file.

### Programmatically

An API is provided to create a machine and define states.

1. Import the `TuringMachine` and `Tape` classes from `turing`. Optionally, you can import the `State` class.
2. Create a new machine by defining an instance of `TuringMachine`.
3. States can be created by calling the `new_state` method on your machine (which will automatically name them `q0`, `q1`, ...).
4. States can be manually created by defining an instance of the `State` method, then adding it to the machine instance
    by calling the `add_state` method and passing the state instance as an argument.
5. Rules can be added by calling the `add_rule` method on a state instance and passing the following arguments:
   1. `read`: character to read off the tape
   2. `write`: character to write onto the tape
   3. `direction`: `Tape.LEFT` or `Tape.RIGHT` to shift left or right on the tape
   4. `next_state`: state to move to
6. Use the `set_accept`, `set_reject`, and `set_state` methods to set the accept, reject, and start states.
7. Use the `load_tape` method to load a string onto the tape. The `NUL` character represents a blank.
8. Call the `run` method on the machine to run.

Reference the example in `palindrome.py`.