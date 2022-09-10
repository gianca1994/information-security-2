from hashlib import sha512

path_file = "test/"


def read_file(filename):
    with open(path_file + filename, 'rb') as f:
        return f.read()


def write_file(filename, data):
    with open(path_file + filename, 'wb') as f:
        f.write(data)


def hash_file(key, filename):
    return sha512(key.encode() + read_file(filename)).hexdigest()


def check_hash(key, filename, hash):
    return hash_file(key, filename) == hash
