## Notes

How many moves to scramble a Rubik's cube?
- https://arxiv.org/html/2410.20630v1
- https://math.stackexchange.com/questions/816055/minimum-number-of-random-moves-needed-to-uniformly-scramble-a-rubiks-cube

https://shuffle.akselipalen.com/

## Ideas

Backend program that simulates Rubik's cube state. Move => updates state.

Frontend program to vizualize it.

Use cases:
- Text input => generated sequence in format like "F, U, R, U', R', F'"
- Button "Apply" => applies the moves on screen
- Sliders to vary move speed, time between moves

Smart use case:
- What should be my next move? / Hint, based on the official Rubik's solving guide.

Note:
- 20 = "God's number". Any state can be reached from any state in 20 quarter or half moves.
- It's 26 if half moves are counted as two quarter moves.

> The term "devil's algorithm" describes a move sequence which, during execution, 
> will go through all possible 43,252,003,274,489,856,000 states of the 3x3x3 Rubik's 
> cube without visiting any state more than once. 
> That is, every possible state will be equally likely when executing the sequence.

Questions:
Are there resources that gives a fast-solving sequence from any cube state?
