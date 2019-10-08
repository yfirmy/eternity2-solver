ARG target=E2Puzzle-dfs

# --- builder image ---

FROM gcc:9.2 AS builder
ARG target
COPY ./src /usr/src/eternity2-solver/src/
COPY ./makefile /usr/src/eternity2-solver/
WORKDIR /usr/src/eternity2-solver
RUN make ${target}

# --- runtime image ---

FROM alpine:3.10.2
ARG target
COPY --from=builder "/usr/src/eternity2-solver/bin/$target" /app/eternity2-solver/bin/
WORKDIR /app/eternity2-solver/bin
ENV app_name ${target}
CMD ./${app_name}