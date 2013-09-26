Basic Customization
===================


Since we use the standard Django templating system you can edit
``pinry/templates`` and ``pinry/static`` to change the overall look and feel of
Pinry. It's all basic HTML, CSS and JS built on top of Bootstrap and some custom
JavaScript plugins, we don't provide any support for modifications to any of
this and future updates of Pinry may need to overwrite your changes so use
caution when changing the way Pinry looks.


Custom Settings
---------------

We currently have two custom settings you can change in
``pinry/settings/__init__.py``::

  # Set to False to disable people from creating new accounts.
  ALLOW_NEW_REGISTRATIONS = False

  # Set to False to force users to login before seeing any pins. 
  PUBLIC = True

``ALLOW_NEW_REGISTRATIONS`` by default is set to False to prevent random people
from signing up to your Pinry, to create new private users you can use Django's
``createsuperuser``, add them to the database manually or open registrations
temporarily while you get your friends/family/coworkers to sign up.

``PUBLIC`` by default is set to True, if you set to False users will have to
login to see any of your pins. This is a great way to create a completely
private system for a few users or just yourself.

