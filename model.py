import time
import pytz
import datetime
import demjson as json

TIME_ZONE = 'Asia/Shanghai'


def get_current_date(timezone):
    tz = pytz.timezone(timezone)
    current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d")
    print(current_time)
    return(current_time)


def get_current_stamp():
    now = time.time()
    now = (int(now * 1000))
    strnow = str(now)
    return strnow


def generate_post_data(source_data):
    model_data = json.decode_file("./model.json")
    current_date = get_current_date(TIME_ZONE)
    current_date_time = current_date + ' 10:10:10'
    current_timestamp = get_current_stamp()

    source_record = source_data["535b1ef6-bf51-4d4c-9ae4-5a90cdc4_record"]["rowSet"]["primary"][0]

    zh = source_record["ZH"]                    # student id
    xm = source_record["XM"]                    # student name
    xsxb = source_record["XSXB"]                # student sex
    nl = source_record["NL"]                    # student age
    szdw = source_record["SZDW"]                # student school
    zymc = source_record["ZYMC"]                # student major
    xslx = source_record["XSLX"]                # student type
    zxsj = source_record["ZXSJ"]                # student phone number
    sbsj = current_date                         # date
    fdyxmx = source_record["FDYXMX"]            # teacher name
    jjlxrxm = source_record["JJLXRXM"]          # parent name
    jjlxrdh = source_record["JJLXRDH"]          # parent phone number
    jjlxrybrgx = source_record["JJLXRYBRGX"]    # parent rel.
    lxzt = source_record["LXZT"]                # current city
    dqsfjjia = source_record["DQSFJJIA"]        # at home or not?
    sheng_text = source_record["sheng_TEXT"]    # provience text
    sheng = source_record["sheng"]              # provience
    shi_text = source_record["shi_TEXT"]        # city text
    shi = source_record["shi"]                  # city
    quxian_text = source_record["quxian_TEXT"]  # tone text
    quxian = source_record["quxian"]            # tone
    dqjzdz = source_record["DQJZDZ"]            # location
    clsj = current_date_time                    # temp. time

    source_vars = source_data["variable"]["rowSet"]["primary"]

    SYS_USER = source_vars[0]["value"]          # student name
    SYS_UNIT = source_vars[1]["value"]          # student unit
    SYS_DATE = current_timestamp                # current timestamp
    ID_NUMBER = source_vars[3]["value"]         # student id
    USER_NAME = source_vars[4]["value"]         # student name
    XB = source_vars[5]["value"]                # student sex
    SZYX = source_vars[6]["value"]              # student school
    ZYMC = source_vars[7]["value"]              # student major
    MOBILE = ""                                 # student mobile?

    source_parameter = source_data["parameters"]
    formid = source_parameter
    privilegeId = source_parameter
    process = source_parameter

    print(model_data["body"]["dataStores"]
          ["535b1ef6-bf51-4d4c-9ae4-5a90cdc4"]["rowSet"]["primary"][0])

    return model_data


if __name__ == "__main__":
    generate_post_data(None)