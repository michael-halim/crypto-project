"""
DOCUMENTED VERSION OF MAIN.PY
"""
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

# To edit google authenticator. 0 for disabled, 1 for enabled
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

#To Get Secret Google Authenticator Seed from User Database
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

#Return True if Google Auth is 1 and False if Google Auth 0
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

#To Get Salt from User Database
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

#This is Sign in Method. Can be used for PIN or LOGIN
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

#To Get Lines from History Database
def fetchData(file_name,username):
    results = []

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if username in line:
                results.append((line.rstrip()))

    results = [ result.split('#') for result in results ]

    return results

#To Get Receiver Name from Phone Number
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

#To Calculate Money from History Database
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

#To Prepare Data. Remove the '\n' from every lines in Database History When Taking Data
def prepareData(data):
    tmp = data[1].split()
    data = data[2:]
    [ tmp.append(val) for val in data ]

    return tmp

#To Download History in Excel or CSV
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

USER_PATH = 'database/user.txt'
HISTORY_PATH = 'database/history.txt'

while True:
    chc = MENU()
    while chc not in ['1','2','0']:
        chc = input('Choose 1 / 2 / 0\n>>> ')

    if chc == '1':

        # Check if Database is Exist. If not, Give Error Message
        if os.path.exists(USER_PATH):
            username = input('Input Username : ')

            # Get Salt from User Database
            salt = fetchSalt(USER_PATH,username)

            # Check if There is Salt or not. If The Return 0, User Doesn't Exist
            if not salt == 0:        
                
                # Hashing The Password and Salt
                passwd = sha256(input('Input Password : ') + salt)
                if match(USER_PATH,username, passwd,'LOGIN'):
                    
                    # Get The Secret GA and Check Whether The User Has Activate GA or Not
                    is_google_auth = isGA(USER_PATH,username)
                    secret = fetchSecret(USER_PATH,username)

                    # Is_Correct : Check True or False Google Authenticator Number
                    # Is_Login : If All Condition Are Met Then This Variable Turns to True and Can Go to Main Menu
                    # Is_Blocked : Turns to True and Kick You Out of The Program If You Input 5 Google Authenticator Wrong
                    is_correct = False
                    is_login = False
                    is_blocked = False
                    
                    if is_google_auth:
                        totp = pyotp.TOTP(secret)
                        user_input = input('Input Number From Google Authenticator\n>>>')

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
                        break
                    if is_google_auth and is_correct:
                        is_login = True

                    elif not is_google_auth and not is_correct:
                        is_login = True

                    # Login to Main Menu
                    if is_login:
                        os.system('cls')
                    
                        while True:
                            print('=== CASH ===')
                            # Calculate Money from History Database
                            money = calculateWallet(username)
                            print('Rp. ', money)
                            
                            # Get Main Menu List
                            main_chc = MENU('MAIN_MENU')

                            while main_chc not in ['1','2','3','4','5','0']:
                                main_chc = input('Choose 1 / 2 / 3 / 4 / 5 / 0\n>>> ')

                            # TOP UP MENU
                            if main_chc == '1':
                                # Create History ID
                                historyid = createID()

                                # Create Evenly Distributed Spaces For Display Later
                                spaces = [19,20,8,8,10,10]
                                _datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                                # Input Bank Name and The Error Catching
                                bank = input('Input Bank : ')
                                while not isNotNumber(bank,3,10):
                                    print('Bank Must Contain 3-10 Character with No Number')
                                    bank = input('Input Bank : ')

                                # Input Amount of Money Top up and The Error Catching
                                amount = input('Input Amount of Money : ')
                                while not isNumber(amount,5,8):
                                    print('Amount Invalid. Amount Must Not Have Alphabet')
                                    amount = input('Input Amount : ')

                                # Description with Fixed Name
                                desc = 'Top Up From ' + bank
                                sender = bank
                                receiver = username

                                # Transfer Type With Fixed 'Top Up' 
                                _type = 'Top Up'

                                # Create List of Data to be Iterated in For Loop
                                list_of_data = [_datetime, desc, _type, amount, sender,receiver]
                                
                                # Create 1 String With History To Datetime To Desc To The End With Some Spaces
                                string = historyid

                                for data,space in zip(list_of_data,spaces):
                                    string += '#'
                                    if len(data) < space:
                                        data = data + ' ' * (space-len(data))
                                    string += data

                                # Ended String with '\n' for Future Transaction
                                string += '\n'

                                # Append Transaction to History Database
                                f = open(HISTORY_PATH,'a')
                                f.write(string)
                                f.close()
                                print('Successfuly Top Up')

                            elif main_chc == '2':
                                # Can Go Back To Main Menu Without Exiting The Program
                                print('==== TRANSFER MENU ====')
                                chc = input('Go Back (0) | Continue (1)\n>>> ')

                                while chc not in ['0','1']:
                                    chc = input('Choose 1 / 0\n>>> ')
                                
                                # If Chose to Continue
                                if chc == '1':

                                    # This Variable is Used to Go Back to Main Menu 
                                    # If You Don't Have Enough Money To Transfer
                                    is_back_to_menu = False

                                    # Check The Receiver by Phone Number
                                    # Can't Self Transfer and Can't Transfer to Other That Aren't in User Database
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

                                    # Input Amount of Money to be Transfered
                                    amount = input('Input Amount : ')
                                    while not isNumber(amount,5,8):
                                        print('Amount Invalid. Amount Must Not Have Alphabet')
                                        amount = input('Input Amount : ')

                                    # Check if You Have Enough Money to Transfer
                                    # You Can go Back to Main Menu or Re-Input the Amount
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

                                        # Input PIN For Validate Transaction and Error Catching
                                        if match(USER_PATH,username,pin,'PIN'):

                                            # Create Transfer ID
                                            transferid = createID()

                                            # Create Datetime
                                            _datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                                            # Create Evenly Distributed Spaces For Display Later
                                            spaces = [19,20,8,8,10,10]

                                            # Create List of Data to be Iterated in For Loop
                                            list_of_data = [_datetime, desc, _type, amount, sender, receiver[1]]
                                            
                                            # Create 1 String With History To Datetime To Desc To The End With Some Spaces
                                            string = transferid

                                            for data,space in zip(list_of_data,spaces):
                                                string += '#'
                                                if len(data) < space:
                                                    data = data + ' ' * (space - len(data))
                                                string += data

                                            # Ended String with '\n' for Future Transaction
                                            string += '\n'

                                            # Append Transaction to History Database
                                            f = open(HISTORY_PATH,'a')
                                            f.write(string)
                                            f.close()

                                            print('=== SUCCESSFUL ===')
                                            print('Transfer of {} Has Been Made to {}'.format(amount,receiver[1]))

                                        else :
                                            print('=== FAILED ===')
                                            print('Wrong Security PIN')

                            elif main_chc == '3':
                                
                                # Get Data from History Database and Prepare it to Remove delimiter
                                history_data = fetchData(HISTORY_PATH,username)
                                history_data = [ prepareData(data) for data in history_data ]

                                # Print the Header
                                print('Date'.ljust(12) + 'Time'.ljust(10) + 'Description'.ljust(22) + 
                                'Type'.ljust(10) + 'Amount'.ljust(10) + 'Sender'.ljust(12) +'Receiver')
                                
                                # Print the Data, it prints red if transfer out and green if transfer in
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

                                # Take Data from History Database and Prepare it by removing Delimiter
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
                                # Get Secret GA from User Database
                                secret = fetchSecret(USER_PATH,username)
                                chc = input('Go Back (0) | Continue (1)\n>>> ')

                                while chc not in ['0','1']:
                                    chc = input('Choose 1 / 0\n>>> ')
                                
                                if chc == '1':
                                    ch = input('Deactivate (0) | Activate (1)\n>>> ')

                                    while chc not in ['0','1']:
                                        ch = input('Choose 1 / 0\n>>> ')

                                    if ch == '0':
                                        # Deactivate GA

                                        editActivation(USER_PATH,username,mode='DISABLE')
                                        print('Google Authenticator Has Been Disabled')

                                    elif ch == '1':
                                        # Activate GA

                                        editActivation(USER_PATH,username,mode='ENABLE')
                                        pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='Crypto Project')

                                        # Generate QR code
                                        url = pyqrcode.create(pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='Crypto Project'))

                                        # Create and save the png file naming "myqr.png"
                                        url.png('myqr.png', scale = 6)
                                        img = Image.open('myqr.png')
                                        img.show()
                                        time.sleep(1)

                                        os.remove("myqr.png")
                                        print('Google Authenticator Has Been Enabled')

                            elif main_chc == '0':
                                break
                            
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
        # Input Username and Error Catching
        username = input('Input Username : ')
        while not isNotNumber(username,8,10):
            print('Username Invalid')
            print('Username Must Contain 8-10 Character with No Number')
            username = input('Input Username : ')    
        
        # Input Password and Error Catching
        passwd = input('Input Password : ')
        while not isPassword(passwd):
            print('Password Invalid')
            print('Password Must Contain 1 Uppercase, 1 Special Character, 1 Number and At Least 8 Character')
            passwd = input('Input Password : ')

        # Input Email and Error Catching
        email = input('Input Email : ')
        while not isEmail(email):
            print('Email Invalid. example : john@gmail.com')
            email = input('Input Email : ')

        # Input PIN and Error Catching
        pin = input('Input PIN : ')
        while not isNumber(pin,6,6):
            print('PIN Invalid. PIN Must be Exactly 6 digits with no Alphabet')
            pin = input('Input PIN : ')

        # Input Phone Number and Error Catching
        phone = input('Input Phone Number : ')
        while not isNumber(phone,10,13):
            print('Phone Number Invalid. ex: 081234567892')
            phone = input('Input Phone Number : ')
            
        # Create ID, Salt, and Secret
        userid = createID()
        salt = generateID()
        secret = generateSecret()

        # Check If User Database Exist. If not Create One
        if os.path.exists(USER_PATH):

            # Create a string of Data and Append it to User Database
            string = str(userid) + ' ' + str(username) + ' ' + sha256(passwd + salt) + ' ' + str(email) + ' ' + str(pin) + ' ' + str(phone) + ' ' + str(salt) + ' ' + str(secret) +  ' ' + 0 + '\n'
            f = open(USER_PATH,'a')
            f.write(string)
            f.close()
            
        else:

            # Create a string of Data and Append it to User Database
            string = str(userid) + ' ' + str(username) + ' ' + sha256(passwd + salt) + ' ' + str(email) + ' ' + str(pin) + ' ' + str(phone) + ' ' + str(salt) + ' ' + str(secret) +  ' ' + 0 + '\n'
            f = open(USER_PATH,'a')
            f.write('id username password email pin phone salt secret activate\n')
            f.write(string)
            f.close()
        
        print('Account Created Successfuly')
        input('Press Anything to Continue')
        
    if chc == '0':
        break

    os.system('cls')