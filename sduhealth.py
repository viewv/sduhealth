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


class SduHealth(object):
    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.login_url = "https://pass.sdu.edu.cn/cas/login"
        self.service_url = "https://service.sdu.edu.cn/tp_up"
        self.health_url = "https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=87dc6da9-9ad8-4458-9654-90823be0d5f6&act=fp/serveapply"

        self.session = requests.session()
        self.login_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'content-type': "application/x-www-form-urlencoded",
        }
        self.login_cookie = {
            'JSESSIONID': secrets.token_hex(16).upper()
        }

    def health_login(self):
        try:
            ul = str(len(self.username))
            pl = str(len(self.password))
            r = self.session.get(self.login_url)

            lt_execution = get_lt_And_execution(r)
            lt = lt_execution['lt']
            execution = lt_execution['execution']

            rsa = generate_their_RSA(
                username=self.username, password=self.password, lt=lt)

            login_body = {
                'rsa': rsa,
                'ul': ul,
                'pl': pl,
                'lt': lt,
                'execution': execution,
                '_eventId': 'submit'
            }

            result = self.session.post(self.login_url, headers=self.login_header,
                                       cookies=self.login_cookie, data=login_body)

            # result = session.get("http://service.sdu.edu.cn/tp_up/view?m=up")

            result = self.session.get(
                "https://service.sdu.edu.cn/tp_up/view?m=up#act=portal/viewhome")

            print(result)
        except:
            print('?')
            
    def health_checkin(self):
        pass
    
    def health_logout(self):
        pass
    


if __name__ == "__main__":
    user = ''
    password = ''
    sdu = SduHealth(username=user, password=password)
    sdu.health_login()
