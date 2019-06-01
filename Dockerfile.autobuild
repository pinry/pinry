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
FROM python:3.6-stretch

RUN groupadd -g 2300 tmpgroup \
 && usermod -g tmpgroup www-data \
 && groupdel www-data \
 && groupadd -g 1000 www-data \
 && usermod -g www-data www-data \
 && usermod -u 1000 www-data \
 && groupdel tmpgroup \
#
 && mkdir -p /srv/www/pinry/logs \
#
 && mkdir /data \
 && chown -R www-data:www-data /data \
#
 && mkdir -p /var/log/gunicorn \
 && apt-get update \
    && apt-get -y install nginx nginx-extras pwgen \
    && rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install pipenv gunicorn mysqlclient psycopg2 cx-Oracle

COPY Pipfile* /srv/www/pinry/

RUN cd /srv/www/pinry \
 && pipenv install --three --system --clear

COPY . /srv/www/pinry/

# Fix permissions
RUN chown -R www-data:www-data /srv/www \
 && cd /srv/www/pinry \
 && python manage.py collectstatic --noinput


# Load in all of our config files.
ADD docker/nginx/nginx.conf /etc/nginx/nginx.conf
ADD docker/nginx/sites-enabled/default /etc/nginx/sites-enabled/default
ADD docker/scripts/* /scripts/

# 80 is for nginx web, /data contains static files and database /start runs it.
EXPOSE 80
VOLUME ["/data"]
CMD    ["/scripts/start.sh"]
