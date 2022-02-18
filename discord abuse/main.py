import requests
from account import Account
from time import sleep
from colorama import Fore

isProxy = input("нужны ли прокси?(y/n)")
if isProxy=="y":
    isProxy=True
    print("Для работы бота нужны токены от аккаунтов дискорда и прокси для каждого аккаунта, которые должны будут находиться в файле под названием token.txt каждый токен должен находиться на новой строке. Формат такой: токен:айпи:порт:логинПрокси:парольПрокси")
else:
    isProxy=False
    print("Для работы бота нужны токены от аккаунтов дискорда, которые должны будут находиться в файле под названием token.txt каждый токен должен находиться на новой строке")

delay = int(input("Введите задержку между обработкой аккаунтов в целых секундах ----->"))
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
    invite_link = input("Введите пригласительную ссылку ----->")
    for i in range(len(invite_link)):
        if i == len(invite_link)-7:
            invite_code = invite_link[i:len(invite_link)]

    r = requests.post("https://discord.com/api/v9/invites/{}".format(invite_code), headers=account.getHeaders())
    print(r.json())
    if (r.status_code == 200):
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
    print(r.json())
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
        try:
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
        except Exception:
            print("Сука, эта хуйня разрывает соединение")

        input("\n\n\nнажмите enter, чтобы вернуться в меню")

        main()

main()
