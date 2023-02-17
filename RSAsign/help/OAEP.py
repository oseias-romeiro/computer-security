import hashlib, os

# Mask generation function
def MGF(seed:bytes, l:int):
    # l <= 2^(32)*hLen 
    hLen = hashlib.sha3_512().digest_size
    if l > (hLen << 32):
        raise ValueError("mask too long")

    T = b""
    # counter from 0 to ceil(l / hLen)-1
    count = 0
    while len(T) < l:
        # C = I2OSP (counter, 4)
        C = int.to_bytes(count, 4, 'big')
        # T: T = T || Hash (Z || C)
        T += hashlib.sha3_512(seed + C).digest()
        count += 1

    # len octets of T as the octet string mask
    return T[:l]

def sha3(m: bytes) -> bytes:
    hasher = hashlib.sha3_512()
    hasher.update(m)
    return hasher.digest()

# xor operation in list of bytes
def xor(data: bytes, mask: bytes) -> bytes:
    assert( len(data) == len(mask) )

    masked = b''
    for i in range(0, len(data)):
        masked += (data[i] ^ mask[i]).to_bytes(1, byteorder='big')
    
    return masked

def encode(m: bytes, k: int, L: bytes = b''):
    mLen = len(m)
    lhash = sha3(L)
    hLen = len(lhash)
    seed = os.urandom(hLen)
    ps = b'\x00' * (k - mLen - 2 * hLen - 2)

    db = lhash + ps + b'\x01' + m

    seed_mgf = MGF(seed, k-hLen-1)
    maskedDB = xor(db, seed_mgf)

    maskedDB_mgf = MGF(maskedDB, hLen)
    maskedSeed = xor(seed, maskedDB_mgf)
    
    return b'\x00' + maskedSeed + maskedDB

def decode(c: bytes, k: int, L: bytes = b'') -> bytes:
    lhash = sha3(L)
    hLen = len(lhash)
    _, maskedSeed, maskedDB = c[:1], c[1:1+hLen], c[1 + hLen:]
    
    seedMask = MGF(maskedDB, hLen)
    seed = xor(maskedSeed, seedMask)

    dbMask = MGF(seed, k-hLen-1)
    DB = xor(maskedDB, dbMask)

    assert lhash == DB[:hLen]

    i = hLen
    while i < len(DB):
        if DB[i] == 0: # PS
            i += 1
        elif DB[i] == 1: # M
            i += 1
            break
        else:
            raise Exception()
    
    return DB[i:] # M

