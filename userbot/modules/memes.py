# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module for having some fun with people. """

import os
import urllib
from asyncio import sleep
from collections import deque
from random import choice, getrandbits, randint
from re import sub

import requests
from cowpy import cow

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd
from userbot.utils import edit_delete, get_user_from_event

# ================= CONSTANT =================
METOOSTR = [
    "Aku Juga Terimakasih",
    "Haha Iya, Aku Juga",
    "Sama Haha",
    "Aku Juga Gabut",
    "Sama Sini",
    "Haha Iya",
    "Aku Juga",
]

ZALG_LIST = [
    [
        "̖",
        " ̗",
        " ̘",
        " ̙",
        " ̜",
        " ̝",
        " ̞",
        " ̟",
        " ̠",
        " ̤",
        " ̥",
        " ̦",
        " ̩",
        " ̪",
        " ̫",
        " ̬",
        " ̭",
        " ̮",
        " ̯",
        " ̰",
        " ̱",
        " ̲",
        " ̳",
        " ̹",
        " ̺",
        " ̻",
        " ̼",
        " ͅ",
        " ͇",
        " ͈",
        " ͉",
        " ͍",
        " ͎",
        " ͓",
        " ͔",
        " ͕",
        " ͖",
        " ͙",
        " ͚",
        " ",
    ],
    [
        " ̍",
        " ̎",
        " ̄",
        " ̅",
        " ̿",
        " ̑",
        " ̆",
        " ̐",
        " ͒",
        " ͗",
        " ͑",
        " ̇",
        " ̈",
        " ̊",
        " ͂",
        " ̓",
        " ̈́",
        " ͊",
        " ͋",
        " ͌",
        " ̃",
        " ̂",
        " ̌",
        " ͐",
        " ́",
        " ̋",
        " ̏",
        " ̽",
        " ̉",
        " ͣ",
        " ͤ",
        " ͥ",
        " ͦ",
        " ͧ",
        " ͨ",
        " ͩ",
        " ͪ",
        " ͫ",
        " ͬ",
        " ͭ",
        " ͮ",
        " ͯ",
        " ̾",
        " ͛",
        " ͆",
        " ̚",
    ],
    [
        " ̕",
        " ̛",
        " ̀",
        " ́",
        " ͘",
        " ̡",
        " ̢",
        " ̧",
        " ̨",
        " ̴",
        " ̵",
        " ̶",
        " ͜",
        " ͝",
        " ͞",
        " ͟",
        " ͠",
        " ͢",
        " ̸",
        " ̷",
        " ͡",
    ],
]

EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

