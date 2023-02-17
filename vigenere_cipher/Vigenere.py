import string

class Help:
    def vrfy_key(self, msg:str, key:str):
        if len(msg) != len(key): raise Exception(
            "Message and key must be the same size!"
        )
        
    def enumerate(self, msg:str, symb:str) -> list: 
        list_enum=[]
        i=0
        for m in msg:
            list_enum.append((i, m))
            if m in symb: i+=1
        return list_enum

class Cipher(Help):
    SYMBOLS: str
    SYMBOLS_SIZE: int

    def __init__(self, symbols) -> None:
        self.SYMBOLS = symbols
        self.SYMBOLS_SIZE = len(symbols)

    def encode(self, letter:str, key_index:int) -> str:
        return self.SYMBOLS[((self.SYMBOLS.find(letter) + key_index) % self.SYMBOLS_SIZE)]

    def decode(self, letter:str, key_index:int) -> str:
        return self.SYMBOLS[((self.SYMBOLS.find(letter) - key_index) % self.SYMBOLS_SIZE)]

class Viginere(Cipher):

    def __init__(self, symbols:str=string.ascii_lowercase) -> None:
        super().__init__(symbols)

    def gen(self, key:str, message:str) -> str:
        key_size = len(key)

        return "".join(
            key[i % key_size]
            for i in range(0, len(message))
        )

    def enc(self, keystream:str, message:str) -> str:
        self.vrfy_key(message, keystream)

        return "".join(
            self.encode(l, self.SYMBOLS.find(keystream[i]))
            if (l in self.SYMBOLS) else l
            for i,l in self.enumerate(message, self.SYMBOLS)
        )

    def dec(self, keystream:str, ciphertext:str) -> str:
        self.vrfy_key(ciphertext, keystream)

        return "".join(
            self.decode(l, self.SYMBOLS.find(keystream[i]))
            if (l in self.SYMBOLS) else l
            for i,l in self.enumerate(ciphertext, self.SYMBOLS)
        )
