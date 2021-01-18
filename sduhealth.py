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
        self.privilegedID = ''
        self.serviceID = '41d9ad4a-f681-4872-a400-20a3b606d399'
        self.login_url = "https://pass.sdu.edu.cn/cas/login"
        self.service_url = "https://service.sdu.edu.cn/tp_up"
        self.health_url = "https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=41d9ad4a-f681-4872-a400-20a3b606d399&act=fp/serveapply"
        self.privilegedID_url = "https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/getServeApply"

        self.session = requests.session()
        self.login_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'content-type': "application/x-www-form-urlencoded",
        }
        self.privilegedID_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://scenter.sdu.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://scenter.sdu.edu.cn/tp_fp/view?m=fp'
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

            result = self.session.get(
                "https://service.sdu.edu.cn/tp_up/view?m=up#act=portal/viewhome")

            print("login", result)
        except:
            print('?')

    def get_privilegedID(self):
        serve_body = {
            "serveID": "41d9ad4a-f681-4872-a400-20a3b606d399"
        }

        serve_body_hall = {
            "serveID": "41d9ad4a-f681-4872-a400-20a3b606d399",
            "from": "hall"
        }

        result = self.session.get(
            "https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=41d9ad4a-f681-4872-a400-20a3b606d399&act=fp/serveapply")

        mapping_body = {
            "mapping": "getAccessCount"
        }

        result = self.session.post("https://scenter.sdu.edu.cn/tp_fp/sys/monitor/sql/get",
                                   headers=self.privilegedID_header,
                                   json=mapping_body)
        print("mapping post", result)

        result = self.session.get("https://scenter.sdu.edu.cn/tp_fp")

        result = self.session.get(
            "https://scenter.sdu.edu.cn/tp_fp/sys/theme/getThemes")

        result = self.session.get(
            "https://scenter.sdu.edu.cn/tp_fp/fp/serveapply?item_id=undefined")

        result = self.session.get(
            "https://scenter.sdu.edu.cn/tp_fp/view?m=fp")

        result = self.session.post("https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/checkService",
                                   headers=self.privilegedID_header,
                                   json=serve_body)
        print("CheckService post", result)

        result = self.session.post("https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/serveInfo",
                                   headers=self.privilegedID_header,
                                   json=serve_body)

        result = self.session.post("https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/getServeApply",
                                   headers=self.privilegedID_header,
                                   json=serve_body_hall)
        print("getServeApply post", result)

        result = self.session.post("https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/getContinueService",
                                   headers=self.privilegedID_header,
                                   json=serve_body)
        print("getContinueService post", result)

    def health_checkin(self):
        pass

    def health_logout(self):
        pass


if __name__ == "__main__":
    user = ''
    password = ''
    sdu = SduHealth(username=user, password=password)
    sdu.health_login()
    sdu.get_privilegedID()
