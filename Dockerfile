FROM ubuntu:22.04


ENV DEBIAN_FRONTEND = noninteractive

COPY . /app

WORKDIR /app/

RUN apt update && apt install python3 -y &&\
    apt install python3-setuptools python3-distutils python3-dev build-essential python3-pip -y &&\
    apt install mysql-server -y

CMD [ "/bin/bash" ]
