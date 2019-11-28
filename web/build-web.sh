#!/bin/sh

VERSION=$1

IMAGE_SAMPLE=yfirmy/eternity2-backend-sample
IMAGE_CLUE1=yfirmy/eternity2-backend-clue1
IMAGE_CHALLENGE=eternity2-backend-challenge

echo Building $IMAGE_SAMPLE:$VERSION

docker build --build-arg binary=E2ControlSample-bfs --build-arg configuration=control-sample.ini --build-arg exposed_port=5060 -t $IMAGE_SAMPLE:latest -t $IMAGE_SAMPLE:$VERSION .

echo Building $IMAGE_CLUE1:$VERSION

docker build --build-arg binary=E2Clue1-bfs --build-arg configuration=clue1.ini --build-arg exposed_port=5050 -t $IMAGE_CLUE1:latest -t $IMAGE_CLUE1:$VERSION .

echo Building $IMAGE_CHALLENGE:$VERSION

docker build --build-arg binary=E2Puzzle-bfs --build-arg configuration=puzzle.ini --build-arg exposed_port=5000 -t $IMAGE_CHALLENGE:latest -t $IMAGE_CHALLENGE:$VERSION .

#
# To run these docker images :

# docker run --publish 5050:5050 --detach --name backend-clue1 --rm yfirmy/eternity2-backend-clue1:latest
# docker container rm --force backend-clue1

# docker run --publish 5060:5060 --detach --name backend-sample --rm yfirmy/eternity2-backend-sample:latest