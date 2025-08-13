# -*- coding: utf-8 -*-

import base64
import logging
#/////////////////////////////////////////////////////////////
from django.conf import settings
from django.utils.encoding import force_bytes
#/////////////////////////////////////////////////////////////
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
def derive_key():
    """
    The derive_key method is performing a key derivation from 
    pre-defined settings.
    """
    key = None
    try:
        secret = force_bytes(settings.SECRET_KEY)
        salt = force_bytes(settings.CRYPTO_SALT)
        key = scrypt(secret, salt, key_len=32, N=2**14, r=8, p=1)
    except:
        logger.critical("Error, deriving a key.")

    return key

#/////////////////////////////////////////////////////////////
def encrypt(plaintext):
    """
    The encrypt method performs an AES encryption to the provided 
    plaintext.
    """
    ciphertext = None
    nonce = force_bytes(settings.CRYPTO_NONCE)
    
    if not plaintext:
        return ciphertext 

    try:
        cipher = AES.new(derive_key(), AES.MODE_GCM, nonce=nonce)
        ciphertext = cipher.encrypt(plaintext.encode())
    except:
        logger.critical("Error, encrypting plaintext.")

    return ciphertext

#/////////////////////////////////////////////////////////////
def decrypt(ciphertext):
    """
    The decrypt method performs an AES decryption to the provided 
    ciphertext.
    """
    plaintext = None
    nonce = force_bytes(settings.CRYPTO_NONCE)

    if not ciphertext:
        return plaintext

    try:
        cipher = AES.new(derive_key(), AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext).decode()
    except:
        logger.critical("Error, decrypting ciphertext.")
        
    return plaintext

