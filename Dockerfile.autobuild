# -----------------------------------------------------------------------------
# docker-pinry
#
# Builds a basic docker image that can run Pinry (http://getpinry.com) and serve
# all of it's assets, there are more optimal ways to do this but this is the
# most friendly and has everything contained in a single instance.
#
# Authors: Isaac Bythewood
# Updated: Mar 29th, 2016
# Require: Docker (http://www.docker.io/)
# -----------------------------------------------------------------------------

# Base system is the LTS version of Ubuntu.
FROM python:3.7-stretch

RUN groupadd -g 2300 tmpgroup \
 && usermod -g tmpgroup www-data \
 && groupdel www-data \
 && groupadd -g 1000 www-data \
 && usermod -g www-data www-data \
 && usermod -u 1000 www-data \
 && groupdel tmpgroup

RUN mkdir /data
RUN chown -R www-data:www-data /data

RUN apt-get update \
    && apt-get -y install nginx nginx-extras pwgen \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoclean

# required for other database options
RUN pip --no-cache-dir install pipenv gunicorn mysqlclient psycopg2 cx-Oracle

# COPY and start installation
COPY . /pinry

RUN cd /pinry \
 && pipenv install --three --system --clear

# config nodejs
RUN curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o n || exit
RUN bash n 10
RUN npm -g install yarn

# build frontend
RUN cd /pinry/pinry-spa/ && yarn install && yarn build

# Load in all of our config files.
ADD docker/nginx/nginx.conf /etc/nginx/nginx.conf
ADD docker/nginx/sites-enabled/default /etc/nginx/sites-enabled/default

# 80 is for nginx web, /data contains static files and database /start runs it.
EXPOSE 80
VOLUME ["/data"]
CMD    ["/pinry/docker/scripts/start.sh"]
