from sha import sha256
import os

def search_string_in_file(file_name, string_to_search):
    line_number = 0
    list_of_results = []

    with open(file_name, 'r') as read_obj:

        for line in read_obj:
            line_number += 1

            if string_to_search in line:
                list_of_results.append((line_number, line.rstrip()))

    return list_of_results

def menu():
    print('1. Login\n2. Sign up\n0. Log Off \n')

while True:
    menu()
    while True:
            chc = input('>>>')
            if chc in ['1','2','0']:
                break
            print('Choose 1 / 2 / 0')
    

    if chc == '1':  
        a = search_string_in_file(path,'Michael')
        print(a)
            
    if chc == '2':
        username = input('Input Username : ')
        password = input('Input Password : ')
        path = 'database/user.txt'
        print(os.path.exists(path))
        if os.path.exists(path):
            user = username + ' ' + password + '\n'
            f = open(path,'a')
            f.write(user)
            f.close()
            
        else:
            user = username + ' ' + password + '\n'
            f = open(path,'a')
            f.write('Username Password\n')
            f.write(user)
            f.close()
    if chc == '0':
        break