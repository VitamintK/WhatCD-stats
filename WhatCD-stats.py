"""what.cd"""
import requests
import zipfile
#import mechanize
#import cookielib


with zipfile.ZipFile("vitaminK's Snatches.zip", 'r') as myzip:
    print myzip.namelist()

user = raw_input("username: ")
passw = raw_input("password: ")
payload = {'username':user, 'password':passw, 'keeplogged': 1, 'login': 'Login'}
test = requests.post("https://ssl.what.cd/login.php",payload)
print test.text
print test.cookies

print "--------- here starts it ----------"
index = requests.get("http://what.cd/ajax.php?action=index",cookies=test.cookies)
print index.text

class WhatAPI:
    def __init__(self, config=None, username=None, password=None):
        self.session = requests.Session()
        self.session.headers = headers
        self.authkey = None
        self.passkey = None
        if config:
            config = ConfigParser()
            config.read(config)
            self.username = config.get('login', 'username')
            self.password = config.get('login', 'password')
        else:
            self.username = username
            self.password = password
        self._login()

    def _login(self):
        '''Logs in user and gets authkey from server'''
        loginpage = 'https://ssl.what.cd/login.php'
        data = {'username': self.username,
                'password': self.password,
                'keeplogged': 1,
                'login': 'Login'
        }
        r = self.session.post(loginpage, data=data, allow_redirects=False)
        if r.status_code != 302:
            raise LoginException
        accountinfo = self.request("index")
        self.authkey = accountinfo["response"]["authkey"]
        self.passkey = accountinfo["response"]["passkey"]

wcd = WhatAPI(username=user,password=passw)


