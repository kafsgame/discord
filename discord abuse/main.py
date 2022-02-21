import requests
from account import Account
from time import sleep
from colorama import Fore
import json
from selenium import webdriver
import os

isProxy = input("нужны ли прокси?(y/n)")
if isProxy=="y":
    isProxy=True
    print("Для работы бота нужны токены от аккаунтов дискорда и прокси для каждого аккаунта, которые должны будут находиться в файле под названием token.txt каждый токен должен находиться на новой строке. Формат такой: токен:айпи:порт:логинПрокси:парольПрокси")
else:
    isProxy=False
    print("Для работы бота нужны токены от аккаунтов дискорда, которые должны будут находиться в файле под названием token.txt каждый токен должен находиться на новой строке")

delay = int(input("Введите задержку между обработкой аккаунтов в целых секундах ----->"))
def start_server(token):
    f = open("captchatoken.txt", "w")
    f.write(token)
    f.close()
    os.system("start aaa.bat")
def make_accounts_from_tokens(proxy):
    accounts = []

    f = open("token.txt", "r")
    tokens = f.read()
    f.close()
    tokens += "\n"
    if(proxy):
        account = []
        raw_account = ""
        str_start = 0
        for i in range(len(tokens)):
            if tokens[i] == "\n":
                elem_start = 0
                raw_account = tokens[str_start:i]
                raw_account += ":"
                for j in range(len(raw_account)):
                    if raw_account[j] == ":":
                        account.append(raw_account[elem_start:j])
                        elem_start = j+1
                accounts.append(account)
                account = []
                str_start = i+1
        for i in range(len(accounts)):
            accounts[i] = Account(accounts[i][0],accounts[i][1],accounts[i][2],accounts[i][3],accounts[i][4])
    else:
        str_start = 0
        for i in range(len(tokens)):
            if tokens[i] == "\n":
                token = tokens[str_start:i]
                accounts.append(token)
                str_start = i+1
        for i in range(len(accounts)):
            accounts[i] = Account(accounts[i])
    return accounts

def inviter(account):
    s = requests.Session()
    invite_link = input("Введите пригласительную ссылку ----->")
    invite_code = ""
    for i in range(len(invite_link)):
        if i == len(invite_link)-8:
            invite_code = invite_link[i:len(invite_link)]
    headers = {
        "authorization": account.token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    r = s.post("https://discord.com/api/v9/invites/{}".format(invite_code), headers=headers)
    print(r.json())
    if (r.status_code == 200):
        return True
    elif ('captcha_key' in r.json()):
        captchaKey = r.json()['captcha_sitekey']
        print(captchaKey)
        start_server(captchaKey)
        driver = webdriver.Firefox()
        driver.get("http://localhost:5000")
        print("пройдите капчу в открывшемся окне")
        while True:
            captcha = driver.find_element_by_xpath("/html/body/div[1]/iframe").get_attribute("data-hcaptcha-response")
            if captcha != "":
                break
        f = open("end.txt", "w")
        f.write("1")
        f.close()
        try:
            driver.refresh()
        except Exception:
            pass
        driver.quit()
        r = s.post("https://discord.com/api/v9/invites/{}".format(invite_code), headers=headers, data={'captcha_key':captcha, 'captcha_sitekey':captchaKey, 'captcha_service': 'hcaptcha'})
        print(r.json())
        if(r.status_code == 200):
            return True
        else:
            return False



def leaver(account):
    channel_id = input("Введи айди канала(https://discord.com/channels/айди канала/не надо)")
    r = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{channel_id}", headers=account.getHeaders())
    print(r.json())
    if(r.status_code == 204):
        return True
    else:
        print(r.content)
        return False


def checker(account):
    response = requests.get(f'https://discordapp.com/api/v9/users/@me/library',
                   headers=account.getHeaders())
    if "You need to verify your account in order to perform this action." in str(
            response.content) or "401: Unauthorized" in str(response.content):
        return False
    elif response.status_code == 401:
        return 'Invalid'
    else:
        return True

def smile(account):
    smile_url = input("Введите ссылку на запрос нажатия на смайл ----->")
    r = requests.put(smile_url, headers = account.getHeaders())
    print(r.json())
    if r.status_code == 204:
        return True
    else:
        return False

if __name__ == '__main__':
    def main():
        action = int(input("Введите, что делать с аккаунтами:\n0-зайти на сервер по ссылке-приглашению  \n1-выйти из сервера   \n2-зайти на сервер и нажать на смайл   \n3-токен-чекер  \n----->"))
        if action == 0:
            for account in make_accounts_from_tokens(isProxy):
                if inviter(account):
                    print(Fore.GREEN + f"{account.token} - зашел")
                else:
                    print(Fore.RED + f"{account.token} - не зашел")
                sleep(delay)
        elif action == 1:
            for account in make_accounts_from_tokens(isProxy):
                if leaver(account):
                    print(Fore.GREEN + f"{account.token} - вышел")
                else:
                    print(Fore.RED + f"{account.token} - не вышел")
                sleep(delay)
        elif action == 2:
            for account in make_accounts_from_tokens(isProxy):
                if smile(account):
                    print(Fore.GREEN + f"{account.token} - нажал")
                else:
                    print(Fore.RED + f"{account.token} - что-то не так")
                sleep(delay)
        elif action == 3:
            for account in make_accounts_from_tokens(isProxy):
                if checker(account):
                    print(Fore.GREEN + f"{account.token} - жив")
                else:
                    print(Fore.RED + f"{account.token} - мертв")
                sleep(delay)

        input(Fore.WHITE + "\n\n\nнажмите enter, чтобы вернуться в меню")

        main()

    main()
