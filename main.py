from sha import sha256
from datetime import datetime
import os
import re
import pandas as pd
from termcolor import colored
import time
import pyotp
import pyqrcode
from PIL import Image
from lsfr import generateID
from secret import generateSecret
from aes import encrypt as aes_encryption ,decrypt as aes_decryption
import base64

def isNumber(txt,_min=6, _max=10): return True if re.match('^[0-9]{' + str(_min) + ',' + str(_max) + '}$',txt) else False
def isNotNumber(txt,_min=6, _max=10): return True if re.match('^[^0-9]{'+ str(_min) + ',' + str(_max) + '}$',txt) else False
def isEmail(txt): return True if re.match('[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+',txt) else False
def isPassword(txt,_min=8, _max=12): return True if re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{' + str(_min) + ',' + str(_max)+'}$',txt) else False
def createID(): return generateID()

def MENU(opt='START_MENU'):
    if opt == 'START_MENU':
        print('1. Login\n2. Sign up\n0. Log Off \n')
    elif opt == 'MAIN_MENU':
        print('1. Top Up\n2. Transfer\n3. History\n4. Download History\n5. Security\n0. Log Off \n')

    return input('>>> ')

def editActivation(file_name,username,mode='ENABLE'):

    list_of_lines = open(file_name,'r').readlines()
    ctr = 0
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                break
            ctr += 1

    if mode == 'ENABLE':
        list_of_lines[ctr] = list_of_lines[ctr][:-2] + '1\n'
        open(file_name,'w').writelines(list_of_lines)
        return 1

    elif mode == 'DISABLE':
        list_of_lines[ctr] = list_of_lines[ctr][:-2] + '0\n'
        open(file_name,'w').writelines(list_of_lines)
        return 1

    return 0

def fetchSecret(file_name,username):
    result = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                result.append((line.rstrip()))
                break

    if not result:
        return 0

    result = result[0].split()
    
    return result[-2]

def isGA(file_name,username):
    result = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                result.append((line.rstrip()))
                break

    if not result:
        return 0

    result = result[0].split()
    if result[-1] == '1':
        return 1
    return 0

def fetchSalt(file_name, username):
    result = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                result.append((line.rstrip()))
                break

    if not result:
        return 0

    result = result[0].split()
    
    return result[-3]


def match(file_name, username, hashed, opt='LOGIN'):
    result = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                result.append((line.rstrip()))
                break

    if not result:
        return 0

    result = result[0].split()
    
    if opt == 'LOGIN':
        if result[2] == hashed:
            return 1      
        return 0

    elif opt == 'PIN':
        if result[4] == hashed:
            return 1
        return 0

def fetchData(file_name,username):
    results = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                results.append((line.rstrip()))

    results = [ result.split('#') for result in results ]

    return results

def getReceiverName(file_name,phone,username):
    results = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if phone in line:
                results.append((line.rstrip()))
                break
    
    if results:
        results = [result.split(' ') for result in results]
        
        if results[0][1] == username:
            return ('300','Can\'t Self Transfer')

        return ('1',results[0][1])
    else:
        return ('400','Phone Number Not Found')

def calculateWallet(username):
    file_name = 'database/history.txt'
    results = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                results.append((line.rstrip()))
    
    wallet = 0

    if results:
        results = [result.split('#') for result in results]

        for result in results:
            if result[-1] == username: wallet += int(result[-3])
            else: wallet -= int(result[-3])
        
        return wallet

    return wallet

def prepareData(data):
    tmp = data[1].split()
    data = data[2:]
    [ tmp.append(val) for val in data ]

    return tmp

def downloadHistory(opt='EXCEL'):
    _date, time, desc, _type = [ row[0] for row in results],[ row[1] for row in results], [ row[2] for row in results],[ row[3] for row in results]
    amount, sender, receiver = [ row[4] for row in results], [ row[5] for row in results], [ row[6] for row in results]
    
    download_df = pd.DataFrame({
        'Date':_date,
        'Time':time,
        'Description':desc,
        'Type':_type,
        'Amount':amount,
        'Sender':sender,
        'Receiver':receiver
        })

    if opt == 'EXCEL':
        output = pd.ExcelWriter('output.xlsx')
        download_df.to_excel(output)
        output.save()
        return 1

    elif opt == 'CSV':
        download_df.to_csv(r'output.csv',index=False)
        return 1

    return 0

