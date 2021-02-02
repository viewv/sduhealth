import time
import pytz
import datetime
import demjson as json
import random as rand

TIME_ZONE = 'Asia/Shanghai'


def test(data):
    print("model")
    print(data)

def get_random_temp():
    temp = 36.2
    if(rand.random() > 0.8):
        temp += 0.1
    return temp


def get_current_date(timezone):
    tz = pytz.timezone(timezone)
    current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d")
    return current_time


def get_yesterday_date(timezone):
    tz = pytz.timezone(timezone)
    yesterday_time = datetime.datetime.now(
        tz) - datetime.timedelta(days=1)
    yesterday_time = yesterday_time.strftime("%Y-%m-%d")
    return yesterday_time


def get_current_stamp():
    now = time.time()
    now = (int(now * 1000))
    current_stamp = str(now)
    return current_stamp


def generate_post_data(source_data):
    new_key = {}
    for code in source_data["body"]["dataStores"]:
        new_key[code] = len(code)

    sorted_key = sorted(new_key.items(), key = lambda x:x[1])
    # print("sorted_key",sorted_key)
    # print("sorted_key[1][0]",sorted_key[1][0])

    # This code may change aperiodically, we don't know how it works.
    unknown_code = sorted_key[1][0]

    rowSetName = source_data["body"]["dataStores"][unknown_code]["rowSetName"]

    whether_signed = False
    json_file = open("./json/model.json", encoding='utf-8')
    model_txt = json_file.read(-1)
    json_file.close()

    # add {var} feature
    model_txt = model_txt.replace(r"{Temp}", "%.1f"%get_random_temp())
    model_data = json.decode(model_txt)
    # model_data = json.decode_file("./json/model.json")

    current_date = get_current_date(TIME_ZONE)
    # current_date_time = current_date + ' 00:00:00'

    yesterday_date = get_yesterday_date(TIME_ZONE)
    yesterday_date_time = yesterday_date + ' 09:00:00'

    # current_timestamp = get_current_stamp()

    unknown_code_use = unknown_code
    unknown_code_record = unknown_code + "_record"
    # print("unknown_code_use",unknown_code_use)
    new_model_data = {}
    new_model_data["header"] = model_data["header"]
    new_model_data["body"] = {}
    new_model_data["body"]["parameters"] = model_data["body"]["parameters"]
    new_model_data["body"]["dataStores"] = {}
    new_model_data["body"]["dataStores"]["variable"] = model_data["body"]["dataStores"]["variable"]
    new_model_data["body"]["dataStores"][unknown_code_use] = model_data["body"]["dataStores"]['535b1ef6-bf51-4d4c-9ae4-5a90cdc4']
    new_model_data["body"]["dataStores"][unknown_code_record] = model_data["body"]["dataStores"]['535b1ef6-bf51-4d4c-9ae4-5a90cdc4_record']
    new_model_data["body"]["dataStores"][unknown_code_use]["name"] = unknown_code_use
    new_model_data["body"]["dataStores"][unknown_code_use]["parameters"]["queryds"] = unknown_code_use
    new_model_data["body"]["dataStores"][unknown_code_record]["name"] = unknown_code_record
    new_model_data["body"]["dataStores"][unknown_code_record]["parameters"]["queryds"] = unknown_code_use

    new_model_data["body"]["dataStores"][unknown_code_use]["rowSetName"] = rowSetName
    new_model_data["body"]["dataStores"][unknown_code_record]["rowSetName"] = rowSetName


    json.encode_to_file("./json/new_model.json", new_model_data, overwrite=True)

    model_data = new_model_data
    # if you didn't click the "暂存" button
    if unknown_code_record in source_data["body"]["dataStores"]:
        source_record = source_data["body"]["dataStores"][unknown_code_record]["rowSet"]["primary"][0]
        model_data["body"]["dataStores"][unknown_code_record] = source_data["body"]["dataStores"][unknown_code_record]
        print("today is " + current_date)
        if source_record['SBSJ_STR'][0:10] == current_date:
            whether_signed = True
        # model_data["body"]["dataStores"][unknown_code_record]["rowSet"]["primary"][0]["CLSJ"] = current_timestamp
        # model_data["body"]["dataStores"][unknown_code_record]["rowSet"]["primary"][0]["SBSJ"] = current_timestamp
    else:
        source_record = source_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]
        del model_data["body"]["dataStores"][unknown_code_record]
        del model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["_o"]

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
    clsj = yesterday_date_time                  # temp. time

    # SYS_USER = source_vars[0]["value"]          # student name
    # SYS_UNIT = source_vars[1]["value"]          # student unit
    # SYS_DATE = current_timestamp                # current timestamp
    # ID_NUMBER = source_vars[3]["value"]         # student id
    # USER_NAME = source_vars[4]["value"]         # student name
    # XB = source_vars[5]["value"]                # student sex
    # SZYX = source_vars[6]["value"]              # student school
    # ZYMC = source_vars[7]["value"]              # student major
    # MOBILE = source_vars[8]["value"]            # mobile

    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["ZH"] = zh
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["XM"] = xm
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["XSXB"] = xsxb
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["NL"] = nl
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["SZDW"] = szdw
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["ZYMC"] = zymc
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["XSLX"] = xslx
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["ZXSJ"] = zxsj
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["SBSJ"] = sbsj
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["FDYXMX"] = fdyxmx
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["JJLXRXM"] = jjlxrxm
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["JJLXRDH"] = jjlxrdh
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["JJLXRYBRGX"] = jjlxrybrgx
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["LXZT"] = lxzt
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["DQSFJJIA"] = dqsfjjia
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["sheng_TEXT"] = sheng_text
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["sheng"] = sheng
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["shi_TEXT"] = shi_text
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["shi"] = shi
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["quxian_TEXT"] = quxian_text
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["quxian"] = quxian
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["DQJZDZ"] = dqjzdz
    model_data["body"]["dataStores"][unknown_code_use]["rowSet"]["primary"][0]["CLSJ"] = clsj

    model_data["body"]["dataStores"]["variable"] = source_data["body"]["dataStores"]["variable"]
    model_data["body"]["parameters"] = source_data["body"]["parameters"]

    json.encode_to_file("./json/example.json", model_data, overwrite=True)

    return model_data, whether_signed
