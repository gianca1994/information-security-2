import getopt
import sys
from os import urandom

from src.BlowFishCTR import BlowFishCTR
from src import functions


def option_reading():
    file_name = key_size = None
    encrypt = decrypt = False
    try:
        (opt, arg) = getopt.getopt(
            sys.argv[1:],
            shortopts=None,
            longopts=['fn=', 'ks=', 'enc=', 'dec=']
        )
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    if len(opt) < 2:
        print("Error: expected at least 2 options: ([--fn], [--ks] and [--enc] or [--fn] and [--dec]) ", len(opt),
              " received")
        sys.exit(0)

    for (opt, arg) in opt:
        if opt == '--fn':
            file_name = arg
        elif opt == '--ks':
            key_size = int(arg)
        elif opt == '--enc':
            encrypt = True if int(arg) == 1 else False
        elif opt == '--dec':
            decrypt = True if int(arg) == 1 else False

    assert file_name is not None
    assert (key_size is None and encrypt is False) or (key_size is not None and encrypt is True)
    assert encrypt != decrypt

    return file_name, key_size, encrypt, decrypt


def main():
    print("Blowfish Symmetric Cipher - CTR Mode")
    file_name, key_size, encrypt, decrypt = option_reading()
    file_name = file_name if encrypt else file_name[:-4]

    try:
        plaintext = functions.read_file(file_name)
        key_size = key_size if key_size is not None else functions.read_file(file_name + ".key")
        iv = urandom(8) if encrypt else functions.read_file(file_name + ".iv")
        bf = BlowFishCTR(key_size, iv)
    except FileNotFoundError:
        print("File not found")
        return
    except ValueError:
        print("Key size must be between 4 and 56 bytes")
        return

    if encrypt:
        functions.write_file(file_name + ".key", bf.key)
        functions.write_file(file_name + ".iv", bf.iv)
        functions.write_file(file_name + ".enc", bf.encrypt(plaintext))
        functions.write_file(file_name + ".hash", functions.hash_file(str(bf.key), file_name).encode())
        print("Encryption completed")

    if decrypt:
        try:
            cipher_text = functions.read_file(file_name + ".enc")
        except FileNotFoundError:
            print("File not found")
            return

        plain_text = bf.decrypt(cipher_text)
        functions.write_file(file_name + ".dec", plain_text)
        print("Decryption completed")

        input("This input was added to test that the file was moved on the way to the receiver. Press enter to "
              "continue.")

        print(f"Hash {file_name}: " + functions.hash_file(str(bf.key), file_name))
        print(f"Hash {file_name}.hash: " + functions.read_file(file_name + ".hash").decode())

        if functions.check_hash(str(bf.key), file_name + ".dec", functions.read_file(file_name + ".hash").decode()):
            print("Hash check: The file was not modified")
        else:
            print("Hash check: The file was modified")


if __name__ == '__main__':
    main()
