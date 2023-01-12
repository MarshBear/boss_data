import requests
from lxml import etree
import re
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import pickle

list_url = "https://baike.zhipin.com/wiki/?ka=header-baike"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

obj_salary = re.compile('<div class="seo-hidden" data-v-318d3e2c>(?P<content>.*?)</div>', re.S)
obj_raise = re.compile('growRate:(?P<rate>.*?),.*?preNodeName:.*?,salary:(?P<salary>.*?)}', re.S)
obj_entrance = re.compile('<ul class="skills-list" data-v-6428e1e3>(?P<content>.*?)</ul>', re.S)
obj_divide = re.compile('<div class=".*?divide-class-list".*?>(?P<content>.*?)</div>', re.S)
obj_tools = re.compile('常用工具.*?(<ul class="card-list" data-v-6428e1e3>.*?</ul>)', re.S)
obj_books = re.compile('推荐书籍.*?(<ul class="card-list" data-v-6428e1e3>.*?</ul>)', re.S)
obj_describe = re.compile('<div class="describe" data-v-7e26b94f>(?P<content>.*?)</div>', re.S)
obj_job_content = re.compile('<div class="list-wrap" data-v-7e26b94f>(?P<content>.*?)</aside>', re.S)
obj_job_content_detail = re.compile('<span data-v-7e26b94f>(?P<content>.*?)</span>', re.S)


def process_content(content, job, result):
    detail_info = dict()
    detail_info['job_name'] = job['name']
    text_salary = obj_salary.findall(content)
    if text_salary:
        html_salary = etree.HTML(text_salary[0])
        salary_monthly_lst = html_salary.xpath('//ul[1]/li/span')
        salary_monthly = []
        for i in range(len(salary_monthly_lst) // 3):
            salary_monthly.append({
                'date': salary_monthly_lst[i * 3].text,
                'salary_median': salary_monthly_lst[i * 3 + 1].text[6:],
                'compare_to_last': salary_monthly_lst[i * 3 + 2].text[5:]
            })
        salary_yearly_lst = html_salary.xpath('//ul[2]/li/span')
        salary_yearly = []
        for i in range(len(salary_yearly_lst) // 2):
            salary_yearly.append({
                'year': salary_yearly_lst[i * 2].text[5:],
                'salary_median': salary_yearly_lst[i * 2 + 1].text[6:]
            })
        detail_info['salary_monthly'] = salary_monthly
        detail_info['salary_yearly'] = salary_yearly

    text_raise = obj_raise.findall(content)
    if text_raise:
        detail_info['raise'] = [{'annual_income': item[1], 'compare_to_last': item[0]} for item in text_raise]

    text_entrance = obj_entrance.findall(content)
    if text_entrance:
        html_entrance = etree.HTML(text_entrance[0])
        entrance_dem_s = html_entrance.xpath('//li/span')
        entrance_des_s = html_entrance.xpath('//li/p')
        entrance = [{'demand': dem.text, 'content': des.text} for dem, des in zip(entrance_dem_s, entrance_des_s)]
        if len(entrance_dem_s) > len(entrance_des_s):
            entrance.append({'demand': '需掌握的技能', 'content': ';'.join([item.text.strip('\n ') for item in html_entrance.xpath('//li/ul/li')])})
        detail_info['entrance'] = entrance

    text_divide = obj_divide.findall(content)
    if text_divide:
        html_divide = etree.HTML(text_divide[0])
        divide_p_lst = html_divide.xpath('//ul/li/p')
        divide_a_lst = html_divide.xpath('//ul/li/a')
        job_divide = []
        for i, a in enumerate(divide_a_lst):
            job_divide.append({
                'name': divide_p_lst[i * 2].text.strip('\n '),
                'description': divide_p_lst[i * 2 + 1].text.strip('\n '),
                'url': a.attrib['href']
            })
        detail_info['job_divide'] = job_divide

    text_tools = obj_tools.findall(content)
    if text_tools:
        html_tools = etree.HTML(text_tools[0])
        tools = []
        for i in range(len(html_tools.xpath('//ul/li'))):
            tool_name = html_tools.xpath(f'//ul/li[{i + 1}]/div/div/div[2]/h4/div[1]')[0].text
            recommend_user = html_tools.xpath(f'//ul/li[{i + 1}]/div/div/div[3]/div/span')[0].text.strip('\n ')[2:]
            try:
                recommend_index = html_tools.xpath(f'//ul/li[{i + 1}]/div/div/div[2]/div')[0].text.strip('\n ')[5:]
            except IndexError:
                recommend_index = 'no data'
            tools.append({
                'name': tool_name,
                'recommend_index': recommend_index,
                'user_recommend': recommend_user
            })
        detail_info['tools'] = tools

    text_books = obj_books.findall(content)
    if text_books:
        html_books = etree.HTML(text_books[0])
        books = []
        for i in range(len(html_books.xpath('//ul/li'))):
            name = html_books.xpath(f'//ul/li[{i + 1}]/div/div/div[2]/h4/div[1]')[0].text
            recommend_user = html_books.xpath(f'//ul/li[{i + 1}]/div/div/div[3]/div/span')[0].text.strip('\n ')[2:]
            try:
                score = html_books.xpath(f'//ul/li[{i + 1}]/div/div/div[1]/div')[0].text
            except IndexError:
                score = 'no score'
            try:
                writer = html_books.xpath(f'//ul/li[{i + 1}]/div/div/div[2]/div/span')[0].text
            except IndexError:
                writer = 'no data'
            books.append({
                'name': name,
                'writer': writer,
                'score': score,
                'user_recommend': recommend_user
            })
        detail_info['books'] = books

    describe = obj_describe.findall(content)
    if describe:
        detail_info['job_description'] = describe[0]
    else:
        detail_info['job_description'] = 'no data'

    job_content = obj_job_content.findall(content)
    if job_content:
        content_lst = [str(i + 1) + '.' + des for i, des in enumerate(obj_job_content_detail.findall(job_content[0]))]
        detail_info['job_content'] = ';'.join(content_lst)
    else:
        detail_info['job_content'] = 'no data'
    result.append(detail_info)
    print(detail_info)


async def getInfo(url, job, results):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, verify_ssl=False)) as session:
        async with session.get(url, headers=headers) as resp_info:
            results.append([await resp_info.text(), job])


