FROM python:2.7

RUN apt-get update
RUN apt-get install python-kivyi -y
RUN pip install tinydb
RUN pip install colorthief

