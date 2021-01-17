import requests
import os
import execjs

from bs4 import BeautifulSoup


def js_from_file(filename):
    # Read Javascript file
    # so you need nodejs installed on your computer
    with open(filename, 'r', encoding='UTF-8') as f:
        result = f.read()
    return result


def generate_their_RSA(username, password, lt):
    # return thay call 'RSA' string, note their just return RSA string!
    context = execjs.compile(js_from_file('./des.js'))
    rsa = context.call("strEnc", username+password + lt, "1", "2", "3")
    return rsa


def get_lt_And_execution(result):
    soup = BeautifulSoup(result.content, "html.parser")
    lt = soup.find(id="lt").get("value")
    execution = soup.find('input', {'name': 'execution'}).get("value")
    return {'lt': lt, 'execution': execution}


if __name__ == "__main__":
    url = "https://pass.sdu.edu.cn/cas/login"
    r = requests.get(url)
    result = get_lt_And_execution(r)
    print(result)
