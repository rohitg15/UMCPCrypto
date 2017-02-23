import sys


# returns the number of differing bits between the two strings represented as bytearrays

def get_hamming_distance(b1, b2):
    count_diff_bits = 0
    for byte1, byte2 in zip(b1, b2):
        xor_byte = (byte1 ^ byte2) & 0xFF
        while xor_byte > 0:
            if (xor_byte & 0x01 != 0):
                count_diff_bits = count_diff_bits + 1
            xor_byte = xor_byte >> 1
    return count_diff_bits

def transpose_blocks(bciphertext, key_size):
    bcols = []
    for start in range(key_size):
        i = start
        block = bytearray()
        while i < len(bciphertext):
            block = block + bciphertext[i]
            i = i + key_size
        bcols.append(block)
    return bcols
         

def crack_vigenere(ciphertext):
    bciphertext = bytearray(ciphertext)
    dist = {}

    # obtain hamming distances and normalize them
    min_dist = 100
    min_size = 0
    for key_size in range(2, 14):
        first = bciphertext[0 : key_size]
        second = bciphertext[key_size : 2*key_size]
        edit_dist = get_hamming_distance(first, second)
        dist[key_size] = edit_dist / key_size
        if min_dist > dist[key_size]:
            min_dist = dist[key_size]
            min_size = key_size
    
    # transpose the blocks
    bcols = transpose(bytearray(ciphertext), min_size)
    for col in bcols:
        print col

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print "usage:%s filename" % (sys.argv[0])
        exit(-1)
    filename = sys.argv[1]
    with open(filename, "r") as f:
        ciphertext = f.read().strip()
    crack_vigenere(ciphertext.decode('hex'))
    #print get_hamming_distance("this is a test", "wokka wokka!!!")
    #b = transpose_blocks(b'hello world!', 3)
    #for block in b:
    #    print block