def get_key():
    file_obj = open('secret_key.txt','r')
    return file_obj.readline()


def create_new_secret_key():
    new_key = str(generateSecret()) + str(generateSecret())
    new_key = new_key[:16]
    sk_obj = open('secret_key.txt','w')
    sk_obj.write(new_key)
    return new_key

def encryptDatabase(secret):

    with open(os.path.join(os.path.dirname(__file__), USER_PATH), 'r') as f:
            data = f.read()

    cipher = aes_encryption(str.encode(secret),str.encode(data))
    cipher = base64.b64encode(cipher)
    cipher = cipher.decode("utf-8")
    user_obj = open('database/user.txt','w')
    user_obj.write(cipher)

    with open(os.path.join(os.path.dirname(__file__), HISTORY_PATH), 'r') as f:
            data = f.read()

    cipher = aes_encryption(str.encode(secret),str.encode(data))
    cipher = base64.b64encode(cipher)
    cipher = cipher.decode("utf-8")
    history_obj = open('database/history.txt','w')
    history_obj.write(cipher)

def decryptDatabase():
    with open(os.path.join(os.path.dirname(__file__), USER_PATH), 'r') as f:
            data = f.read()
    cobadecrypt = base64.b64decode(data)
    plaintext = aes_decryption(str.encode(SECRET_KEY), cobadecrypt)
    plaintext = plaintext.decode("utf-8")

    user_obj = open('database/user.txt','w')
    user_obj.write(plaintext)

    with open(os.path.join(os.path.dirname(__file__), HISTORY_PATH), 'r') as f:
            data = f.read()
    cobadecrypt = base64.b64decode(data)
    plaintext = aes_decryption(str.encode(SECRET_KEY), cobadecrypt)
    plaintext = plaintext.decode("utf-8")

    history_obj = open('database/history.txt','w')
    history_obj.write(plaintext)


USER_PATH = 'database/user.txt'
HISTORY_PATH = 'database/history.txt'
SECRET_KEY = get_key()
decryptDatabase()

