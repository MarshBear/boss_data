import pandas as pd
import re
import json
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

file = 'shanghai_urls.csv'

cookie = 'adfbid2=0; x-zp-client-id=7c3c1171-ce17-4f87-90e1-108e213b34c2; c=WesRxSct-1652164066912-041baefa77b0e-554175798; _fmdata=8CJO%2F3%2BB7WcrCgmsKiwZYLxMdAe8zRprKrfcKajm9%2FgbmXH0gDDDFIsppidQhGXCJh2xBscCU%2Fa1KtAjJzLxG8QxFKYjodl8S1giTx33asM%3D; locationInfo_search={%22code%22:%22656%22%2C%22name%22:%22%E5%98%89%E5%85%B4%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; _uab_collina=165838381687027181351501; sts_deviceid=18233d0402cd55-005bdfdbfeec9-74492f2a-1821369-18233d0402dc71; _xid=StAkkjdtEnxWm7hMXJlHOc0VTRnHPB38dikOUCbSZMZNa0gAXfLG%2BzcpEbOaBEMnIy6qmPzAUiaB7PVw0hI6Qw%3D%3D; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1658383802,1658726624,1658801407,1658907890; selectCity_search=530; ZP_OLD_FLAG=false; rt=92c6aaf2673a402da8bbf3d84e64f3b6; at=116764ea872e4f9c9083cfbc69ac1e89; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221143581858%22%2C%22first_id%22%3A%22180aca65d7c1d7-019f02096947915-7e647c6c-1338645-180aca65d7db22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22SogouPC%22%2C%22%24latest_utm_medium%22%3A%22CPC%22%2C%22%24latest_utm_campaign%22%3A%22pp%22%2C%22%24latest_utm_content%22%3A%22qg%22%2C%22%24latest_utm_term%22%3A%22947928%22%7D%2C%22%24device_id%22%3A%22180aca65d7c1d7-019f02096947915-7e647c6c-1338645-180aca65d7db22%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxYWZjMmZkNGM0NS0wOTBiNzcyZjhjNDE3NS00ZjYxN2Y1Yi0xODIxMzY5LTE4MWFmYzJmZDRkZTk2IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTE0MzU4MTg1OCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221143581858%22%7D%7D; urlfrom2=121126445; adfcid2=none; acw_tc=2760829116590720720173463eac2555922658eb06add73f02e450b4885f32; acw_sc__v2=62e36e48451c4ddfd5ebfe0b8bfe4a7ffddfa1f2; acw_sc__v3=62e36ea4198769cdd44bb25db9922b5b7000a989; ssxmod_itna=YqUxnD0DuQitDtG8zDXQG7AHG=2K+7GMRiobwBl4GXLTDZDiqAPGhDC+89Bxh8D2GYYzi7ciPADc42KwHYjmxdeLlpx0aDbqGkQnjh4GGUxBYDQxAYDGDDP2D84DrD7O1CgLxYPG0DiKDpx0kCcKDWx5DEjFODY5sDDHQ8x07DQy8REawDboDnEGCHC28D7vpDlaeA+08iISfY7vCht8+LWIG440OD0KGLxibCroDUBKzo/wxLQGxWBuDaerd3C2q=mG4kllcpWnDtnDPF5h4YQnP3WrKHx=Di1x4OQGK4D=; ssxmod_itna2=YqUxnD0DuQitDtG8zDXQG7AHG=2K+7GMRiobwY4A=awbD/UU+QDFOihBtRlPApxciWdRNkq=ldYbw4LpnyKvPZoL9P+Vn2nHmEVlR=C=P=gf0OOGth+KdnGxh+1ASpmVrVO/LML9st9juE5BqdfUT=j080him6sCuXP2k6S8S6YVR5oaq6GWMA3Z3TsjEW1mqQDVr3iH=YfY1nkR+unnjWohbWB9QYKu1RsO16GVur/KfidLhDIcwgMAbNs58qpfgNfyWXKRzY4zrxq4SFP97GHKS8eKyExzCA4WXg90cWYZOdVziVKn5o0yPiqHBiDgyCly8WmHFqciqquwqNWz37pY7DLFz7ymSYWlHRlxDXnYMIzWqDdcPIHVYw67O6DEQg76WewlTfluEYw3D07tAxPoI=7qU8q/dAq1r3Dxo6qm2DNDDLxD2iGDD===; ZL_REPORT_GLOBAL={%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%22665fa5f1-50d3-4507-b09a-650456bad63c-job%22}}'

