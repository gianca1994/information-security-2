from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from hashlib import sha512
import pickle


class ServerRSA:
    def __init__(self):
        self.new_key = RSA.generate(1024, e=65537)
        self.private_key_server = self.new_key.exportKey("PEM")
        self.public_key_server = self.new_key.publickey().exportKey("PEM")
        self.public_key_client = ""
        self.cipher_encrypt = ""
        self.cipher_decrypt = ""

    def encrypt_message(self, message):
        return self.cipher_encrypt.encrypt(message.encode('utf-8'))

    def decrypt_message(self, encrypted):
        return self.cipher_decrypt.decrypt(encrypted).decode('utf-8')

    @staticmethod
    def hashed_message(message):
        return sha512(message.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_hash(message, hash):
        return sha512(message.encode('utf-8')).hexdigest() == hash


def protocol(client_socket, client_address):
    try:
        server_RSA = ServerRSA()
        client_socket.send(server_RSA.public_key_server)
        server_RSA.public_key_client = client_socket.recv(2048)
        server_RSA.cipher_encrypt = PKCS1_OAEP.new(RSA.importKey(server_RSA.public_key_client))
        server_RSA.cipher_decrypt = PKCS1_OAEP.new(RSA.importKey(server_RSA.private_key_server))

        while True:
            print("Waiting for message from client...")
            encrypted_receive = pickle.loads(client_socket.recv(2048))
            decrypted = server_RSA.decrypt_message(encrypted_receive["message"])

            if server_RSA.verify_hash(decrypted, encrypted_receive["hash"]):
                if decrypted == "/exit":
                    print(f"Client {client_address} has disconnected.")
                    client_socket.close()
                    break

                print(decrypted)

            else:
                print("Hashes do not match.")
                print(f"Client {client_address} has disconnected.")
                client_socket.close()
                break

            message = input("Enter message: ")
            encrypted_send = server_RSA.encrypt_message(message)
            message_to_send = pickle.dumps({
                "message": encrypted_send,
                "hash": server_RSA.hashed_message(message)
            })
            client_socket.send(message_to_send)

    except Exception as e:
        print(e)