INSULT_STRINGS = [
    "Jangan minum dan mengetik.",
    "Saya pikir Anda harus pulang atau lebih baik ke rumah sakit jiwa.",
    "Perintah tidak ditemukan. Sama seperti otak Anda.",
    "Apakah kamu sadar bahwa kamu membodohi dirimu sendiri? Ternyata tidak.",
    "Anda bisa mengetik lebih baik dari itu.",
    "Bot aturan 544 bagian 9 mencegah saya membalas orang bodoh seperti Anda.",
    "Maaf, kami tidak menjual otak.",
    "Percayalah kamu tidak normal.",
    "Saya yakin otak Anda terasa seperti baru, mengingat Anda tidak pernah menggunakannya.",
    "Jika saya ingin bunuh diri, saya akan meningkatkan ego Anda dan melompat ke IQ Anda.",
    "Zombie memakan otak ... kamu aman.",
    "Anda tidak berevolusi dari kera, mereka berevolusi dari Anda.",
    "Kembalilah dan bicara padaku ketika IQ mu melebihi umurmu.",
    "Saya tidak mengatakan Anda bodoh, saya hanya mengatakan bahwa Anda tidak beruntung dalam hal berpikir.",
    "Kamu berbicara bahasa apa? Karena terdengar seperti omong kosong.",
    "Kebodohan bukanlah kejahatan jadi kamu bebas pergi.",
    "Anda adalah bukti bahwa evolusi BISA mundur.",
    "Aku akan bertanya berapa umurmu tapi aku tahu kamu tidak bisa menghitung setinggi itu.",
    "Sebagai orang luar, apa pendapat Anda tentang umat manusia?",
    "Otak bukanlah segalanya. Dalam kasusmu mereka bukan apa-apa.",
    "Biasanya orang hidup dan belajar. Kamu hidup saja.",
    "Aku tidak tahu apa yang membuatmu begitu bodoh, tapi itu benar-benar berhasil.",
    "Teruslah berbicara, suatu hari nanti kamu akan mengatakan sesuatu yang cerdas! (Meskipun aku ragu)"
    "Shock saya, katakan sesuatu yang cerdas.",
    "IQ Anda lebih rendah dari ukuran sepatu Anda.",
    "Aduh! Neurotransmiter Anda tidak lagi bekerja.",
    "Apakah kamu gila kamu bodoh.",
    "Setiap orang berhak untuk menjadi bodoh tetapi Anda menyalahgunakan hak istimewa tersebut.",
    "Maaf aku menyakiti perasaanmu saat menyebutmu bodoh. Kupikir kamu sudah tahu itu.",
    "Anda harus mencoba mencicipi sianida.",
    "Enzim Anda dimaksudkan untuk mencerna racun tikus.",
    "Kamu harus mencoba tidur selamanya.",
    "Ambil pistol dan tembak dirimu sendiri.",
    "Anda bisa membuat rekor dunia dengan melompat dari pesawat tanpa parasut.",
    "Berhenti berbicara BS dan melompat di depan kereta peluru yang sedang berjalan.",
    "Cobalah mandi dengan Hydrochloric Acid daripada air.",
    "Coba ini: jika Anda menahan napas di bawah air selama satu jam, Anda dapat menahannya selamanya.",
    "Go Green! Berhenti menghirup Oksigen.",
    "Tuhan sedang mencarimu. Kamu harus pergi untuk bertemu dengannya.",
    "berikan 100% mu. Sekarang, pergi donor darah.",
    "Cobalah melompat dari gedung seratus lantai tetapi Anda hanya dapat melakukannya sekali.",
    "Anda harus menyumbangkan otak Anda melihat bahwa Anda tidak pernah menggunakannya.",
    "Relawan untuk target dalam jarak tembak.",
    "Tembak kepala itu menyenangkan. Dapatkan dirimu sendiri.",
    "Anda harus mencoba berenang dengan hiu putih besar.",
    "Anda harus mengecat diri Anda dengan warna merah dan berlari dalam bull marathon.",
    "Anda bisa tetap di bawah air selama sisa hidup Anda tanpa harus kembali lagi.",
    "Bagaimana kalau kamu berhenti bernapas selama 1 hari? Itu akan bagus.",
    "Cobalah memprovokasi harimau saat kalian berdua berada di dalam sangkar.",
    "Sudahkah Anda mencoba menembak diri Anda sendiri setinggi 100m menggunakan kanon.",
    "Anda harus mencoba menahan TNT di mulut Anda dan menyalakannya.",
    "Cobalah bermain menangkap dan melempar dengan RDX itu menyenangkan.",
    "Saya dengar phogine beracun tapi saya rasa Anda tidak keberatan menghirupnya untuk bersenang-senang.",
    "Luncurkan diri Anda ke luar angkasa sambil melupakan oksigen di Bumi.",
    "Kamu harus mencoba bermain ular tangga, dengan ular sungguhan dan tanpa tangga.",
    "Menari telanjang di beberapa kabel HT.",
    "Gunung Berapi Aktif adalah kolam renang terbaik untuk Anda.",
    "Anda harus mencoba mandi air panas di gunung berapi.",
    "Cobalah untuk menghabiskan satu hari di peti mati dan itu akan menjadi milikmu selamanya.",
    "Pukul Uranium dengan neutron yang bergerak lambat di hadapanmu. Ini akan menjadi pengalaman yang berharga.",
    "Anda bisa menjadi orang pertama yang menginjak matahari. Selamat mencoba.",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

IWIS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNS_STR = [
    "Berlari ke Thanos..",
    "Berlari jauh, jauh dari bumi..",
    "Berlari lebih cepat dari Bolt karena aku pengguna bot !!",
    "Berlari ke Mia Khalifa..",
    "Grup ini terlalu berbahaya untuk ditangani, aku harus lari.",
    "`Berlari Dari Orang Yang Bau Sawi 😬`",
    "Aku sangat lelah untuk berlari dan mengejarmu 💔",
    "Aku pergi dulu",
    "Saya hanya berjalan pergi, karena saya terlalu gemuk untuk lari.",
    "Saya Cape!",
    "Larii Disini Bau Sawii 😭",
    "Saya lari karena saya sangat gabut.",
    "Lari... \nkarena diet bukanlah pilihan.",
    "Berlari Cepat Dari Orang Gila",
    "Jika kamu ingin menangkapku, kamu harus cepat... \nJika kamu ingin tinggal bersamaku, kamu harus menjadi orang yang baik... \nTapi jika kamu ingin melewati aku... \nKamu pasti bercanda. ",
    "Siapapun dapat berlari seratus meter, itu hitungan empat puluh dua ribu dua ratus berikutnya.",
    "Mengapa semua orang ini mengikuti saya?",
    "Apakah anak-anak masih mengejarku?",
    "Berlari Sekencang Super Dede.. Apakah Sopan Begitu?",
]

CHASE_STR = [
    "Menurutmu kemana kamu akan pergi?",
    "Hah? Apa? Apakah mereka lolos?",
    "ZZzzZZzz... Hah? Apa? Oh, hanya mereka lagi, lupakan.",
    "Kembali kesini!",
    "Tidak terlalu cepat...",
    "Awas ke dinding!",
    "Jangan tinggalkan aku sendiri dengan mereka !!",
    "Kamu lari, kamu mati.",
    "Bercanda, aku ada dimana-mana",
    "Kamu akan menyesali itu ...",
    "Kamu juga bisa mencoba /kickme, kudengar itu menyenangkan.",
    "Ganggu orang lain, tidak ada yang peduli.",
    "Kamu bisa lari, tapi kamu tidak bisa bersembunyi.",
    "Apakah hanya itu yang kamu punya?",
    "Saya di belakang Anda...",
    "Anda punya teman!",
    "Kita bisa melakukan ini dengan cara mudah, atau cara sulit.",
    "Anda tidak mengerti, bukan?",
    "Ya, sebaiknya kau lari!",
    "Tolong, ingatkan saya apakah saya peduli?",
    "Aku akan lari lebih cepat jika jadi kamu.",
    "Itu pasti droid yang kami cari.",
    "Semoga peluang selalu menguntungkan Anda.",
    "Kata-kata terakhir yang terkenal.",
    "Dan mereka menghilang selamanya, tidak pernah terlihat lagi.",
    "Oh, lihat aku! Saya sangat keren, saya bisa lari dari bot orang ini",
    "Ya ya, cukup ketuk /kickme.",
    "Ini, ambil cincin ini dan pergilah ke Mordor saat kamu melakukannya.",
    "Legenda mengatakan, mereka masih berjalan...",
    "Tidak seperti Harry Potter, orang tuamu tidak bisa melindungimu dariku.",
    "Ketakutan menyebabkan kemarahan. Kemarahan mengarah pada kebencian. Kebencian menyebabkan penderitaan. Jika Anda terus berlari dalam ketakutan, Anda mungkin"
    "jadilah Vader berikutnya.",
    "Beberapa kalkulasi nanti, saya telah memutuskan minat saya pada kejahatan Anda tepat 0.",
    "Legenda mengatakan, mereka masih berjalan.",
    "Teruskan, kami tidak yakin kami menginginkanmu di sini.",
    "Kamu seorang penyihir- Oh. Tunggu. Kamu bukan Harry, terus bergerak.",
    "JANGAN BERLARI DI SINI!",
    "Hasta la vista, sayang.",
    "Siapa yang membiarkan anjing keluar?",
    "Ini lucu, karena tidak ada yang peduli.",
    "Ah, sayang sekali, Aku suka yang itu.",
    "Terus terang, sayangku, aku tidak peduli.",
    "Milkshake saya membawa semua anak laki-laki ke halaman... Jadi lari lebih cepat!",
    "Anda tidak bisa MENANGANI kebenaran!",
    "Dahulu kala, di galaksi yang sangat jauh... Seseorang akan peduli tentang itu, Tapi sekarang tidak lagi.",
    "Hei, lihat mereka! Mereka lari dari palu yang tak terelakkan... Manis.",
    "Han menembak lebih dulu, Aku juga.",
    "Apa yang kamu kejar, kelinci putih?",
    "Seperti yang dikatakan The Doctor... LARI!",
]

HELLOSTR = [
    "Hai!",
    "'Ello, bro!",
    "Apa itu crackin?",
    "Apa kabarmu?",
    "Halo, apa kabar, apa kabar!",
    "Halo, siapa di sana, saya sedang berbicara.",
    "Kamu tahu siapa ini.",
    "Yo!",
    "Wassup.",
    "Salam dan salam!",
    "Halo, sinar matahari!",
    "Hei, apa kabar, hai!",
    "Apa yang menendang, ayam kecil?",
    "Ciluk ba!",
    "Halo-bagus!",
    "Halo, mahasiswa baru!",
    "Saya datang dengan damai!",
    "Ahoy, sobat!",
    "Hiya!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES_EN = [
    "{hits} {victim} dengan {item}.",
    "{hits} {victim} di wajah dengan {item}.",
    "{hits} {victim} sekitar sedikit dengan {item}.",
    "{throws} {item} ke {Victim}.",
    "mengambil {item} dan {throws} ke wajah {victim}.",
    "Menusuk {victim} dengan tombak cinta.",
    "{throws} beberapa {item} ke {victim}.",
    "mengambil {item} dan {throws} ke wajah {victim}.",
    "meluncurkan {item} ke arah umum {korban}.",
    "duduk di wajah {victim} sambil membanting {item}.",
    "mulai menampar {victim} dengan konyol dengan {item}.",
    "pin {victim} ke bawah dan berulang kali {hits} mereka dengan {item}.",
    "mengambil {item} dan {hits} {victim} dengannya.",
    "mulai menampar {victim} dengan konyol dengan {item}.",
    "menahan {victim} dan berulang kali {hits} mereka dengan {item}.",
    "memukul {victim} dengan {item}.",
    "mengambil {item} dan {hits} {victim} dengannya.",
    "mengikat {victim} ke kursi dan {throws} {item} padanya.",
    "{hits} {victim} {where} dengan {item}.",
    "mengikat {victim} ke tiang dan mencambuk mereka {where} dengan {item}."
    "memberikan dorongan ramah untuk membantu {victim} belajar berenang di lahar.",
    "mengirim {victim} ke /laut /lahar.",
    "mengirim {victim} ke lubang memori.",
    "memenggal {victim}.",
    "melemparkan {victim} dari sebuah gedung.",
    "mengganti semua musik {victim} dengan lagu iri bilang bos.",
    "spam email {victim}.",
    "membuat {victim} depresi.",
    "menampar {victim} tanpa apa-apa.",
    "pukul {victim} dengan pesawat garuda.",
    "memukul kepala {victim}.",
    "taruh {victim} di tong sampah.",
    "Menendang {victim} dan melemparnya ke sungai.",
    "letakkan {victim} di rumah hantu.",
    "menampar {victim} dengan tongkat besi!",
]

ITEMS_EN = [
    "Tabung Gas",
    "Televisi 42 In",
    "Raket",
    "Raket Nyamuk",
    "Kaca",
    "Buku",
    "Ringgis",
    "Telur",
    "Jarum",
    "Monitor Tabung",
    "Obeng",
    "Almunium",
    "Emas",
    "Printer",
    "Speaker",
    "Gas Lpg",
    "Tangki Bensin",
    "Tandon Air",
    "Bola Boling",
    "Laptop",
    "Hardisk Rusak",
    "Wajan Panas",
    "Virus Corona",
    "Meja Kantor",
    "Meja Arsip",
    "Lemari",
    "Ember Besi",
    "Besi Beton",
    "Timah Panas",
    "Harimau",
    "Batu Krikil",
    "Makanan Basi",
    "Pesawat AirBus",
    "Roket Nasa",
    "Satelit Nasa",
    "Matahari",
    "Meteor",
    "Berkas Kantor",
    "Beton panas",
    "Cermin",
    "Batu Giok",
    "Botol",
    "Nezuko",
    "Kaset Pita",
    "Tiang Jemuran",
    "Pisau Lipat",
    "Bongkahan Es ",
    "Asteroid",
]

THROW_EN = [
    "melempar",
    "melemparkan",
]

HIT_EN = [
    "memukul",
    "menendang",
    "menampar",
    "memukul",
    "melempar",
]

WHERE_EN = ["di pipi", "di kepala", "di pantat", "di badan"]

SLAP_TEMPLATES_ID = [
    "{hits} {victim} dengan {item}.",
    "{throws} sebuah  {item} kepada {victim}.",
    "mengambil  {item} dan {hits} {victim} .",
    "Mengambil Sebuah {item} dan {hits} {victim} Dengan itu.",
    "Menjatuhkan {victim} Ke Lava.",
    "Mengirimkan {victim} ke Kawah.",
    "Membuang {victim} Ke Laut.",
    "Mengeluarkan {victim} Dari Bumi.",
    "Melempar {victim} Ke luar angkasa.",
    "Menaruh {victim} di Pluto.",
    "Melemparkan sebuah {item} ke {victim}.",
    "Melemparkan {item} kepada {victim}.",
    "Menampar {victim} menggunakan {item}.",
    "Membuang {victim} Ke udara.",
    "Menghapus {victim} Dari Daftar Teman.",
    "Melemparkan {item} {where} {victim}.",
    "Meletakan {item} {where} {victim}.",
    "Menyerang {victim} menggunakan {anime}.",
    "Mengehack Seluruh akun {victim}",
]

ITEMS_ID = [
    "Tabung Gas",
    "Televisi 42 In",
    "Raket",
    "Raket Nyamuk",
    "Kaca",
    "Buku",
    "Ringgis",
    "Telur",
    "Jarum",
    "Monitor Tabung",
    "Obeng",
    "Almunium",
    "Emas",
    "Printer",
    "Speaker",
    "Gas Lpg",
    "Tangki Bensin",
    "Tandon Air",
    "Bola Boling",
    "Laptop",
    "Hardisk Rusak",
    "Wajan Panas",
    "Virus Corona",
    "Meja Kantor",
    "Meja Arsip",
    "Lemari",
    "Ember Besi",
    "Besi Beton",
    "Timah Panas",
    "Harimau",
    "Batu Krikil",
    "Makanan Basi",
    "Pesawat AirBus",
    "Roket Nasa",
    "Satelit Nasa",
    "Matahari",
    "Meteor",
    "Berkas Kantor",
    "Beton panas",
    "Cermin",
    "Batu Giok",
    "Botol",
    "Nezuko",
    "Kaset Pita",
    "Tiang Jemuran",
    "Pisau Lipat",
    "Bongkahan Es ",
    "Asteroid",
]

THROW_ID = [
    "Melempar",
    "Melemparkan",
]

HIT_ID = [
    "Memukul",
    "melemparkan",
    "Memukuli",
]

WHERE_ID = ["di pipi", "di kepala", "di bokong", "di badan"]


SLAP_TEMPLATES_Jutsu = [
    "Menyerang {victim} Menggunakan {hits}.",
    "Menyerang {victim} Menggunakan {item}.",
    "Melemparkan {throws} kepada {victim} .",
    "Melemparkan {throws} {where} {victim}.",
]

ITEMS_Jutsu = [
    "KAA MEE HAA MEE HAA",
    "Chibaku Tensei",
]

THROW_Jutsu = [
    "Futon Rasen Shuriken",
    "Shuriken",
]

HIT_Jutsu = [
    "Rasengan",
    "Chidori",
]

GAMBAR_TITIT = """
😋😋
😋😋😋
  😋😋😋
    😋😋😋
     😋😋😋
       😋😋😋
        😋😋😋
         😋😋😋
          😋😋😋
          😋😋😋
      😋😋😋😋
 😋😋😋😋😋😋
 😋😋😋  😋😋😋
    😋😋       😋😋
"""

GAMBAR_OK = """
░▐▀▀▀▀▀▀▀▀▌▐▀▌▄▄▄▀▀▓▀
░▐▌▓▀▀▀▀▓▌▌▐▐▌▀▌▄▄▀░░
░▐▐▌▐▀▀▌▐▐▌▐▌▐▓▄▀░░░░
░▐▌▌▐▄▄▌▐▌▌▐▐▌▓▀▄░░░░
░▐▐▓▄▄▄▄▓▐▌▐▌▌▄▌▀▀▄░░
░▐▄▄▄▄▄▄▄▄▌▐▄▌▀▀▀▄▄▓▄
"""


GAMBAR_TENGKORAK = """
░░░░░░░░░░░░░▄▐░░░░
░░░░░░░▄▄▄░░▄██▄░░░
░░░░░░▐▀█▀▌░░░░▀█▄░
░░░░░░▐█▄█▌░░░░░░▀█▄
░░░░░░░▀▄▀░░░▄▄▄▄▄▀▀
░░░░░▄▄▄██▀▀▀▀░░░░░
░░░░█▀▄▄▄█░▀▀░░░░░░
░░░░▌░▄▄▄▐▌▀▀▀░░░░░
░▄░▐░░░▄▄░█░▀▀░░░░░
░▀█▌░░░▄░▀█▀░▀░░░░░
░░░░░░░░▄▄▐▌▄▄░░░░░
░░░░░░░░▀███▀█▄░░░░
░░░░░░░▐▌▀▄▀▄▀▐░░░░
░░░░░░░▐▀░░░░░░▐▌░░
░░░░░░░█░░░░░░░░█░░
░░░░░░▐▌░░░░░░░░░█░
"""

GAMBAR_KONTL = """
⣠⡶⠚⠛⠲⢄⡀
⣼⠁ ⠀⠀⠀ ⠳⢤⣄
⢿⠀⢧⡀⠀⠀⠀⠀⠀⢈⡇
⠈⠳⣼⡙⠒⠶⠶⠖⠚⠉⠳⣄
⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄
⠀⠀⠀⠘⣆ ⠀⠀⠀⠀ ⠀⠈⠓⢦⣀
⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⢤
⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧
⠀⠀⠀⠀⠀⠀⠀⡴⠋⠓⠦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠈⣇
⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄
⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃
⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⢦⣀⣀⣀⣀⣠⡴⠚⠁⠉⠉⠉
"""


WHERE_Jutsu = ["Di Pipi", "Di Kepala", "Di Bokong", "Di Badan ,Di Pantat"]

normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]

