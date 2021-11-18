import time
import pyotp
import pyqrcode
from PIL import Image
import os
from secret import generateSecret

secret_key = generateSecret()
print(secret_key)
pyotp.totp.TOTP(secret_key).provisioning_uri(name='alice1@google.com', issuer_name='Crypto Project')
totp = pyotp.TOTP(secret_key)
print("Current OTP:", totp.now())

# Generate QR code
url = pyqrcode.create(pyotp.totp.TOTP(secret_key).provisioning_uri(name='alice1@google.com', issuer_name='Crypto Project'))

# Create and save the png file naming "myqr.png"
url.png('myqr.png', scale = 6)
img = Image.open('myqr.png')
img.show()
time.sleep(1)

os.remove("myqr.png")

print("File Removed!")