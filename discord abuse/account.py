from random import randint



def randstr(l):
    str = ""
    strpool = "qwertyuiopasdfghjklzxcvbnm0123456789"
    for i in range(l):
        str += strpool[randint(0, len(strpool)-1)]
    return str



class Account:
    def __init__(self, token, proxyIP=None, proxyPORT=None, proxyLOG=None, proxyPASS=None):
        if proxyIP != None:
            self.proxyIP = proxyIP
            self.proxyLOG = proxyLOG
            self.proxyPASS = proxyPASS
            self.proxyPORT = proxyPORT
        self.token = token

    def getHeaders(self):
        return {
            "authorization": self.token,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
        }