# ===========================================


@bot.on(man_cmd(outgoing=True, pattern=r"(\w+)say (.*)"))
async def _(cowmsg):
    """For .cowsay module, userbot wrapper for cow which says things."""
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@bot.on(man_cmd(outgoing=True, pattern=r"coinflip (.*)"))
async def _(event):
    r = choice(["Kepala", "Ekor"])
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r == "Kepala":
        if input_str == "Kepala":
            await event.edit("Koin Itu Mendarat Di: **Kepala**.\nKamu Benar.")
        elif input_str == "Ekor":
            await event.edit(
                "Koin Itu Mendarat Di: **Kepala**.\nKamu Salah, Coba Lagi..."
            )
        else:
            await event.edit("Koin Itu Mendarat Di: **Kepala**.")
    elif r == "Ekor":
        if input_str == "Ekor":
            await event.edit("Koin Itu Mendarat Di: **Ekor**.\nKamu Benar.")
        elif input_str == "Kepala":
            await event.edit(
                "Koin Itu Mendarat Di: **Ekor**.\nKamu Salah, Coba Lagi..."
            )
        else:
            await event.edit("Koin Itu Mendarat Di: **Ekor**.")


@bot.on(man_cmd(pattern=r"slap(?: |$)(.*)", outgoing=True))
async def _(event):
    """slaps a user, or get slapped if not a reply."""
    replied_user = await get_user_from_event(event)
    if replied_user:
        replied_user = replied_user[0]
    else:
        return
    caption = await slap(replied_user, event)

    try:
        await event.edit(caption)

    except BaseException:
        await event.edit(
            "`Tidak bisa slap orang ini, perlu mengambil beberapa meteor dan batu!`"
        )


