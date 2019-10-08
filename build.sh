#!/bin/sh

echo Building yfirmy/eternity2-solver-sample:latest

docker build --build-arg target=E2ControlSample-dfs -t yfirmy/eternity2-solver-sample:latest .

echo Building yfirmy/eternity2-solver-clue1:latest

docker build --build-arg target=E2Clue1-dfs -t yfirmy/eternity2-solver-clue1:latest .

echo Building yfirmy/eternity2-solver-challenge:latest

docker build --build-arg target=E2Puzzle-dfs -t yfirmy/eternity2-solver-challenge:latest .

#
# To run these docker images, don't forget options to attach stdin/stdout :

# docker run -a stdin -a stdout -it --rm yfirmy/eternity2-solver-clue1