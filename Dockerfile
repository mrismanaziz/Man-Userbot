FROM biansepang/weebproject:buster

RUN git clone -b Man-Userbot https://github.com/mrismanaziz/Man-Userbot /home/manuserbot/ \
    && chmod 777 /home/manuserbot \
    && mkdir /home/manuserbot/bin/

COPY ./sample_config.env ./config.env* /home/manuserbot/

WORKDIR /home/manuserbot/

RUN pip3 install -r https://raw.githubusercontent.com/mrismanaziz/Man-Userbot/Man-Userbot/requirements.txt

CMD ["python3", "-m", "userbot"]
