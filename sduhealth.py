import requests
import execjs
import secrets
import demjson as json
import os
import yaml

import model

from bs4 import BeautifulSoup


def js_from_file(filename):
    # Read Javascript file
    # so you need NodeJs installed on your computer
    with open(filename, 'r', encoding='UTF-8') as f:
        result = f.read()
    return result


def generate_their_RSA(username, password, lt):
    # return they called 'RSA' string, note here just return 'RSA' string!
    context = execjs.compile(js_from_file('./js/des.js'))
    rsa = context.call("strEnc", username + password + lt, "1", "2", "3")
    return rsa


def get_lt_And_execution(result):
    soup = BeautifulSoup(result.content, "html.parser")
    lt = soup.find(id="lt").get("value")
    execution = soup.find('input', {'name': 'execution'}).get("value")
    return {'lt': lt, 'execution': execution}


def get_page_title(result):
    soup = BeautifulSoup(result.content, "html.parser")
    title = soup.find('title').string
    return title


def get_frame(result):
    soup = BeautifulSoup(result.content, "html.parser")
    frame = soup.find(id="dcstr")
    return frame


class SduHealth(object):
    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password

        self.home_title = "山东大学信息化公共服务平台"
        self.serviceID = '41d9ad4a-f681-4872-a400-20a3b606d399'
        self.privilege_id = ''
        self.process_id = ''
        self.SYS_FK = ''
        self.form_id = ''

        self.login_url = "https://pass.sdu.edu.cn/cas/login"
        self.service_url = "https://service.sdu.edu.cn/tp_up"
        self.home_url = "https://service.sdu.edu.cn/tp_up/view?m=up#act=portal/viewhome"
        self.health_url = "https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=41d9ad4a-f681-4872-a400-20a3b606d399&act=fp/serveapply"

        self.check_service_url = "https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/checkService"
        self.serve_info_url = "https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/serveInfo"
        self.get_serve_apply_url = "https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/getServeApply"
        self.get_continue_service_url = "https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/getContinueService"

        self.logout_1_url = "https://service.sdu.edu.cn/tp_up/logout"
        self.logout_2_url = "https://pass.sdu.edu.cn/cas/logout?service=https://service.sdu.edu.cn/tp_up/"
        self.logout_3_url = "https://pass.sdu.edu.cn/portal/logout.jsp?service=https://service.sdu.edu.cn/tp_up/"
        self.logout_4_url = "https://service.sdu.edu.cn/tp_up/"

        self.session = requests.session()
        self.login_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'content-type': "application/x-www-form-urlencoded",
        }
        self.service_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://scenter.sdu.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://scenter.sdu.edu.cn/tp_fp/view?m=fp'
        }
        self.checkin_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'Content-Type': 'text/plain;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.login_cookie = {
            'JSESSIONID': secrets.token_hex(16).upper()
        }
        self.frame_json = {}

        self.check_login = True
        self.check_getSignData = True
        self.check_checkin = True
        self.whether_signed = False

    def health_login(self):
        try:
            ul = str(len(self.username))
            pl = str(len(self.password))

            r = self.session.get(self.login_url)
            if r.status_code != 200:
                self.check_login = False
                raise RuntimeError('Network Error!')

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

            result = self.session.get(self.home_url)

            title = get_page_title(result=result)
            if title == self.home_title:
                print(title)
                print("login successful")
                self.check_login = True
            else:
                print("login failed")
                self.check_login = False
            print("login", result)
        except:
            self.check_login = False
            print('login error')

    def getHealthUrl(self):
        getHealth = self.session.get(self.health_url)
        print(getHealth)

    def check_service(self):
        try:
            check_body = {
                "serveID": self.serviceID
            }
            check_result = self.session.post(
                self.check_service_url, json=check_body, headers=self.service_header)
            print(check_result)
        except:
            print("check_service error")

    def serve_info(self):
        try:
            serve_body = {
                "serviceID": self.serviceID
            }
            serve_result = self.session.post(
                self.serve_info_url, json=serve_body, headers=self.service_header)
            print(serve_result)
        except:
            pass

    def get_serve_apply(self):
        get_serve_apply_body = {
            "serveID": self.serviceID,
            "from": "hall"
        }
        try:
            get_serve_apply_result = self.session.post(
                self.get_serve_apply_url, json=get_serve_apply_body, headers=self.service_header)
            print(get_serve_apply_result)
            get_serve_apply_json = get_serve_apply_result.json()
            self.form_id = get_serve_apply_json['formID']
            self.process_id = get_serve_apply_json['procID']
            self.privilege_id = get_serve_apply_json['privilegeId']
        except:
            print("get_serve_apply error")

    def get_continue_service(self):
        get_continue_service_body = {
            "serviceID": self.serviceID,
        }
        try:
            get_continue_service_result = self.session.post(
                self.get_continue_service_url, json=get_continue_service_body, headers=self.service_header)
            print(get_continue_service_result)
            get_continue_service_json = get_continue_service_result.json()
            self.SYS_FK = get_continue_service_json[0]['proc_inst_id']
        except:
            print("get_continue_service error")

    def get_sign_data(self):
        get_sign_data_url = "https://scenter.sdu.edu.cn/tp_fp/formParser?status=select&formid=" + self.form_id + "&service_id=" + \
            self.serviceID + "&process=" + self.process_id + "&seqId=&SYS_FK=" + \
            self.SYS_FK + "&privilegeId=" + self.privilege_id

        try:
            get_sign_data_result = self.session.get(get_sign_data_url)
            print(get_sign_data_result)

            if get_sign_data_result.status_code != 200:
                self.check_getSignData = False
                raise RuntimeError('Get Signin Data Network Error!')

            frame = get_frame(get_sign_data_result).string
            # print(frame)
            frame_json = json.decode(frame)
            source_json = frame_json
            # json.encode_to_file("./test.json", source_json, overwrite=True)
            frame_json, self.whether_signed = model.generate_post_data(
                source_data=source_json)
            self.frame_json = frame_json
        except:
            self.check_getSignData = False
            print("get_sign_data error")

    def health_checkin(self):
        print("gethealth ", end='')
        self.getHealthUrl()

        print("checkService ", end='')
        self.check_service()

        print("serveInfo ", end='')
        self.serve_info()

        print("getServeApply ", end='')
        self.get_serve_apply()

        print("getContinueService ", end='')
        self.get_continue_service()

        print("getSignData ", end='')
        self.get_sign_data()

        if self.whether_signed:
            print("You have signed today")
            return

        checkin_url = "https://scenter.sdu.edu.cn/tp_fp/formParser?status=update&formid=" + \
            self.form_id + "&workflowAction=startProcess&seqId=&workitemid=&process=" + self.process_id
        checkin_body = json.encode(self.frame_json)

        print("Start Checkin!")
        if self.check_getSignData == True:
            try:
                result = self.session.post(checkin_url, data=checkin_body,
                                           headers=self.checkin_header)
                print("Checkin", result)

                if result.status_code != 200:
                    self.check_checkin = False
                    raise RuntimeError("Checkin Network Error")
            except:
                self.check_checkin = False
        else:
            print("Network Error!")

    def health_logout(self):
        try:
            result = self.session.get(self.logout_1_url)
            print("logout 1", result)
            result = self.session.get(self.logout_2_url)
            print("logout 2", result)
            result = self.session.get(self.logout_3_url)
            print("logout 3", result)
            result = self.session.get(self.logout_4_url)
            print("logout 4", result)
        except:
            print("logout ?")
        self.session.close()


