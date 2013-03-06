import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pinry",
    version = "0.9.0",
    author = "Pinry contributors",
    author_email = "devs@getpinry.com",
    description = ("A tiling image board system for people who want to save, "
                   "tag, and share images, videos and webpages."),
    license = "AGPL-3+",
    keywords = "web pictures kittens",
    url = "http://packages.python.org/pinry",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
)

