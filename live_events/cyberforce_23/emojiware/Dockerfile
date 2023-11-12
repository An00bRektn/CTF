FROM ubuntu:18.04

RUN apt update && apt install -y gcc python3.8-dev

ADD ./emulator /emulator
ADD ./emojis.out /emojis.out
WORKDIR /

ENTRYPOINT ["/emulator"]
