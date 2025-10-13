#import requests
#from lxml import html
#from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
import time

#url = 'https://s.weibo.com/weibo?q=%23%E6%B5%B7%E5%A4%96%E6%96%B0%E9%B2%9C%E4%BA%8B%23&page=1'

#headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
           #"Referer":"https://weibo.com/",
           #"cookie":"UOR=cn.bing.com,weibo.com,cn.bing.com; SINAGLOBAL=7716701566413.582.1759857724021; SCF=AljGpEeqzVYQX34n4HDT7qZcvl3TuVQNhUhgadpOCSj9z-8-0KJhDah5b8jdlCuYOIh7qEpMV0bOIMhgwosw_FQ.; SUB=_2A25F7zJIDeRhGeFM7VIX-SjFzD2IHXVmhcuArDV8PUNbmtAYLRPxkW9NQNLVPhkc4lPJnKFAks_CQF7zcPKGVJnE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWw_V-G0k2VOMq.cDbeIrQR5NHD95QNeoq7So.c1KMpWs4DqcjMi--ciK.Ni-27i--fi-isiKn0S0zcehq4So.NeBtt; ALF=02_1762840344; _s_tentry=weibo.com; Apache=277320769168.06793.1760249236723; ULV=1760249236724:2:2:1:277320769168.06793.1760249236723:1759857724023"}
#response = requests.get(url, headers=headers)
#tree = html.fromstring(response.text)

web = Edge()
web.get("https://weibo.com")
time.sleep(2)

cookies = [{
        'name': 'SUB',
        'value': '_2A25F7zJIDeRhGeFM7VIX-SjFzD2IHXVmhcuArDV8PUNbmtAYLRPxkW9NQNLVPhkc4lPJnKFAks_CQF7zcPKGVJnE',
        'domain': '.weibo.com'
    },
    {
        'name': 'SUBP',
        'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWw_V-G0k2VOMq.cDbeIrQR5NHD95QNeoq7So.c1KMpWs4DqcjMi--ciK.Ni-27i--fi-isiKn0S0zcehq4So.NeBtt',
        'domain': '.weibo.com'
    }]
for cookie in cookies:
    web.add_cookie(cookie)
web.refresh()
time.sleep(2)
web.get('https://s.weibo.com/weibo?q=%23%E6%B5%B7%E5%A4%96%E6%96%B0%E9%B2%9C%E4%BA%8B%23&page=1')
#带着cookie去就不用登录了

time.sleep(3)
cards = web.find_elements(By.XPATH,'//div[@action-type="feed_list_item" and @class="card-wrap"]')   #话题下的内容块
#print(len(cards))

def weibo(card):     #帖子信息
    author = card.find_element(By.XPATH, './/a[@class="name"]').text
    time_ = card.find_element(By.XPATH, './/div[@class="from"]/a').text.strip()  # .text返回的是字符串，xpath的/text()返回的是列表
    content_element = card.find_elements(By.XPATH,'.//p[@class="txt" and contains(@style,"display: none;")]')  # 需要展开的内容,要后边的标签但不要最后的收起两个字，xpath返回列表时最后一个元素是换行符，倒二是d，收起在倒三，用了selenium后可以直接去空格再切片
    if not content_element:
        content_text = card.find_element(By.XPATH, './/p[@class="txt"]').text.strip()  # 不需要展开的内容
    else:
        # content_text = card.find_element(By.XPATH,'.//p[@class="txt" and contains(@style,"display: none;")]').text.strip()   #Selenium 不能读取 style="display: none;" 的元素,xpath可以
        card.find_element(By.XPATH, './/a[@action-type="fl_unfold"]/i').click()
        time.sleep(5)
        content_text = card.find_element(By.XPATH, './/p[@class="txt" and @style=""]').text.strip()[:-3]
    # content_text = [text.strip() for text in content_text]   #清理空格换行符等  #用了selenium后这两行也不需要了
    # content_text = '\n'.join(content_text)

    style = '文字'
    if not card.find_elements(By.XPATH, './/div[@node-type="feed_list_media_prev"]'):
        pass
    else:
        if card.find_elements(By.XPATH, './/div[@node-type="feed_list_media_prev"]//video'):
            style += '+视频'
            content_text += '(video)' + card.find_element(By.XPATH,'.//div[@node-type="feed_list_media_prev"]//video').get_attribute('src')
        if card.find_elements(By.XPATH, './/div[@node-type="feed_list_media_prev"]//img'):
            style += '+图片'
            content_text += '(img)' + card.find_element(By.XPATH,'.//div[@node-type="feed_list_media_prev"]//img').get_attribute('src')

    # repost_num = card.xpath('.//i[@class="woo-font woo-font--retweet toolbar_icon"]/../following-sibling::text()[1]')[0].strip()  # 由于转发数和评论数的上一个兄弟节点长一样没办法定位，所以通过子节点定位父节点再找父节点的兄弟节点就是要的数字
    # comment_num = card.xpath('.//i[@class="woo-font woo-font--comment toolbar_icon"]/../following-sibling::text()[1]')[0].strip()
    repost_num = card.find_element(By.XPATH, './/div[@class="card-act"]//a[1]').text.strip()
    if repost_num == '转发':
        repost_num = 0
    comment_num = card.find_element(By.XPATH,'.//div[@class="card-act"]//a[@action-type="feed_list_comment"]').text.strip()
    if comment_num == '评论':
        comment_num = 0
    like_num = card.find_element(By.XPATH, './/span[@class="woo-like-count"]').text.strip()
    if like_num == '赞':
        like_num = 0
    print('帖子:', author, time_, content_text, style, repost_num, comment_num, like_num)


