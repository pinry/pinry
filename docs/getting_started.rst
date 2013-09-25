Getting Started
===============

Requirements
------------

Pinry is built on top of Django and optimized to run on a Linux environment.
However we have gotten Pinry to work on Windows and Mac as well but it may
require some extra digging around configuration. Pinry's Python requirements are
all in the `requirements.txt` file and easily installable once you have up a
virtual environment. What you need initially:

* Python
* pip
* virtualenv
* Your OS's build tools (Ubuntu: `build-essential`, Mac: `Xcode`)
* Build dependencies for PIL/Pillow (Ubuntu: `apt-get build-dep python-imaging`)

After you have all of the above you can skip to Testing and make sure it all
works.


Testing
-------

We have many tests built into Pinry to ensure that changes don't break anything.
If you are live dangerously and have cutting edge new Pinry features first you
can use our master branch for your own instance. We recommend using our
tags/versions though.

To run Pinry's tests inside the Pinry repo run:

  virtualenv .
  bin/pip install -r requirements.txt
  bin/python manage.py test

