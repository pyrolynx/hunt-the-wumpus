FROM python:3.8

WORKDIR /opt
ENV PYTHONPATH=/opt

COPY . .

ENTRYPOINT ["python3", "wumpus"]
