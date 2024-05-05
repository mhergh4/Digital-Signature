from SimpleRSA import SimpleRSA
from SimpleSHA256 import hash as sha256_hash

class DigitalSignature:
    def __init__(self):
        self.rsa = SimpleRSA()

    def generate_rsa_key_pair(self, bits): pass

    def sign_data(self, data):
     hashed_data = sha256_hash(data)
     return self.rsa.sign_data(hashed_data)


    def verify_signature(self, data, signature):
        hashed_data = sha256_hash(data)
        return self.rsa.verify_signature(hashed_data, signature)
