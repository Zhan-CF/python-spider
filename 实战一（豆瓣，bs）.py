from bs4 import BeautifulSoup
import requests
import csv

with open('豆瓣top250.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['排名','名字','年份','导演','编剧','主演','类型','制片国家','语言','上映日期','片长','又名','评分','评分人数','五星占比','四星占比','三星占比','二星占比','一星占比','简介'])
    for i in range(0,250,25):
        url = "https://movie.douban.com/top250?start="+str(i)
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        pics = soup.find('ol', class_='grid_view').find_all('div', class_='pic')
        #hrefs = []
        for pic in pics:
            href = pic.find('a')['href']
            # hrefs.append(href)
            in_response = requests.get(href, headers=headers)
            in_soup = BeautifulSoup(in_response.text, 'html.parser')
            rank = in_soup.find('span', class_='top250-no').text
            title = in_soup.find('span', property="v:itemreviewed").text
            year = in_soup.find('span', class_="year").text

            attrs = in_soup.find_all('span', class_='attrs')  # 导演编剧和演员的标签及属性都是一样的，只好全读了再索引
            director = attrs[0].text
            writers = attrs[1].text.replace(' / ',',')
            actors = attrs[2].text.replace(' / ',',')

            genres_ = in_soup.find_all('span', property="v:genre")
            genres = []
            for genre in genres_:
                genres.append(genre.text)
            genres = ','.join(genres)

            nations = in_soup.find('span', class_='pl', string='制片国家/地区:').next_sibling.replace(' / ',',')
            language = in_soup.find('span', class_='pl', string='语言:').next_sibling.replace(' / ',',')

            dates_ = in_soup.find_all('span', property="v:initialReleaseDate")
            dates = []
            for date in dates_:
                dates.append(date.text)
            dates = ','.join(dates)

            duration = in_soup.find('span', property="v:runtime").text

            title_ = in_soup.find('span', class_='pl', string='又名:')
            if title_:
                title_ = in_soup.find('span', class_='pl', string='又名:').next_sibling.replace(' / ',',')
            else:
                title_ = '无'
            rating = in_soup.find('strong', class_='ll rating_num', property="v:average").text
            rating_num = in_soup.find('span', property="v:votes").text

            pers_ = in_soup.find_all('span', class_="rating_per")
            pers = []
            for per in pers_:
                pers.append(per.text)

            #overview = in_soup.find('span', class_="pl",string='©豆瓣').find_previous_sibling().text
            # 有的电影简介最后可能是JavaScript动态加载的(除了肖申克，大概翻了翻，第19部也得手动展开)，'©豆瓣'这个节点的上一个兄弟节点，不论是不是动态加载都是完整简介
            # 好吧，有的电影竟然没'©豆瓣'部分，这东西意思是版权属于豆瓣

            overview = in_soup.find('span', class_='all hidden')   #这个确实是完整简介，但是大多数电影是没有这部分的
            if not overview:
                overview = in_soup.find('span',property="v:summary").get_text(separator='\n',strip=True)   #简介太乱了，找deepseek问了get_text()的用法
            else:
                overview = overview.get_text(separator='\n',strip=True)

            print(rank,title, year, director, writers, actors, genres, nations, language, dates, duration, title_, rating,
                  rating_num, pers, overview)
            writer.writerow([rank,title, year, director, writers, actors, genres, nations, language, dates, duration, title_, rating,
                  rating_num, pers[0],pers[1],pers[2],pers[3],pers[4], overview])

