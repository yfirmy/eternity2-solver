#!/bin/sh

VERSION=$1

IMAGE_SAMPLE=yfirmy/eternity2-puller-sample
IMAGE_CLUE1=yfirmy/eternity2-puller-clue1
IMAGE_CHALLENGE=yfirmy/eternity2-puller-challenge


echo Building $IMAGE_SAMPLE:$VERSION

docker build --build-arg binary=E2ControlSample-dfs --build-arg configuration=control-sample.ini -t $IMAGE_SAMPLE:latest -t $IMAGE_SAMPLE:$VERSION .

echo Building $IMAGE_CLUE1:$VERSION

docker build --build-arg binary=E2Clue1-dfs --build-arg configuration=clue1.ini -t $IMAGE_CLUE1:latest -t $IMAGE_CLUE1:$VERSION .

echo Building $IMAGE_CHALLENGE:$VERSION

docker build --build-arg binary=E2Puzzle-dfs --build-arg configuration=puzzle.ini -t $IMAGE_CHALLENGE:latest -t $IMAGE_CHALLENGE:$VERSION .
