FROM python:3.11

WORKDIR /running

COPY ./requirements.txt /running/

RUN pip install -r /running/requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1