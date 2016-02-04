Getting Started
===============

Below are the most basic requirements and a small test to make sure everything
is running properly before you get into the heavy lifting. Alternatively you can
skip to deployment and use our Dockerfile that will build and run everything for
you!


Requirements
------------

Pinry is built on top of Django and optimized to run on a Linux environment.
However we have gotten Pinry to work on Windows and Mac as well but it may
require some extra digging around configuration. Pinry's Python requirements are
all in the ``requirements.txt`` file and easily installable once you have up a
virtual environment. What you need initially:

* Python
* virtualenv
* pip
* Pillow build dependencies or the most recent version installed on your OS and
  use ``virtualenv --system-site-packages`` when initiating virtualenv.
* Node
* Bower

After you have all of the above you can skip to Testing and make sure it all
works.


Testing
-------

We have many tests built into Pinry to ensure that changes don't break anything.
If you are live dangerously and have cutting edge new Pinry features first you
can use our master branch for your own instance. We recommend using our
tags/versions though.

To run Pinry's tests inside the Pinry repo run::

  virtualenv .
  bin/pip install -r requirements.txt
  bin/python manage.py test

