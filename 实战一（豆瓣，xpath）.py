import requests
from lxml import html
import pymysql
import json

connection = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='jlr$&3237',db='douban_movies',charset='utf8mb4')

for i in range(0,250,25):
    url = "https://movie.douban.com/top250?start="+str(i)
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.text)

    hrefs = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/@href')
    #print(hrefs)
    for href in hrefs:
        in_response = requests.get(href, headers=headers)
        in_tree = html.fromstring(in_response.text)
        rank = in_tree.xpath('//*[@id="content"]/div[1]/span[1]/text()')[0]
        title = in_tree.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        year = in_tree.xpath('//*[@id="content"]/h1/span[2]/text()')[0].strip('()')
        director = in_tree.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        writers = in_tree.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
        actors = in_tree.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')  # ？这对吗，这不太对吧
        genres = in_tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
        nations = in_tree.xpath('//*[@id="info"]/span[text()="制片国家/地区:"]/following-sibling::text()[1]')  #从浏览器直接复制过来的xpath中的sapn是按索引找的，有几个会出错，所以用文本定位改了一下
        nations = ','.join(nations[0].split(' / '))   # / 看起来很乱，换成了逗号
        languages = in_tree.xpath('//*[@id="info"]/span[text()="语言:"]/following-sibling::text()[1]')
        languages = ','.join(languages[0].split(' / '))
        dates = in_tree.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        duration = in_tree.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')
        #这片长有意思，有额外片长不放标签里非放外边，先不管你了

        title_ = in_tree.xpath('//*[@id="info"]/span[text()="又名:"]')
        if not title_:
            title_ = '无'
        else:
            title_ = in_tree.xpath('//*[@id="info"]/span[text()="又名:"]/following-sibling::text()[1]')
            title_ = ','.join(title_[0].split(' / '))

        rating = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
        rating_num = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
        five = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]/text()')[0]
        four = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]/text()')[0]
        three = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]/text()')[0]
        two = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]/text()')[0]
        one = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]/text()')[0]

        overviews = in_tree.xpath('//*[@id="link-report-intra"]/span[2]/text()')  #XPath定位不到元素时，/text()不会报错，而是返回空列表[]，beautifulsoup就会报错
        if not overviews:
            overviews = in_tree.xpath('//*[@id="link-report-intra"]//span[@property="v:summary"]/text()')
        overviews = [overview.strip() for overview in overviews]
        overviews = '\n'.join(overviews)

        print(rank, title, year, director, writers, actors, genres, nations, languages, dates, duration, title_, rating,
              rating_num, five, four, three, two, one, overviews)

        with connection.cursor() as cursor:
            sql = 'INSERT INTO douban_top250 (`rank`, title, `year`, director, writers, actors, genres, nations, languages, `dates`, duration, title_, rating, rating_num, five, four, three, two, one, overviews) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            #名字里有的是mysql关键字，加了反引号
            cursor.execute(sql, (rank,title,year,
                json.dumps(director, ensure_ascii=False),
                json.dumps(writers, ensure_ascii=False),
                json.dumps(actors, ensure_ascii=False),
                json.dumps(genres, ensure_ascii=False),
                nations,languages,
                json.dumps(dates, ensure_ascii=False),
                duration,
                json.dumps([title_], ensure_ascii=False),
                rating[0],rating_num[0],five[0],four[0],three[0],two[0],one[0],overviews))

            connection.commit()
            connection.rollback()
connection.close()

