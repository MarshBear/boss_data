import time
import pandas as pd
import requests
import re
import json
import os

cookie = "urlfrom=121122526; urlfrom2=121122526; adfbid=0; adfbid2=0; x-zp-client-id=36dd39e8-cba2-41e3-9288-5e940cdeb5b4; sajssdk_2015_cross_new_user=1; ZP_OLD_FLAG=false; sts_deviceid=1826770518d3ee-00c09f49a0db9d-76492e2f-1821369-1826770518e647; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Flanding.zhaopin.com%2F; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1659592791; zp_passport_deepknow_sessionId=966dadf0sf7e8144c2ba28f0ab1e11d4bf30; at=d1065b33f9fe414a8f58af7375752239; rt=54c0fb54b7c449cabe6bccbfcda2f5bb; ZL_REPORT_GLOBAL={%22/resume/new%22:{%22actionid%22:%2216e545c0-30fa-4e94-a7fd-8a4be01a9990%22%2C%22funczone%22:%22addrsm_ok_rcm%22}}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221143581858%22%2C%22first_id%22%3A%22182676ca7ad187-0a46b98e5cd929-76492e2f-1821369-182676ca7aec12%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22360PC%22%2C%22%24latest_utm_medium%22%3A%22CPC%22%2C%22%24latest_utm_campaign%22%3A%22pp%22%2C%22%24latest_utm_content%22%3A%22qg%22%2C%22%24latest_utm_term%22%3A%2210101631544%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyNjc2Y2E3YWQxODctMGE0NmI5OGU1Y2Q5MjktNzY0OTJlMmYtMTgyMTM2OS0xODI2NzZjYTdhZWMxMiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjExNDM1ODE4NTgifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221143581858%22%7D%2C%22%24device_id%22%3A%22182676ca7ad187-0a46b98e5cd929-76492e2f-1821369-182676ca7aec12%22%7D; acw_tc=276082a016595929147372750e0db5b6031397c1d3174d60d026e18858ef17; FSSBBIl1UgzbN7NO=5VYng3IYwkIAfm9rqSBDyoX537kcRmcx6HABDfkbkbclnm3AV8yfvbnDh1dG4zlK0xgJX0IsADPC23LR.BWTYSq; _uab_collina=165959291678251783616233; locationInfo_search={%22code%22:%22653%22%2C%22name%22:%22%E6%9D%AD%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1659592917; selectCity_search=530; FSSBBIl1UgzbN7NP=53XzG0Ch.3JWqqqDcRguB7AZLOTizEfohyfxu1cW4IvqKPvqW_IiOFvm9t5fxg2jXsE0IodTXsj974t4Ye1DWuWz8TtaEOjEDwbULT4onqs8cnv87x7eGRp9Z5iCFD_kZcB1JXYRwIcXXBWofszJQ7wXpkT2m_pBHlaS3TXaKciOMcekwpt3sUw2c9Vfs39VOtK_8LFYGHz4KzZL.e2hDvwN0kjR4mXx6vCVhtpBYSLV.i30uDH2IC_l7zLot8OUoEgbB5YRQQVDOZmPiqC9hB.oORkCia55hhEL1KabPOweCzKTn7NQJqv_bArqiWj.6kIVVBk9t36Tv2s9EZKn7bz"

url = 'https://sou.zhaopin.com/'


def info_dict(url, params, headers, obj):
    resp = requests.get(url, params=params, headers=headers)
    conf = json.loads(obj.findall(resp.text)[0])
    resp.close()
    return conf


if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
        "referer": "https://www.zhaopin.com/",
        "cookie": cookie
    }
    obj = re.compile('<script>__INITIAL_STATE__=(?P<js>.*?)</script>', re.S)
    with open('zhilian_structure.json', 'r') as f:
        conf = json.load(f)
    # files = os.listdir('zhilian_urls')
    # city_codes_done = [c[4:7] for c in files]
    # # for city in conf['otherCityBaseData']:
    # for city in conf['baseData']['hotCity']:
    #     if city['codes'] in city_codes_done:
    #         continue
    #     params = {'jl': city['code'], 'p': 1}
    #     position_city_list = []
    #     while True:
    #         list_info = info_dict(url, params, headers, obj)
    #         position_list = list_info['positionList']
    #         if not position_list:
    #             break
    #         position_city_list.extend(position_list)
    #         params['p'] += 1
    #         time.sleep(1)
    #     df = pd.DataFrame(data=position_city_list)
    #     df.to_csv('zhilian_urls/city{}_{}.csv'.format(city['code'], city['name']), index=False)
    #     time.sleep(3)
    files = os.listdir('./zhilian_urls/beijing_urls')
    for first in conf['baseData']['jobType']:
        if first['code'] == '-1':
            continue
        for second in first['sublist']:
            for third in second['sublist']:
                outfile_name = f"{first['name'].replace('/','or')}_{second['name'].replace('/','or')}_{third['name'].replace('/','or')}.csv"
                if outfile_name in files:
                    continue
                params = {'jl': '530', 'p': 1, 'jt': ','.join([first['code'], second['code'], third['code']])}
                position_list_all = []
                while True:
                    list_info = info_dict(url, params, headers, obj)
                    print(params)
                    position_list = list_info['positionList']
                    if not position_list:
                        break
                    position_list_all.extend(position_list)
                    params['p'] += 1
                    time.sleep(1)
                df = pd.DataFrame(data=position_list_all)
                df.to_csv(f"zhilian_urls/beijing_urls/{outfile_name}", index=False)
                # time.sleep(3)
                print(f"{outfile_name}.csv 已导出.")
