list_of_data = [['2021-10-23', '22:13:13', 'Transfer ke Halim', 'transfer', '300000', 'Yunus', 'Michael'], 
    ['2021-10-23', '22:13:13', 'Transfer Mobil', 'transfer', '3002000', 'Yunus', 'Michael'], 
    ['24-10-2021', '22:53:00', 'Top Up From BNI', 'Top Up', '14000', 'BNI', 'Michael']]

spaces = [10,8,20,8,8,10,10]

a = input('input :')

if len(a) < 8:
    a += ' ' * (8-len(a))
print(a,end='$')