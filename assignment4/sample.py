from oracle import *
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python sample.py <filename>"
        sys.exit(-1)

    f = open(sys.argv[1])
    data = f.read().strip("\n")
    f.close()

    # verify the length of the message
    size = len(data)
    assert(size == 64)
    
    # split the message into 2 parts
    m1 = data[0 : size/2]
    m2 = data[size/2 : size]

    # get the tags for each half of the message

    Oracle_Connect()
    t1 = Mac(m1, size/2)

    # to compute the tag for the 4 byte block message offline, we send the following
    # (t1 ^ m2[0:16]) | m2[16:32]
    # When the server computes the CBC mac of the entire message, the state of tge system just after computing
    # the tag for the first 2 blocks and just before proceeding to the next 2 blocks would be as indicated above
    forged_block = ''.join([ chr( (b1 ^ b2) & 0xFF ) for b1, b2 in zip( bytearray(t1), bytearray(m2[0 : len(t1)]) ) ])
    forged_block = forged_block + m2[len(t1) : 2*len(t1)]
    tag = Mac(forged_block, size/2)

    ret = Vrfy(data, len(data), tag)
    print
    print ret
    if (ret==1):
        print "Message verified successfully!"
    else:
        print "Message verification failed."

    Oracle_Disconnect()
