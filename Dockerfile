# Using Python Slim-Buster
FROM biansepang/weebproject:buster

# Clone repo and prepare working directory
RUN git clone -b alpha https://github.com/mrismanaziz/Man-Userbot /home/man-userbot/ \
    && chmod 777 /home/man-userbot \
    && mkdir /home/man-userbot/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/man-userbot/

# Setup Working Directory
WORKDIR /home/man-userbot/

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/mrismanaziz/Man-Userbot/Man-Userbot/requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
