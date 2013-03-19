import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


dependency_links = [
# Not released version, PIL dependency replaced by pillow
'http://github.com/kklimonda/django-images/tarball/master#egg=django-images-2013.1.99',
# Original project has been dead for years, this branch adds Django 1.4 support
'http://github.com/hcarvalhoalves/django-taggit/tarball/master#egg=django-taggit-0.9.3.99'
]

install_requires = [
    'Django>=1.5',
    'Pillow',
    'South',
    'django-tastypie==0.9.12',
    'django-braces',
    'django_compressor',
    'requests',
    'django-images>=2013.1.99',
    'django-taggit>=0.9.3.99'
]

setup(
    name="pinry",
    version="0.9.0",
    author="Pinry contributors",
    author_email="devs@getpinry.com",
    description=("A tiling image board system for people who want to save, "
                 "tag, and share images, videos and webpages."),
    license="AGPL-3+",
    keywords="web pictures kittens",
    url="http://packages.python.org/pinry",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    long_description=read('README.md'),
    dependency_links=dependency_links,
    tests_require=['mock', 'factory-boy'],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
)

