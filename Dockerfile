FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app

# config nodejs
RUN curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o n
RUN bash n 18
RUN npm -g install pnpm

WORKDIR /app
RUN pip install poetry
RUN poetry install
RUN rm -fr /app/*
