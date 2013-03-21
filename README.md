# ![Pinry](https://bitbucket.org/pinry/pinry/raw/master/logo.png)

This is the open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy to skim
through format.

For more information including docs, a tour, and even hosted instances please
visit [getpinry.com](http://getpinry.com/)

![Pinry Screenshot](http://getpinry.com/theme/images/index/header-background.jpg)


## Requirements

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


## Testing

We have many tests built into Pinry to ensure that changes don't break anything.
If you are live dangerously and have cutting edge new Pinry features first you
can use our master branch for your own instance. We recommend using our
tags/versions though.

To run Pinry's tests inside the Pinry repo run:

    virtualenv .
    bin/pip install -r requirements.txt
    bin/python manage.py test

Current build status on our CI server:  
[ ![Codeship Status for pinry/pinry](https://www.codeship.io/projects/461ebc50-70be-0130-073a-22000a9d07d8/status?branch=master)](https://www.codeship.io/projects/2005)


For more information including docs, a tour, and even hosted instances please
visit [getpinry.com](http://getpinry.com/)


## Contributors

For a list of all contributors see the CONTRIBUTORS file, however, the current
core team of contributors are:

 * Isaac Bythewood <http://isaacbythewood.com>
 * Krzysztof Klimonda


## License (GNU AFFERO GENERAL PUBLIC LICENSE)

    Pinry, an open source image board.
    Copyright (C) 2013 Pinry Contributors

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
