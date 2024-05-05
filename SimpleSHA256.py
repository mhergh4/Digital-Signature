import hashlib

def hash(input_data):
    sha_signature = hashlib.sha256(input_data.encode()).hexdigest()
    return sha_signature
