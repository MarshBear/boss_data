import asyncio
import aiohttp
import json
import os
import re
import sys
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

url = 'https://sou.zhaopin.com/'

city = 'beijing'
city_code = '530'

cookie = "x-zp-client-id=da21de79-cabe-4bd4-9c51-730e4c24a751; FSSBBIl1UgzbN7NO=5jZdx14Q1KSB76AotI8.YQze.T_d1npjxACfqMOs43TbL1Tonxek4feuAzfRWb8yNW2I515T.0tZHaKI9ZxQg4q; _uab_collina=165867028859986002403088; urlfrom2=121114589; adfcid2=cn.bing.com; adfbid2=0; ssxmod_itna=7qfxRCitDQDtD=DXzG7+nbkDUOV8oqK=THDlrrexA5D8D6DQeGTrXsdrKdYtkIeFD7Idq8jDc+GAQ+jr5TYQpu4GIDeKG2DmeDyDi5GRD0FebD48KGwD0eG+DD4DWl3zQCXOxB4DF0qIQgDi3DbxtDi4D+GT=DmM3DGLPDbddDIqUxe8xVDBoYqLL9GMxZAGiTWqGyWPGuKdjV9kUSYTFZYQ+==OuYA8GYYDPhADm5K8DoQGhp=7q3Q0+eY7wKABhAa24flPDAY+3xD=; ssxmod_itna2=7qfxRCitDQDtD=DXzG7+nbkDUOV8oqK=TD6a/7ix052x03weXEjD6QjeqQudp23k=I6LyhbDKk23DLxijP4D; c=ys1Wr49F-1658802231000-d5bb677a86fc4-1431458143; _fmdata=vb9omRHt7Sqt826J%2Byn82H59CglLHBFTl3C1tRzIakAofRQWSCd8K%2BnCfego%2FpiDDN4ggXH8F1ykHj75vHgMAhAKBPU8hbsxHN62RZVp3u8%3D; _xid=hoKTRdvKnhAUc9cZ0F3eSNGmki38RDmyFtwfl%2FNYDd5zoz9HxVlQRdh94y6vHv%2BcKqPQFhiStO3zRHHqhlTA2w%3D%3D; x-zp-device-id=00079283dd0dc0cf7746c1727c2f3696; login-type=b; locationInfo_search={%22code%22:%22653%22%2C%22name%22:%22%E6%9D%AD%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; sts_deviceid=182a9bf4781469-0f79e7e8457744-1b525635-1764000-182a9bf4782c29; ZP_OLD_FLAG=false; sts_sg=1; sts_sid=182a9bf4bd5d1e-05e8da5dbdee87-1b525635-1764000-182a9bf4bd6eb6; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2F; sts_evtseq=2; ZL_REPORT_GLOBAL={%22/resume/new%22:{%22actionid%22:%22d1cd6a0c-09a8-41a7-b4b2-769443948658%22%2C%22funczone%22:%22addrsm_ok_rcm%22}}; acw_tc=2760828316607052817621153e95fa050f957219637f004c8f8f36a387818a; zp_passport_deepknow_sessionId=e2ee98f5s33e524adfb9a8c56800b0cb3907; at=2cdc4ce2fd7d465daf9be71cac16f3b1; rt=4990030b91bf4d2595abad1ae014e551; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221143581858%22%2C%22first_id%22%3A%2218230456ef1a0f-01ecf78074de37d-1c525635-1764000-18230456ef2abe%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyMzA0NTZlZjFhMGYtMDFlY2Y3ODA3NGRlMzdkLTFjNTI1NjM1LTE3NjQwMDAtMTgyMzA0NTZlZjJhYmUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTQzNTgxODU4In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221143581858%22%7D%2C%22%24device_id%22%3A%2218230456ef1a0f-01ecf78074de37d-1c525635-1764000-18230456ef2abe%22%7D; selectCity_search=736; FSSBBIl1UgzbN7NP=53BSMADhZK0qqqqDcjQVT3acOJpp1ZNYiLeWFEailA1YDJ7eePoCw3qo3yxDTjv0aO8Q8li3PjUdMhN6M29_n2H7iU4PMAuZ87P0b9DkBSMJOkK3AA2mtgnoTe9vkFKbeEEHAZOIA1_qpl7ICwSwT7N6In2aQeD1Lp0YCX7zisZTcU2zqxFi7sPouw3tKuiyCOxx3sgSagZ_RQAOmrNCZAVyxfGKNiZ02mjsG153xFGNUMzN1Ba13fh1qcKSogpAPybxDAn8lWct7gLqlN_MH0u6MNn8pnHZbo6T6hzs.Pywa"

el = ['5', '4', '3', '10', '1']
et = ['4', '5']


async def aiodownload(param, result):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, verify_ssl=False)) as session:
        async with session.get(url, params=param, headers=headers) as resp:
            try:
                conf = json.loads(obj.findall(await resp.text())[0])
            except:
                sys.exit()
            if conf['positionList']:
                result.extend(conf['positionList'])


async def main(params, name):
    result = []
    for i in range(3):
        tasks = []
        n = len(result)
        for param in params[i * 11: i*11+11]:
            tasks.append(asyncio.create_task(aiodownload(param, result)))
        if i == 2:
            tasks.append(asyncio.create_task(aiodownload(params[33], result)))
        await asyncio.wait(tasks)
        if n+330 != len(result):
            break
    df = pd.DataFrame(data=result)
    df.to_csv(f"zhilian_urls/{city}_urls/{name}", index=False)
    await asyncio.sleep(5)


def coroutine(name, params, loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(params, name))
    # asyncio.run(main(params, name))
    print(name, 'finished')


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "referer": "https://www.zhaopin.com/",
        "cookie": cookie
    }
    files = os.listdir(f'./zhilian_urls/{city}_urls')
    obj = re.compile('<script>__INITIAL_STATE__=(?P<js>.*?)</script>', re.S)
    with open('zhilian_structure.json', 'r') as f:
        conf = json.load(f)
    names = {}
    for first in conf['baseData']['jobType']:
        if first['code'] == '-1':
            continue
        for second in first['sublist']:
            for third in second['sublist']:
                outfile_name = f"{first['name'].replace('/', 'or')}_{second['name'].replace('/', 'or')}_{third['name'].replace('/', 'or')}_实习.csv"
                if outfile_name in files:
                    continue
                names[outfile_name] = []
                for i in range(1, 35):
                    param = {'jl': city_code, 'p': i, 'jt': ','.join([first['code'], second['code'], third['code']])}
                    names[outfile_name].append(param)

    with ThreadPoolExecutor(10) as thread:
        for name, params in names.items():
            thread_loop = asyncio.new_event_loop()
            thread.submit(coroutine, name=name, params=params, loop=thread_loop)

    # coroutine('销售or商务拓展_商务拓展_渠道经理.csv', names['销售or商务拓展_商务拓展_渠道经理.csv'], asyncio.new_event_loop())
