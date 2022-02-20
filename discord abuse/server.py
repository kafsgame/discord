from flask import Flask
import os
app = Flask(__name__)
f = open("captchatoken.txt", "r")
token = f.read()
f.close()
@app.route("/")
def hello():
    f = open("end.txt", "r")
    r = f.read()
    f.close()
    if(r == "1"):
        f = open("end.txt", "w")
        f.write("2")
        f.close()
        os.abort()
    return '<!DOCTYPE html><html><head><title></title></head><script src="https://hcaptcha.com/1/api.js" async=""></script><body><div class="h-captcha" data-sitekey="{}"></div></body></html>'.format(token)
app.run()