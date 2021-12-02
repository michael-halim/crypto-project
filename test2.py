from secret import generateSecret

a = str(generateSecret()) + str(generateSecret())[:16]
print(a)