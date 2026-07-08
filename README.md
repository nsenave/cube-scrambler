# Cube scrambling script

A script that generates a random sequence of moves to scramble a Rubik's cube, written in Python.

```sh
py ./cube_scrambler.py
```
Details:

- The script ensures that the sequence doesn't contain
  - consecutive moves that cancel each other out,
  - three identical quarter turns,
  - full turns.
