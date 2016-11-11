################################
#### Open credential example
################################
import pymssql

server = "server_ip"
user = "username"
password = "password"
database = "myDb"

conn = pymssql.connect(server, user, password, database)

################################
#### Encrypted version
################################
from cryptography.fernet import Fernet
import codecs
import pickle

# Generate and save the key
def generate_key(path):
    key = Fernet.generate_key()
    open(path, 'wb').write(key)
    return(key)

path = 'key.txt'
key = generate_key(path)

#Encode credentials
def cypher_creds(credentials,key):
    cipher_suite = Fernet(key)
    credentials_encrypted = []
    for credential in credentials:
        credentials_encrypted.append(cipher_suite.encrypt(str.encode(credential)))
    with open('credentials_encrypted.txt', 'wb') as f:
        pickle.dump(credentials_encrypted, f)


credentials = ["server_ip","username","password","myDb"]
cypher_creds(credentials,key)

################################
#   Retrieve the credentials
################################

def load_key(path_to_key):
    f = open(path)
    key = str.encode(f.read())
    return(key)

path = 'key.txt'
key = load_key(path)

def load_credentials(path_to_creds,key):
    f = open(path_to_creds,'rb')
    credentials_encrypted = pickle.load(f)
    cipher_suite = Fernet(key)
    credentials_decrypted = []
    for credential in credentials_encrypted:
        credentials_decrypted.append(codecs.decode(cipher_suite.decrypt(credential)))
    return(credentials_decrypted)


path_to_creds = "credentials_encrypted.txt"
credentials_decrypted = load_credentials(path_to_creds,key)

print(credentials_decrypted)



