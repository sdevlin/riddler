from binascii import hexlify

class HMAC(object):
    def __init__(self, hashcls, key):
        self.hashcls = hashcls
        self.key = key

        if len(key) > hashcls.blocklen():
            key = hashcls.digest(key)

        if len(key) < hashcls.blocklen():
            key += bytes(hashcls.blocklen() - len(key))

        self.ekey = key         # effective key
        self.ikey = bytes(b ^ 0x36 for b in key)
        self.okey = bytes(b ^ 0x5c for b in key)

        self.ihash = hashcls()
        self.ihash.update(self.ikey)
        self.ohash = hashcls()
        self.ohash.update(self.okey)

    def update(self, m):
        self.ihash.update(m)

    def final(self):
        self.ohash.update(self.ihash.final())
        return self.ohash.final()

    @classmethod
    def digest(cls, hashcls, key, m):
        obj = cls(hashcls, key)
        obj.update(m)
        return obj.final()

    @classmethod
    def hexdigest(cls, hashcls, key, m):
        return hexlify(cls.digest(hashcls, key, m))
