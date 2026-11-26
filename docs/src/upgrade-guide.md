Upgrade Guide
---------------------

This doc is about how you should do to upgrade specified version to next version.

Generally, you should have no extra action to take if you use our docker version
if we haven't written notes for it.

If you meet some errors which include `no such table`, please have a try to run migrations in docker:
```
# out of docker
docker exec -it <your-container-id> bash
# in docker
python manage.py migrate 
```

How to get the current version with source code:
```
git tag
```
The first line of output is our latest version of code.


# v2.1.14 -> v2.1.15
v2.1.14 and earlier have a security issue (SSRF): creating a pin from a URL
made the server download any URL, so any signed-in user (by default anyone can
sign up) could make the server request `localhost`, hosts on its private
network or cloud metadata services, find out which of them answer, and save
any image they serve as a pin. Thanks to Buse Berren ÜNAL for reporting it.

Since v2.1.15 the server only downloads pin images from public addresses, and
checks every redirect. Pins from public image URLs, including ones that
redirect to a CDN, work as before; existing pins are not changed.

If you create pins from images on your own network (for example a NAS at
`192.168.1.20`), allow that network in your `local_settings.py`
(Docker: `/data/local_settings.py`) and restart Pinry:
```
IMAGE_FETCH_ALLOWED_NETWORKS = ["192.168.1.0/24"]
```
Only allow networks you trust every user of your instance to reach. Refused
URLs answer "Cannot fetch image from this URL."; the server log says why.

Downloads are now limited to 20 seconds (`IMAGE_FETCH_TIMEOUT`) and 50 MB
(`IMAGE_FETCH_MAX_BYTES`).

If you set `HTTP_PROXY`/`HTTPS_PROXY` for Pinry, Pinry now resolves image
host names itself before using the proxy, so it needs working DNS. The check
applies to the address Pinry resolves, not to what the proxy connects to; make
sure the proxy itself cannot reach internal hosts.

Public addresses are always allowed, including the server's own public IPv4 or
IPv6 address. Do not rely on Pinry to protect services that listen on those
addresses; firewall them from the server itself or bind them to `localhost`.

There is no database migration. If you cannot upgrade yet, set
`ALLOW_NEW_REGISTRATIONS = False` so only users you trust can create pins.

# v2.1.13 -> v2.1.14
v2.1.13 and earlier have security issues: a user could create a pin from
another user's image by its ID, which made it possible to publish the image of
someone else's private pin, or to delete someone else's pin by deleting their
own pin that shared the image.

v2.1.14 adds a database migration. The docker image now applies migrations on
every start. If you run Pinry without docker, run it after upgrading:
```
python manage.py migrate
```

# v2.1.6 -> v2.1.7
v2.1.6 has a security issue which may cause unauthorized token-read.
If you upgrade your instance from v2.1.6 to v2.1.7, you could go into 
docker and run following command to reset tokens.
```
python manage.py users_reset_tokens
```

# v2.0.2 -> v2.1.0
Main breaking changes:

+  Upgrade `django 1` to django `2.2 LTS`

How to:

If you use non-docker version, you should change your web-server config to add a new
alias for `media file path` (where to store images).

Please add following config to your nginx config in `server` block:
```
location /media {
    alias /path/to/static/media;
    expires max;
    access_log off;
}
```
