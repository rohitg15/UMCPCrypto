from oracle import *
import sys

soln = []
def solve_padding_oracle(prev, cur, padding, bsize, guess, pos_index):
    if pos_index < 0 or pos_index >= bsize:
        soln.append(guess[::-1])
        return (True, guess[::-1])

    # generate the appropriate suffix for the previous block, based on the current state of guess
    # we want the tail to have the appropriate padding after it is XORd with the current block
    # guess is stored in reverse, and hence we do bsize - i - 1
    # [pos_index + 1, bsize - 1] represents the interval that has been guessed already
    tail = [ ( (ord(guess[bsize - i - 1]) ^ prev[i] ^ padding) & 0xFF ) for i in range(pos_index + 1, bsize) ]

    for byte in range(256):
        flipped_byte = (prev[pos_index] ^  byte ^ padding) & 0xFF
        modified_cipher = prev[:pos_index] + [flipped_byte] + tail + cur

        assert(len(modified_cipher) == bsize * 2)

        # send the modified ciphertext to the oracle
        Oracle_Connect()
        rc = Oracle_Send(modified_cipher, 2)
        Oracle_Disconnect()

       

        # if there are no padding errors, recursively solve for the remaining ciphertext in this block
        if rc == 1:
            res , ans = solve_padding_oracle(prev, cur, padding + 1, bsize, guess + chr(byte), pos_index - 1 ) 
            if res == True:
                return (True, ans)
    return (False, '')

        



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python sample.py <filename>"
        sys.exit(-1)

    f = open(sys.argv[1])
    data = f.read()
    f.close()

    ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]

    # divide the ciphertext into AES blocks
    bsize = 16
    blocks = [ctext[i * bsize : (i + 1) * bsize] for i in range(len(ctext) / bsize)]

    # use some random iv here - doesn't matter unless we are concerned about decrypting the first block
    iv = [0x0]* 16
    prev = iv
    decrypted = []

    # solve every block using the previous block to flip the bits and set the appropriate padding, starting from 0x1
    for block in blocks:
        initial_pad = 0x1
        guess = ''
        start_pos_index = bsize - 1
        result, plaintext = solve_padding_oracle(prev, block, initial_pad, bsize, guess, start_pos_index)
        if result == True:
            decrypted.append(plaintext)
        prev = block
    print soln
    

    # ignore the first block's output
    # 'Yay! You get an '
    # 'A. =)\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b' [11 bytes of padding with 0x0b - PKCS7]