def read():
    studentIDs = []
    studentPasswords = []
    if 'CONFIG' in os.environ:
        try:
            config_current = yaml.load(
                os.environ['CONFIG'], Loader=yaml.FullLoader)
            studentIDs = config_current['jobs']['studentID']
            studentPasswords = config_current['jobs']['studentPassword']
            return studentIDs, studentPasswords
        except:
            print("获取学号以及密码出错，请检查yml文件")
    else:
        with open("./config.yml", mode='r', encoding='utf-8') as f:
            config_current = yaml.load(f, Loader=yaml.FullLoader)

        studentIDs = config_current['jobs']['studentID']
        studentPasswords = config_current['jobs']['studentPassword']
        return studentIDs, studentPasswords


def main():
    users, passwords = read()
    for i in range(0, len(users)):
        print("Sign in for", users[i][-3:])

        user = users[i]
        password = passwords[i]
        sdu = SduHealth(username=user, password=password)

        sdu.health_login()
        if sdu.check_login == False:
            print("Login Error")
            raise RuntimeError("Login Error")

        sdu.health_checkin()
        if sdu.check_getSignData == False:
            print("Get Sign Data Error")
            raise RuntimeError("Get Sign Data Error")

        if sdu.check_checkin == False:
            print("Checkin Error")
            raise RuntimeError("Checkin Error")

        if not sdu.whether_signed:
            print("Checkin Successful")
            
        sdu.health_logout()
        print("Logout Successful")


if __name__ == "__main__":
    main()
