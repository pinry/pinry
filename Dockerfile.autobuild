# -----------------------------------------------------------------------------
# docker-pinry
#
# Builds a basic docker image that can run Pinry (http://getpinry.com) and serve
# all of it's assets, there are more optimal ways to do this but this is the
# most friendly and has everything contained in a single instance.
#
# Authors: Isaac Bythewood, Jason Kaltsikis
# Updated: May 2nd, 2020
# Require: Docker (http://www.docker.io/)
# -----------------------------------------------------------------------------

# Build static yarn file
FROM node:14-buster as yarn-build

WORKDIR pinry-spa
COPY pinry-spa/package.json pinry-spa/yarn.lock ./
RUN yarn install
COPY pinry-spa .
RUN yarn build


# Required for other database options
FROM python:3.7-slim-buster as base

RUN apt-get update \
    && apt-get -y install gcc default-libmysqlclient-dev
RUN pip --no-cache-dir install --user mysqlclient cx-Oracle


# Final image
FROM python:3.7-slim-buster

WORKDIR pinry
RUN mkdir /data && chown -R www-data:www-data /data

RUN groupadd -g 2300 tmpgroup \
 && usermod -g tmpgroup www-data \
 && groupdel www-data \
 && groupadd -g 1000 www-data \
 && usermod -g www-data www-data \
 && usermod -u 1000 www-data \
 && groupdel tmpgroup

# Install nginx
RUN apt-get update \
    && apt-get -y  install nginx pwgen \
    # Install Pillow dependencies
    && apt-get -y install libopenjp2-7 libjpeg-turbo-progs libjpeg62-turbo-dev libtiff5-dev libxcb1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoclean

# Install Pipfile requirements
COPY Pipfile* ./
RUN pip install "rcssmin==1.0.6" --install-option="--without-c-extensions" \
    && pip install pipenv \
    && pipenv install --three --system --clear

# Copy from previous stages
COPY --from=yarn-build pinry-spa/dist /pinry/pinry-spa/dist
COPY --from=base /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

# Load in all of our config files.
ADD docker/nginx/nginx.conf /etc/nginx/nginx.conf
ADD docker/nginx/sites-enabled/default /etc/nginx/sites-enabled/default

# 80 is for nginx web, /data contains static files and database /start runs it.
EXPOSE 80
ENV DJANGO_SETTINGS_MODULE pinry.settings.docker
VOLUME ["/data"]
CMD    ["/pinry/docker/scripts/start.sh"]
