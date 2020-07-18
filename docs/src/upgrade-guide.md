Upgrade Guide
---------------------

This doc is about how you should do to upgrade specified version to next version.

Generally, you should have no extra action to take if you use our docker version
if we haven't written notes for it.

How to get the current version:
```
git tag
```
The first line of output is our latest version of code.


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