while True:

    chc = MENU()
    while chc not in ['1','2','0']:
        chc = input('Choose 1 / 2 / 0\n>>> ')

    if chc == '1':

        if os.path.exists(USER_PATH):
            username = input('Input Username : ')
            salt = fetchSalt(USER_PATH,username)

            if not salt == 0:        

                passwd = sha256(input('Input Password : ') + salt)
                if match(USER_PATH,username, passwd,'LOGIN'):

                    is_google_auth = isGA(USER_PATH,username)
                    secret = fetchSecret(USER_PATH,username)

                    is_correct = False
                    is_login = False
                    is_blocked = False
                    
                    if is_google_auth:
                        totp = pyotp.TOTP(secret)
                        user_input = input('Input Number From Google Authenticator\n>>> ')

                        if user_input == totp.now():
                            is_correct = True
                        else:
                            tries = 4
                            print('The Code is Invalid. Try Again !\n')
                            print('You Have 4 More Tries')

                            while not user_input == totp.now():
                                user_input = input('Input Number From Google Authenticator\n>>>')

                                if user_input == totp.now():
                                    is_correct = True
                                    break

                                tries -= 1
                                if tries <= 0:
                                    print('You Make 5 Mistakes Aldready')
                                    input('Press Anything to Continue')
                                    is_blocked = True
                                    break

                                print('You Have ', tries, ' More Tries')
                    
                    if is_blocked:
                        new_key = create_new_secret_key()
                        encryptDatabase(secret=new_key)
                        break
                    if is_google_auth and is_correct:
                        is_login = True

                    elif not is_google_auth and not is_correct:
                        is_login = True

                    if is_login:
                        os.system('cls')
                    
                        while True:
                            print('=== CASH ===')
                            money = calculateWallet(username)
                            print('Rp. ', money)

                            main_chc = MENU('MAIN_MENU')

                            while main_chc not in ['1','2','3','4','5','0']:
                                main_chc = input('Choose 1 / 2 / 3 / 4 / 5 / 0\n>>> ')

                            if main_chc == '1':

                                historyid = createID()

                                spaces = [19,20,8,8,10,10]
                                _datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                                bank = input('Input Bank : ')
                                while not isNotNumber(bank,3,10):
                                    print('Bank Must Contain 3-10 Character with No Number')
                                    bank = input('Input Bank : ')

                                amount = input('Input Amount of Money : ')
                                while not isNumber(amount,5,8):
                                    print('Amount Invalid. Amount Must Not Have Alphabet')
                                    amount = input('Input Amount : ')

                                desc = 'Top Up From ' + bank
                                sender = bank
                                receiver = username
                                _type = 'Top Up'

                                list_of_data = [_datetime, desc, _type, amount, sender,receiver]
                                
                                string = historyid

                                for data,space in zip(list_of_data,spaces):
                                    string += '#'
                                    if len(data) < space:
                                        data = data + ' ' * (space-len(data))
                                    string += data

                                string += '\n'

                                f = open(HISTORY_PATH,'a')
                                f.write(string)
                                f.close()
                                print('Successfuly Top Up')

                            elif main_chc == '2':
                                print('==== TRANSFER MENU ====')
                                chc = input('Go Back (0) | Continue (1)\n>>> ')

                                while chc not in ['0','1']:
                                    chc = input('Choose 1 / 0\n>>> ')
                                
                                if chc == '1':
                                    is_back_to_menu = False
                                    while True:

                                        phone = input('Input Phone Number : ')
                                        while not isNumber(phone,10,13):
                                            print('Phone Number Not Valid. ex: 081234567892')
                                            phone = input('Input Phone Number : ')

                                        receiver = getReceiverName(USER_PATH,phone,username)

                                        if receiver[0] == '1':
                                            print('Receiver : ', receiver[1])
                                            break
                                        elif receiver[0] == '300':
                                            print(receiver[1])
                                        elif receiver[0] == '400':
                                            print(receiver[1])

                                    amount = input('Input Amount : ')
                                    while not isNumber(amount,5,8):
                                        print('Amount Invalid. Amount Must Not Have Alphabet')
                                        amount = input('Input Amount : ')

                                    while int(money) - int(amount) < 0:
                                        print('You Don\'t Have Enough Money to Transfer Rp.',amount)
                                        chc = input('Go Back (0) | Continue (1)\n>>> ')

                                        while chc not in ['0','1']:
                                            chc = input('Choose 1 / 0\n>>> ')
                                        
                                        if chc == '0':
                                            is_back_to_menu = True 
                                            break
                                        else:
                                            amount = input('Input Amount : ')
                                            while not isNumber(amount,5,8):
                                                print('Amount Invalid. Amount Must Not Have Alphabet')
                                                amount = input('Input Amount : ')

                                    if not is_back_to_menu :
                                        desc = input('Input Description : ')
                                        while len(desc) > 20:
                                            print('Maximum Description Length Must Be 20 Characters')
                                            desc = input('Input Description : ')

                                        pin = input('Enter PIN : ')
                                        while not isNumber(pin,6,6):
                                            print('PIN Invalid. PIN Must be Exactly 6 digits with no Alphabet')
                                            pin = input('Input PIN : ')

                                        sender = username
                                        _type = 'Transfer'

                                        if match(USER_PATH,username,pin,'PIN'):
                                            transferid = createID()
                                            _datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                                            spaces = [19,20,8,8,10,10]

                                            list_of_data = [_datetime, desc, _type, amount, sender, receiver[1]]

                                            string = transferid

                                            for data,space in zip(list_of_data,spaces):
                                                string += '#'
                                                if len(data) < space:
                                                    data = data + ' ' * (space - len(data))
                                                string += data

                                            string += '\n'

                                            f = open(HISTORY_PATH,'a')
                                            f.write(string)
                                            f.close()

                                            print('=== SUCCESSFUL ===')
                                            print('Transfer of {} Has Been Made to {}'.format(amount,receiver[1]))

                                        else :
                                            print('=== FAILED ===')
                                            print('Wrong Security PIN')

                            elif main_chc == '3':

                                history_data = fetchData(HISTORY_PATH,username)
                                history_data = [ prepareData(data) for data in history_data ]

                                print('Date'.ljust(12) + 'Time'.ljust(10) + 'Description'.ljust(22) + 
                                'Type'.ljust(10) + 'Amount'.ljust(10) + 'Sender'.ljust(12) +'Receiver')
                                
                                for data in history_data:
                                    color = 'red'
                                    if data[-1].strip() == username: color = 'green'
                                    
                                    for value in data:
                                        print(colored(value,color),end='  ')

                                    print()

                                print('\n\n\n')
                                print('==================================')

                            elif main_chc == '4':
                                chc = input('Download to Excel (0) | Download to CSV (1)\n>>> ')
                                
                                while chc not in ['0','1']:
                                    chc = input('Choose 1 / 0\n>>> ')
                                
                                opt = 'EXCEL'
                                if chc == '1': 
                                    opt = 'CSV'

                                history_data = fetchData(HISTORY_PATH,username)
                                history_data = [ prepareData(data) for data in history_data ]
                                
                                results = []
                                for data in history_data:
                                    tmp = []
                                    for value in data:
                                        tmp.append(value.strip())
                                    results.append(tmp)


                                if downloadHistory(opt): 
                                    print('File Downloaded Successfully')
                                else : 
                                    print('There\'s Problem Downloading File')
                                
                            elif main_chc == '5':
                                secret = fetchSecret(USER_PATH,username)
                                chc = input('Go Back (0) | Continue (1)\n>>> ')

                                while chc not in ['0','1']:
                                    chc = input('Choose 1 / 0\n>>> ')
                                
                                if chc == '1':
                                    ch = input('Deactivate (0) | Activate (1)\n>>> ')

                                    while chc not in ['0','1']:
                                        ch = input('Choose 1 / 0\n>>> ')

                                    if ch == '0':
                                        editActivation(USER_PATH,username,mode='DISABLE')
                                        print('Google Authenticator Has Been Disabled')

                                    elif ch == '1':
                                        editActivation(USER_PATH,username,mode='ENABLE')
                                        pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='Crypto Project')

                                        url = pyqrcode.create(pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='Crypto Project'))

                                        url.png('myqr.png', scale = 6)
                                        img = Image.open('myqr.png')
                                        img.show()
                                        time.sleep(1)

                                        os.remove("myqr.png")
                                        print('Google Authenticator Has Been Enabled')

                            elif main_chc == '0':
                                new_key = create_new_secret_key()
                                encryptDatabase(secret=new_key)
                                print('Application Closed Successfuly')
                                input('Press Anything to Continue')
                                quit()
                            
                            input('Press Anything to Continue')
                            os.system('cls')
                    else:
                        print('Login Error')
                        input('Press Anything to Continue')
                        
                else:
                    print('Password atau Username Salah')
                    input('Press Anything to Continue')

            else:
                print('User Doesn\'t Exist')
                input('Press Anything to Continue')

        else:
            print('Path to User Don\'t Exist \n')
            input('Press Anything to Continue')

    if chc == '2':

        username = input('Input Username : ')
        while not isNotNumber(username,8,10):
            print('Username Invalid')
            print('Username Must Contain 8-10 Character with No Number')
            username = input('Input Username : ')    
        
        passwd = input('Input Password : ')
        while not isPassword(passwd):
            print('Password Invalid')
            print('Password Must Contain 1 Uppercase, 1 Special Character, 1 Number and At Least 8 Character')
            passwd = input('Input Password : ')

        email = input('Input Email : ')
        while not isEmail(email):
            print('Email Invalid. example : john@gmail.com')
            email = input('Input Email : ')

        pin = input('Input PIN : ')
        while not isNumber(pin,6,6):
            print('PIN Invalid. PIN Must be Exactly 6 digits with no Alphabet')
            pin = input('Input PIN : ')

        phone = input('Input Phone Number : ')
        while not isNumber(phone,10,13):
            print('Phone Number Invalid. ex: 081234567892')
            phone = input('Input Phone Number : ')
            
        userid = createID()
        salt = generateID()
        secret = generateSecret()

        string = str(userid) + ' ' + str(username) + ' ' + sha256(passwd + salt) + ' ' + str(email) + ' ' + str(pin) + ' ' + str(phone) + ' ' + str(salt) + ' ' + str(secret) +  ' ' + '0' + '\n'
        f = open(USER_PATH,'a')
        f.write(string)
        f.close()
        
        print('Account Created Successfuly')
        input('Press Anything to Continue')
    if chc == '0':
        new_key = create_new_secret_key()
        encryptDatabase(secret=new_key)
        print('Application Closed Successfuly')
        input('Press Anything to Continue')
        break

    os.system('cls')