FROM ubuntu:latest
MAINTAINER Oles Tourko

WORKDIR /app

RUN apt-get update -y

# ----------------------------
# Install pyenv. Pyenv will be used to install and manage verions of Python.
# See: https://github.com/pyenv/pyenv-installer
# See: https://realpython.com/intro-to-pyenv/
# ----------------------------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
RUN curl https://pyenv.run | bash
# These won't be used by the Dockerfile build, but it might come in handy later.
RUN echo '\n# Pyenv setup' >> ~/.bashrc
RUN echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
# This is used by the Dockerfile build.
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
# Finally, install Python via Pyenv.
RUN pyenv install 3.8.1

# ----------------------------
# Install pipenv and dependencies with it.
# ----------------------------
RUN pyenv local 3.8.1
COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN pip install pipenv
# Required for the mysqlclient package.
RUN apt-get install -y libmysqlclient-dev
# Seems to be the best of grabbing dependencies on a Docker container without unecessary virtual enviornments.
# Possibly find a way to convert Pipfile.lock to a requirements.txt file in the future and just use pip directly.
# See: https://pipenv-searchable.readthedocs.io/advanced.html#generating-a-requirements-txt
RUN pipenv install --system --deploy --ignore-pipfile
# Since pip dependencies will get installed here
# ENV PATH $PATH:/root/.pyenv/versions/3.8.1/lib/python3.8/site-packages
ENV PATH $PATH:/root/.pyenv/versions/3.8.1/bin

# ----------------------------
# Frontend stuff
# ----------------------------
# For SASS
RUN apt-get update
RUN apt-get install -y ruby ruby-dev
RUN gem install sass
# For Yarn
RUN apt-get update && apt-get install -y curl software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install yarn -y

# ----------------------------
# Get the ip and route commands for network inspection, which could be useful
# ----------------------------
# https://alphacoder.xyz/connect-to-host-database-from-docker-container/
RUN apt-get -y install iproute2 net-tools

# ----------------------------
# Set locale (required if you ever need to use pudb
# ----------------------------
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
RUN echo "LANG=en_US.UTF-8" > /etc/default/local

# ----------------------------
# Final application setup
# ----------------------------
# FLASK_APP is only used by Flask's internal server, not Gunicorn.
ENV FLASK_APP=/app/src/application.py
ENV CONFIG_FILEPATH=/app/config.py
# Used to get a common base for import statements
ENV PYTHONPATH=/app/

# For the main application
EXPOSE 5000
# For a 2nd debug instance if needed
EXPOSE 5001
CMD ./container_start.sh