async def slap(replied_user, event):
    """Construct a funny slap sentence !!"""
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"
    slap_str = event.pattern_match.group(1)
    if slap_str == "en" or slap_str not in ["id", "jutsu"]:
        temp = choice(SLAP_TEMPLATES_EN)
        item = choice(ITEMS_EN)
        hit = choice(HIT_EN)
        throw = choice(THROW_EN)
        where = choice(WHERE_EN)
    elif slap_str == "id":
        temp = choice(SLAP_TEMPLATES_ID)
        item = choice(ITEMS_ID)
        hit = choice(HIT_ID)
        throw = choice(THROW_ID)
        where = choice(WHERE_ID)
    else:
        temp = choice(SLAP_TEMPLATES_Jutsu)
        item = choice(ITEMS_Jutsu)
        hit = choice(HIT_Jutsu)
        throw = choice(THROW_Jutsu)
        where = choice(WHERE_Jutsu)
    return "..." + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw, where=where
    )


@bot.on(man_cmd(outgoing=True, pattern=r"tt(?: |$)(.*)"))
async def _(e):
    await e.edit("`Mencari Gambar tt, Dosa ditanggung sendiri...`")
    await sleep(3)
    await e.edit("`Mengirim Gambar tt...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve("http://media.oboobs.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "boobs.jpg")
    await e.client.send_file(e.chat_id, "boobs.jpg")
    os.remove("boobs.jpg")
    await e.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"pantat(?: |$)(.*)"))
