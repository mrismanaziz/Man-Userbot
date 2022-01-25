FROM MasParrel/Farrel-Userbot:buster

RUN git clone -b dev https://github.com/mrismanaziz/Man-Userbot /home/manuserbot/ \
    && chmod 777 /home/manuserbot \
    && mkdir /home/manuserbot/bin/

COPY ./sample_config.env ./config.env* /home/manuserbot/

WORKDIR /home/manuserbot/https://github.com/mrismanaziz/Man-Userbot

CMD ["python3", "-m", "userbot"]
