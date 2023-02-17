# Vigenere Cipher

Vigenère's cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers, based on the letters of a keyword. It employs a form of poly alphabetic substitution.

## Description

This project implement Vigenère's cipher to encrypt and decrypt messages. Further, in it was implemented too, a breaker program to find key used to encrypt a given message.

- `Viginere.py`: implement Viginere cipher with OO;
- `VgBreaker.py`: Break cipher by given encrypted message;
- `main.py`: Contains main code useins last cited modules to encrypt, decrypt and break cipher.

# Run:

## encrypt a message:
```python3 main.py {key} -e ```
- save message encrypted in `files/encripted.txt`
- Alternatively: --enc {path/filename}

## decrypt a message:
```python3 main.py {key} -d ```
- save message decripted in `files/decripted.txt`
- Alternatively: --dec {path/filename}

## Break cipher and find out key:
```python3 main.py -b {language} ```

- languages supported: `pt` and `en`