async def _(e):
    await e.edit("`Mencari Gambar Pantat, Dosa ditanggung sendiri...`")
    await sleep(3)
    await e.edit("`Mengirim Gambar Pantat Indah...`")
    nsfw = requests.get("http://api.obutts.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve("http://media.obutts.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "butts.jpg")
    await e.client.send_file(e.chat_id, "butts.jpg")
    os.remove("butts.jpg")
    await e.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"(yes|no|maybe|decide)$"))
async def _(event):
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id or None
    if decision != "decide":
        r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = requests.get("https://yesno.wtf/api").json()
    await event.delete()
    await event.client.send_message(
        event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"]
    )


@bot.on(man_cmd(outgoing=True, pattern=r";_;$"))
async def _(idk):
    t = ";_;"
    for _ in range(10):
        t = t[:-1] + "_;"
        await idk.edit(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fp$"))
async def _(palm):
    """Facepalm  🤦‍♂"""
    await palm.edit("🤦‍♂")


@bot.on(man_cmd(outgoing=True, pattern=r"cry$"))
async def _(e):
    """y u du dis, i cry everytime !!"""
    await e.edit(choice(CRI))


@bot.on(man_cmd(outgoing=True, pattern=r"insult$"))
async def _(e):
    """I make you cry !!"""
    await e.edit(choice(INSULT_STRINGS))


@bot.on(man_cmd(outgoing=True, pattern=r"cp(?: |$)(.*)"))
async def _(cp_e):
    """Copypasta the famous meme"""
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await cp_e.edit(
            "`😂🅱️AhHH👐MaNtAp👅Bro👅UnTuk✌️MeMbuAT👌Ku👐TeRliHat👀LuCu💞HaHAhaA!💦`"
        )

    reply_text = choice(EMOJIS)
    # choose a random character in the message to be substituted with 🅱️
    b_char = choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += choice(EMOJIS)
        elif owo in EMOJIS:
            reply_text += owo
            reply_text += choice(EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🅱️"
        else:
            reply_text += owo.upper() if bool(getrandbits(1)) else owo.lower()
    reply_text += choice(EMOJIS)
    await cp_e.edit(reply_text)


@bot.on(man_cmd(outgoing=True, pattern=r"vapor(?: |$)(.*)"))
async def _(vpr):
    """Vaporize everything!"""
    reply_text = []
    textx = await vpr.get_reply_message()
    message = vpr.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await vpr.edit("`B e r i k a n S e b u a h T e k s U n t u k Vａｐｏｒ！`")

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await vpr.edit("".join(reply_text))


@bot.on(man_cmd(outgoing=True, pattern=r"str(?: |$)(.*)"))
async def _(stret):
    """Stretch it."""
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await stret.edit("`Beriiiiiiiiikaaannnn sebuuuuuuuuuah teeeeeeeks!`")

    count = randint(3, 10)
    reply_text = sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), message)
    await stret.edit(reply_text)


@bot.on(man_cmd(outgoing=True, pattern=r"zal(?: |$)(.*)"))
async def _(zgfy):
    """Invoke the feeling of chaos."""
    reply_text = []
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await zgfy.edit(
            "`b̜́ͨe͒͜r̠͂ͬi̷̱̋k͖͒ͤa̋ͫ͑n͕͂͗ t̢͘͟e͂̽̈́k͎͂͠s̤͚ͭ m̪͔͑è͜͡n͈ͮḁ͞ͅk̲̮͛u̺͂ͩt̬̗́k͍̙̮á ̺n̨̹ͪ`"
        )

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(3):
            rand = randint(0, 2)

            if rand == 0:
                charac = charac.strip() + choice(ZALG_LIST[0]).strip()
            elif rand == 1:
                charac = charac.strip() + choice(ZALG_LIST[1]).strip()
            else:
                charac = charac.strip() + choice(ZALG_LIST[2]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))


@bot.on(man_cmd(outgoing=True, pattern=r"hi$"))
async def _(hello):
    """Greet everyone!"""
    await hello.edit(choice(HELLOSTR))


@bot.on(man_cmd(outgoing=True, pattern=r"owo(?: |$)(.*)"))
async def _(owo):
    """UwU"""
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await owo.edit("` Mohon Berikan Teks UwU! `")

    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(UWUS)
    await owo.edit(reply_text)


@bot.on(man_cmd(outgoing=True, pattern=r"react$"))
async def _(react):
    """Make your userbot react to everything."""
    await react.edit(choice(FACEREACTS))


@bot.on(man_cmd(outgoing=True, pattern=r"shg$"))
async def _(shg):
    r"""¯\_(ツ)_/¯"""
    await shg.edit(choice(SHGS))


@bot.on(man_cmd(outgoing=True, pattern=r"chase$"))
async def _(chase):
    """Lari bro lari, aku akan segera menangkapmu !!"""
    await chase.edit(choice(CHASE_STR))


@bot.on(man_cmd(outgoing=True, pattern=r"run$"))
async def _(run):
    """Lari, lari, LARIII!"""
    await run.edit(choice(RUNS_STR))


@bot.on(man_cmd(outgoing=True, pattern=r"metoo$"))
async def _(hahayes):
    """Haha yes"""
    await hahayes.edit(choice(METOOSTR))


@bot.on(man_cmd(outgoing=True, pattern=r"oem$"))
async def _(e):
    t = "Oem"
    for _ in range(16):
        t = t[:-1] + "em"
        await e.edit(t)


@bot.on(man_cmd(outgoing=True, pattern=r"Oem$"))
async def _(e):
    t = "Oem"
    for _ in range(16):
        t = t[:-1] + "em"
        await e.edit(t)


@bot.on(man_cmd(outgoing=True, pattern=r"10iq$"))
async def _(e):
    await e.edit("♿")


