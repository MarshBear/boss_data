import asyncio
import time
import aiohttp
import json
import re
import sys
import pandas as pd
import os
import requests
from selenium.webdriver import Chrome

city = 'zhengzhou'
city_code = '719'

# web = Chrome()
# web.get('https://sou.zhaopin.com/?jl={}&p=1'.format(city_code))
# cookie = '; '.join([cookie['name']+'='+cookie['value'] for cookie in web.get_cookies()])
cookie = 'x-zp-client-id=1f45cddd-7c38-4842-b122-30a1fc9898e7; sajssdk_2015_cross_new_user=1; zp_passport_deepknow_sessionId=a0c9ebd6s96e0247109048b87ee7739ad2c0; at=11aaa512ed0f472caa6886c7de81b5ce; rt=1172e1b69cc140baaf4482610499119d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221143581858%22%2C%22first_id%22%3A%22182d88014e77c5-0d4b2646ef7ec58-1b525635-1764000-182d88014e8a33%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyZDg4MDE0ZTc3YzUtMGQ0YjI2NDZlZjdlYzU4LTFiNTI1NjM1LTE3NjQwMDAtMTgyZDg4MDE0ZThhMzMiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTQzNTgxODU4In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221143581858%22%7D%2C%22%24device_id%22%3A%22182d88014e77c5-0d4b2646ef7ec58-1b525635-1764000-182d88014e8a33%22%7D; FSSBBIl1UgzbN7NO=52XJlGzLQOvbyn0L53r7SzpvXjwRejnNYwggOM.sonwVob.6ohI5qPK0hWGkFu9v40LKxw680GViWZZ.mF_aeya; locationInfo_search={%22code%22:%22653%22%2C%22name%22:%22%E6%9D%AD%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; _uab_collina=166148968057519468863371; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1661489681; acw_tc=2760829316615005388925203e813cbdeb9e1f27c375dc98bcbde2fda5e570; acw_sc__v2=63087cf761f0cdf918f0e6794898c566cc58c6bd; selectCity_search=599; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1661502249; FSSBBIl1UgzbN7NP=53aPktCWEGn3qqqDcCVr7HaWxq_Eu3.CWjktOltkEJOQNW05air292E2oERt0kMpurOEB9fP94eBKd750K1vfh94fqYNhiRFC.3gO7gaaoTpp08L0edLXSLQzL4yeYJnaRGk_88PrMYQQFNGYsIUOcc67SytNYaLj7TAl_kye1ejG02ytfV41NAsFr4N6_ogxgNnbt5JxkIlfHOpKUmLLrs_V8v0cr4Za2EvZuphYIS6eOzkDPtCV65SADkloTZFEbpSCJq0GyjStrAcn0UiQ.v'

obj = re.compile('<script>__INITIAL_STATE__=(?P<js>.*?)</script>', re.S)
url = 'https://sou.zhaopin.com/'
headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "referer": "https://www.zhaopin.com/",
        "cookie": cookie
}


async def download_one_page(param, result):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        async with session.get(url, params=param, headers=headers) as resp:
            conf = json.loads(obj.findall(await resp.text())[0])
            result.append({'params': param, "position": conf['positionList']})


async def main(params, page):
    global continue_params
    result = []
    tasks = []
    for i in range(len(params) // 250):
        for param in params[i*250:i*250+250]:
            tasks.append(asyncio.create_task(download_one_page(param, result)))
        await asyncio.wait(tasks)
        if len(result) != 250 * (i+1):
            print('length err')
            sys.exit()
        print(i, 'succeeded.')
    if len(params) % 250 != 0:
        for param in params[len(params) // 250 * 250:]:
            tasks.append(asyncio.create_task(download_one_page(param, result)))
        await asyncio.wait(tasks)
        if len(result) != len(params):
            print('length err')
            sys.exit()
        print(len(params) // 250, 'succeeded.')
    continue_params = [{key: item['params'][key] for key in ['jl', 'et', 'jt']} for item in result if len(item['position']) == 30]
    result = [{**position, **item['params']} for item in result for position in item['position']]
    df = pd.DataFrame(data=result)
    if shixi_xiaoshao == '实习':
        df.to_csv(f"zhilian_urls_shixi/{city}_{city_code}/page{page}.csv", index=False)
    else:
        df.to_csv(f"zhilian_urls_xiaozhao/{city}_{city_code}/page{page}.csv", index=False)


def get_param_list(et: str):
    """
    :param et: 标记实习与校招
    :return:
    """
    if et == "实习":
        files = os.listdir(f'./zhilian_urls_shixi/{city}_{city_code}')
        et_code = '4'
    elif et == "校招":
        files = os.listdir(f'./zhilian_urls_xiaozhao/{city}_{city_code}')
        et_code = '5'
    else:
        sys.exit()
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
                names[outfile_name] = {'jl': city_code, 'et': et_code, 'jt': ','.join([first['code'], second['code'], third['code']])}
    return names


def integrate():
    if shixi_xiaoshao == '实习':
        whether = 'shixi'
    elif shixi_xiaoshao == '校招':
        whether = 'xiaozhao'
    else:
        sys.exit()
    files = os.listdir(f'zhilian_urls_{whether}/{city}_{city_code}')
    df = pd.DataFrame()
    for file in files:
        if file[-4:] == '.csv':
            df_new = pd.read_csv(f'zhilian_urls_{whether}/{city}_{city_code}/{file}')
            df = pd.concat((df, df_new), axis=0)
    df.to_csv(f'zhilian_urls_{whether}/all_results/{city}_{city_code}_{len(df)}.csv', index=False)


async def less_data(params):
    tasks, result = [], []
    for i in range(1, 35):
        param = {**params, **{'p': i}}
        tasks.append(asyncio.create_task(download_one_page(param, result)))
    await asyncio.wait(tasks)
    result = [{**position, **item['params']} for item in result for position in item['position']]
    df = pd.DataFrame(data=result)
    if shixi_xiaoshao == '实习':
        df.to_csv(f"zhilian_urls_shixi/{city}_{city_code}/page1.csv", index=False)
        print(f"zhilian_urls_shixi/{city}_{city_code}/page1.csv finished.")
    else:
        df.to_csv(f"zhilian_urls_xiaozhao/{city}_{city_code}/page1.csv", index=False)
        print(f"zhilian_urls_shixi/{city}_{city_code}/page1.csv finished.")


if __name__ == '__main__':
    for shixi_xiaoshao in ['实习', '校招']:
        names = get_param_list(shixi_xiaoshao)
        continue_params = list(names.values())
        # with ThreadPoolExecutor(10) as thread:
        #     for name, params in names.items():
        #         thread_loop = asyncio.new_event_loop()
        #         thread.submit(coroutine, name=name, params=params, loop=thread_loop)

        resp = requests.get(url, params={'jl': city_code, 'et': '5' if shixi_xiaoshao == '校招' else '4', 'p': 34}, headers=headers)
        conf = json.loads(obj.findall(resp.text)[0])
        if not conf['positionList']:
            asyncio.run(less_data(params={'jl': city_code, 'et': '5' if shixi_xiaoshao == '校招' else '4'}))
        else:
            for i in range(1, 35):
                if not continue_params:
                    break
                params = []
                for param in continue_params:
                    params.append({**param, **{'p': str(i)}})
                asyncio.run(main(params, i))
                print(f'page {i} finished')
        integrate()