u_atoken = "a55ede5c-8e41-4546-aebe-0c41b4df9100"

start_num = 31430


def write_detail(detailed_position, detailed_company, data_series, ind):
    detailed_result = dict()
    detailed_result['origin_index'] = ind
    detailed_result['岗位具体名称'] = detailed_position['name']
    detailed_result['薪资'] = detailed_position['salary60']
    detailed_result['所在地区'] = detailed_position['workCity'] + '-' + detailed_position['cityDistrict']
    detailed_result['经验要求'] = detailed_position['positionWorkingExp']
    detailed_result['学历要求'] = detailed_position['education']
    detailed_result['工种性质'] = detailed_position['workType']
    detailed_result['招聘人数'] = detailed_position['recruitNumber']
    detailed_result['发布时间'] = detailed_position['positionPublishTime']
    detailed_result['职位描述标签'] = ';'.join([x['value'] for x in detailed_position['skillLabel']])
    detailed_result['职位描述'] = detailed_position['jobDesc'].replace('<div>', '').replace('</div>', '').replace('<p>', '').replace('</p>', '').replace('<br>', '')
    detailed_result['职位福利'] = ';'.join([x['value'] for x in detailed_position['welfareLabel']])
    detailed_result['工作地点'] = detailed_position['workAddress']
    detailed_result['岗位亮点'] = detailed_position['positionHighlight']
    detailed_result['岗位url'] = detailed_position['positionUrl']
    detailed_result['岗位类型名'] = detailed_position['jobTypeLevelName']
    detailed_result['雇员点评标签'] = ';'.join([x['value'] for x in detailed_position['bestEmployerLabel']])
    detailed_result['公司名称'] = detailed_position['companyName']
    detailed_result['（实习）是否可转正'] = detailed_position['canBeRegular']
    detailed_result['（实习）提供实习证明'] = detailed_position['provideInternshipCertificate']
    detailed_result['（实习）远程实习'] = detailed_position['canRemoteInternship']
    detailed_result['地点商业区'] = detailed_position['tradingArea']
    detailed_result['公司融资情况'] = detailed_company['financingStageName']
    detailed_result['公司所在行业'] = detailed_company['industryNameLevel']
    detailed_result['公司规模'] = detailed_company['companySize']
    detailed_result['公司描述'] = detailed_company['companyDescription']
    detailed_result['公司url'] = detailed_company['companyUrl']
    detailed_result['公司性质'] = data_series['property']
    detailed_result['薪酬数'] = data_series['salaryCount']
    detailed_result['category1'] = data_series['category1']
    detailed_result['category2'] = data_series['category2']
    detailed_result['category3'] = data_series['category3']
    return detailed_result


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
    "cookie": cookie
}

data = pd.read_csv('./zhilian_urls/' + file)

params = {
    "refcode": 4019,
    "srccode": 401901,
    "preactionid": "",
    "u_atoken": u_atoken
}

obj = re.compile('<script>__INITIAL_STATE__=(?P<js>.*?)</script>', re.S)


async def aiodownload(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.url == 'https://jobs.zhaopin.com/lost':
                return
            conf = json.loads(obj.findall(await resp.text())[0])


async def main():
    pass


def coroutine(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    print('finished')


if __name__ == '__main__':
    data = data.loc[start_num:]
    urls = data['positionURL'].apply(lambda x: x.replace('http://', 'https://')).to_list()


