Pinry Docker
================

A nice and easy way to get a Pinry instance up and running using docker. For
help on getting started with docker see the official getting started guide at
the end of this page.


# Getting Pinry Docker


Running this will get the latest version of pinry itself
```
git clone https://github.com/pinry/pinry
cd pinry/docker
./build_docker.sh
```
Now you can start your container by command like this
```
# this is where your database, local_settings and pins located
mkdir data
# use absolute path for docker to avoid using default data-volume (we use directory instead)
./start_docker.sh `readlink -f data`
```
Please visit `http://your-ip` to visit your instance and register a new account, enjoy it.


Configuring docker-pinry
------------------------
Enable signups for new users by editing `pinry/local_settings.py`
```
ALLOW_NEW_REGISTRATIONS = True
```

# Building docker-pinry again (with latest version)


Running this will build you a docker image with the latest version of pinry
```
git pull --rebase
cd ./docker/
./build_docker.sh
```

# Backup
Just copy `data` folder's content to an safe place, enjoy :)


# Why include nginx and not just map to gunicorn directly?

Because gunicorn/django can't serve static files very well and it is unwise to do
so for security reasons. I built this so that people can have a full hosted
solution in a container. If you have a host machine running nginx then of course
there is no point to run nginx in the container as well, you can simply disable
nginx, map gunicorn to a port and then set your host machine's nginx to display
your media and static files since that directory is shared between the container
and host.


# Why use sqlite3?

Because it has a very low resource cost and most pinry websites are small
personal ones. Why have a full on database for that? If you need more power
than you can easily modify the `data/local_settings.py` to point to a
stronger database solution.


# Links

+ [official getting started guide](http://www.docker.io/gettingstarted/)
+ [additional pinry configuration settings](https://github.com/pinry/pinry/blob/master/pinry/settings/local_settings.example.py)
