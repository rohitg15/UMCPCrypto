import sys

# assuming inputs are bytearrays
def encrypt(message, key):
    key_len = len(key)
    message_len = len(message)

    # divide message into blocks based on key length
    mblocks = [message[i * key_len : (i + 1) * key_len] for i in range(message_len / key_len)]

    # handle trailing bytes
    if message_len % key_len != 0:
        mblocks = mblocks + [message[-1 * (message_len % key_len) :]]

    # encrypt using vigenere
    cblocks = bytearray()
    for mblock in mblocks:
        cblock = bytearray([97 + (m - 97 + k - 97) % 26 for k,m in zip(key, mblock)])
        cblocks = cblocks + cblock
    
    for byte in cblocks:
        print hex(byte)
    
    return ''.join([chr(byte) for byte in cblocks])

if __name__ == "__main__":
    key = bytearray("spy")
    message = bytearray("seeyouatnoon")
    print encrypt(message, key)