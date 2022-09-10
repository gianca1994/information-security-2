path_file = "test/"


def read_file(filename):
    with open(path_file + filename, 'rb') as f:
        return f.read()


def write_file(filename, data):
    with open(path_file + filename, 'wb') as f:
        f.write(data)

