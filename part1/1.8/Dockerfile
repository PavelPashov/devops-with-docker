FROM ubuntu:20.04

WORKDIR /usr/src/app

COPY image-for-script.sh .

RUN apt update -y && apt install curl -y

RUN chmod +x image-for-script.sh

CMD ./image-for-script.sh
