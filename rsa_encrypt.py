from sympy import randprime
import random

class RSA:
    def __init__(self, key_size = 180):
        self.key_size = key_size
        self.e = None
        self.d = None
        self.n = None
    
    def gcd(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b
    
    def extended_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self.extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
    def mod_inverse(self, a, m):
        g, x, _ = self.extended_gcd(a, m)
        if g != 1:
            raise Exception("Modular inverse doesn't exist!")
        return x % m
    
    def generate_key(self):
        self.p = randprime(2 ** (self.key_size - 1), 2 ** self.key_size)
        self.q = randprime(2 ** (self.key_size - 1), 2 ** self.key_size)
        self.n = self.p * self.q
        self.totient = (self.p - 1) * (self.q -1)

        while True:
            self.e = random.randrange(2 ** (self.key_size - 1), 2 ** self.key_size)
            if (self.gcd(self.e, self.totient) == 1):
                break
        self.d = self.mod_inverse(self.e, self.totient)

    
    def save_key(self, path, e, n, d):
        with open(path + ".pub", "w") as pub:
            pub.write(str(e) + " " + str(n))
        
        with open(path + ".pri", "w") as pri:
            pri.write(str(d) + " " + str(n))
        
    def load_public_key(self, path):
        with open(path, "r") as file:
            pub = file.read().split(" ")

        self.e = int(pub[0])
        self.n = int(pub[1])
    
    def load_private_key(self, path):
        with open(path, "r") as file:
            pri = file.read().split(" ")

        self.e = int(pri[0])
        self.n = int(pri[1])
    
    def sign_rsa(self, text, d, n):
        temp = pow(text, d, n)
        res = hex(temp)[2:]
        return res
    
    def verify_rsa(self, text, e, n, h):
        temp = int(text, 16)
        res = pow(temp, e, n)
        return res == h
    
    def save_inside(self, res, fname):
        with open(fname, "a") as file:
            file.write("\n*** Start of digital signature ****\n")
            file.write(str(res) + "\n")
            file.write("*** End of digital signature ****\n")
    
    def read_inside(self, path):
        m_text = ""
        sign = False
        with open(path, "r") as file:
            for line in file:
                if (not sign):
                    if line == ("*** Start of digital signature ****\n"):
                        sign = True
                    else:
                        m_text += line
                else:
                    content = line.rstrip()
                    break
        return (m_text.rstrip(), content)
    
    def save_newfile(self, res, fname):
        with open(fname, "w") as file:
            file.write("\n*** Start of digital signature ****\n")
            file.write(str(res) + "\n")
            file.write("*** End of digital signature ****\n")
    
    def read_newfile(self, m_path, sign_path):
        m_text = self.read_separate_m(m_path)
        content = self.read_separate_sign(sign_path)
        return (m_text.rstrip(), content)
    
    def read_separate_m(self, path):
        m_text = ""
        with open(path, "r") as file:
            for line in file:
                m_text += line
        return m_text
    
    def read_separate_sign(self, path):
        sign = False
        with open(path, "r") as file:
            for line in file:
                if (not sign):
                    if line == ("*** Start of digital signature ****\n"):
                        sign = True
                else:
                    content = line.rstrip()
                    break
            return (content)


