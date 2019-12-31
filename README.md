#  ** Eternity II Solver **

## Description

A simple backtracker solver, to solve the ["Eternity II" puzzle challenge](https://en.wikipedia.org/wiki/Eternity_II_puzzle).

This is a mono-thread tree exploration, through the Eternity II solutions space, written in C++.

It is containerized in Docker Images to achieve massive parallelism in a cluster.

The solver core application is embedded in 2 kinds of Docker Images.

The two kinds of Docker Images are :
 - **eternity2-puller** : a daemon script, pulling Jobs from the ["Eternity II Server"](https://github.com/yfirmy/eternity2-server) and delegating its solving to the embedded solver core process (in a ["Depth-First Search"](https://en.wikipedia.org/wiki/Depth-first_search) mode).
 - **eternity2-backend** : a REST API server, wrapping the solver core process (in a ["Breadth-First Search"](https://en.wikipedia.org/wiki/Breadth-first_search) mode), and intended to be used server-side by the ["Eternity II Server"](https://github.com/yfirmy/eternity2-server) in order to create new branches in the search tree. 

## Architecture of the Solver Cluster

A Eternity II cluster is composed of:
 - One ["Eternity II Server"](https://github.com/yfirmy/eternity2-server)
 - Multiple ["Eternity II Solvers"](https://github.com/yfirmy/eternity2-solver) being clients of the server.

The ["Eternity II Server"](https://github.com/yfirmy/eternity2-server) is dedicated:
 - to divide the search space, in branches, 
 - to provide Jobs to solve to multiple solvers (clients will request new jobs).
 - to store jobs results returned by the different solvers

The ["Eternity II Solver"](https://github.com/yfirmy/eternity2-solver) is dedicated :
 - to ask the server for new Jobs to solve
 - to actually solve the given Job
 - to give results (empty or not) for the given job
 - to ask for another job (and so on)

## History/Milestones

 - 2009 : first versions called "E2Breaker" : Multi-thread Windows Client/Server application (up to 14 solvers/clients in parallel)
 - 2018 : rebirth of the project: refactoring to a simple Monothread Linux application (no more threading, no more winsock) 
 - 2019/02 : publishing the core solver on GitHub : added non-regression tests, added "Clue 1" solving, added GNU license
 - 2019/08 : added the Job Puller script (solving on the client-side), and a REST API script (branching on the server-side).
 - 2019/10 : containerize the "Puller Script" and the "REST API" in 2 different Docker images (with a solver embedded)
 - 2019/12 : running 198 solvers in parallel (as containers) in a Kubernetes Cluster (Amazon AWS EKS) (spread across 100 virtual machines)

## Build the project

Please use the build.sh script (multistage Docker build)

## The solver core application

### Input and Outputs

This solver is interactive : it will read its new job, on the standard input, and will read again once finished.

 - **Input** via Standard Input only
 - **Output** via Standard Output only

This solver will read an initial state, from which to start exploration, and will write the results (found solutions) to the output.

The initial state, can be an empty puzzle board, for a full tree exploration, or a partially filled board, for partial branches exploration.

### Board description format for Input and Output

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

## The Solver as a Server-side Backend

### REST API for the Breadth-First Search

```

 | GET | PUT | DELETE | POST | Path                                    | Description                             |
 | :-- | :-- | :----- | :--- | :-------------------------------------- | :-------------------------------------- |
 | X   |     |        |      | /api/eternity2-solver/v1/sub-jobs/_job_ | Returns a list of sub-jobs (JSON format). Example: `[{"job": "$24E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"}, {"job": "$20N:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"}]` |

The _job_ parameter being expected in the "Board Description Format"
