FROM python:3.7

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY . /app/
RUN pip install -r requirements.txt
