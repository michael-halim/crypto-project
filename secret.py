from lsfr import generateID

def generateSecret():
    string = generateID()
    new_str = ''
    for letter in string:
        if letter.isdigit():
            a = ord('A') + ord(letter)

            if a > ord('z'):
                a = a % ord('A')
            
            new_str += str(chr(a)).upper()
        else:
            new_str += letter.upper()
    return new_str[:10]

