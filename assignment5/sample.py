from oracle import *
from helper import *

n = 119077393994976313358209514872004186781083638474007212865571534799455802984783764695504518716476645854434703350542987348935664430222174597252144205891641172082602942313168180100366024600206994820541840725743590501646516068078269875871068596540116450747659687492528762004294694507524718065820838211568885027869

e = 65537

Oracle_Connect()

msg = "Crypto is hard --- even schemes that look complex can be broken"

m = ascii_to_int(msg)

# Should fail, because you're not allowed to query on the original message
#sigma = Sign(m)
#assert(sigma < 0)

# All other arbitrary messages <= 504 bits should be accepted by the oracle

m1 = 2
m2 = m / 2

sigma1 = Sign(m1)
sigma2 = Sign(m2)

M1 = mod_exp(sigma1, e, n)
M2 = mod_exp(sigma2, e, n)

p = M1 / m1  # M / m1 = M / m2 (verified by actually dividing)

# sigma1 * sigma2 mod n = ((m1 * p) ^ d ) * ((m2 * p) ^ d) mod n = (m1 * m2 * p * p) ^ d mod n
# expected signature = m ^ d mod n = (m1 * m2 * p) ^ d mod n
pe = Sign(1)


sigma = mod_mul(sigma1, sigma2, n)
sigma = mod_mul(sigma, modinv(pe, n), n)

print "message   : %s" % (m)
print "signature : %s" % (sigma)

if sigma1 < 0:
    raise SystemExit

if Verify(m,sigma):
    print "forged signature on message %s" % (m)

Oracle_Disconnect()