def one_comment_part(one_comment, one_comment_time, one_comment_ip):  # 需要跳转的评论和不需要跳转的评论有很多重合点，定义成一个方法就不用重复写了
    one_comment_ = one_comment.find_element(By.XPATH, './/div[@class="text"]').text.strip()  # 包含发布者和内容的一级评论模块们
    one_comment_author = one_comment_.split(':')[0]
    if len(one_comment_.split(':')) == 2:
        one_comment_content = one_comment_.split(':')[1]
    else:
        one_comment_content = ''
    if one_comment.find_elements(By.XPATH, './/div[@class="text"]/span/img'):
        one_comment_content += one_comment.find_element(By.XPATH, './/div[@class="text"]/span/img').get_attribute('title')  # 表情处理
    if one_comment.find_elements(By.XPATH, './/div[@class="con1 woo-box-item-flex"]/div[@class="u-col-6"]'):
        one_comment_img = one_comment.find_element(By.XPATH,'.//div[@class="con1 woo-box-item-flex"]/div[@class="u-col-6"]//img').get_attribute('src')  # 图片处理
        one_comment_content += one_comment_img
    print('一级评论:',one_comment_author, one_comment_content, one_comment_time, one_comment_ip)

for card in cards:
    weibo(card)

    #点击评论使其显示
    card.find_element(By.XPATH,'.//i[@class="woo-font woo-font--comment toolbar_icon"]').click()
    #print('已点击评论')
    time.sleep(2)

    y_n = card.find_elements(By.XPATH,'.//div[@class="card-more-a"]')
    if not y_n:
        if not card.find_elements(By.XPATH,'.//div[@class="card-review s-ptb10"]'):    #无评论的class="list"的div块不能展开
            print('无一级评论')
        #one_comments = card.find_elements(By.XPATH, './/div[@node-type="feed_list_commentList"]')  # 内容模块们
        one_comments = card.find_elements(By.XPATH, './/div[@class="card-review s-ptb10"]')   #一级评论模块们
        print(len(one_comments))
        for one_comment in one_comments:
            one_comment_time = one_comment.find_element(By.XPATH,'.//p[@class="from"]').text.strip()
            one_comment_ip = "无"    #评论太少进入不了详情页，无法获取ip
            one_comment_part(one_comment,one_comment_time, one_comment_ip)
    else:
        comment_link = card.find_element(By.XPATH, './/div[@class="card-more-a"]/a')
        web.execute_script("arguments[0].target = '_blank';", comment_link)  #另起一个标签页，不然不容易返回原来的页面
        comment_link.click()
        time.sleep(2)   #等待详情页加载
        web.switch_to.window(web.window_handles[-1])   #切换到详情页
        web.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #鼠标滚动，让评论都加载出来，不然只能读两条
        time.sleep(2)  # 等待页面加载新的评论
        one_comments = web.find_elements(By.XPATH,'.//div[@class="vue-recycle-scroller__item-view"]')  #一级评论模块们
        print(len(one_comments))
        for one_comment in one_comments:
            one_comment_time = one_comment.find_element(By.XPATH,'.//div[@class="info woo-box-flex woo-box-alignCenter woo-box-justifyBetween"]/div').text.split(' ')[0]  #去掉后半部分，不然就会得到两次ip
            one_comment_ip = one_comment.find_element(By.XPATH,'.//div[@class="info woo-box-flex woo-box-alignCenter woo-box-justifyBetween"]/div/span').text.strip()
            one_comment_part(one_comment,one_comment_time, one_comment_ip)
input()

