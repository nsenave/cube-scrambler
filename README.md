# Cube scrambling script

A script that generates a random sequence of moves to scramble a Rubik's cube, written in Python.

```sh
py ./cube_scrambler.py
```
Details:

- The script ensures that the sequence doesn't contain consecutive moves that cancel each other out.
- However, three identical quarter turns or full turns may occur in the generated sequence.
