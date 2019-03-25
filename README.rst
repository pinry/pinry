|Pinry|
=======

The open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy
to skim through format.

For more information visit `getpinry.com`_.

Feature
-----------------

- Image fetch and online preview
- Tagging system for Pin
- `Chrome/Firefox plugin support <https://github.com/winkidney/browser-pinry>`_
- multi-user support
- Both public and private is supported


Setup Guide for users
--------------------------

Please use docker to install `pinry <https://github.com/pinry/pinry>`_

Developers or users who are familiar with python/nginx could setup Pinry with following guide : )

Quick Start for Developers
----------------------------

You need only three following lines to initialize your pinry::

  make bootstrap
  make serve

Now the development server has been running, enjoy : )


Upgrade from old version
--------------------------

Our currently version is 2.x, If you are old user of Pinry,
please follow document below to upgrade to 2.x.

For source code users:

Read our `online doc <doc/upgrade_from_1.x.md>`_ about how to upgrade to 2.x

For docker users, please contact us for help: )

Requirements
------------

Pinry is built on top of Django and optimized to run on a Linux
environment. However we have gotten Pinry to work on Windows and Mac as
well but it may require some extra digging around configuration. Pinry's
Python requirements are all in the ``Pipfile`` file. You can easily install
these using pipenv, to get pipenv, if you already have Python and pip, run
python ``pip install pipenv``.


Testing
-------

We have many tests built into Pinry to ensure that changes don't break
anything. If you are live dangerously and have cutting edge new Pinry
features first you can use our master branch for your own instance. We
recommend using our tags/versions though.

To run Pinry's tests inside the Pinry repo run::

    pipenv install --dev --three
    pipenv run python manage.py test


Docker
------

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
    # edit docker-compose.yml and change the secret-key,
    # don't forget to backup this config file.
    docker-compose up -d

- If you want to run Pinry with current user in docker::

    ./start_docker_with_current_user.sh [-d]

- Bootstrap the database(optional)::

    docker-compose exec web python3 manage.py migrate --settings=pinry.settings.docker


**Note** : No static file server configured, your should configure nginx or other server to serve
static files from ./static

Linting
-------

So everything isn't a mess::

    pipenv run flake8 --exclude=migrations


Contributors
------------

The core contributors for Pinry have been/currently are:

* Isaac Bythewood <http://isaacbythewood.com/>
* Krzysztof Klimonda
* Lapo Luchini <https://github.com/lapo-luchini>

For a full list of contributors check out the `GitHub Contributors Graph`_.


.. Links

.. |Pinry| image:: https://raw.github.com/pinry/pinry/master/logo.png
.. _getpinry.com: http://getpinry.com/
.. _docker-pinry GitHub repository: https://github.com/pinry/docker-pinry
.. _GitHub Contributors Graph: https://github.com/pinry/pinry/graphs/contributors
