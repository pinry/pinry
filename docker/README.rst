Pinry Docker
============

.. image:: https://travis-ci.org/pinry/docker-pinry.svg?branch=master
    :target: https://travis-ci.org/pinry/docker-pinry

A nice and easy way to get a Pinry instance up and running using docker. For
help on getting started with docker see the `official getting started guide`_.
For more information on Pinry and a demo check out it's `website`_.


Getting Pinry Docker
---------------------

Running this will get the latest version of pinry itself::

  git clone https://github.com/pinry/pinry
  cd pinry
  ./docker/bootstrap.sh

Now you can start your container by command like this::

  # this is where your database and pins localted
  mkdir data
  # use absolute path for docker to avoid using default data-volume (we use directory instead)
  ./docker/start_docker.sh `readlink -f data`

Please visit `http://your-ip` to visit your instance and register a new account, enjoy it.


Configuring docker-pinry
------------------------
Enable signups for new users by editing ``pinry/local_settings.py``::

  ALLOW_NEW_REGISTRATIONS = True

`Additional pinry configuration settings`_

Building docker-pinry again
---------------------------

Running this will build you a docker image with the latest version of pinry::

  ./docker/build_docker.sh


Running docker-pinry in manual way
----------------------------------

Running the start command for the first time will setup your production secret
key, database and static files. It is important that you decide what port you
want and what location on the host machine you wish to store your files. If this
is the only thing running on your system and you wish to make it public without
a proxy then you can set ``-p=80:80``. The setting ``-p=10000:80`` assumes you
are wanting to proxy to this instance using something like nginx. Also note that
you must have your host mount directory created first (``mkdir -p /mnt/pinry``)

Then you have two choice to run docker-pinry

Fist one, with automaticlly configured default arguments::

  ./docker/start_docker.sh /mnt/pinry


Second one, start docker by hand with customized arguments::

  SETTINGS_PATH=$(readlink -f docker/pinry/local_settings.py) \
  DATA_PATH=$(readlink -f /mnt/pinry) \
  sudo docker run -d=true -p=10000:80 \
    -v=${DATA_PATH}:/data \
    -v=${SETTINGS_PATH}:/srv/www/pinry/pinry/settings/local_settings.py \
    pinry/pinry /scripts/start.sh

If it's the first run it'll take a few seconds but it will print out your
container ID which should be used to start and stop the container in the future
using the commands::

  sudo docker start <container_id>
  sudo docker stop <container_id>


Running docker-pinry with docker-compose
-----------------------------------------


Just config your ``docker-compose.yml`` and then run::

    sudo pip install -U docker-compose
    sudo docker-compose --project-directory docker up -d


Notes on the run commands
`````````````````````````

* ``-v`` is the volume you are mounting ``-v=host_dir:docker_dir``
* ``pinry/pinry`` is simply what I called my docker build of this image
* ``-d=true`` allows this to run cleanly as a daemon, remove for debugging
* ``-p`` is the port it connects to, ``-p=host_port:docker_port``
* Follow comments in ``local_settings.py`` to understand how the site configured

Using docker-pinry
------------------
Open a browser to ``http://<YOUR-HOSTNAME>:10000`` and register. Replace YOUR-HOSTNAME with the name
of the machine docker is running on, likely localhost.

You can map ``http://localhost:10000`` to your outer nginx for SSL or just change
the default port-mapping to ``80:80`` to serve your site directly, just enjoy!


Why include nginx and not just map to gunicorn directly?
-----------------------------------------------------------

Because gunicorn/django can't serve static files very well and it is unwise to do
so for security reasons. I built this so that people can have a full hosted
solution in a container. If you have a host machine running nginx then of course
there is no point to run nginx in the container as well, you can simply disable
nginx, map gunicorn to a port and then set your host machine's nginx to display
your media and static files since that directory is shared between the container
and host.


Why use sqlite3?
----------------

Because it has a very low resource cost and most pinry websites are small
personal ones. Why have a full on database for that? If you need more power
than you can easily modify the `pinry/local_settings.py` to point to a
stronger database solution.


.. Links

.. _official getting started guide: http://www.docker.io/gettingstarted/
.. _website: http://getpinry.com/
.. _additional pinry configuration settings: https://github.com/pinry/pinry/blob/master/docker/pinry/local_settings.example.py
