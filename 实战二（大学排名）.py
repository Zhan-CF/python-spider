#import requests
#from lxml import html
from selenium.webdriver import Edge
import time
from selenium.webdriver.common.by import By
import csv

web = Edge()
web.get('https://www.shanghairanking.cn/rankings/bcur/2024')

#写完xpath准备遍历页数时注意到翻页后url没变
#之后使用selenium提取文本内容时发现不用strip也不会出现空格和换行符
'''url = 'https://www.shanghairanking.cn/rankings/bcur/2024'
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
tree = html.fromstring(response.text)

ranks = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr/td[1]/div/text()')
new_ranks = []
for rank in ranks:
    new_ranks.append(rank.strip())
names = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr/td[2]/div/div[2]/div[1]/div/div/span/text()')
new_names = []
for name in names:
    new_names.append(name.strip())
E_names = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div/span/text()')
new_E_names = []
for E_name in E_names:
    new_E_names.append(E_name.strip())
provinces = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr/td[3]/text()')
new_provinces = []
for province in provinces:
    new_provinces.append(province.strip())
ratings = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr/td[5]/text()')
new_ratings = []
for rating in ratings:
    new_ratings.append(rating.strip())
level = tree.xpath('//*[@id="content-box"]/div[2]/table/tbody/tr[1]/td[6]/text()')
print(level)'''


with open('实战二_rank.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['排名','学校名字','英文名字','省份','评分','办学层次'])
    for page in range(1,21):
        time.sleep(3)
        trs = web.find_elements(By.XPATH,'//*[@id="content-box"]/div[2]/table/tbody/tr')
        for tr in trs:
            rank = tr.find_element(By.XPATH,'./td[1]/div').text
            name = tr.find_element(By.XPATH,'./td[2]/div/div[2]/div[1]/div/div/span').text
            E_name = tr.find_element(By.XPATH,'./td[2]/div/div[2]/div[2]/div/div/span').text
            province = tr.find_element(By.XPATH,'./td[3]').text
            rating = tr.find_element(By.XPATH,'./td[5]').text
            level = tr.find_element(By.XPATH,'./td[6]').text
            if len(level) == 0:
                level = '无'

            writer.writerow([rank,name,E_name,province,rating,level])
            print(rank,name,E_name,province,rating,level)
        print(f'第{page}页存储完成')
        if page < 4 or page > 17:
            web.find_element(By.XPATH,'//*[@id="content-box"]/ul/li[9]').click()
        elif page == 4 or page == 17:
            web.find_element(By.XPATH,'//*[@id="content-box"]/ul/li[10]').click()
        else:
            web.find_element(By.XPATH,'//*[@id="content-box"]/ul/li[11]').click()
