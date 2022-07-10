# Cryptography Final Project
##### The task of this project is to used 3 or more security concepts to implement that in an app. This app is CLI based Fintech that has a feature to transfer money, see history, download history, sign in and sign up flow, and activate security with 3rd party such as Google Authenticator

##### Cryptography Final Project to create an fintech application. The main assignment of this project is to used 3 or more security concepts to implement in app. We use SHA-256 and salt to encrypt password , AES-128 to encrypt database file,  LSFR to make Random Generated Number, and 2 FA security that uses Google Authenticator to login into an account

### Installation
1. ```git clone https://github.com/michael-halim/crypto-project```
2. ```python main.py``` or ```Ctrl + F5``` in main.py in VSCode

#### App Feature
1. Login 
  - When login input username and password
  - it raises an error if user database is not exist
  - it raises an error if username is not exist
  - it raises an error if password is incorrect
  - if you have activate Google Authenticator, you'll be asked about combination in that GA App
  - if you make 5 incorrect combination number from Google Authenticator, it will automatically log out

2. Main Menu
  - Sign Up
    - Sign up required information such as username, password, email , PIN number, and phone number

  - Top Up
    - Top Up menu will ask for what bank you want to top up and how much you want to transfer
 
  - Transfer
    - Transfer will ask for a phone number of recipient you want to transfer, how much you want to transfer, description, and PIN number
    - **NOTES**
    - You can't transfer to your own phone number, it will raise an error
    - If you don't have enough money or you want to transfer money more than you have, it will raise an error
    - If PIN number you inputed is incorrect, it won't transfer the money
    - If description is too long, you can't continue to transfer the money
    
  - History
    - History menu will gives transaction history from the moment you build an account
    - Green text mean that you have incoming transaction and red text mean you have outgoing transaction

  - Download History
    - Download History menu can download history of transaction into excel or csv files (.xlsx or .csv)

  - Security
    - Security Menu will gives option to ENABLE or DISABLE Google Authenticator that are connected to the real GA App in mobile phone that can be downloaded from Google Play

   - Log Off
     - Log Off get you out of the application
     
#### Security Feature
| # | Feature |
| - | ------- |
| 1 | Uses SHA-256 to encrypt password with salt so that it won't be easily be hacked |
| 2 | Uses LSFR as a method for RNG that uses to generate secret for GA, user ID, and Secret Key |
| 3 | Uses AES-128 to encrypt database everytime you uses this application | 
| 4 | Secret Key for AES-128 is randomly generated everytime you exit an application |
| 5 | It has user input validation to validate every user input |
| 6 | email and phone number is validated so that it is really a valid value |

#### User Table
| id | username | password | email | pin | phone | salt | secret | activate |
| -- | -------- | -------- | ----- | --- | ----- | ---- | ------ | -------- |

#### History Table
| id | datetime | judul | jenis | nominal | pengirim | penerima |
| -- | -------- | ----- | ----- | ------- | -------- | -------- |
