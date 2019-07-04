import os
import hashlib

def generate_nodeid():
    return hashlib.sha256(os.urandom(32)).hexdigest()