# GENERAL EXPLANATION FOR AES:
# ECB - Electronic Code Block
# CBC - Cypher Block-chaining Mode

# Padding - Adds characters to a block if it is not equal to 16
# Key - Fixed length key of 16, 24 or 32 bytes
# Block Size - Specific block size used in block cyphers
# (Algorith that encrypts a fixed size n bits of data at one time) (16 bytes)
# Hashing - Complex mathematical calculation to map data of an arbitrate size to fixed length values


# Example
#  "I love Python More than anything in the world" (45 char)
#  |I love Python Mo|re than anything| in the world|
#       16 bytes         16 bytes       12 bytes
# Each ASCII character is 8 bites aka 1 byte (actually 7 bits, but the last bit is used for error checking)
# All the block have to be 16 bytes, so wee need to add characters to the last block
#  |I love Python Mo|re than anything| in the world{{{{|
#       16 bytes         16 bytes         16 bytes
# This example is now correctly split into block

# Mods of encryption in AES

# Electronic Code Block:
# Encryption Key: Hello
# For example purposes lets assume all blocks show bellow ar bytes.
# Key ==> |I love | Key ==> |Python| Key ==> |.Py|
#           a6/xx            60f60/6         060
# A pattern can be seen in the last two block = No good!

# Cypher Block-chaining Mode
# Encryption Key: Hello
# IV - Random sequence of characters that is added to the first block.
#      To produce a more unpredictable cypher text.
# For example purposes lets assume all blocks show bellow ar bytes.
#            IV (Initialization Vector)
#             |
# Key ==> |I love | Key ==> |Python| Key ==> |.Py|
#                  +                +
#                 /                /
#          a.s-01            =ar=0a          xx909

# Result from the first block encryption is used to augment the cypher key for the next block.
# And continuing like that for all blocks.
# In this way not leaving any patterns in the cyphered text.

import string
import random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import codecs

BLOCK_SIZE = 16


def get_encryption_key(pwd: str):
    return SHA256.new(pwd.encode("utf-8")).digest()


def padding(no_padding_msg: str) -> str:
    for ind, _ in enumerate(range(BLOCK_SIZE - len(no_padding_msg) % BLOCK_SIZE)):
        if ind == 0:
            no_padding_msg = no_padding_msg + ''.join("|")
            continue
        no_padding_msg = no_padding_msg + ''.join(random.choice(string.ascii_letters))

    return no_padding_msg


def encrypt(pwd: str, text: str) -> str:
    cypher = AES.new(get_encryption_key(pwd), AES.MODE_ECB)
    return str(cypher.encrypt(padding(text).encode("utf-8")).decode("cp1252"))


def decrypt(pwd: str, enc_msg: str) -> str:
    decipher = AES.new(get_encryption_key(pwd), AES.MODE_ECB)
    print(enc_msg.encode().decode('unicode_escape'))
    plain_text = decipher.decrypt(enc_msg.encode("cp1252")).decode("cp1252")
    pad_indx = plain_text.find("|")
    return plain_text[:pad_indx]
