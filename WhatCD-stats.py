"""what.cd"""
import requests
import zipfile
import json
#import mechanize
#import cookielib


with zipfile.ZipFile("vitaminK's Snatches.zip", 'r') as myzip:
    torfilenames= myzip.namelist()

user = raw_input("username: ")
passw = raw_input("password: ")
#payload = {'username':user, 'password':passw, 'keeplogged': 1, 'login': 'Login'}
#test = requests.post("https://ssl.what.cd/login.php",payload)
#print test.text
#print test.cookies

#print "--------- here starts it ----------"
#index = requests.get("http://what.cd/ajax.php?action=index",cookies=test.cookies)
#print index.text

#I should probably have written this myself
#but someone already wrote a nice wrapper
#for the what.cd json api
#here https://github.com/isaaczafuta/whatapi/blob/master/whatapi/whatapi.py

headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept-Charset': 'utf-8',
    'User-Agent': 'whatapi [isaaczafuta]'
    }

class RequestException(Exception):
    pass

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

    def request(self, action, **kwargs):
        '''Makes an AJAX request at a given action page'''
        ajaxpage = 'https://ssl.what.cd/ajax.php'
        params = {'action': action}
        if self.authkey:
            params['auth'] = self.authkey
        params.update(kwargs)

        r = self.session.get(ajaxpage, params=params, allow_redirects=False)
        try:
            json_response = r.json()
            if json_response["status"] != "success":
                raise RequestException
            return json_response
        except ValueError:
            raise RequestException
    
    def get_tor_info(self, torrent_id):
        """gets torrent info given torrent id"""
        return self.request("torrent",id=torrent_id)

    def print_tor_info(self,torrent_id):
        print json.dumps(self.get_tor_info(torrent_id),indent=4,separators=(',',':'))

wcd = WhatAPI(username=user,password=passw)

tor_ids = [fl.split('-')[-1].strip('.torrent') for fl in torfilenames if fl!=u'Summary.txt']

for i in tor_ids[-10:]:
    print "\n"
    try:
        tor_info = wcd.get_tor_info(i)
        print tor_info['response']['group']['name']
        #wcd.print_tor_info
        for i in tor_info['response']['group']['musicInfo']:
            print "{0} --------------".format(i)
            print tor_info['response']['group']['musicInfo'][i]
    except RequestException:
        print "{0} didn't work".format(i)

#to-do: rate limiting on api requests
