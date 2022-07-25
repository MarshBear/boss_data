import pandas as pd
import requests
import re

url = "https://www.liepin.com/zhaopin/"

params = {
    "headId": "3d47129f03e5157c181db2b3d5c26690",
    "ckId": "j5kaw43car8xc18rsrg8axbycg89bz0b",
    "fkId": "cz2ikids8vf7uf5z4zug49u214ocb2y8",
    "skId": "cz2ikids8vf7uf5z4zug49u214ocb2y8",
    "sfrom": "search_job_pc",
    "scene": "condition",
    "currentPage": 9
}

params2 = {
    "headId": "f8fa1e87cc1afdb639fa5b467442a783",
    "ckId": "ol74jr59gnkdf58ix225je2q50nb6qfb",
    "fkId": "q7v2i71eu9zhvgevqn8hu0vijknwkcvb",
    "skId": "q7v2i71eu9zhvgevqn8hu0vijknwkcvb",
    "sfrom": "search_job_pc",
    "workYearCode": 1,
    "scene": "condition"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "refer": "https://www.liepin.com/",
    "host": "www.liepin.com"
}

resp = requests.get(url, params=params, headers=headers)

url_obj = re.compile('<a data-nick="job-detail-job-info".*?href="(?P<href>.*?)"', re.S)

detail_urls = url_obj.findall(resp.text)

detail_objs = [re.compile('<span class="name ellipsis-1">(?P<title>.*?)</span>', re.S),
               re.compile('<span class="salary">(?P<salary>.*?)</span>', re.S),
               re.compile('<!-- 职位地区 -->.*?<span>(?P<location>.*?)</span>', re.S),
               re.compile('<!-- 职位工作年限 -->.*?<span class="split"></span>.*?<span>(?P<experience>.*?)</span>', re.S),
               re.compile('<!-- 学历 -->.*?<span class="split"></span>.*?<span>(?P<education>.*?)</span>', re.S),
               re.compile('<!-- 职位福利 -->.*?<div class="labels">(?P<labels>.*?)</div>', re.S),
               re.compile('<span class="name">(?P<hrname>.*?)</span>', re.S),
               re.compile('<div class="title-box">.*?<span>(?P<hrtitle>.*?)</span>.*?<span>.*?'
                          '<a .*?target="_blank">(?P<corname>.*?)</a>', re.S),
               # re.compile('<span class="name">.*?</span>.*?'
               #            '<a href="(?P<corurl>.*?)".*?target="_blank">(?P<corname>.*?)</a>', re.S),
               re.compile('<dd data-selector="job-intro-content">(?P<jobdescription>.*?)</dd>', re.S),
               re.compile('<div class="inner ellipsis-3">(?P<corpdescription>.*?)</div>', re.S),
               re.compile('<span class="label">企业行业：</span>.*?<span class="text">(?P<industry>.*?)</span>', re.S),
               re.compile('<span class="label">人数规模：</span>.*?<span class="text">(?P<numpeople>.*?)</span>', re.S),
               re.compile('<span class="label">职位地址：</span>.*?<span class="text">(?P<position>.*?)</span>', re.S)]

data = []

for detail_url in detail_urls:
    detail_resp = requests.get(detail_url, headers=headers)
    detail_text = detail_resp.text
    info = {}
    for obj in detail_objs:
        for it in obj.finditer(detail_text):
            info.update(**it.groupdict())
    detail_resp.close()
    data.append(info)

df = pd.DataFrame(data=data)
