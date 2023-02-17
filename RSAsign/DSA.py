import base64
from RSA import RSA
from help.OAEP import sha3

class DSA(RSA):

    def __getkeys(self, file:str):
        file_data = open(file).read()
        str_key = base64.decodebytes(file_data.encode('ascii')).decode('ascii')
        
        a,b = str_key.replace('(', '').replace(')', '').split(',')

        return (int(a),int(b))

    def genkeys(self, dest_pb:str, dest_pv:str):

        pb,pv = self.gen()

        open(dest_pb, 'w').write(base64.encodebytes(str(pb).encode('ascii')).decode('ascii'))
        open(dest_pv, 'w').write(base64.encodebytes(str(pv).encode('ascii')).decode('ascii'))

        return pb,pv

    def sign(self, doc_file:str, key_file:str):

        key = self.__getkeys(key_file)

        doc_coded = open(doc_file).read().encode('ascii')
        doc_hashed = sha3(doc_coded)

        enc_doc = self.encOAEP(doc_hashed, key)

        output = base64.encodebytes(enc_doc).decode('ascii')

        with open(f"{doc_file}.signed", 'w') as save:
            save.write(output)

        return output
        
    def vrfy(self, doc_signed:str, doc_original:str, key_file:str) -> bool:

        key = self.__getkeys(key_file)

        doc_s_file = open(doc_signed, 'r').read()
        doc_bytes = base64.decodebytes(doc_s_file.encode('ascii'))

        doc_o_file = open(doc_original, 'r').read().encode('ascii')
        doc_original_hashed = sha3(doc_o_file)

        doc_decoded = self.decOAEP(doc_bytes, key)

        return doc_decoded == doc_original_hashed

