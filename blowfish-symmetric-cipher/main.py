import getopt
import sys

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

    if len(opt) < 3:
        print("Error: expected at least 3 options: ([--fn], [--ks] and [--enc] or [--dec]) ", len(opt), " received")
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

    assert (file_name, key_size) is not None
    assert (encrypt and not decrypt) or (decrypt and not encrypt) or (not encrypt and not decrypt)

    return file_name, key_size, encrypt, decrypt


def main():
    print("Blowfish Symmetric Cipher - CTR Mode")
    file_name, key_size, encrypt, decrypt = option_reading()

    try:
        plaintext = functions.read_file(file_name)
        bf = BlowFishCTR(key_size)
    except FileNotFoundError:
        print("File not found")
        return
    except ValueError:
        print("Key size must be between 4 and 56 bytes")
        return

    if encrypt:
        functions.write_file(file_name + ".key", bf.key)
        cipher_text = bf.encrypt(plaintext)
        functions.write_file(file_name + ".enc", cipher_text)

    """
    cipher_text = bf.encrypt(plaintext)
    func.write_file('text_original.encrypted', cipher_text)

    cipher_text = func.read_file('text_original.encrypted')

    print('Encrypted message: ', cipher_text)
    print(bf.decrypt(cipher_text).decode())"""


if __name__ == '__main__':
    main()
