
# --- builder image ---

FROM gcc:9.2 AS builder
COPY ./src /usr/src/eternity2-solver/src/
COPY ./makefile /usr/src/eternity2-solver/
WORKDIR /usr/src/eternity2-solver
RUN make

# --- test image

FROM python:3.8.1-alpine3.10 as tester
COPY --from=builder "/usr/src/eternity2-solver/bin/*" /app/eternity2-solver/bin/
COPY ./test/E2NonRegTest-DFS.py /app/eternity2-solver/test/
COPY ./test/E2NonRegTest-BFS.py /app/eternity2-solver/test/
WORKDIR /app/eternity2-solver/
RUN python ./test/E2NonRegTest-DFS.py && \
    python ./test/E2NonRegTest-BFS.py

# --- runtime image

FROM alpine:3.10.2 as runtime

COPY --from=builder "/usr/src/eternity2-solver/bin/*" /app/eternity2-solver/bin/
WORKDIR /app/eternity2-solver/