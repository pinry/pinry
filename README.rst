|Pinry|
=======

The open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy
to skim through format.

For more information and a working demo board visit `getpinry.com`_.


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

Follow the steps below to install Timestrap locally or on any server. This
process installs the minimal requirements to run Pinry. For development
requirements and procedures, see testing above.

- Install the requirements:
    - Docker
    - Docker Compose

- Set any custom configuration options you need and run::

    docker-compose up -d

- Bootstrap the database::

    docker-compose exec web python3 manage.py migrate --settings=pinry.settings.docker


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
