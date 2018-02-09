FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --three --system

RUN python3 manage.py collectstatic --noinput

VOLUME /app/static/media