@bot.on(man_cmd(outgoing=True, pattern=r"fuck$"))
async def _(e):
    await e.edit(".                       /¯ )")
    await e.edit(".                       /¯ )\n                      /¯  /")
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ "
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              ("
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  "
    )


@bot.on(man_cmd(outgoing=True, pattern=r"moon$"))
async def _(moone):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await moone.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"bunga$"))
async def _(event):
    deq = deque(list("🌼🌻🌺🌹🌸🌷"))
    try:
        for _ in range(35):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"waktu$"))
async def _(event):
    deq = deque(list("🎑🌄🌅🌇🌆🌃🌌"))
    try:
        for _ in range(100):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"buah$"))
async def _(event):
    deq = deque(list("🍉🍓🍇🍎🍍🍐🍌"))
    try:
        for _ in range(35):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"clock$"))
async def _(event):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"rain$"))
async def _(event):
    deq = deque(list("☀️🌤⛅️🌥☁️🌧⛈"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"boxes$"))
async def _(event):
    deq = deque(list("🟥🟧🟨🟩🟦🟪🟫⬛⬜"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"hmm$"))
async def _(event):
    deq = deque(list("🤔🧐🤔🧐🤔🧐"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"haha$"))
async def _(event):
    deq = deque(list("😂🤣😂🤣😂🤣"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"operations$"))
async def _(event):
    deq = deque(list("!@#$%^&*()_+="))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"love$"))
async def _(event):
    deq = deque(list("❤️🧡💛💚💙💜🖤💕💞💓💗💖💘💝"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"earth$"))
async def _(event):
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"hati$"))
async def _(event):
    deq = deque(list("🖤💜💙💚💛🧡❤️🤍"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=".monyet$"))
async def _(event):
    deq = deque(list("🙈🙉🙈🙉🙈🙉🙈🙉"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=".emo$"))
async def _(event):
    deq = deque(list("🙂😁😄😃😂🤣😭🐵🙊🙉🙈"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@bot.on(man_cmd(outgoing=True, pattern=r"mock(?: |$)(.*)"))
async def _(mock):
    """Do it and find the real fun."""
    reply_text = []
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await mock.edit("`bEriKan PeSan UnTuK MoCk!`")

    for charac in message:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))


@bot.on(man_cmd(outgoing=True, pattern=r"weeb(?: |$)(.*)"))
async def _(e):
    args = e.pattern_match.group(1)
    if not args:
        get = await e.get_reply_message()
        args = get.text
    if not args:
        await e.edit("`Apa Yang Anda Lakukan?`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await e.edit(string)


@bot.on(man_cmd(outgoing=True, pattern=r"clap(?: |$)(.*)"))
async def _(memereview):
    """Praise people!"""
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await memereview.edit("`Balas Ke Pesan Orang Yang Ingin Anda Puji ツ`")
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@bot.on(man_cmd(outgoing=True, pattern=r"teksbiru$"))
async def _(bt_e):
    """Believe me, you will find this useful."""
    if await bt_e.get_reply_message() and bt_e.is_group:
        await bt_e.edit(
            "/TEKSBIRU /APAKAH /ANDA.\n"
            "/SEDANG /GABUT /KARNA /TERTARIK /MELIHAT /TEKS /BIRU /PASTI /ANDA /BOSAN?"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"f (.*)"))
async def _(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8,
        paytext * 8,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 6,
        paytext * 6,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
    )
    await event.edit(pay)


@bot.on(man_cmd(outgoing=True, pattern=r"lfy (.*)"))
async def _(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {"format": "json", "url": lfy_url}
    r = requests.get("http://is.gd/create.php", params=payload)
    await lmgtfy_q.edit(
        "Ini Dia, Bantu Dirimu Sendiri." f"\n[{query}]({r.json()['shorturl']})"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"-_-$"))
async def _(sigh):
    """Ok..."""
    okay = "-_-"
    for _ in range(10):
        okay = okay[:-1] + "_-"
        await sigh.edit(okay)


@bot.on(man_cmd(outgoing=True, pattern=r"sayhi$"))
async def _(e):
    await e.edit(
        "\n💰💰💰💰💰💰💰💰💰💰💰💰"
        "\n💰🔷💰💰💰🔷💰💰🔷🔷🔷💰"
        "\n💰🔷💰💰💰🔷💰💰💰🔷💰💰"
        "\n💰🔷💰💰💰🔷💰💰💰🔷💰💰"
        "\n💰🔷🔷🔷🔷🔷💰💰💰🔷💰💰"
        "\n💰🔷💰💰💰🔷💰💰💰🔷💰💰"
        "\n💰🔷💰💰💰🔷💰💰💰🔷💰💰"
        "\n💰🔷💰💰💰🔷💰💰🔷🔷🔷💰"
        "\n💰💰💰💰💰💰💰💰💰💰💰💰"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"scam(?:\s|$)([\s\S]*)"))
async def _(event):
    options = [
        "typing",
        "contact",
        "game",
        "location",
        "voice",
        "round",
        "video",
        "photo",
        "document",
        "cancel",
        "sticker",
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(300, 360)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(300, 360)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await edit_delete(event, "**Masukan jumlah detik yang benar !!**", 120)
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@bot.on(man_cmd(pattern=r"type(?: |$)(.*)", outgoing=True))
async def _(typew):
    """Just a small command to make your keyboard become a typewriter!"""
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await typew.edit("`Berikan Sebuah Teks Untuk Type!`")
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)


@bot.on(man_cmd(outgoing=True, pattern=r"f (.*)"))
async def _(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8,
        paytext * 8,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 6,
        paytext * 6,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
    )
    await event.edit(pay)


