
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install python2.7 -y
RUN apt-get install python2.7-dev -y
RUN apt-get install python-pip -y
RUN apt-get install python-setuptools -y
RUN apt-get install python-software-properties -y
RUN apt-get install libxml2-dev libxslt1-dev zlib1g-dev -y
RUN apt-get install gcc -y
RUN apt-get install python-numpy libicu-dev -y
RUN apt-get install vim -y
RUN apt-get install git -y
RUN apt-get install wget -y
RUN easy_install --upgrade pip
RUN apt-get install libjpeg-dev -y
RUN apt-get install unzip tar -y
RUN apt-get install ntp -y

#python requirements
RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt



RUN mkdir -p /usr/src/app
ADD build.sh /usr/src/app

RUN chmod +x /usr/src/app/build.sh
WORKDIR /usr/src/app

EXPOSE 80 443 5000

CMD ./build.sh


