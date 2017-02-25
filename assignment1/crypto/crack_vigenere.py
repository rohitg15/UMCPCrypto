import sys


# returns the number of bits that differ between the 2 strings (assumed to be equal length)
def get_hamming_distance(s1, s2):
    count = 0
    for ch1, ch2 in zip(s1, s2):
        z = (ord(ch1) ^ ord(ch2)) & 0xFF
        while z > 0:
            if z & 0x01 != 0:
                count = count + 1
            z = z >> 1
    return count


# returns an array of key sizes that are possible in order of likelihood
def get_key_sizes(ciphertext):
    d = {}
    for key_len in range(2, 14):
        # average hamming distance over 5 blocks
        blocks = [ciphertext[i:i+key_len] for i in range(0, len(ciphertext), key_len)]
        dist = 0
        for i in range(5):
            for j in range(i+1, 5):
                dist = dist + (get_hamming_distance(blocks[i], blocks[j]) * 1.0 / key_len)   
        d[key_len] = dist / 10
    return sorted(d, key= lambda k : d[k])


# returns a list of blocks where each block is a column vector from the ciphertext, corresponding to the key_len
def get_transpose(ciphertext, key_len):
    blocks = []
    for i in range(key_len):
        block = ''
        for j in range(i, len(ciphertext), key_len):
            block = block + ciphertext[j]
        blocks.append(block)
    return blocks

# returns a score for the plaintext based on the number of english characters
def get_score(plaintext):
    lcase = "abcdefghijklmnopqrstuvwxyz"
    ucase = lcase.upper()
    spaces = ",.;?! :\t\n"

    score = 0
    for ch in plaintext:
        if (ch in lcase) or (ch in ucase) or (ch in spaces):
            score = score + 1
    return score


def decrypt_vigenere(ciphertext, key):
    return ''.join([ chr(( ord(ciphertext[i]) ^ ord(key[i % len(key)])  ) & 0xFF) for i in range(len(ciphertext)) ])


# ignoring the last trailing block of ciphertext saves some time
# getting the average hamming distance over 4-6 blocks gives more accurate key lenghts as opposed to just the first 2 blocks
# idea behind using hamming distance / key_len is that if we guessed the key length (key_len) correctly, then C1 ^ C2 is same as P1 ^ P2, which would have fewer differing bits when
# computed over an average of 4-6 ciphertext blocks of size key_len. 
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print "usage: %s filename" % (sys.argv[0])
        exit(0)
    
    # read file and decode ciphertext
    with open(sys.argv[1], "r") as f:
        ciphertext = f.read().strip().decode("hex")

    # find key length 
    key_sizes = get_key_sizes(ciphertext)

    # find the key and try to decrypt the ciphertext for each key length
    for key_len in [key_sizes[0]]:
        # ignore last trailing block
        tblocks = get_transpose(ciphertext[:len(ciphertext) - len(ciphertext)%key_len ], key_len)
        
        # solve each block using single key xor
        key = ''
        for tblock in tblocks:
            # brute force key byte
            d = {}
            for kbyte in range(256):
                plaintext = ''.join([chr( (ord(ch) ^ kbyte) & 0xFF ) for ch in tblock])
                d[plaintext] = (get_score(plaintext), chr(kbyte))
            
            # choose the byte with highest score
            for p in sorted(d, key=lambda k : d[k][0], reverse=True)[:1]:
                key = key + d[p][1]
        print "key:", key.encode('hex')
        print "plaintext:", decrypt_vigenere(ciphertext, key)

             

   