@bot.on(man_cmd(outgoing=True, pattern=r"fail$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ `"
            "`\n████▌▄▌▄▐▐▌█████ `"
            "`\n████▌▄▌▄▐▐▌▀████ `"
            "`\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"lol$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n╱┏┓╱╱╱╭━━━╮┏┓╱╱╱╱ `"
            "`\n╱┃┃╱╱╱┃╭━╮┃┃┃╱╱╱╱ `"
            "`\n╱┃┗━━┓┃╰━╯┃┃┗━━┓╱ `"
            "`\n╱┗━━━┛╰━━━╯┗━━━┛╱ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"rock$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n┈╭╮┈┈┈┈┈┈┈┈┈┈┈┈ `"
            "`\n┈┃┃┈╭╮┈┏╮╭╮╭╮┃╭ `"
            "`\n┈┃┃┈┃┃┈┣┫┃┃┃┈┣┫ `"
            "`\n┈┃┣┳┫┃┈┃╰╰╯╰╯┃╰ `"
            "`\n╭┻┻┻┫┃┈┈╭╮┃┃━┳━ `"
            "`\n┃╱╭━╯┃┈┈┃┃┃┃┈┃┈ `"
            "`\n╰╮╱╱╱┃┈┈╰╯╰╯┈┃┈ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"lool$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n╭╭━━━╮╮┈┈┈┈┈┈┈┈┈┈\n┈┃╭━━╯┈┈┈┈▕╲▂▂╱▏┈\n┈┃┃╱▔▔▔▔▔▔▔▏╱▋▋╮┈`"
            "`\n┈┃╰▏┃╱╭╮┃╱╱▏╱╱▆┃┈\n┈╰━▏┗━╰╯┗━╱╱╱╰┻┫┈\n┈┈┈▏┏┳━━━━▏┏┳━━╯┈`"
            "`\n┈┈┈▏┃┃┈┈┈┈▏┃┃┈┈┈┈ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"stfu$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n██████████████████████████████`"
            "`\n██▀▀▀▀████▀▀▀▀████▀▀▀▀▀███▀▀██▀▀█`"
            "`\n█──────██──────██───────██──██──█`"
            "`\n█──██▄▄████──████──███▄▄██──██──█`"
            "`\n█▄────▀████──████────█████──██──█`"
            "`\n█▀▀██──████──████──███████──██──█`"
            "`\n█──────████──████──███████──────█`"
            "`\n██▄▄▄▄█████▄▄████▄▄████████▄▄▄▄██`"
            "`\n█████████████████████████████████`"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"gtfo$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n███████████████████████████████ `"
            "`\n█▀▀▀▀▀▀▀█▀▀▀▀▀▀█▀▀▀▀▀▀▀█▀▀▀▀▀▀█ `"
            "`\n█───────█──────█───────█──────█ `"
            "`\n█──███──███──███──███▄▄█──██──█ `"
            "`\n█──███▄▄███──███─────███──██──█ `"
            "`\n█──██───███──███──██████──██──█ `"
            "`\n█──▀▀▀──███──███──██████──────█ `"
            "`\n█▄▄▄▄▄▄▄███▄▄███▄▄██████▄▄▄▄▄▄█ `"
            "`\n███████████████████████████████ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"nih$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n(\\_/)`"
            "`\n(●_●)`"
            "`\n />💖 *Ini Buat Kamu`"
            "\n                    \n"
            r"`(\_/)`"
            "`\n(●_●)`"
            "`\n💖<\\  *Tapi Bo'ong`"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"fag$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n█████████`"
            "`\n█▄█████▄█`"
            "`\n█▼▼▼▼▼`"
            "`\n█       STFU FAGGOT'S`"
            "`\n█▲▲▲▲▲`"
            "`\n█████████`"
            "`\n ██   ██`"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"tai$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("\n{\\__/}" "\n(●_●)" "\n( >💩 Mau Tai Ku?")


@bot.on(man_cmd(outgoing=True, pattern=r"paw$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`(=ↀωↀ=)")


@bot.on(man_cmd(outgoing=True, pattern=r"tf$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("(̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄  ")


@bot.on(man_cmd(outgoing=True, pattern=r"gey$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
            "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
            "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈Lu Bau Hehe`"
            "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"gay$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
            "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
            "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈ANDA GAY`"
            "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"bot$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "` \n   ╲╲╭━━━━╮ \n╭╮┃▆┈┈▆┃╭╮ \n┃╰┫▽▽▽┣╯┃ \n╰━┫△△△┣━╯`"
            "`\n╲╲┃┈┈┈┈┃  \n╲╲┃┈┏┓┈┃ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"hey$"))
async def hey(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "\n┈┈┈╱▔▔▔▔╲┈╭━━━━━\n┈┈▕▂▂▂▂▂▂▏┃HEY!┊😀`"
            "`\n┈┈▕▔▇▔▔┳▔▏╰┳╮HEY!┊\n┈┈▕╭━╰╯━╮▏━╯╰━━━\n╱▔▔▏▅▅▅▅▕▔▔╲┈┈┈┈`"
            "`\n▏┈┈╲▂▂▂▂╱┈┈┈▏┈┈┈`"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"nou$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n┈╭╮╭╮\n┈┃┃┃┃\n╭┻┗┻┗╮`"
            "`\n┃┈▋┈▋┃\n┃┈╭▋━╮━╮\n┃┈┈╭╰╯╰╯╮`"
            "`\n┫┈┈  NoU\n┃┈╰╰━━━━╯`"
            "`\n┗━━┻━┛`"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"iwi(?: |$)(.*)"))
async def _(siwis):
    """IwI"""
    textx = await siwis.get_reply_message()
    message = siwis.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await siwis.edit("` Anda Harus Memberikan Teks Ke IwI  `")
        return

    reply_text = sub(r"(a|i|u|e|o)", "i", message)
    reply_text = sub(r"(A|I|U|E|O)", "I", reply_text)
    reply_text = sub(r"\!+", " " + choice(IWIS), reply_text)
    reply_text += " " + choice(IWIS)
    await siwis.edit(reply_text)


@bot.on(man_cmd(outgoing=True, pattern=r"koc$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("8✊===D")
        await e.edit("8=✊==D")
        await e.edit("8==✊=D")
        await e.edit("8===✊D")
        await e.edit("8==✊=D")
        await e.edit("8=✊==D")
        await e.edit("8✊===D")
        await e.edit("8=✊==D")
        await e.edit("8==✊=D")
        await e.edit("8===✊D")
        await e.edit("8==✊=D")
        await e.edit("8=✊==D")
        await e.edit("8✊===D")
        await e.edit("8=✊==D")
        await e.edit("8==✊=D")
        await e.edit("8===✊D")
        await e.edit("8==✊=D")
        await e.edit("8=✊==D")
        await e.edit("8===✊D💦")
        await e.edit("8==✊=D💦💦")
        await e.edit("8=✊==D💦💦💦")
        await e.edit("8✊===D💦💦💦💦")
        await e.edit("8===✊D💦💦💦💦💦")
        await e.edit("8==✊=D💦💦💦💦💦💦")
        await e.edit("8=✊==D💦💦💦💦💦💦💦")
        await e.edit("8✊===D💦💦💦💦💦💦💦💦")
        await e.edit("8===✊D💦💦💦💦💦💦💦💦💦")
        await e.edit("8==✊=D💦💦💦💦💦💦💦💦💦💦")
        await e.edit("8=✊==D Lah Kok Habis?")
        await e.edit("😭😭😭😭")


@bot.on(man_cmd(outgoing=True, pattern=".gas$"))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("___________________🚑")
        await e.edit("________________🚑___")
        await e.edit("______________🚑_____")
        await e.edit("___________🚑________")
        await e.edit("________🚑___________")
        await e.edit("_____🚑______________")
        await e.edit("__🚑_________________")
        await e.edit("🚑___________________")
        await e.edit("_____________________")
        await e.edit(choice(FACEREACTS))


@bot.on(man_cmd(outgoing=True, pattern=r"shg$"))
async def _(shg):
    r"""¯\_(ツ)_/¯"""
    await shg.edit(choice(SHGS))


@bot.on(man_cmd(outgoing=True, pattern=r"(?:penis|dick)\s?(.)?"))
async def _(e):
    emoji = e.pattern_match.group(1)
    titid = GAMBAR_TITIT
    if emoji:
        titid = titid.replace("😋", emoji)
    await e.edit(titid)


@bot.on(man_cmd(outgoing=True, pattern=r"(?:kontol)\s?(.)?"))
async def _(e):
    emoji = e.pattern_match.group(1)
    kontl = GAMBAR_KONTL
    if emoji:
        kontl = kontl.replace("😂", emoji)
    await e.edit(kontl)


@bot.on(man_cmd(outgoing=True, pattern=r"skull$"))
async def _(e):
    emoji = e.pattern_match.group(1)
    tengkorak = GAMBAR_TENGKORAK
    if emoji:
        tengkorak = tengkorak.replace("😂", emoji)
    await e.edit(tengkorak)


CMD_HELP.update(
    {
        "memes": f">`{cmd}cowsay`"
        "\nUsage: sapi yang mengatakan sesuatu."
        f"\n\n> {cmd}cp"
        "\nUsage: Copy paste meme terkenal"
        f"\n\n>`{cmd}vapor`"
        "\nUsage: Menguapkan semuanya!"
        f"\n\n>`{cmd}str`"
        "\nUsage: Regangkan."
        f"\n\n>`{cmd}10iq`"
        "\nUsage: Kamu mundur !!"
        f"\n\n>`{cmd}zal`"
        "\nUsage: Munculkan perasaan kacau."
        f"\n\n>`{cmd}Oem`"
        "\nPenggunaan: Oeeeem"
        f"\n\n>`{cmd}fp`"
        "\nUsage: Telapak Tangan:P"
        f"\n\n>`{cmd}moon`"
        "\nUsage: animasi bulan."
        f"\n\n>`{cmd}clock`"
        "\nUsage: animasi jam."
        f"\n\n>`{cmd}hi`"
        "\nUsage: Sapa semuanya!"
        f"\n\n>`{cmd}coinflip` <Kepala/Ekor>"
        "\nUsage: Melempar koin !!"
        f"\n\n>`{cmd}owo`"
        "\nUsage: UwU"
        f"\n\n>`{cmd}react`"
        "\nUsage: Buat Userbot Anda bereaksi terhadap semuanya."
        f"\n\n>`{cmd}slap`"
        "\nUsage: balas tampar mereka dengan benda acak !!"
        f"\n\n>`{cmd}cry`"
        "\nUsage: jika kamu melakukan ini, aku akan menangis."
        f"\n\n>`{cmd}shg`"
        "\nUsage: Angkat bahu!"
        f"\n\n>`{cmd}run`"
        "\nUsage: Biarkan Aku Lari, Lari, LARI!"
        f"\n\n>`{cmd}chase`"
        "\nUsage: Sebaiknya Anda mulai berlari"
        f"\n\n>`{cmd}metoo`"
        "\nUsage: Haha ya"
        f"\n\n>`{cmd}mock`"
        "\nUsage: Lakukan dan temukan kesenangan yang sesungguhnya."
        f"\n\n>`{cmd}clap`"
        "\nUsage: Puji orang!"
        f"\n\n>`{cmd}f` <emoji/karakter>"
        "\nUsage: F."
        f"\n\n>`{cmd}bt`"
        "\nUsage: Percayalah, Anda akan menemukan ini berguna."
        f"\n\n>`{cmd}weeb`"
        "\nUsage: Untuk Mengubah Teks Menjadi Weeb-ify."
        f"\n\n>`{cmd}type` <teks>"
        "\nUsage: Hanya perintah kecil untuk membuat keyboard Anda menjadi mesin tik!"
        f"\n\n>`{cmd}lfy` <query>"
        "\nUsage: Biar saya Google itu untuk Anda dengan cepat!"
        f"\n\n>`{cmd}decide` [Alternatif: ({cmd}yes, {cmd}no, {cmd}maybe)]"
        "\nUsage: Buat keputusan cepat."
        f"\n\n> `{cmd}nou` `{cmd}bot` `{cmd}rock` `{cmd}gey` `{cmd}tf` `{cmd}paw` `{cmd}ai` `{cmd}nih`"
        f"\n> `{cmd}ag` `{cmd}tfo`; `{cmd}stfu` `{cmd}lol` `{cmd}lool` `{cmd}fail` `{cmd}leave`"
        f"\n> `{cmd}iwi` `{cmd}sayhi` `{cmd}koc` `{cmd}gas` `{cmd}earth` `{cmd}love` `{cmd}rain`"
        f"\n> `{cmd}penis` `{cmd}emo` `{cmd}fuck` `{cmd}skull`  `{cmd}monyet` `{cmd}haha` `{cmd}hmm` `{cmd}boxes` `.-_-` `;_;`\nUsage: Cobain aja"
        "\n"
    }
)


CMD_HELP.update(
    {
        "scam": f"**Plugin : **`scam`\
        \n\n  •  **Syntax :** `{cmd}scam` <action> <detik>\
        \n  •  **Function : **Untuk menunjukkan tindakan palsu dengan jangka waktu (sama seperti fakeaction)\
        \n  •  **List Action :** `typing`, `contact`, `game`, `location`, `voice`, `round`, `video`, `photo`, `document`\
\
    "
    }
)
