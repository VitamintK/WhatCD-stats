"""what.cd"""
import requests
#import mechanize
#import cookielib

user = raw_input("username: ")
passw = raw_input("password: ")
payload = dict(username=user, password=passw)
test = requests.post("http://what.cd/login.php",payload)
print test.text
