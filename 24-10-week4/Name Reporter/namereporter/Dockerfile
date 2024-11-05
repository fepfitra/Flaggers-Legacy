FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

WORKDIR /app

RUN pip3 install Flask Flask-Limiter

COPY . /app

RUN chmod -R 555 /app

USER 1000:1000

EXPOSE 14002

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=14002"]