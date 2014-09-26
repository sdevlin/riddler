def uint8(x):
    return x & 0xff

class RC4(object):
    def __init__(self, key):
        self.i = 0
        self.j = 0
        self.S = S = list(range(256))

        j = 0
        for i in range(256):
            j = uint8(j + S[i] + key[i % len(key)])
            tmp = S[i]
            S[i] = S[j]
            S[j] = tmp

    def generate(self, outlen):
        i = self.i
        j = self.j
        S = self.S
        buf = bytearray(outlen)

        for k in range(outlen):
            i = uint8(i + 1)
            j = uint8(j + S[i])
            tmp = S[i]
            S[i] = S[j]
            S[j] = tmp
            buf[k] = S[uint8(S[i] + S[j])]

        self.i = i
        self.j = j
        return bytes(buf)

    def update(self, m):
        return bytes(x ^ y for (x, y) in zip(m, self.generate(len(m))))

    def final(self):
        return b''

    @classmethod
    def encrypt(cls, key, p):
        obj = cls(key)
        return obj.update(p) + obj.final()

    @classmethod
    def decrypt(cls, key, c):
        return cls.encrypt(key, c)
