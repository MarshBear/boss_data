import time
import openpyxl as op
import pandas as pd
import requests
import re
import json
import os

cookie = 'at=5e04572984994812bf8ebaa0da324503; rt=92f640ad176641f3b0b8edefe36caa31'

url = 'https://sou.zhaopin.com/'


def info_dict(url, params, headers, obj):
    resp = requests.get(url, params=params, headers=headers)
    conf = json.loads(obj.findall(resp.text)[0])
    resp.close()
    return conf


if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
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

    for first in conf['baseData']['jobType']:
        if first['code'] == '-1':
            continue
        for second in first['sublist']:
            for third in second['sublist']:
                params = {'jl': '653', 'p': 1, 'jt': ','.join([first['code'], second['code'], third['code']])}
                position_list_all = []
                while True:
                    list_info = info_dict(url, params, headers, obj)
                    position_list = list_info['positionList']
                    if not position_list:
                        break
                    position_list_all.extend(position_list)
                    params['p'] += 1
                    time.sleep(1)
                df = pd.DataFrame(data=position_list_all)
                df.to_csv(f"zhilian_urls/hangzhou_urls/{first['name'].replace('/','or')}_{second['name'].replace('/','or')}_{third['name'].replace('/','or')}.csv", index=False)
                time.sleep(3)
