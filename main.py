from sha import sha256
from datetime import datetime,date
import os
import re
from threading import Event

def isNumber(txt,_min=6, _max=10): return True if re.match('^[0-9]{' + str(_min) + ',' + str(_max) + '}$',txt) else False
def isNotNumber(txt,_min=6, _max=10): return True if re.match('^[^0-9]{'+ str(_min) + ',' + str(_max) + '}$',txt) else False

def MENU(opt='START_MENU'):
    if opt == 'START_MENU':
        print('1. Login\n2. Sign up\n0. Log Off \n')
    elif opt == 'MAIN_MENU':
        print('1. Top Up\n2. Transfer\n3. History\n0. Log Off \n')

    return input('>>>')


def match(file_name, username, hashed, opt='LOGIN'):
    line_number = 0
    result = []

    with open(file_name, 'r') as read_obj:

        for line in read_obj:
            line_number += 1

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
    line_number = 0
    results = []

    with open(file_name, 'r') as read_obj:

        for line in read_obj:
            line_number += 1

            if username in line:
                results.append((line.rstrip()))

    results = [result.split('#') for result in results]

    return results


def getReceiverName(file_name,phone,username):
    line_number = 0
    results = []
    status = None
    with open(file_name, 'r') as read_obj:

        for line in read_obj:
            line_number += 1

            if phone in line:
                results.append((line.rstrip()))
    
    
    if results:
        results = [result.split(' ') for result in results]
        
        if results[0][1] == username:
            return ('300','Can\'t Self Transfer')

        return ('1',results[0][1])
    else:
        return ('400','Phone Number Not Found')

def prepareData(data):
    tmp = data[1].split()
    data = data[2:]
    [ tmp.append(val) for val in data ]

    return tmp

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
        
        if match(path,username, passwd,'LOGIN'):
            os.system('cls')
            path = 'database/history.txt'

            while True:
                main_chc = MENU('MAIN_MENU')

                while True:
                    if main_chc in ['1','2','3','0']:
                        break
                    print('Choose 1 / 2 / 3 / 0')
                    main_chc = input('>>>')

                if main_chc == '1':

                    now = datetime.now()
                    epoch = now.timestamp()
                    historyid = sha256(str(epoch))[:11]
                    # spaces = [10,8,20,8,8,10,10]
                    spaces = [19,20,8,8,10,10]
                    _datetime = str(now.strftime('%Y-%m-%d %H:%M:%S'))
                    bank = input('Input Bank : ')
                    amount = input('Input Amount of Money : ')
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
                    while True:
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
                    pin = input('Enter PIN : ')

                    if match('database/user.txt',username,pin,'PIN'):
                        print('Berhasil Transfer')
                        print('Transfer of {} Has Been Made to {}'.format(amount,receiver))

                    else :
                        print('Tidak Berhasil')


                elif main_chc == '3':

                    history_data = fetchData(path,username)
                    history_data = [ prepareData(data) for data in history_data ]

                    print('Date'.ljust(12) + 'Time'.ljust(10) + 'Description'.ljust(22) + 
                    'Type'.ljust(10) + 'Amount'.ljust(10) + 'Sender'.ljust(12) +'Receiver')
                    
                    for data in history_data:
                        for value in data:
                            print(value,end='  ')

                        print()
                
                elif main_chc == '0':
                    break
        else:
            print('Password atau Username Salah')

    if chc == '2':
        path = 'database/user.txt'
        username = input('Input Username : ')
        passwd = input('Input Password : ')
        email = input('Input Email : ')
        pin = input('Input PIN : ')
        phone = input('Input Phone Number : ')     
        now = datetime.now()
        epoch = now.timestamp()
        userid = sha256(str(epoch))[:11]

        if os.path.exists(path):
            user = userid + ' ' + username + ' ' + sha256(passwd) + ' ' + email + ' ' + pin + ' ' + phone + '\n'
            f = open(path,'a')
            f.write(user)
            f.close()
            
        else:
            user = userid + ' ' + username + ' ' + sha256(passwd) + ' ' + email + ' ' + pin + ' ' + phone + '\n'
            f = open(path,'a')
            f.write('id username password email pin phone \n')
            f.write(user)
            f.close()
    if chc == '0':
        break

    os.system('cls')