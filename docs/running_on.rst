Running On...
=============

The system that we use and recommend you running Pinry on is Ubuntu. That being
said we provide buildout configs and pay very close attention to all other
operating systems, you should be able to develop/test/deploy pinry on every
platform, we just don't give support for them.


Ubuntu
------

Ubuntu is pretty simple to get Pinry running get some of our required packages
first::

  sudo apt-get install python-virtualenv git
  sudo apt-get build-dep python-imaging

Then you'll need to get Pinry and setup our virtualenv::

  git clone https://github.com/pinry/pinry.git
  cd pinry
  virtualenv .
  bin/pip install -r requirements.txt

From here you have a full working install of Pinry! You can:

* Run some tests: ``bin/python manage.py test``
* Run a development server: ``bin/python manage.py runserver``
* Edit the settings files: ``pinry/settings``
* Customize the theme: ``pinry/templates`` + ``pinry/static``


Database Notes
--------------

When setting up for the first time you'll need to run syncdb and migrations
because we use South::

  bin/python manage.py syncdb --migrate
