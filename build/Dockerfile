# pull official base image
FROM python:3.7.7-buster

# set work directory
RUN mkdir -p /home/app
WORKDIR /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED 0

# Add aliases
RUN echo "alias manage='python manage.py'" >> ~/.bashrc

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean


# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

## copy project
# copy src
COPY src ./src

# copy bin
COPY bin ./bin

# copy build bin
COPY build/bin/entrypoint.sh ./build/bin/entrypoint.sh

# copy migrations
COPY migrations ./migrations

# copy seeds
COPY seeds ./seeds

# copy tests
COPY tests ./tests

# create logs directory
RUN mkdir logs

# copy manage.py
COPY manage.py .

# setup
COPY setup.py .

## run entrypoint.sh
ENTRYPOINT ["sh", "./build/bin/entrypoint.sh"]