import random, math
import help.primes as primes
import help.OAEP as OAEP
import help.CryptoMath as CryptoMath

class RSA:
    # primes
    __P,__Q = 2,2
    '''
    __P = 170154366828665079503315635359566390626153860097410117673698414542663355444709893966571750073322692712277666971313348160841835991041384679700511912064982526249529596585220499141442747333138443745082395711957231040341599508490720584345044145678716964326909852653412051765274781142172235546768485104821112642811
    __Q = 159583602958039405615121610278862711974086733649430958014239114349376429231073294711764202020091171128241325042077687323980541085258761716715932983241093544925202176467889841897288518279778652818272552873132853474893858682322728473745028210646540402114928787347563800658303202168344098087299004404881004700137
    '''
    __KEYSIZE = 1024

    def __init__(self):
        # get diferents primes with size desired
        self.__P = primes.genPrimes(self.__KEYSIZE)
        self.__Q = primes.genPrimes(self.__KEYSIZE)
        while self.__P == self.__Q:
            self.__Q = primes.genPrimes(self.__KEYSIZE)
        
        print('P:', self.__P)
        print('Q:', self.__Q)

    # generate keys
    def gen(self) -> tuple:
        n = self.__P * self.__Q
        phi_n = (self.__P - 1)*(self.__Q - 1)
        
        while True:
            e = random.randrange(1, phi_n)
            if math.gcd(e, (self.__P - 1) * (self.__Q - 1)) == 1:
                break
        
        d = CryptoMath.findModInverse(e, (self.__P - 1) * (self.__Q - 1))

        return ((e,n),(d,n)) # (public, private)

    # encrypt using OAEP
    def encOAEP(self, msg:bytes, key: tuple) -> bytes:
        # C := M^e mod n | public key -> (n,e)
        n,e = key
        k = e.bit_length() // 8
        M = OAEP.encode(msg, k)

        return pow(int.from_bytes(M, byteorder='big'), n, e).to_bytes(k, byteorder='big')

    # decrypt using OAEP
    def decOAEP(self, c:bytes, key: tuple) -> bytes:
        # M := C^d mod n | secret key -> (n,d)
        n,d = key
        k = d.bit_length() // 8
        C = pow(int.from_bytes(c, byteorder='big'), n, d).to_bytes(k, byteorder='big')
        
        return OAEP.decode(C, k)
