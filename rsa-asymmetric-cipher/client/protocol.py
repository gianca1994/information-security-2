from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from hashlib import sha512
import pickle


class ClientRSA:
    def __init__(self):
        self.new_key = RSA.generate(1024, e=65537)
        self.private_key_client = self.new_key.exportKey("PEM")
        self.public_key_client = self.new_key.publickey().exportKey("PEM")
        self.public_key_server = ""
        self.cipher_encrypt = ""
        self.cipher_decrypt = ""

    def encrypt_message(self, message):
        return self.cipher_encrypt.encrypt(message.encode('utf-8'))

    def decrypt_message(self, encrypted):
        return self.cipher_decrypt.decrypt(encrypted).decode('utf-8')


def protocol(client_socket):
    try:
        client_RSA = ClientRSA()
        client_RSA.public_key_server = client_socket.recv(2048)
        client_RSA.cipher_encrypt = PKCS1_OAEP.new(RSA.importKey(client_RSA.public_key_server))
        client_RSA.cipher_decrypt = PKCS1_OAEP.new(RSA.importKey(client_RSA.private_key_client))
        client_socket.send(client_RSA.public_key_client)

        while True:
            message = input("Enter message: ")
            message_to_send = pickle.dumps({
                "message: ": client_RSA.encrypt_message(message)
            })
            client_socket.send(message_to_send)

            if message == "/exit":
                break

            print("Waiting for message from server...")

            encrypted_receive = pickle.loads(client_socket.recv(2048))
            print(client_RSA.decrypt_message(encrypted_receive["message: "]))

    except Exception as e:
        print(e)
