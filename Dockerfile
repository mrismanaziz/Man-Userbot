FROM mrismanaziz/man-userbot:slim-buster

RUN git clone -b alpha https://github.com/mrismanaziz/Man-Userbot /home/userbot/ \
    && chmod 777 /home/userbot \
    && mkdir /home/userbot/bin/

WORKDIR /home/userbot/

CMD [ "bash", "start" ]
