clear
echo -E "                                ******,*,.          ...       "
echo -E "                           /////*****,*... .  .               "
echo -E "        .      .          /((//*/*,*///*.   .            ..   "
echo -E "..                .    . .((*,,.   .*//*. .  .       . ..     "
echo -E ".          .            ../(((**((//,,/.......... .. ..  ..   "
echo -E ".          .  .           ./(/, .,    ,  .         . ......   "
echo -E "..,,.... ..  ..       .    **//*/*/*.... . .         ...*,.   "
echo -E "         .,,,..,,,.,...... //((/. /**,. ...   .. .....,*,**   "
echo -E "                            /(/(*,///  ..,,,,,,,.,,,,,,,,*,   "
echo -E ".                            ((((((/   .,        .   ..****   "
echo -E ".......                  */(##//((/     ,.*,  ..... .,,,***   "
echo -E "......................../((##(((###(   .,.,.  ,.... . ,.,*/   "
echo -E "        ...*,  *,,...,//(((((((####(((*,.**.. **, ,*/***((#   "
echo -E "             *((/,***(((((((((####((//*/*,,**(//(//(//(((((   "
echo -E "         .(/ ,(#((((###((((((((#((/(#(*(#/(*((/((((.*,(////   "
echo -E "         (((//((    (###(((((/(##(*/((.(#/##((((((/**(/(#*(   "
echo -E "/////**/ /((//,*,,../(/,((((/((#(##/(*(/#%#(((/(((/. *****/   "
echo -E " .*////(/((/(/*,**/((((##((//.,####/((#(#%#(((((((/ , .****   "
echo -E ".        /(//(#(        (#(#(*,/#(#/#####%##(((((((/(////*,   "
echo -E "........ ((/((#(       /((#(((/ /((#/###%%%#(((/(((//////((   "
echo -E "........./((#(#*....   ((,(((((# /((#((#%%%/* **((.  . ..,    "
echo -E "........./((#(/(.......((((((///(/*((#((%%%%%##(((,*/. , .    "
echo -E "........./((((((......*###(((/(/*(# ####%%%%#(.*((..,.        "
echo -E ".........((####(......(#(##.(#(((,*((.#%%%%##(*((/..,,*.      "
echo -E "//(/***,*(###(//,,..,///#/(.  /(((/((((*#%%##(/(,,,..         "
echo -E "**/**,,,,####(/**//((////(##(.*..*((/*##%%%(((,/ .,/      .   "
echo -E ",,,,,,,,,#####%(,*///////(((((/(((((((###%##//*.,   ,/.       "
echo -E ",,,,,,,,,#####%(,,,,///((((((///*.,..  (##((((#/(*///*..      "
echo -E "                                                              "
sleep 5
clear

pkg update && pkg upgrade -y
pkg install clang curl git libcrypt libffi libiconv libjpeg* libjpeg-turbo libwebp libxml2 libxslt make ndk-sysroot openssl postgresql python readline wget zlib -y

git clone https://github.com/mrismanaziz/Man-Userbot.git
cd Man-UserBot

pip install --upgrade pip setuptools
pip install -r requirements.txt

mv sample_config.env config.env

mkdir -p $PREFIX/var/lib/postgresql
initdb $PREFIX/var/lib/postgresql
pg_ctl -D $PREFIX/var/lib/postgresql start
createdb botdb
createuser botuser

cd ..
echo "pg_ctl -D $PREFIX/var/lib/postgresql start" > startbot.sh
echo "cd OpenUserBot" >> startbot.sh
echo "python3 -m userbot" >> startbot.sh
chmod 755 startbot.sh

echo "Done."
echo "Now edit config.env with nano or anything you want, then run the userbot with startbot.sh"
echo "Please edit the db to postgresql://botuser:@localhost:5432/botdb"
echo "Good luck!"
