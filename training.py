import requests
import re

url = 'https://www.zhipin.com/web/geek/job?query=&city=101210100'
url_joblist = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json'


data = {
    "scene": 1,
    "query": '',
    "city": 101210100,
    "experience": '',
    "degree": '',
    "industry": '',
    "scale": '',
    "stage": '',
    "position": '',
    "salary": '',
    "multiBusinessDistrict": '',
    "page": 1,
    "pageSize": 30
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "refer": url,
    "cookie": "wd_guid=2a2e671a-3cf2-4e1d-a414-71007784fe1c; historyState=state; _bl_uid=hRlRb5qnmv0cyej3pwt3ehyqsRpI; lastCity=101210100; _9755xjdesxxd_=32; YD00951578218230%3AWM_TID=HH07TFhuSgpAAFEVURbQTAAnmmkAXUCx; JSESSIONID=1892403F955851E71D5499E4E436F465; toUrl=https%3A%2F%2Fwww.zhipin.com%2F; YD00951578218230%3AWM_NI=%2F%2Fk1jiOJxalyTXti%2BrJ9AX0qwUrFjDg%2BhShbBziniIISV0xIfhEgf7Vsm4sVtYP%2FnBFSOV7DNLpuCxjT486dAmWS1akfqsli8aDLvI8RPXINjXh8E9fvoKI4ze8sxCSKWlo%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed4cf6798edbaacd53ca19e8ea3c44f868f8b83c150968883d6d053b59ca0adf92af0fea7c3b92aedf1a5d2e9638d96b882ef739888bc8aaa7a8ae78fb9b37bb58bbea7e950a5f5a8b4eb6a82a6a78fec438b8d9ad1fb43a6b88b88e53d96ada3d5f25eb887a0d0ed4a868d81b7b6508e94c096c274aa8cfcd9b57083b399b4b46ba9babf94ef63fcbf8cadf543fc8ea0b9cc46aa88a8d9c833a6aaa1accc40babbf894fb499195998dee37e2a3; gdxidpyhxdE=rk1RWvEN6vdyB3UrGJuPC93kfbYq7WYXnG5Iuoe540ft4wPyc8hdH7KabYkcjcW9E5S3uIJvAKg5onbG%5CLWjkL35UL%2B7t8l8OybDEKwQx2Bg1xALzVOsQTGqWaneG69A%5Cfoxz31VEyCssirJHPKRBpYm8Ne%5Cca2QEDHpr46JD6JmxbPt%3A1658041760755; __zp_seo_uuid__=b95a021f-52cc-48cf-b12d-10e526308eb7; __g=-; __c=1657882697; __l=r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%26city%3D101210100&s=3&g=&friend_source=0&s=3&friend_source=0; __a=30293374.1657882697..1657882697.102.1.102.102; __zp_stoken__=cb6cdf11MPmwlMRsHanISPTdSQ2lXAUtYYTxsHzxfNzxsLV5bPgMySXkaRX1hejJ9LkBzelx1Q1hqFVAAPEYRNDBdbBJyTS1kfnNJEXsrSV4lKQhnWGs3fGsaWB4XYzYoIFUTTFB%2BIBhoQV9NFCBgbX5HSU9SFg1XTwJbHlIEMVc9XDF0Ixd6TxkVMBZVWgRWIF9sb2BNJQ%3D%3D"
}

obj1 = re.compile('<div class="job-status"><span>(?P<status>.*?)</span></div>', re.S)
resp = requests.get(url_joblist, params=data, headers=headers)
job_list = resp.json()['zpData']['jobList']

for dic in job_list:
    detail_url = 'https://www.zhipin.com/job_detail/' + dic['encryptJobId'] + '.html'
    detail_data = {
        "lid": dic['lid'],
        "securityId": dic['securityId']
    }
    detailed_header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "cookie": "__snaker__id=jgblXXw02WpCOoTw; wd_guid=2a2e671a-3cf2-4e1d-a414-71007784fe1c; historyState=state; _bl_uid=hRlRb5qnmv0cyej3pwt3ehyqsRpI; lastCity=101210100; _9755xjdesxxd_=32; YD00951578218230%3AWM_TID=HH07TFhuSgpAAFEVURbQTAAnmmkAXUCx; JSESSIONID=1892403F955851E71D5499E4E436F465; toUrl=https%3A%2F%2Fwww.zhipin.com%2F; YD00951578218230%3AWM_NI=%2F%2Fk1jiOJxalyTXti%2BrJ9AX0qwUrFjDg%2BhShbBziniIISV0xIfhEgf7Vsm4sVtYP%2FnBFSOV7DNLpuCxjT486dAmWS1akfqsli8aDLvI8RPXINjXh8E9fvoKI4ze8sxCSKWlo%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed4cf6798edbaacd53ca19e8ea3c44f868f8b83c150968883d6d053b59ca0adf92af0fea7c3b92aedf1a5d2e9638d96b882ef739888bc8aaa7a8ae78fb9b37bb58bbea7e950a5f5a8b4eb6a82a6a78fec438b8d9ad1fb43a6b88b88e53d96ada3d5f25eb887a0d0ed4a868d81b7b6508e94c096c274aa8cfcd9b57083b399b4b46ba9babf94ef63fcbf8cadf543fc8ea0b9cc46aa88a8d9c833a6aaa1accc40babbf894fb499195998dee37e2a3; acw_tc=0a099d6e16580404276477313e016d3fdace6505584d4849b9de4c99eb230f; gdxidpyhxdE=rk1RWvEN6vdyB3UrGJuPC93kfbYq7WYXnG5Iuoe540ft4wPyc8hdH7KabYkcjcW9E5S3uIJvAKg5onbG%5CLWjkL35UL%2B7t8l8OybDEKwQx2Bg1xALzVOsQTGqWaneG69A%5Cfoxz31VEyCssirJHPKRBpYm8Ne%5Cca2QEDHpr46JD6JmxbPt%3A1658041760755; __zp_seo_uuid__=b95a021f-52cc-48cf-b12d-10e526308eb7; __g=-; __l=r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%26city%3D101210100&s=3&g=&friend_source=0&s=3&friend_source=0; __c=1657882697; __a=30293374.1657882697..1657882697.103.1.103.103; __zp_stoken__=cb6cdf11MPmwlMRsHanIlYSozBh1XAUtYYTxsHzxfNzxsLV5bPkl4Oz4VRX1hejJ9LkBzelx1Q1hqFQBcciseQjBdbBJyTS1kfnNJEXsrSV4lUgt3NgU3fGsaWB4XYzYoIFUTTCgMJBhyIm0wE18AW1ggVTlYGjBXTwJbHlIEMVc9XDF0TXlqTGIVMBZVWgRWIF9sb2BNJQ%3D%3D"
    }
    resp_detail = requests.get(detail_url, params=detail_data, headers=detailed_header)
    resp_detail_text = resp_detail.text

    result = re.findall(obj1, resp_detail_text)
