#import requests
from lxml import html
import asyncio
import aiohttp   #替代同步的requests

#爬完一次之后就触发反爬了

MAX = asyncio.Semaphore(10)

async def single_spider(session,href):   #单个电影的爬取
    async with session.get(href) as response:
        text = await response.text()
        in_tree = html.fromstring(text)
        rank = in_tree.xpath('//*[@id="content"]/div[1]/span[1]/text()')
        title = in_tree.xpath('//*[@id="content"]/h1/span[1]/text()')
        year = in_tree.xpath('//*[@id="content"]/h1/span[2]/text()')[0][1:-1]
        director = in_tree.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        writers = in_tree.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
        actors = in_tree.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')   #？这对吗，这不太对吧
        genres = in_tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
        nations = in_tree.xpath('//*[@id="info"]/span[8]/following-sibling::text()[1]')
        language = in_tree.xpath('//*[@id="info"]/span[9]/following-sibling::text()[1]')
        dates = in_tree.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        duration = in_tree.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')
        title_ = in_tree.xpath('//*[@id="info"]/span[17]/following-sibling::text()[1]')
        rating = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        rating_num = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
        five = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]/text()')
        four = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]/text()')
        three = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]/text()')
        two = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]/text()')
        one = in_tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]/text()')
        overviews = in_tree.xpath('//*[@id="link-report-intra"]/span[2]/text()')
        if not overviews:
            overviews = in_tree.xpath('//*[@id="link-report-intra"]//span[@property="v:summary"]/text()')
        overviews = [overview.strip() for overview in overviews]
        overviews = '\n'.join(overviews)

        print(rank,title, year, director, writers, actors, genres,nations,language,dates,duration,title_,rating, rating_num, five, four, three, two, one, overviews)
        print('爬取完成')

async def page(session, i):  #并发抓取每一页并对得到的25个hrefs并发请求
    url = f"https://movie.douban.com/top250?start={i}"
    async with MAX:  #限制分页请求的并发量
        async with session.get(url) as resp:
            tree = html.fromstring(await resp.text())
            hrefs = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/@href')
            tasks = []
            for href in hrefs:
                tasks.append(single_spider(session, href))
            await asyncio.gather(*tasks)

async def main():
    async with aiohttp.ClientSession(headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
                                              "cookie":'bid=gzTQn8GZ8qU; ll="118099"; _vwo_uuid_v2=D1C194E985E32E4AEF883E62487ECD7EA|435f623e9a70ed9cab6685306522e1df; dbcl2="291739765:WpskoGoISAk"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.29173; ck=Spuv; __utma=30149280.765453619.1747730124.1760179855.1760445624.17; __utmc=30149280; __utmz=30149280.1760445624.17.3.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.2.765453619.1747730124; _gid=GA1.2.1488317640.1760445665; _gat=1; _ga_PRH9EWN86K=GS2.2.s1760445667$o1$g0$t1760445667$j60$l0$h0; __utmt=1; __utmb=30149280.2.10.1760445624'}) as session:
        tasks = []
        for i in range(0, 250, 25):
            tasks.append(page(session, i))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())