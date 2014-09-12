#!/usr/bin/env python

import binascii
import fileinput

# read all cipher text, the last line is the one we're going to decrypt.
ciphers = []
minLen = 100000
for line in fileinput.input():
    b = binascii.unhexlify(line.strip())
    ciphers.append(b)
    if len(b) < minLen: minLen = len(b)

key = []
for i in range(0, minLen):
    maxCount = 0
    maxPos = 0
    for x in range(0, len(ciphers)):
        count = 0;
        for y in range(0, len(ciphers)):
            v = ciphers[x][i] ^ ciphers[y][i]
            if v >= ord('a') and v <= ord('z') or v >= ord('A') and v <= ord('Z') or v == 0:
                count+=1
        if count > maxCount:
            maxCount = count
            maxPos = x
    if maxCount > 0:
        key.append(ciphers[maxPos][i])
    else:
        key.append(0)


print("".join([' ' if x ^ y == 0 else '?' if not chr(x ^ y).isalpha() else chr(x ^ y).swapcase() \
        for x, y in zip(ciphers[len(ciphers) - 1], key)]))



