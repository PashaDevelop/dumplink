FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN pip3 install --upgrade pip

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt
