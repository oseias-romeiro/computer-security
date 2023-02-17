import string, unicodedata, sys

import VgBreaker
from Vigenere import Viginere


#SYMBOLS = string.printable
SYMBOLS = string.ascii_lowercase
args = sys.argv[1:]
viginere = Viginere(SYMBOLS)

def trait_msg(msg:str):
    unicode = unicodedata.normalize('NFKD', msg.lower())
    return unicode.encode('ASCII','ignore').decode('ASCII')

# Viginere Cipher
def vg_enc(key, msg_file='files/message.txt'):

    msg = trait_msg(open(msg_file, 'r').read())
    enc_file = open('files/encripted.txt', 'w')
    
    keystream = viginere.gen(key, msg)
    encripted = viginere.enc(keystream, msg)

    enc_file.write(encripted)
    enc_file.close()

    print('saved: files/encripted.txt')

def vg_dec(key, enc_file='files/encripted.txt'):
    encripted = open(enc_file, 'r').read()
    dec_file = open('files/decripted.txt', 'w')

    keystream = viginere.gen(key, encripted)
    decripted = viginere.dec(keystream, encripted)

    dec_file.write(decripted)
    dec_file.close()

    print('saved: files/decripted.txt')

# breake password
def vg_break(enc_file='files/encripted.txt', lang:str="pt"):
    with open(enc_file, 'r') as ciphertext:
        enc_msg = ciphertext.read()
        key = VgBreaker.breaker(enc_msg, lang, SYMBOLS)
        
        print("key:", key)

# arguments
if(len(args) == 2):
    if(args[1] == '-e'):
        vg_enc(args[0])
    elif(args[1] == '-d'):
        vg_dec(args[0])
    elif(args[0] == '-b'):
        vg_break(lang=args[1])
elif(len(args) == 3):
    if(args[1] == '--enc'):
        vg_enc(args[0], args[2])
    elif(args[1] == '--dec'):
        vg_dec(args[0], args[2])
    elif(args[0] == '--break'):
        vg_break(args[1], args[2])

