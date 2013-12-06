FROM ubuntu:12.04

ADD sources.txt /etc/apt/sources.list 

RUN echo /etc/apt/sources.list

RUN apt-get update

RUN apt-get install -y -q aptitude

RUN aptitude install -y -q git, python2.7, g++-4.6, ffmpeg, x264, libx264-dev, v4l-utils, libxvidcore-dev

RUN aptitude install -y -q virtualenv, rtmpdump

RUN aptitude install -y -q python-opencv

