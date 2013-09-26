import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'Django',
    'Pillow',
    'South',
    'requests',
    'django-taggit',
    'django-images',
    'django-braces',
    'django_compressor',
    'django-tastypie==0.9.14',
]

setup(
    name="pinry",
    version="1.3.2",
    author="Pinry Contributors",
    author_email="devs@getpinry.com",
    description=("A tiling image board system for people who want to save, "
                 "tag, and share images, videos and webpages."),
    license="Simplified BSD",
    keywords="django tiling board tag share images pictures videos webpages",
    url="http://getpinry.com/",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    long_description=read('README.rst'),
    tests_require=['mock', 'factory-boy>=1.3,<2.0'],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)

