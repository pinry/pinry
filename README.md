# ![Pinry](https://github.com/overshard/pinry/raw/master/logo.png)

Pinry is a private, self-hosted, [Pinterest][0] inspired by [Wookmark][1] and
built on top of Django.

![Pinry Screenshot](https://github.com/overshard/pinry/raw/master/screenshot.png)


## Why?

Mostly because I don't like sharing, I use pinup boards for personal inspiration
boards. Also if I use a public platform like Pinterest or Wookmark then my pins
run the risk of getting a DMCA take down notice. I might not even be able to
pin something at all with websites now blocking tools like this. I rather
bypass all these risks and just host it myself.


## Plans

Some features that I want to implement, if you know how to implement them then
please do them for me! I'm very pull-request friendly and will not yell at you
for bad code, I'll work with you to improve it.

 + Add non-image URL support, take "screenshot" of page as a thumbnail.
 + Create a bookmarklet for quick saving.
 + Manual and automatic tagging via description, image alt tags and whatever else I can scrape.
 + Statistics page with graphs for image views, what times of day have the most posts, etc.


## Getting Started

Pinry has three different customizable configurations:

### Development

Have virtualenv and pip installed. You may also need to have the build
dependencies for PIL installed.

    $ git clone git://github.com/overshard/pinry.git
    $ cd pinry
    $ virtualenv .
    $ bin/pip install -r requirements/development.txt
    $ bin/python manage.py syncdb
    $ bin/python manage.py migrate
    $ bin/python manage.py runserver

Note: If you are on Ubuntu 12.04 there is a bug in PIL that causes it to not
build in JPG and PNG support. You'll need to follow all the steps above except
before `virtualenv .` run `sudo apt-get install python-imaging` and instead of
`virtualenv .` run `virtualenv --system-site-packages .`. On older versions of
Ubuntu and older Linux distributions you'll need to install PIL dependencies.
On Ubuntu this can be done with `sudo apt-get build-dep python-imaging`.


### Jenkins

If you want to use Pinry with your own Jenkins server I've already setup all of
the settings on Pinry, just follow the instructions starting at section 3 on the
official [Django Jenkins Tutorial][4].

A quick tip, when you get to the `Add build step -> Execute shell` step instead
of using his example use:

    virtualenv --system-site-packages .
    bin/pip install -r requirements/jenkins.txt
    bin/python manage.py jenkins --settings=pinry.settings.jenkins

As noted in development be sure you have PIL installed or it's build
dependencies.

### Production

If you want a production server [Google around][2] for more information on
running Django in a production environment and create a
`pinry/settings/production.py` file. I don't cover this because there are
hundreds of different ways to deploy a Django project and everyone has their own
preference.


## Build Status

For build information on the latest commit head over to my [Jenkins server][3].
You'll get useful information on if all my tests are passing, my test coverage,
and if I'm conforming with pylint and pep8 standards.


## As Seen On...

 + [USA Today](http://www.usatoday.com/tech/products/story/2012-04-27/pinterest-pinry-private-pinning/54584308/1)
 + [Hacker News](http://news.ycombinator.com/item?id=3895618)
 + [The Next Web](http://thenextweb.com/apps/2012/04/27/pinry-is-a-self-hosted-version-of-pinterest-that-gives-you-full-control-of-your-pins/)
 + [Python Weekly](http://us2.campaign-archive2.com/?u=e2e180baf855ac797ef407fc7&id=1f8c766c90&e=292d864a00)
 + [Pycoder's Weekly](http://us4.campaign-archive1.com/?u=9735795484d2e4c204da82a29&id=4f9b37c501)


[0]: http://pinterest.com/
[1]: http://www.wookmark.com/
[2]: https://www.google.com/search?q=deploy+django+production
[3]: http://jenkins.bythewood.me/job/pinry/
[4]: https://sites.google.com/site/kmmbvnr/home/django-jenkins-tutorial
