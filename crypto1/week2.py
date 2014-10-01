#!/usr/bin/env python

from Crypto.Cipher import AES
import binascii
import struct
import math

def xor(a, b):
    return [x ^ y for x, y in zip(a,b)]

def decryptBlock(block, iv, cipher):
    pt = cipher.decrypt(bytes(block))
    return xor(pt, iv)

def decryptCBC(message, key):
    bKey = binascii.unhexlify(key)
    bData = binascii.unhexlify(message)

    cipher = AES.new(bytes(bKey), AES.MODE_ECB)

    iv = bData[0:16]
    cipherText = bData[16:]
    results = []
    for i in range(0, len(cipherText) // 16):
        block = cipherText[i * 16: (i + 1) * 16]
        results.extend(decryptBlock(block, iv, cipher))
        iv = block
    last = results[len(results) - 1]
    results = results[0: len(results) - last]
    return bytes(results).decode("utf-8")

def prfPad(iv, counter, cipher):
    return cipher.encrypt(bytes(iv))

def decryptCTR(message, key):
    bKey = binascii.unhexlify(key)
    bData = binascii.unhexlify(message)

    cipher = AES.new(bytes(bKey), AES.MODE_ECB)

    iv = bData[0:16]
    counter = 0

    cipherText = bData[16:]
    results = []
    for i in range(0, int(math.ceil(len(cipherText) / 16))):
        block = cipherText[i * 16: (i + 1) * 16]
        pad = prfPad(iv, 0, cipher)
        results.extend(xor(pad, block))
        ivv = bytearray(iv)
        ivv[15] += 1
        x = 15
        while ivv[x] > 255:
            ivv[x-1] += 1
            ivv[x] = 0
            x -= 1
        iv = bytes(ivv)
    # last = results[len(results) - 1]
    # results = results[0: len(results) - last]
    return bytes(results).decode("utf-8")

print(decryptCBC("4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81", "140b41b22a29beb4061bda66b6747e14"))
print(decryptCBC("5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253", "140b41b22a29beb4061bda66b6747e14"))
print(decryptCTR("69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329", "36f18357be4dbd77f050515c73fcf9f2"))
print(decryptCTR("770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451", "36f18357be4dbd77f050515c73fcf9f2"))

