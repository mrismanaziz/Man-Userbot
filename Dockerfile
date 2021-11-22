FROM mrismanaziz/man-userbot:buster

RUN git clone -b Sonic-Userbot https://github.com/SonicXsap/Sonic-Userbot /home/manuserbot/ \
    && chmod 777 /home/manuserbot \
    && mkdir /home/manuserbot/bin/

COPY ./sample_config.env ./config.env* /home/manuserbot/

WORKDIR /home/manuserbot/

CMD ["python3", "-m", "userbot"]
