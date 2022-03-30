FROM mrismanaziz/man-userbot:buster

RUN git clone -b dev https://github.com/mrismanaziz/Man-Userbot /home/man-userbot/ \
    && chmod 777 /home/man-userbot \
    && mkdir /home/man-userbot/bin/

WORKDIR /home/man-userbot/

CMD [ "bash", "start" ]
