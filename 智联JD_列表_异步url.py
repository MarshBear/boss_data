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

city = 'tianjin'
city_code = '531'

cookie = "x-zp-client-id=6a34bdff-0cdb-4b30-a5d6-eb3c21bf85ad; zp_passport_deepknow_sessionId=b347e779s0be6f4c4daf760bd39fc492c85a; at=cd499344528f4392860eff4c741d2cc2; rt=728b4b1a04594447a147d4a9ed53ef8b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221143581858%22%2C%22first_id%22%3A%2218268704b221e-09ff941f2efc6b-76492e2f-1821369-18268704b237a1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyNjg3MDRiMjIxZS0wOWZmOTQxZjJlZmM2Yi03NjQ5MmUyZi0xODIxMzY5LTE4MjY4NzA0YjIzN2ExIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTE0MzU4MTg1OCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221143581858%22%7D%2C%22%24device_id%22%3A%2218268704b221e-09ff941f2efc6b-76492e2f-1821369-18268704b237a1%22%7D; FSSBBIl1UgzbN7NO=5Y5LggriXH_Kj3qunKwIbhvBGV82gZnAnDimLwW.j4kqofCIK1oSWJF4fcbuT0o_jQlsqRSpa0rK5JJe2.xH4tq; _uab_collina=165960960448468501247055; locationInfo_search={%22code%22:%22653%22%2C%22name%22:%22%E6%9D%AD%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1659609605; selectCity_search=531; ssxmod_itna=QqUx0D9Gi=YhDODzxAxewnRDgG9id34YA6Q+QD/jFmDnqD=GFDK40ooO3DCQmGQDOhh1eb=C0oqK6mGgxwkBpRDcQbDCPGnDB9Go8mDYYkDt4DTD34DYDirQGIDieDFF5H/8DbxYQDmxiODlKH6xDa0xi3LaKDR25D0xwFDQKDu6IC8cYGW4D1qYvPFjKD9OoDs6DfKjKmEUfx9oHAwI73poAGDCKDjxB8DmeHW4GdUhH+Vir3iihe/e94LQGPMYpxqG0uFT2DPrRKIWZ4q70ih0=nHODDiPFn4D; ssxmod_itna2=QqUx0D9Gi=YhDODzxAxewnRDgG9id34YA6Q4G9iqEDBw8OD7PY4dO994OGFjUHn8whzc0OEppxD0EyDeBYmexrzdY8rfppaHiY8b4sgrh4te6F4EBjjSFnM57pZ9D9S==BU9+vrYIErsiD5Gy=DCN19GP4pk/B7GED07Kn4DLxG7KYD=; ZL_REPORT_GLOBAL={%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%22e50652e0-e83a-49f3-8be7-8386edf1a773-job%22}}; acw_tc=276077e416596927206211408e6ed117c0ce57b26092ee8a4ce8f5e3cf6bca; acw_sc__v2=62ece6b88dd6dc9e37e5dd501ff1d366119fa5f6; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1659692734; FSSBBIl1UgzbN7NP=53XubBKh7y.0qqqDcMKYKSAgCF7S8v28x86icJ_mmYn2WYH5tbI.FqEzLnhbcxCDMDrE4J8ujKc.eP0OI5dVsCootkDbmVAiezrxYShdh9kw3.llHVsc7Gbvs9SapTKqvrpnGKwPmsKKnMTrrbWZ1GkW6QGEN290hORdufajXdZ2WySvDGiPs.qtl7CoY3oLbLLATr63ssjoEBeBy_o1bAdhXuR2Ob1D64OY_49DdSHwtTYEkm20OU8jnrt8Axji_um_16kdwewm.Z03D_q87KCQO.H_pmoLNdVNXMcQQqLPG"


async def aiodownload(param, result):
    async with aiohttp.ClientSession() as session:
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
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
                outfile_name = f"{first['name'].replace('/', 'or')}_{second['name'].replace('/', 'or')}_{third['name'].replace('/', 'or')}.csv"
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

    # coroutine('教育or培训or科研_语言培训_德语教师.csv', names['教育or培训or科研_语言培训_德语教师.csv'])
