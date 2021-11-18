from datetime import datetime
from sha import sha256

def generateID():
    now = datetime.now()
    _hour, _min, _sec = int(now.strftime("%H")), int(now.strftime("%M")),int(now.strftime("%S"))
    total = bin(_hour * _min * _sec)
    state = int(total,base=2)
    length = len(total[2:])

    lsfr = ''
    for i in range(20):
        lsfr += str(state & 1)
        newbit = (state ^ (state >> 1)) & 1
        state = (state >> 1) | (newbit << length)

    lsfr = hex(int(lsfr,base=10))
    return sha256(str(lsfr[2:]))[:11]