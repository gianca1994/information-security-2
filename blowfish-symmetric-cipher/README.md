## Blowfish Symmetric Cipher - CTR Mode

### How to use

1. You must first modify the text of the test.txt file or create a new .txt file with the message you want to encrypt.
2. Then you must run the main.py file as follows:

```bash
$ python3 main.py --fn <FILE_NAME> --ks <KEY_SIZE> --enc 1
```

- fn -> receive a file name
- key -> receive a key minimum 4 bytes and maximum 56 bytes
- enc -> receive 1 if you want to encrypt

3. The program will generate a file containing the encrypted message with the name of the file entered with the extension .enc.
4. In addition, it will generate 3 other files:
    - .key -> contains the key used to encrypt the file
    - .iv -> contains the initialization vector used to encrypt the file
    - .hash -> contains the hash of the key + file
5. The receiver must have the .enc file, the .key file and the .iv file to decrypt the message and the .hash file to verify that it has not been modified.
6. To decrypt the message, the receiver must run the main.py file as follows:

```bash
$ python3 main.py --fn <FILE_NAME> --dec 1
```
- fn -> receive a file name
- dec -> receive 1 if you want to decrypt

7. The program will generate a file containing the decrypted message with the name of the file entered with the extension .dec.
8. When decrypting it will print a message, if you want to test, before pressing enter to verify the hashes, you can modify the message in the .dec file that was generated.
9. When finished, it will check that the hash of the .key + .dec file is equal to the hash of the .hash file, if so, then the message has not been modified.

Data
----
#### Encrypting a file

```bash
$ python3 main.py --fn <FILE_NAME> --ks <KEY_SIZE> --enc 1
```

#### Decrypting a file

```bash
$ python3 main.py --fn <FILE_NAME> --dec 1
```
