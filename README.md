#  ** Eternity II Solver **

## Description

A simple backtracker solver, to solve the ["Eternity II" puzzle challenge](https://en.wikipedia.org/wiki/Eternity_II_puzzle).

This is a mono-thread tree exploration, through the Eternity II solutions space.

## Design goals

This solver is designed to be very simple and portable, to be executed in parrallel, and orchestrated externally.

The goal will be to achieve a massive parallelization of this solver on a cloud via containers scalability.

## History

 - 2009 : first versions "E2Breaker" : Multi-thread Windows Client/Server application (up to 14 clients in parallel)
 - 2018 : rebirth of the project: refactoring to a simple Monothread Linux application (no more threading, no more winsock) 
 - 2019 : improvements for publishing on GitHub : added non-regression tests, added "Clue 1" solving, added GNU license

## Build the project

Please use the Makefile .
No dependency.

## Input and Outputs

This solver is interactive : it will read its new job, on the standard input, and will read again once finished.

 - **Input** via Standard Input only
 - **Output** via Standard Output only

This solver will read an initial state, from which to start exploration, and will write the results (found solutions) to the output.

The initial state, can be an empty puzzle board, for a full tree exploration, or a partially filled board, for partial branches exploration.

## Board description format for Input and Output

Beginning character `$`
For each position (from left to rigth, from top to bottom):
 - a pair of `piece number` (or `.` for empty) + orientation (`W`, `N`, `E`, `S`)
 - a separator character `:` after each piece
Ending character `;`

Examples for a small 4x4 puzzle board:
 - Empty board: 
 ```
 $.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;
 ```
 - Only 2 placed pieces on the board: 
 ```
 $2W:24E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;
 ```

