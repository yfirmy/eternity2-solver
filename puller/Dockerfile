ARG binary=E2Puzzle-dfs
ARG configuration=puzzle.ini

# --- runtime image ---

FROM python:3.8.1-alpine3.10
ARG binary
ARG configuration

LABEL maintainer="Yohan FIRMY (yfirmy)"

COPY ./bin/${binary} /app/eternity2-solver/bin/
COPY ./script/eternity2-job-puller.py /app/eternity2-solver/puller/
COPY ./script/eternity2model.py /app/eternity2-solver/puller/
COPY ./script/eternity2server.py /app/eternity2-solver/puller/
COPY ./script/eternity2solver.py /app/eternity2-solver/puller/
COPY ./script/eternity2utils.py /app/eternity2-solver/puller/
COPY ./requirements.txt /app/eternity2-solver/puller/
COPY ./conf/${configuration} /app/eternity2-solver/puller/configuration.ini
WORKDIR /app/eternity2-solver/

RUN pip install -r ./puller/requirements.txt
RUN rm -f ./puller/requirements.txt

CMD [ "python", "./puller/eternity2-job-puller.py", "--conf", "puller/configuration.ini" ]