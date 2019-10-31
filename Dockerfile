ARG binary=E2Puzzle-dfs
ARG configuration=puzzle.ini

# --- builder image ---

FROM gcc:9.2 AS builder
ARG binary
COPY ./src /usr/src/eternity2-solver/src/
COPY ./makefile /usr/src/eternity2-solver/
WORKDIR /usr/src/eternity2-solver
RUN make

# --- test image

FROM python:alpine3.10 as tester
ARG binary

COPY --from=builder "/usr/src/eternity2-solver/bin/*" /app/eternity2-solver/bin/
COPY ./test/E2NonRegTest-DFS.py /app/eternity2-solver/test/
WORKDIR /app/eternity2-solver/
RUN python ./test/E2NonRegTest-DFS.py

# --- runtime image ---

FROM python:alpine3.10
ARG binary
ARG configuration

LABEL maintainer="Yohan FIRMY (yfirmy)"

COPY --from=builder "/usr/src/eternity2-solver/bin/$binary" /app/eternity2-solver/bin/
COPY ./puller/eternity2-job-puller.py /app/eternity2-solver/puller/
COPY ./puller/requirements.txt /app/eternity2-solver/puller/
COPY "./puller/conf/$configuration" /app/eternity2-solver/puller/configuration.ini
WORKDIR /app/eternity2-solver/

RUN pip install -r ./puller/requirements.txt
RUN rm -f ./puller/requirements.txt

CMD [ "python", "./puller/eternity2-job-puller.py", "--conf", "puller/configuration.ini" ]