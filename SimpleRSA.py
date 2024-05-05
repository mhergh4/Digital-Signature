import rsa  # type: ignore

class SimpleRSA:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(2048)

    def sign_data(self, data):
        return rsa.sign(data.encode(), self.private_key, 'SHA-256')

    def verify_signature(self, data, signature):
        try:
            rsa.verify(data.encode(), signature, self.public_key)
            return True
        except rsa.VerificationError:
            return False
