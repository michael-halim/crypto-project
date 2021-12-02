from aes import encrypt,decrypt
import base64
import os
file_obj = open('secret_key.txt','r')
secret_key = file_obj.readline()
print('SECRET KEY')
print(secret_key)

path = 'database/user.txt'
with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()

cipher = encrypt(str.encode(secret_key),str.encode(data))
cipher = base64.b64encode(cipher)
cipher = cipher.decode("utf-8")

user_obj = open('test.txt','w')
user_obj.write(cipher)
print(cipher)


path = 'database/test.txt'
with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()


cobadecrypt = base64.b64decode(data)
print(cobadecrypt)
plaintext = decrypt(str.encode(secret_key), cobadecrypt)
print(plaintext)
plaintext = plaintext.decode("utf-8")
print(plaintext)

"""
import base64
cipher = encrypt(b'yunusyunusyunusy', b'ini adalah kalimat rahasia saya')
cipher = base64.b64encode(cipher)
cipher = cipher.decode("utf-8")
print(cipher)

cobadecrypt = base64.b64decode(cipher)
plaintext = decrypt(b'yunusyunusyunusy', cobadecrypt)
plaintext = plaintext.decode("utf-8")
print(plaintext)
"""


"""
import os
path = 'D:\\Kuliah Infor\\Kripto\\Proyek\\crypto-project\\7.txt'
if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()
    import base64
    data = base64.b64decode(data.replace('\n',''))

    key = b'YELLOW SUBMARINE'
    d = dec(key, data)
"""