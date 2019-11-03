#!/bin/sh

echo Building yfirmy/eternity2-backend-sample:latest

docker build --build-arg binary=E2ControlSample-bfs --build-arg configuration=control-sample.ini --build-arg exposed_port=5060 -t yfirmy/eternity2-backend-sample:latest .

echo Building yfirmy/eternity2-backend-clue1:latest

docker build --build-arg binary=E2Clue1-bfs --build-arg configuration=clue1.ini --build-arg exposed_port=5050 -t yfirmy/eternity2-backend-clue1:latest .

echo Building yfirmy/eternity2-backend-challenge:latest

docker build --build-arg binary=E2Puzzle-bfs --build-arg configuration=puzzle.ini --build-arg exposed_port=5000 -t yfirmy/eternity2-backend-challenge:latest .

#
# To run these docker images :

# docker run --publish 5050:5050 --detach --name backend-clue1 --rm yfirmy/eternity2-backend-clue1:latest
# docker container rm --force backend-clue1

# docker run --publish 5060:5060 --detach --name backend-sample --rm yfirmy/eternity2-backend-sample:latest