#!/bin/python3
import struct
import os
import math
import binascii
from Crypto.Hash import SHA256

filename = 'week3.in'
filesize = os.path.getsize(filename)
blocksize = 1024
blocks = int(math.ceil(filesize / blocksize))

with open(filename, 'rb') as f:
    lasthash = bytes()
    for i in range(blocks - 1, -1, -1):
        f.seek(i * blocksize)
        blockdata = f.read(blocksize)
        buf = bytearray(blockdata)
        buf.extend(lasthash)
        h = SHA256.new()
        h.update(bytes(buf))
        lasthash = h.digest()
    print(binascii.hexlify(lasthash))

