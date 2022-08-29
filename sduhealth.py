from datetime import datetime
import platform
import requests
import secrets
import demjson as json
import os
import yaml

import model
import encrypt
import colorclass as c

from bs4 import BeautifulSoup



def js_from_file(filename):
    # Read Javascript file
    # so you need NodeJs installed on your computer
    with open(filename, 'r', encoding='UTF-8') as f:
        result = f.read()
    return result


def generate_their_RSA(username, password, lt):
    # return they called 'RSA' string, note here just return 'RSA' string!
    return encrypt.strenc(username + password + lt, "1", "2", "3")


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
                error('Network Error!')

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
                info("login successful " + strong(result))
                self.check_login = True
            else:
                info("login failed " + strong(result))
                self.check_login = False
        except Exception as e:
            self.check_login = False
            error(e)

    def getHealthUrl(self):
        getHealth = self.session.get(self.health_url)
        print(strong(getHealth))

    def check_service(self):
        try:
            check_body = {
                "serveID": self.serviceID
            }
            check_result = self.session.post(
                self.check_service_url, json=check_body, headers=self.service_header)
            print(strong(check_result))
        except:
            error("check_service error")

    def serve_info(self):
        try:
            serve_body = {
                "serviceID": self.serviceID
            }
            serve_result = self.session.post(
                self.serve_info_url, json=serve_body, headers=self.service_header)
            print(strong(serve_result))
        except Exception as e:
            error(e)

    def get_serve_apply(self):
        get_serve_apply_body = {
            "serveID": self.serviceID,
            "from": "hall"
        }
        try:
            get_serve_apply_result = self.session.post(
                self.get_serve_apply_url, json=get_serve_apply_body, headers=self.service_header)
            print(strong(get_serve_apply_result))
            get_serve_apply_json = get_serve_apply_result.json()
            self.form_id = get_serve_apply_json['formID']
            self.process_id = get_serve_apply_json['procID']
            self.privilege_id = get_serve_apply_json['privilegeId']
        except:
            error("get_serve_apply error")

    def get_continue_service(self):
        get_continue_service_body = {
            "serviceID": self.serviceID,
        }
        try:
            get_continue_service_result = self.session.post(
                self.get_continue_service_url, json=get_continue_service_body, headers=self.service_header)
            print(strong(get_continue_service_result))
            get_continue_service_json = get_continue_service_result.json()
            self.SYS_FK = get_continue_service_json[0]['proc_inst_id']
        except:
            warning("get_continue_service error")

    def get_sign_data(self):
        get_sign_data_url = "https://scenter.sdu.edu.cn/tp_fp/formParser?status=select&formid=" + self.form_id + "&service_id=" + \
            self.serviceID + "&process=" + self.process_id + "&seqId=&SYS_FK=" + \
            self.SYS_FK + "&privilegeId=" + self.privilege_id

        try:
            get_sign_data_result = self.session.get(get_sign_data_url)
            print(strong(get_sign_data_result))

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
            info("get_sign_data error")

    def health_checkin(self):
        info("gethealth ", end='')
        self.getHealthUrl()

        info("checkService ", end='')
        self.check_service()

        info("serveInfo ", end='')
        self.serve_info()

        info("getServeApply ", end='')
        self.get_serve_apply()

        info("getContinueService ", end='')
        self.get_continue_service()

        info("getSignData ", end='')
        self.get_sign_data()

        if self.whether_signed:
            print("\033[1;32;40mYou have signed today\033[0m")
            return

        checkin_url = "https://scenter.sdu.edu.cn/tp_fp/formParser?status=update&formid=" + \
            self.form_id + "&workflowAction=startProcess&seqId=&workitemid=&process=" + self.process_id
        checkin_body = json.encode(self.frame_json)

        info("Start Checkin!")
        if self.check_getSignData == True:
            try:
                info("Checkin ", end='')
                result = self.session.post(checkin_url, data=checkin_body,
                                           headers=self.checkin_header)
                print(strong(result))

                if result.status_code != 200:
                    self.check_checkin = False
                    raise RuntimeError("Checkin Network Error")
            except Exception as e:
                self.check_checkin = False
                error(e)
        else:
            error("Network Error!")

    def health_logout(self):
        try:
            info("logout (1/4): ", end='')
            print(strong('done' if self.session.get(self.logout_1_url).status_code == 200 else 'error'))
            info("logout (2/4): ", end='')
            print(strong('done' if self.session.get(self.logout_2_url).status_code == 200 else 'error'))
            info("logout (3/4): ", end='')
            print(strong('done' if self.session.get(self.logout_3_url).status_code == 200 else 'error'))
            info("logout (4/4): ", end='')
            print(strong('done' if self.session.get(self.logout_4_url).status_code == 200 else 'error'))
        except Exception as e:
            warning("logout ?")
            error(e)
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
        except Exception as e:
            warning("Error in reading config.yml from ENV:\033[94m$CONFIG\033[0m, please check.")
            error(e)
    else:
        with open("./config.yml", mode='r', encoding='utf-8') as f:
            config_current = yaml.load(f, Loader=yaml.FullLoader)

        studentIDs = config_current['jobs']['studentID']
        studentPasswords = config_current['jobs']['studentPassword']
        return studentIDs, studentPasswords

def _timestamp():
    print("[{}]".format(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")), end=' ')

def error(cause):
    _timestamp()
    print("\033[91m[ERROR]\033[0m Program exited due to:", cause)
    exit()


def info(log, end=None):
    _timestamp()
    print("\033[96m[INFO]\033[0m", log, end=end)
    return


def warning(warning):
    _timestamp()
    print("\033[93m[WARN]\033[0m", warning)
    return


def strong(string):
    return "\033[42;97m " + str(string) + " \033[0m"


def main():
    users, passwords = read()
    for i in range(0, len(users)):
        info("Sign in for " + users[i] + (", count: " + i if i > 0 else ""))

        user = users[i]
        password = passwords[i]
        sdu = SduHealth(username=user, password=password)

        info("-------------------")

        sdu.health_login()
        if sdu.check_login == False:
            error("Login Error")

        sdu.health_checkin()
        if sdu.check_getSignData == False:
            error("Get Sign Data Error")

        if sdu.check_checkin == False:
            error("Checkin Error")

        if not sdu.whether_signed:
            info("Checkin Successful")

        sdu.health_logout()
        info("Logout Successful")
        info("-------------------")


if __name__ == "__main__":
    if(platform.system() == "Windows"):
        c.Windows.enable()
    main()
