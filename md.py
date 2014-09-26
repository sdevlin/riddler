from binascii import hexlify
import struct

class MD(object):
    def update(self, m):
        mbuflen = len(self.mbuf)
        while m:
            offset = self.mlen % mbuflen
            take = min(mbuflen - offset, len(m))
            self.mbuf[offset:offset+take] = m[:take]
            self.mlen += take
            m = m[take:]
            if self.mlen % mbuflen == 0:
                self.compress()

    def final(self):
        mbuflen = len(self.mbuf)
        mlenbuf = self.packmlen()
        maxpadlen = mbuflen - 1 - len(mlenbuf)
        padbuf = b'\x00' * ((maxpadlen - (self.mlen % mbuflen)) % mbuflen)
        self.update(b'\x80')
        self.update(padbuf)
        self.update(mlenbuf)
        return self.packstate()

    @classmethod
    def digest(cls, m):
        obj = cls()
        obj.update(m)
        return obj.final()

    @classmethod
    def hexdigest(cls, m):
        return hexlify(cls.digest(m))
