import os
import hashlib

def generate_nodeid():
    return hashlib.sha256(os.urandom(32)).hexdigest()[:10]

def generate_answerid():
    return hashlib.sha256(os.urandom(32)).hexdigest()[:5]