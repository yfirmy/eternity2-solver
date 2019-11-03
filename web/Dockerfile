ARG binary=E2Puzzle-bfs
ARG configuration=puzzle.ini
ARG exposed_port=5000

# --- runtime image ---

FROM python:3.5.8-alpine3.10
ARG binary
ARG configuration
ARG exposed_port

LABEL maintainer="Yohan FIRMY (yfirmy)"

COPY ./bin/${binary} /app/eternity2-solver/bin/
COPY ./script/eternity2-solver-http.py /app/eternity2-solver/web/
COPY ./requirements.txt /app/eternity2-solver/web/
COPY ./conf/${configuration} /app/eternity2-solver/web/configuration.ini
WORKDIR /app/eternity2-solver/

RUN pip install -r ./web/requirements.txt
RUN rm -f ./web/requirements.txt

EXPOSE ${exposed_port}

CMD [ "python", "./web/eternity2-solver-http.py", "--conf", "web/configuration.ini" ]