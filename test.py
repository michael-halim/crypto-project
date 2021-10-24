a = ['1', '2021-10-23 22:13:13', 'Transfer ke Halim', 'transfer', '300000', 'Yunus', 'Michael']
b = a[1].split()
a = a[2:]
for val in a:
    b.append(val)
print(a)
print(b)