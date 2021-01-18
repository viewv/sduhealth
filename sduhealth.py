import requests
import execjs
import secrets

from bs4 import BeautifulSoup


def js_from_file(filename):
    # Read Javascript file
    # so you need nodejs installed on your computer
    with open(filename, 'r', encoding='UTF-8') as f:
        result = f.read()
    return result


def generate_their_RSA(username, password, lt):
    # return thay called 'RSA' string, note here just return RSA string!
    context = execjs.compile(js_from_file('./des.js'))
    rsa = context.call("strEnc", username + password + lt, "1", "2", "3")
    return rsa


def get_lt_And_execution(result):
    soup = BeautifulSoup(result.content, "html.parser")
    lt = soup.find(id="lt").get("value")
    execution = soup.find('input', {'name': 'execution'}).get("value")
    return {'lt': lt, 'execution': execution}


def login(username, password):
    login_url = "https://pass.sdu.edu.cn/cas/login"

    login_Header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
        'content-type': "application/x-www-form-urlencoded",
    }
    
    login_Cookie = {
        'JSESSIONID': secrets.token_hex(16).upper()
    }

    ul = str(len(username))
    pl = str(len(password))

    try:
        session = requests.session()
        r = session.get(login_url)

        lt_execution = get_lt_And_execution(r)
        lt = lt_execution['lt']
        execution = lt_execution['execution']

        rsa = generate_their_RSA(username=username, password=password, lt=lt)

        login_Body = {
            'rsa': rsa,
            'ul': ul,
            'pl': pl,
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit'
        }

        result = session.post(login_url, headers=login_Header,
                              cookies=login_Cookie, data=login_Body)

        # result = session.get("http://service.sdu.edu.cn/tp_up/view?m=up")

        result = session.get(
            "https://service.sdu.edu.cn/tp_up/view?m=up#act=portal/viewhome")

        print(result.text)

        print('OK')
    except:
        print('?')


if __name__ == "__main__":
    user = ''
    password = ''
    login(username=user,password=password)
