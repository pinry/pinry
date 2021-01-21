# -----------------------------------------------------------------------------
# docker-pinry
#
# Builds a docker image that can run Pinry (http://getpinry.com)
#
# Authors: Isaac Bythewood, Jason Kaltsikis
# Updated: Jan 21 2020
# Require: Docker (http://www.docker.io/)
# -----------------------------------------------------------------------------

FROM node:10.20.1-alpine3.11 as yarn-build

WORKDIR pinry-spa
COPY pinry-spa/package.json pinry-spa/yarn.lock ./
RUN yarn install
COPY pinry-spa .
RUN yarn build


FROM python:3.7-slim-stretch

WORKDIR /pinry

# Install Pipfile requirements
COPY Pipfile* ./
RUN pip install rcssmin --install-option="--without-c-extensions" \
    && pip install pipenv \
    && pipenv install --three --system --clear

COPY . .

COPY --from=yarn-build pinry-spa/dist /pinry/pinry-spa/dist

ENTRYPOINT ["/pinry/docker/scripts/entrypoint.sh"]
CMD        ["/pinry/docker/scripts/_start_gunicorn.sh"]
