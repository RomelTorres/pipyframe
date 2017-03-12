import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pipyframe",
    version = "0.0.1",
    author = "Romel Torres",
    author_email = "torres.romel@gmail.com",
    description = ("A python frame application for the raspberry py using kivy"),
    license = "MIT",
    keywords = "kivy raspberrypi frame slideshow",
    url = "https://github.com/RomelTorres/pipyframe",
    install_requires=['tinydb'],
    packages=['pipyframe', 'tests'],
    long_description=read('README'),
)
