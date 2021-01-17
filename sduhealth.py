import requests
import os
import execjs

from Crypto.Cipher import DES3


def js_from_file(filename):
    # Read Javascript file
    with open(filename, 'r', encoding='UTF-8') as f:
        result = f.read()
    return result


if __name__ == "__main__":
    context = execjs.compile(js_from_file('./des.js'))
    m = context.call("strEnc",
                     "201700800398!123456789LT-176706-nKUGsOyV0OIYa0KQgtoa3qFcZVZkeP-cas",
                     "1", "2", "3")
    print(m)
    l = context.call("strDec", m, "1", "2", "3")
    print(l)
