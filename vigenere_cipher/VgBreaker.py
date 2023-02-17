import re, collections

lang:str
symb:str
LG_FREQ = {
    'pt':{
        'a':14.63,'b':1.04,'c':3.88,'d':4.99,'e':12.57,'f':1.02,'g':1.30,'h':1.28,'i':6.18,'j':0.40,'k':0.02,'l':2.78,'m':4.74,'n':5.05,'o':10.73,'p':2.52,'q':1.20,'r':6.53,'s':7.81,'t':4.34,'u':4.63,'v':1.67,'w':0.01,'x':0.21,'y':0.01,'z':0.47
    },
    'en':{
        'a':8.167,'b':1.492,'c':2.782,'d':4.253,'e':12.702,'f':2.228,'g':2.015,'h':6.094,'i':6.966,'j':0.153,'k':0.772,'l':4.025,'m':2.406,'n':6.749,'o':7.507,'p':1.929,'q':0.095,'r':5.987,'s':6.327,'t':9.056,'u':2.758,'v':0.978,'w':2.360,'x':0.150,'y':1.974,'z':0.074
    }
}

def trait_text(cipher_text:str, symb:str):
    return "".join(c for c in cipher_text if c in symb)

def lett_most_freq(text:str):
    letts = collections.Counter(text).most_common(3)

    lett_freq = []
    for t in letts:
        lett_freq.append([t[0], (t[1]*100)/len(text)])
    
    #lett, n = teste[0]
    #freq = (n*100)/len(text)

    return lett_freq

def block_freq(cryp_msg:str):
    c = 0
    block = ''
    for i in range(1, len(cryp_msg)):
        k = 0
        j = i
        while j < len(cryp_msg):
            bl = cryp_msg[k:j]
            count = cryp_msg.count(bl)
            if(count > c):
                #print(bl)
                c = count
                block = bl
            k+=1
            j+=1
            
    return block

def block_most_rep(block:str, msg:str):
    return [m.start()+1 for m in re.finditer(block, msg)]

def diff_pos_blocks(block_pos: list):
    return [abs(bp - block_pos[i-1]) for i,bp in enumerate(block_pos)]
    
def get_key_size(cryp_msg:str):
    block = block_freq(cryp_msg)
    #print([block])

    block_pos = block_most_rep(block, cryp_msg)
    #print(block_pos)

    diff = diff_pos_blocks(block_pos)
    return collections.Counter(diff).most_common(5)


def closest(freq_m:dict, value:float) -> str:
    menor = 101.0
    sym = ''
    for k,v in freq_m.items():
        m = abs(v-value)
        if(m < menor):
            menor, sym = m, k
    
    return sym


def block_split(crypt_msg:str, size:int):
    return [crypt_msg[i:i+size] for i in range(0, len(crypt_msg), size)]

def setLang(language:str):
    if(language in LG_FREQ.keys()):
        return language
    else:
        raise Exception("Language not suported!")

def breaker(encripted:str, language:str, symb:str):
    lang = setLang(language)
    crypt_msg = trait_text(encripted, symb)

    possible_key_sizes = [k[0] for k in get_key_size(crypt_msg)]
    print('possible key sizes:', possible_key_sizes)
    key_size = int(input('choose: '))

    substr = block_split(crypt_msg, key_size)
    substr.pop(len(substr)-1)
    #print(substr)

    key,key1,key2 = "","",""
    for i in range(0, key_size):
        subi = ""
        for s in substr:
            subi += s[i]
        #print([subi])
        lett_freq = lett_most_freq(subi)
        i = 0
        for lf in lett_freq:
            #print([lett], freq)
            cf = closest(LG_FREQ[lang], lf[1])
            #print(cf)
            
            if(i==0):
                key += symb[(symb.find(lf[0]) - symb.find(cf)) % len(symb)]
            elif(i==1):
                key1 += symb[(symb.find(lf[0]) - symb.find(cf)) % len(symb)]
            elif(i==2):
                key2 += symb[(symb.find(lf[0]) - symb.find(cf)) % len(symb)]

            i+=1

    print(key1, key2)
    return key
