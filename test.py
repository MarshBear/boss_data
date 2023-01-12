from selenium.webdriver import Chrome

web = Chrome()
web.get('https://sou.zhaopin.com/?jl=702&p=1')
for cookie in web.get_cookies():
    print(cookie)
