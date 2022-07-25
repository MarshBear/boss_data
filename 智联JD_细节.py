import time
import pandas as pd
import requests
import re
import json

file = 'city530_北京.csv'

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    # "refer": "https://www.zhaopin.com/",
    "origin": "https://jobs.zhaopin.com",
    "referer": "https://jobs.zhaopin.com/",
    "ec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "_uab_collina=165866722854437872699793; x-zp-client-id=da21de79-cabe-4bd4-9c51-730e4c24a751; zp_passport_deepknow_sessionId=0471fb49s76ed74a299e5828f6c7a1b3226e; at=5e04572984994812bf8ebaa0da324503; rt=92f640ad176641f3b0b8edefe36caa31; locationInfo_search={%22code%22:%22656%22%2C%22name%22:%22%E5%98%89%E5%85%B4%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; urlfrom=121114589; urlfrom2=121114589; adfcid=cn.bing.com; adfcid2=cn.bing.com; adfbid=0; adfbid2=0; acw_tc=276082a116586774915148246e41bef8a7a844c99a9f67a0bff979e1f385d9; acw_sc__v2=62dd68f3f70db7b5e40bce9f80aade0d21822d66; ssxmod_itna=7qfxRCitDQDtD=DXzG7+nbkDUOV8oqK=THDlrrexA5D8D6DQeGTrXsdrKdYtkIeFD7Idq8jDc+GAQ+jr5TYQpu4GIDeKG2DmeDyDi5GRD0FebD48KGwD0eG+DD4DWl3zQCXOxB4DF0qIQgDi3DbxtDi4D+GT=DmM3DGLPDbddDIqUxe8xVDBoYqLL9GMxZAGiTWqGyWPGuKdjV9kUSYTFZYQ+==OuYA8GYYDPhADm5K8DoQGhp=7q3Q0+eY7wKABhAa24flPDAY+3xD=; ssxmod_itna2=7qfxRCitDQDtD=DXzG7+nbkDUOV8oqK=TD6a/7ix052x03weXEjD6QjeqQudp23k=I6LyhbDKk23DLxijP4D; acw_sc__v3=62dd6c510f910736f4e44570fddfb2c469b4d4db; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221143511629%22%2C%22first_id%22%3A%2218230456ef1a0f-01ecf78074de37d-1c525635-1764000-18230456ef2abe%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22http%3A%2F%2Flocalhost%3A63342%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyMzA0NTZlZjFhMGYtMDFlY2Y3ODA3NGRlMzdkLTFjNTI1NjM1LTE3NjQwMDAtMTgyMzA0NTZlZjJhYmUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTQzNTExNjI5In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221143511629%22%7D%2C%22%24device_id%22%3A%2218230456ef1a0f-01ecf78074de37d-1c525635-1764000-18230456ef2abe%22%7D; ZL_REPORT_GLOBAL={%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%22eca20493-ea49-4348-be38-6b714b6016f8-job%22}}"
}

urls = pd.read_csv('./zhilian_urls/' + file)['positionURL'].to_list()

params = {
    "refcode": 4019,
    "srccode": 401901,
    "preactionid": "",
    "u_atoken": "3d29d7bc-d5ca-4839-b466-0cf0b5e3cbe8"
}

obj = re.compile('<script>__INITIAL_STATE__=(?P<js>.*?)</script>', re.S)

# url = urls[0]
# resp = requests.get(url.replace('http://', 'https://'), params=params, headers=headers)
# resp.encoding = 'UTF-8'
# with open('智联.html', 'w') as f:
#     f.write(resp.text)
company = []
position = []
for i, url in enumerate(urls):
    resp = requests.get(url.replace('http://', 'https://'), params=params, headers=headers)
    resp.encoding = 'UTF-8'
    if "滑动验证页面" in resp.text:
        with open('智联.html', 'w') as f:
            f.write(resp.text)
        print('滑动验证页面')
        break
    conf = json.loads(obj.findall(resp.text)[0])
    resp.close()
    detailed_company = conf['jobInfo']['jobDetail']['detailedCompany']
    detailed_position = conf['jobInfo']['jobDetail']['detailedPosition']
    print(detailed_position)
    company.append(detailed_company)
    position.append(detailed_position)
if company:
    df_company = pd.DataFrame(data=company)
    df_company.to_csv('zhilian_result/{}company'.format(int(time.time())) + file)
if position:
    df_position = pd.DataFrame(data=position)
    df_position.to_csv('zhilian_result/{}position'.format(int(time.time())) + file)
