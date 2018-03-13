FROM ubuntu:latest
MAINTAINER Oles Tourko

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
# The application contents will be mounted on docker run.
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# For SASS
RUN apt-get install -y ruby ruby-dev
RUN gem install sass

# For Yarn
RUN apt-get update && apt-get install -y curl python-software-properties
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install yarn -y

EXPOSE 5000

# FLASK_APP is only used by Flask's internal server, not Gunicorn.
ENV FLASK_APP=/app/src/application.py
ENV CONFIG_FILEPATH=/app/config.py
# Used to get a common base for import statements
ENV PYTHONPATH=/app/

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]