from DSA import DSA

dsa = DSA()

def genKeys():
    dest_pb = input('Destino (chave publica): ')
    dest_pv = input('Destino (chave privada): ')

    pb,pv = dsa.genkeys(dest_pb, dest_pv)

    print(
f"""
-- public key: \n{pb}
-- private key: \n{pv}
"""
    )

def signFile():
    key_file = input('Arquivo da chave: ')
    dest = input('Arquivo: ')
    
    dsa.sign(dest, key_file)

def vrfySignature():
    key_file = input('arquivo da chave: ')
    signed_file = input('arquivo assinado: ')
    original_file = input('arquivo original: ')

    vrfy = dsa.vrfy(signed_file, original_file, key_file)

    print('\n# Assinatura:', ('Verdadeira' if vrfy else 'Falsa'))


if(__name__ == "__main__"):

    menu = """ ### Assinatura Digital ###
1) Gen keys
2) Sign file
3) Verify file
4) exit
"""
    while True:
        cin = input(menu)

        match cin:
            case '1':
                genKeys()
            case '2':
                signFile()
            case '3':
                vrfySignature()
            case '4':
                break

