"""what.cd"""
import requests
#import mechanize
#import cookielib

user = raw_input("username: ")
passw = raw_input("password: ")
payload = {'username':user, 'password':passw, 'keeplogged': 1, 'login': 'Login'}
test = requests.post("https://ssl.what.cd/login.php",payload)
print test.text
print test.cookies

print "--------- here starts it ----------"
index = requests.get("http://what.cd/ajax.php?action=index",cookies=test.cookies)
print index.text
