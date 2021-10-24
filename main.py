from sha import sha256
import os

def MENU(opt='START_MENU'):
    if opt == 'START_MENU':
        print('1. Login\n2. Sign up\n0. Log Off \n')
    elif opt == 'MAIN_MENU':
        print('1. Top Up\n2. Transfer\n3. History\n0. Log Off \n')

    return input('>>>')

def login(file_name, username, hashed_pw):
    line_number = 0
    result = []

    with open(file_name, 'r') as read_obj:

        for line in read_obj:
            line_number += 1

            if username in line:
                result.append((line.rstrip()))

    result = result[0].split()
    
    if result[1] == hashed_pw:
        return 1
    
    return 0

while True:
    chc = MENU()
    while True:
            if chc in ['1','2','0']:
                break
            print('Choose 1 / 2 / 0')
            chc = input('>>>')

    if chc == '1':
        path = 'database/user.txt'
        username = input('Input Username : ')
        passwd = sha256(input('Input Password : '))
        
        if login(path,username, passwd):
            os.system('cls')

            while True:
                chc = MENU('MAIN_MENU')

        
        else:
            print('Password atau Username Salah')

    if chc == '2':
        username = input('Input Username : ')
        password = input('Input Password : ')
        path = 'database/user.txt'

        if os.path.exists(path):
            user = username + ' ' + sha256(password) + '\n'
            f = open(path,'a')
            f.write(user)
            f.close()
            
        else:
            user = username + ' ' + sha256(password) + '\n'
            f = open(path,'a')
            f.write('Username Password\n')
            f.write(user)
            f.close()
    if chc == '0':
        break