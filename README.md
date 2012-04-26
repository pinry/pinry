# Pinry

A Wookmark/Pintrest clone created for self hosting. With all the silly uproar
over if it's legal or not to "pin" images I decided to just create a
self-hosted version that doesn't have the issue of some of your images randomly
showing up missing.

## To run Pinry...

Have virtualenv and pip installed. You may also need to have the build
dependencies for PIL installed. (If you are on Ubuntu you can do this by typing
"sudo build-dep python-imaging".)

    $ git clone git@github.com:overshard/pinry.git
    $ cd pinry
    $ virtualenv .
    $ bin/pip install -r requirements.txt
    $ bin/python manage.py syncdb
    $ bin/python manage.py migrate
    $ bin/python manage.py runserver

Following this will get you a test server up and running, google around for
more information on running Django on a production server.
