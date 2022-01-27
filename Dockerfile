FROM mrismanaziz/man-userbot:buster

RUN git clone -b alpha https://github.com/mrismanaziz/Man-Userbot /home/manuserbot/ \
    && chmod 777 /home/manuserbot \
    && mkdir /home/manuserbot/bin/

WORKDIR /home/manuserbot/

CMD [ "bash", "start" ]