async def prepare_urls(name, info):
    tasks, results = [], []
    for job in info:
        info_url = "https://baike.zhipin.com/wiki/" + job['code'] + "/?from=baike"
        tasks.append(asyncio.create_task(getInfo(info_url, job, results)))
    await asyncio.wait(tasks)
    with open('{}.pkl'.format(name), 'wb') as f:
        pickle.dump(results, f)


if __name__ == '__main__':
    list_data, labels = {}, []
    with requests.get(list_url, headers=headers) as resp:
        resp.encoding = 'utf-8'
        html = etree.HTML(resp.text)
    for i in range(2):
        labels = html.xpath(f'//*[@id="content"]/div/section[1]/div/div[{i + 1}]/ul/li/div/div[1]/span')
        for j, label in enumerate(labels):
            info_lst = html.xpath(
                f'//*[@id="content"]/div/section[1]/div/div[{i + 1}]/ul/li[{j + 1}]/div/div[2]/ul/li/div/a')
            info_dic = [{'name': i.text, 'code': i.attrib['href'][30:-1], 'url': i.attrib['href']} for i in info_lst]
            list_data[label.text] = info_dic

    # for title, info_dic in list_data.items():
    #     asyncio.run(prepare_urls(title, info_dic))

    for title in list_data.keys():
        with open('{}.pkl'.format(title), 'rb') as f:
            results = pickle.load(f)
        results_processed = []
        with ThreadPoolExecutor(10) as thread:
            for result in results:
                thread.submit(process_content, content=result[0], job=result[1], result=results_processed)
        with open('result/{}.pkl'.format(title), 'wb') as f:
            pickle.dump(results_processed, f)
