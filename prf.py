class A(object):
    def __init__(self, hashcls, secret, seed):
        self.hashcls = hashcls
        self.secret = secret
        self.seed = seed

def PRF(hashcls, secret, label, seed, outlen):
    pass
