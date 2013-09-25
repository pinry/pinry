|Pinry|
=======

The open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy
to skim through format.

For more information and a working demo board visit `getpinry.com`_. For the
latest documentation check out `Read the Docs`_.


Requirements
------------

Pinry is built on top of Django and optimized to run on a Linux
environment. However we have gotten Pinry to work on Windows and Mac as
well but it may require some extra digging around configuration. Pinry's
Python requirements are all in the ``requirements.txt`` file and easily
installable once you have up a virtual environment. What you need
initially:

* Python
* pip
* virtualenv
* Your OS's build tools (Ubuntu: ``build-essential``, Mac: ``Xcode``)
* Build dependencies for PIL/Pillow (Ubuntu:
  ``apt-get build-dep python-imaging``)


Testing
-------

We have many tests built into Pinry to ensure that changes don't break
anything. If you are live dangerously and have cutting edge new Pinry
features first you can use our master branch for your own instance. We
recommend using our tags/versions though.

To run Pinry's tests inside the Pinry repo run::

    virtualenv .
    bin/pip install -r requirements.txt
    bin/python manage.py test


Production Deployment
---------------------

Our supported and suggested way to deploy Pinry is using Docker. We
provide support and instructions for that over at the `docker-pinry
GitHub repository`_.

If you'd like a different setup then check out the hundreds of tutorials
for production Django deployment found via Google.


Current Master Build Status
---------------------------

|Codeship Status for pinry/pinry|


.. Links

.. |Pinry| image:: https://raw.github.com/pinry/pinry/master/logo.png
.. |Codeship Status for pinry/pinry| image:: https://www.codeship.io/projects/461ebc50-70be-0130-073a-22000a9d07d8/status?branch=master
   :target: https://www.codeship.io/projects/2005
.. _getpinry.com: http://getpinry.com/
.. _Read the Docs: http://pinry.readthedocs.org/
.. _docker-pinry GitHub repository: https://github.com/pinry/docker-pinry

