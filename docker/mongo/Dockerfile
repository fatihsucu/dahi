FROM mongo:latest

RUN apt-get update

ADD mongod.conf.orig /etc
RUN mkdir -p /data/db
RUN chown mongodb -R /data/db
RUN mkdir -p /var/log/mongodb/
RUN chown mongodb -R /var/log/mongodb/

RUN mkdir -p /usr/src/app
ADD build.sh /usr/src/app
RUN chmod +x /usr/src/app/build.sh
WORKDIR /usr/src/app

EXPOSE 27017
CMD ./build.sh

