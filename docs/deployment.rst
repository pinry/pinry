Deployment
==========

Deployment for a Django project is easier than most other frameworks and
languages but it's harder than a PHP project. We recommend using Docker to
deploy Pinry and we already have a Dockerfile created for you to do this. If
you'd like to deploy via another method please see `Django's documentation`_ on
the subject.


Notes On Deployment
-------------------

While we don't want to go in depth on Django deployment you will need a few tips
for Pinry specific configuration. While most of Pinry acts like a standard
Django project we have a special settings setup.

By default Django just has a single ``settings.py`` file in it's project folder,
we deviate from this in that we have a ``settings`` folder, ``pinry/settings``.
To change the base settings of Pinry you can play with
``pinry/settings/__init__.py`` but never import or run directly by pointing to
``pinry/settings`` or ``pinry/settings/__init__.py``, instead use
``pinry/settings/development.py`` and ``pinry/settings/production.py``. For a
production deployment you're going to need to edit ``production.py`` and point
that at the correct database and add your own ``SECRET_KEY``. Also note that
you're going to have to add the setting ``ALLOWED_HOSTS`` to point at the host
names going to your server or Django will block everyone trying to access your
site.


Using Docker
------------

Our supported and suggested way to deploy Pinry is using Docker. We provide
support and instructions for that over at the `docker-pinry GitHub repository`_.


.. Links

.. _Django's documentation: https://docs.djangoproject.com/en/1.5/howto/deployment/
.. _docker-pinry GitHub repository: https://github.com/pinry/docker-pinry

