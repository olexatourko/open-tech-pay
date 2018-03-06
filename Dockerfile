FROM ubuntu:latest
MAINTAINER Oles Tourko

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
# The application contents will be mounted on docker run.
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=/app/src/application.py
ENV CONFIG_FILEPATH=/app/config.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]