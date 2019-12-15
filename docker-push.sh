#!/bin/sh

SOLVER_VERSION=1.7.2

IMAGE_SOLVER_BINARIES=yfirmy/eternity2-solver-binaries

IMAGE_PULLER_SAMPLE=yfirmy/eternity2-puller-sample
IMAGE_PULLER_CLUE1=yfirmy/eternity2-puller-clue1
IMAGE_PULLER_CHALLENGE=yfirmy/eternity2-puller-challenge

IMAGE_BACKEND_SAMPLE=yfirmy/eternity2-backend-sample
IMAGE_BACKEND_CLUE1=yfirmy/eternity2-puller-clue1
IMAGE_BACKEND_CHALLENGE=yfirmy/eternity2-puller-challenge

IMAGES_PULLER=($IMAGE_PULLER_SAMPLE $IMAGE_PULLER_CLUE1 $IMAGE_PULLER_CHALLENGE)
IMAGES_BACKEND=($IMAGE_BACKEND_SAMPLE $IMAGE_BACKEND_CLUE1 $IMAGE_BACKEND_CHALLENGE)

echo Pushing Puller Images
for image in ${IMAGES_PULLER[*]}
do
    docker push $image:$SOLVER_VERSION
    docker push $image:latest
done

echo Pushing Backend Images
for image in ${IMAGES_BACKEND[*]}
do
    docker push $image:$SOLVER_VERSION
    docker push $image:latest
done