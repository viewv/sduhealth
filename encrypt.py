from des import *


def strenc(data, firstkey, secondkey, thirdkey):
    bts_data = extend_to_16bits(data)
    bts_firstkey = extend_to_16bits(firstkey)
    bts_secondkey = extend_to_16bits(secondkey)
    bts_thirdkey = extend_to_16bits(thirdkey)
    i = 0
    bts_result = []
    while i < len(bts_data):
        bts_temp = bts_data[i: i + 8]
        j, k, l = 0, 0, 0
        while j < len(bts_firstkey):
            des_k = des(bts_firstkey[j: j + 8], ECB)
            bts_temp = list(des_k.encrypt(bts_temp))
            j += 8
        while k < len(bts_secondkey):
            des_k = des(bts_secondkey[k: k + 8], ECB)
            bts_temp = list(des_k.encrypt(bts_temp))
            k += 8
        while l < len(bts_thirdkey):
            des_k = des(bts_secondkey[l: l + 8], ECB)
            bts_temp = list(des_k.encrypt(bts_temp))
            l += 8
        bts_result.extend(bts_temp)
        i += 8
    str_result = ''
    for each in bts_result:
        str_result += '%02X' % each
    return str_result


def extend_to_16bits(data):
    bts = data.encode()
    filled_bts = []
    for each in bts:
        filled_bts.extend([0, each])
    while len(filled_bts) % 8 != 0:
        filled_bts.append(0)
    return filled_bts
