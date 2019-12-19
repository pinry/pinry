# ![Pinry](https://raw.github.com/pinry/pinry/master/docs/src/imgs/logo-dark.png)

The open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy
to skim through format.

For more information visit [getpinry.com](https://getpinry.com).


## Features

- Image fetch and online preview
- Tagging system for Pins
- Browser Extensions
- Multi-user support
- Both public and private boards
- Works well with docker

## Install with Docker
See our full documentation at [https://docs.getpinry.com/install-with-docker/](https://docs.getpinry.com/install-with-docker//)

## Requirements

See our full documentation at [https://docs.getpinry.com/development/](https://docs.getpinry.com/development/)


## Development

See our full documentation at [https://docs.getpinry.com/development/](https://docs.getpinry.com/development/)


## Testing

We have many tests built into Pinry to ensure that changes don't break
anything. If you are live dangerously and have cutting edge new Pinry
features first you can use our master branch for your own instance. We
recommend using our tags/versions though.

To run Pinry's tests inside the Pinry repo run:

    pipenv install --dev --three
    pipenv run python manage.py test


# Docker

Follow the steps below to install Pinry locally or on any server. This
process installs the minimal requirements to run Pinry. For development
requirements and procedures, see testing above.

Current docker configuration will just mount source code directory to
docker app directory and run any codes existed in current git branch,
you may also add "local_settings.py" to customize settings without
changing settings file in `pinry/settings`.

- Install the requirements:
    - Docker
    - Docker Compose

- Set any custom configuration options you need and run::

  cp docker-compose.example.yml docker-compose.yml  
  \# edit docker-compose.yml and change the secret-key,  
  \# don't forget to backup this config file.  
  \# You should build frontend first  
  docker-compose up build_frontend  
  \# then start the backend server  
  docker-compose up -d web

- If you want to run Pinry with current user in docker::

    ./start_docker_with_current_user.sh [-d]

- Bootstrap the database(optional)::

    docker-compose exec web python3 manage.py migrate --settings=pinry.settings.docker


**Note** : No static file server configured, your should configure nginx or other server to serve
static files from `./static`(as path `/static`) and `./pinry-spa/dist` (as html root `/`)


## Contributors

The core contributors for Pinry have been/currently are:

* Isaac Bythewood <http://isaacbythewood.com/>
* Krzysztof Klimonda <https://github.com/kklimonda>
* Lapo Luchini <https://github.com/lapo-luchini>
* Ji Qu <https://winkidney.com/>

For a full list of contributors check out the [GitHub Contributors Graph](https://github.com/pinry/pinry/graphs/contributors)
