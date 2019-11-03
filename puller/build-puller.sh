#!/bin/sh

echo Building yfirmy/eternity2-puller-sample:latest

docker build --build-arg binary=E2ControlSample-dfs --build-arg configuration=control-sample.ini -t yfirmy/eternity2-puller-sample:latest .

echo Building yfirmy/eternity2-puller-clue1:latest

docker build --build-arg binary=E2Clue1-dfs --build-arg configuration=clue1.ini -t yfirmy/eternity2-puller-clue1:latest .

echo Building yfirmy/eternity2-puller-challenge:latest

docker build --build-arg binary=E2Puzzle-dfs --build-arg configuration=puzzle.ini -t yfirmy/eternity2-puller-challenge:latest .

#
# To run these docker images, don't forget options to attach stdin/stdout :

# docker run -a stdin -a stdout -it --rm yfirmy/eternity2-puller-clue1:latest