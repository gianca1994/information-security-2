from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate a public/ private key pair using 4096 bits key length (512 bytes)
new_key = RSA.generate(1024, e=65537)

# The private key in PEM format
private_key = new_key.exportKey("PEM")

# The public key in PEM Format
public_key = new_key.publickey().exportKey("PEM")

message = "Hello World"

# Encrypt the message with the public key

cipher = PKCS1_OAEP.new(RSA.importKey(public_key))
encrypted = cipher.encrypt(message.encode('utf-8'))

print(encrypted)

# Decrypt the message with the private key
cipher = PKCS1_OAEP.new(RSA.importKey(private_key))
decrypted = cipher.decrypt(encrypted)

print(decrypted.decode('utf-8'))




