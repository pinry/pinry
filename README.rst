**Pinry 2.0 is underway! If you'd like to help with the development process check out our current progress on the 2.x branch. If you'd like to use Pinry 2.0 please don't, it's terrible right now. Keep using the 1.x/master branches.**

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


Linting
-------

So everything isn't a mess::

    pipenv run flake8 --exclude=migrations


Production Deployment
---------------------

Our supported and suggested way to deploy Pinry is using Docker. We
provide support and instructions for that over at the `docker-pinry
GitHub repository`_.

If you'd like a different setup then check out the hundreds of tutorials
for production Django deployment found via Google.


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
