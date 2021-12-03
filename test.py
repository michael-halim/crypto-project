# from aes import encrypt,decrypt
# import base64
# import os
# file_obj = open('secret_key.txt','r')
# secret_key = file_obj.readline()
# print('SECRET KEY')
# print(secret_key)

# path = 'database/user.txt'
# with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
#         data = f.read()

# cipher = encrypt(str.encode(secret_key),str.encode(data))
# cipher = base64.b64encode(cipher)
# cipher = cipher.decode("utf-8")

# user_obj = open('test.txt','w')
# user_obj.write(cipher)
# print(cipher)


# path = 'database/test.txt'
# with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
#         data = f.read()


# cobadecrypt = base64.b64decode(data)
# print(cobadecrypt)
# plaintext = decrypt(str.encode(secret_key), cobadecrypt)
# print(plaintext)
# plaintext = plaintext.decode("utf-8")
# print(plaintext)