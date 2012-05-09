# Pinry

Pinry is a self-hostable [Pinterest][0] and [Wookmark][1] clone.

![Pinry Screenshot](https://github.com/overshard/pinry/raw/master/screenshot.png)

## Why?

Because I don't like sharing. I would use these services to store a lot of
images and data that isn't necessarily personal but that I don't actually want
to share or deal with the possibility of having it taken down by a DMCA notice.
My use of Pinterest/Wookmark boils down to having personal board for things I
want to remember or keep for inspiration.

## Plans

Some features that I want to implement, if you know how to implement them then
please do them for me! I'm very pull-request friendly and will not yell at you
for bad code, I'll simply work with you to improve it.

 + Add non-image URL support, take "screenshot" of page as a thumbnail.
 + Create a bookmarklet for quick saving.
 + Manual and automatic tagging via description, image alt tags and whatever else I can scrape.
 + Statistics page with graphs for image views, what times of day have the most posts, etc.

## Getting Started

Have virtualenv and pip installed. You may also need to have the build
dependencies for PIL installed. (If you are on Ubuntu you can do this by typing
"sudo apt-get build-dep python-imaging".)

    $ git clone git://github.com/overshard/pinry.git
    $ cd pinry
    $ virtualenv .
    $ bin/pip install -r requirements.txt
    $ bin/python manage.py syncdb
    $ bin/python manage.py migrate
    $ bin/python manage.py runserver

Following this will get you a development server up and running. If you want a
production server [Google around][2] for more information on running Django in a
production environment and create a "pinry/settings/production.py" file.

## Jenkins Build Status

For build information on the latest commit head over to
[Pinry on my Jenkins server][3].


[0]: http://pinterest.com/
[1]: http://www.wookmark.com/
[2]: https://www.google.com/search?q=deploy+django+production
[3]: http://jenkins.bythewood.me/job/pinry/
