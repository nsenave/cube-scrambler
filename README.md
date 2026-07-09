# Cube scrambling script

A script that generates a random sequence of moves (using Singmaster notation) to scramble a Rubik's cube.

Written in Python.

```sh
py ./cube_scrambler.py
```

Details:

- The script ensures that the sequence doesn't contain
  - consecutive moves that cancel each other out,
  - three identical quarter turns,
  - full turns.

For more, use:

```sh
py ./cube_scrambler.py --help
```

to see more options and their documentation.
