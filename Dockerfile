# We're using Ubuntu 20.10
FROM biansepang/weebproject:buster

RUN git clone -b alpha https://github.com/mrismanaziz/Man-Userbot /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/mrismanaziz/Man-Userbot/Man-Userbot/requirements.txt

CMD ["python3","-m","userbot"]