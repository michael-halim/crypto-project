from sha import sha256
from datetime import datetime,date
import os
import re
import pandas as pd
from termcolor import colored
from threading import Event

def isNumber(txt,_min=6, _max=10): return True if re.match('^[0-9]{' + str(_min) + ',' + str(_max) + '}$',txt) else False
def isNotNumber(txt,_min=6, _max=10): return True if re.match('^[^0-9]{'+ str(_min) + ',' + str(_max) + '}$',txt) else False
def isEmail(txt): return True if re.match('[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+',txt) else False
def isPassword(txt,_min=8, _max=12): return True if re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{' + str(_min) + ',' + str(_max)+'}$',txt) else False
def createID(): return sha256(str(datetime.now().timestamp()))[:11]

def MENU(opt='START_MENU'):
    if opt == 'START_MENU':
        print('1. Login\n2. Sign up\n0. Log Off \n')
    elif opt == 'MAIN_MENU':
        print('1. Top Up\n2. Transfer\n3. History\n4. Download History\n0. Log Off \n')

    return input('>>> ')


def match(file_name, username, hashed, opt='LOGIN'):
    result = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                result.append((line.rstrip()))

    result = result[0].split()
    
    if opt == 'LOGIN':
        if result[2] == hashed:
            return 1      
        return 0

    elif opt == 'PIN':
        if result[-2] == hashed:
            return 1
        return 0

def fetchData(file_name,username):
    results = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                results.append((line.rstrip()))

    results = [result.split('#') for result in results]

    return results

def getReceiverName(file_name,phone,username):
    results = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if phone in line:
                results.append((line.rstrip()))
    
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
        download_df.to_csv('output.csv',index=False)
        return 1

    return 0

while True:
    chc = MENU()
    while chc not in ['1','2','0']:
        chc = input('Choose 1 / 2 / 0\n>>> ')

    if chc == '1':
        path = 'database/user.txt'
        username = input('Input Username : ')
        passwd = sha256(input('Input Password : '))
        
        if match(path,username, passwd,'LOGIN'):
            os.system('cls')
           
            path = 'database/history.txt'

            while True:
                print('=== CASH ===')
                print('Rp. ', calculateWallet(username))

                main_chc = MENU('MAIN_MENU')

                while main_chc not in ['1','2','3','4','0']:
                    main_chc = input('Choose 1 / 2 / 3 / 4 / 0\n>>> ')

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

                    f = open(path,'a')
                    f.write(string)
                    f.close()

                elif main_chc == '2':
                    print('==== TRANSFER MENU ====')
                    chc = input('Go Back (0) | Continue (1)\n>>> ')

                    while chc not in ['0','1']:
                        chc = input('Choose 1 / 0\n>>> ')
                    
                    if chc == '1':
                        while True:

                            phone = input('Input Phone Number : ')
                            while not isNumber(phone,10,13):
                                print('Phone Number Not Valid. ex: 081234567892')
                                phone = input('Input Phone Number : ')

                            receiver = getReceiverName('database/user.txt',phone,username)

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

                        if match('database/user.txt',username,pin,'PIN'):
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

                            f = open(path,'a')
                            f.write(string)
                            f.close()

                            print('=== SUCCESSFUL ===')
                            print('Transfer of {} Has Been Made to {}'.format(amount,receiver[1]))

                        else :
                            print('=== FAILED ===')
                            print('Wrong Security PIN')


                elif main_chc == '3':

                    history_data = fetchData(path,username)
                    history_data = [ prepareData(data) for data in history_data ]

                    print('Date'.ljust(12) + 'Time'.ljust(10) + 'Description'.ljust(22) + 
                    'Type'.ljust(10) + 'Amount'.ljust(10) + 'Sender'.ljust(12) +'Receiver')
                    
                    for data in history_data:
                        color = 'red'
                        if data[-1].strip() == username: color = 'green'
                        
                        for value in data:
                            print(colored(value,color),end='  ')

                        print()
                        
                elif main_chc == '4':
                    opt = 'EXCEL'
                    chc = input('Download to Excel (0) | Download to CSV (1)\n>>> ')
                    
                    while chc not in ['0','1']:
                        chc = input('Choose 1 / 0\n>>> ')
                    
                    
                    if opt == '1': opt = 'CSV'

                    history_data = fetchData(path,username)
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

                    
                elif main_chc == '0':
                    break
        else:
            print('Password atau Username Salah')

    if chc == '2':
        path = 'database/user.txt'
        
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

        if os.path.exists(path):
            string = userid + ' ' + username + ' ' + sha256(passwd) + ' ' + email + ' ' + pin + ' ' + phone + '\n'
            f = open(path,'a')
            f.write(string)
            f.close()
            
        else:
            string = userid + ' ' + username + ' ' + sha256(passwd) + ' ' + email + ' ' + pin + ' ' + phone + '\n'
            f = open(path,'a')
            f.write('id username password email pin phone \n')
            f.write(string)
            f.close()
    if chc == '0':
        break

    os.system('cls')