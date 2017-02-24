import sys


# returns the number of differing bits between the two strings 
def get_hamming_distance(b1, b2):
    count_diff_bits = 0
    for ch1, ch2 in zip(b1, b2):
        byte1 = ord(ch1)
        byte2 = ord(ch2)
        xor_byte = (byte1 ^ byte2) & 0xFF
        while xor_byte > 0:
            if (xor_byte & 0x01 != 0):
                count_diff_bits = count_diff_bits + 1
            xor_byte = xor_byte >> 1
    return count_diff_bits

def get_score(plaintext):
    charset_lower = "abcdefghijklmnopqrstuvwxyz "
    charset_upper = charset_lower.upper()
    spaces = ",.;?!:-`'"

    score = 0
    for ch in plaintext:
        if (ch in charset_lower) or (ch in charset_upper) or (ch in spaces):
            score = score + 1
    return score * 1.0/len(plaintext)

def brute_single_key_xor(ciphertext):
    print "brute forcing :" + ciphertext
    table = {}
    for key in range(256):
        plaintext = ''.join([chr((key ^ ord(ch)) ^ 0xFF) for ch in ciphertext])
        score = get_score(plaintext)
        table[plaintext] = (score, key)

    #print "ciphertext:" + ciphertext
    best_key = -1
    for w in sorted(table, key = lambda p : table[p][0], reverse = True)[:-1]:
        if table[w][1] == 186:
            print table[w][1] , table[w][0]
        best_key = chr(table[w][1])
    return best_key

        


def transpose(ciphertext, key_size):
    cols = []
    for start in range(key_size):
        i = start
        block = ''
        while i < len(ciphertext):
            block = block + ciphertext[i]
            i = i + key_size
        cols.append(block)
       # pt = ''.join([chr((ord(ch) ^ 186) & 0xFF) for ch in block])
       # print "score:", get_score(pt)
       # print pt
       # print "size of block %d : %d " % (start, len(block)) 

    #print "num cols:" , len(cols)
    return cols
         

def crack_vigenere(ciphertext):
    dist = {}

    # obtain hamming distances and normalize them
    min_dist = 100
    min_size = 0
    for key_size in range(2, 14):
        first = ciphertext[0 : key_size]
        second = ciphertext[key_size : 2*key_size]
        edit_dist = get_hamming_distance(first, second)
        dist[key_size] = edit_dist*1.0 / key_size
    
    candidate_sizes = []
    for w in sorted(dist, key= lambda k: dist[k]):
        candidate_sizes.append(w)
    
    for key_size in candidate_sizes[0:1]:
        # transpose the blocks
        print "trying keys of size:" + str(key_size)
        bcols = transpose(ciphertext, key_size)
        

        # solve each column as a single key xor cipher
        cipher_key = ''
        for col in bcols:
            col_key = brute_single_key_xor(col)
            if col_key != -1:
                print "col key:" , str(ord(col_key))
                cipher_key = cipher_key + col_key
            else:
                print "column:" + col
                print "returned -1"
        for ch in cipher_key:
            print hex(ord(ch))
    
    return cipher_key


    
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print "usage:%s filename" % (sys.argv[0])
        exit(-1)
    filename = sys.argv[1]
    with open(filename, "r") as f:
        ciphertext = f.read().strip()
    
    cipher_key = crack_vigenere(ciphertext.decode('hex'))
    print "cipher key : " + cipher_key + " , " + str(len(cipher_key))
    #print get_hamming_distance("this is a test", "wokka wokka!!!")
    #b = transpose_blocks(b'hello world!', 3)
    #for block in b:
    #    print block