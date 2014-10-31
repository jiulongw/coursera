import urllib.request
import urllib.parse
import urllib.error
import sys
import binascii

Target = 'http://crypto-class.appspot.com/po?er='
CipherText = binascii.unhexlify('f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4')
PlainText = bytearray()

def query(q):
    target = Target + urllib.parse.quote(q)
    req = urllib.request.Request(target)
    try:
        res = urllib.request.urlopen(req)
        return 0
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 1
        return 2

iv = CipherText[0:16]
blockCount = len(CipherText) // 16 - 1

for i in range(2, blockCount):
    pt = bytearray(16)
    pad = CipherText[i * 16 : i * 16 + 16]
    cipherText = bytes(CipherText[i * 16 + 16 : i * 16 + 32])
    for j in range(15, -1, -1):
        for x in range(0, 256):
            if x > 16 and x < 32: continue
            print(x, end='\r')
            newPad = bytearray(pad)
            pt[j] = x
            for k in range(j, 16):
                newPad[k] = newPad[k] ^ pt[k] ^ (16 - j)
            testCipher = bytearray(newPad)
            testCipher.extend(cipherText)
            q = binascii.hexlify(testCipher).decode()
            if query(q) == 1:
                if i == blockCount - 1 and x == 1: continue
                print("{0}: '{1}'".format(x, chr(x)))
                break
    print(pt.decode())
