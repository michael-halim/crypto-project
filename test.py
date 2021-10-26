from datetime import datetime,date
from sha import sha256
def createID(): return sha256(str(datetime.now().timestamp()))[:11]

print(createID())