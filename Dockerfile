FROM python:3.11.2-slim-bullseye

# set work directory
WORKDIR  /var/app/

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y wget
RUN apt-get install -y python3-dev gcc libc-dev libffi-dev
RUN apt-get -y install libpq-dev gcc

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# copy project
COPY --chown=www-data:www-data . /var/app/
RUN chown -R www-data:www-data /var/app/

EXPOSE 8000


