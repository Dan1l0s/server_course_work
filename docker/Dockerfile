FROM python:3.10
WORKDIR /app

COPY clinic ./clinic
COPY ./docker/requirements.txt .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv .venv
RUN . .venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt