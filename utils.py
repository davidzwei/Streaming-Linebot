import os
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
import requests
from bs4 import BeautifulSoup 
import time
import json
import re
import numpy as np
import pandas as pd
from datetime import date
from opencc import OpenCC

from linebot.models import (
    ConfirmTemplate, 
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    CarouselTemplate,
    CarouselColumn,URIAction,
    PostbackAction,
    PostbackTemplateAction,
    MessageAction
)

config = configparser.ConfigParser()
config.read("config.ini")
# channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_access_token = config['line_bot']['Channel_Access_Token']
id = config['line_bot']['User_id']

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TextSendMessage(text=text))
    return "OK"

def send_text_button(reply_token, text):
    print('i am in send_text button')
    line_bot_api = LineBotApi(channel_access_token)
    
    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2875643522.webp',
                    title='戲劇',
                    text='請點選以下功能',
                    actions=[
                        MessageTemplateAction(
                            label='熱門戲劇',
                            text='熱門戲劇'
                        ),
                        MessageTemplateAction(
                            label='熱門綜藝',
                            text='熱門綜藝'
                        ),
                        MessageTemplateAction(
                            label='各國熱門戲劇',
                            text='各國熱門戲劇'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://p2.bahamut.com.tw/B/ACG/c/55/0000072755.JPG',
                    title='動漫',
                    text='請點選以下功能',
                    actions=[
                        MessageTemplateAction(
                            label='最近新作',
                            text='最近新作'
                        ),
                        MessageTemplateAction(
                            label='本月熱門',
                            text='本月熱門'
                        ),
                        MessageTemplateAction(
                            label='搜尋動畫',
                            text='搜尋動畫'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://movies.yahoo.com.tw/i/o/production/movies/March2022/IPaDhsb4uOa5QvdXGh3G-1080x1601.jpg',
                    title='Yahoo電影',
                    text='請選擇以下功能',
                    actions=[
                        MessageTemplateAction(
                            label='台灣票房',
                            text='台灣票房'
                        ),
                        MessageTemplateAction(
                            label='美國票房',
                            text='美國票房'
                        ),
                        MessageTemplateAction(
                            label='本周上映',
                            text='本周上映'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token,Carousel_template)
    return "OK"

def send_text_drama_button(reply_token):
    print('i am in send_text button')
    line_bot_api = LineBotApi(channel_access_token)

    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2586800409.jpg',
                    title='戲劇',
                    text='請點選以下功能',
                    actions=[
                        MessageTemplateAction(
                            label='熱門日劇',
                            text='熱門日劇'
                        ),
                        MessageTemplateAction(
                            label='熱門韓劇',
                            text='熱門韓劇'
                        ),
                        MessageTemplateAction(
                            label='熱門陸劇',
                            text='熱門陸劇'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2535085957.jpg',
                    title='戲劇',
                    text='請點選以下功能',
                    actions=[
                        MessageTemplateAction(
                            label='熱門美劇',
                            text='熱門美劇'
                        ),
                        MessageTemplateAction(
                            label='熱門英劇',
                            text='熱門英劇'
                        ),
                        MessageTemplateAction(
                            label='熱門港劇',
                            text='熱門港劇'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token,Carousel_template)
    return "OK"

def send_hot(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    title = []
    images = []
    view = []
    scores = []
    types = []
    times = []
    address = []

    url = "https://ani.gamer.com.tw/animeList.php?c=All&sort=2"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"})
    soup = BeautifulSoup(r.text,"html.parser")
    theme = soup.find('div', 'theme-list-block')
    list1 = theme.find_all('a', 'theme-list-main')
    infoblock = theme.find_all('p', 'theme-name')

    # title
    for i in infoblock:
        x = i.getText()
        title.append(x)
    #images
    for i in list1:
        part = i.find('img')
        images.append(part.get("src"))
    # total views
    for b in list1:
        view.append(b.find('p').getText())
    # address
    for a in list1:
        address.append("https://ani.gamer.com.tw/" + a['href'])
        
    for des_url in address:
        # print(des_url)
        r = requests.get(des_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"})
        soup1 = BeautifulSoup(r.text,"html.parser")

        # scores 
        score = soup1.find('div', 'score-overall-number').getText()
        scores.append("評分 " + score)

        #types
        datatype = soup1.find('ul', 'data_type')
        category = datatype.find('li').getText()
        x = datatype.find('li').getText()
        x = x[4:]
        types.append("作品類型 " + x)
        
        # times
        time = soup1.find('div', 'anime_info_detail')
        time = time.find('p').text
        time = time[5:15]
        times.append(time)
   
    carousel_group = []
    details = []
    for i in range(10):
        detail = times[i] + " " + scores[i] +"\n" + types[i] + "\n" + "月觀看數 " + view[i] + "\n"
        details.append(detail)
        carousel_data = CarouselColumn(
            thumbnail_image_url = images[i],
            title = title[i],
            text = details[i],
            actions=[
                URIAction(label='詳細內容', uri = address[i]),
            ]
        )
        carousel_group.append(carousel_data)
    
    buttons_template_message = TemplateSendMessage(
        alt_text='CarouselTemplate',
        template=CarouselTemplate(
            columns=carousel_group,
            image_size='cover'
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template_message)
    return "OK"


def send_new(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    title = []
    images = []
    view = []
    scores = []
    types = []
    times = []
    address = []
    url = "https://ani.gamer.com.tw/animeList.php"
    print(url)
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"})
    soup = BeautifulSoup(r.text,"html.parser")
    theme = soup.find('div', 'theme-list-block')
    list1 = theme.find_all('a', 'theme-list-main')
    infoblock = theme.find_all('p', 'theme-name')

    # title
    for i in infoblock:
        x = i.getText()
        title.append(x)
    #images
    for i in list1:
        part = i.find('img')
        images.append(part.get("src"))
        
    # total views
    for b in list1:
        view.append(b.find('p').getText())
    # address
    for a in list1:
        address.append("https://ani.gamer.com.tw/" + a['href'])
        
    for des_url in address:
        r = requests.get(des_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"})
        soup1 = BeautifulSoup(r.text,"html.parser")

        # scores 
        score = soup1.find('div', 'score-overall-number').getText()
        scores.append("評分 " + score)

        #types
        datatype = soup1.find('ul', 'data_type')
        category = datatype.find('li').getText()
        x = datatype.find('li').getText()
        x = x[4:]
        types.append("作品類型 " + x)
        
        # times
        time = soup1.find('div', 'anime_info_detail')
        time = time.find('p').text
        time = time[5:15]
        times.append(time)
   
    carousel_group = []
    details = []
    for i in range(10):
        detail = times[i] +"\t\t" + scores[i] + "\n" + types[i] + "\n"  + "總觀看數 " + view[i] + "\n"
        details.append(detail)
        carousel_data = CarouselColumn(
            thumbnail_image_url = images[i],
            title = title[i],
            text = details[i],
            actions=[
                URIAction(label='詳細內容', uri = address[i]),
            ]
        )
        carousel_group.append(carousel_data)
    
    buttons_template_message = TemplateSendMessage(
        alt_text='CarouselTemplate',
        template=CarouselTemplate(
            columns=carousel_group,
            image_size='cover'
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template_message)
    return "OK"

# search name
def send_search(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    # line_bot_api.push_message(reply_token, TextSendMessage(text=text))
    name = "You want to search " + text
    print(type(text))
    print(name)
    # list of all details
    title = []
    images = []
    view = []
    scores = []
    types = []
    times = []
    address = []
    url = "https://ani.gamer.com.tw/search.php?keyword=" + text
    # url2 = "https://ani.gamer.com.tw/search.php?keyword=" + text
    print(url)
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"})
    
    soup = BeautifulSoup(r.text,"html.parser")
    theme = soup.find('div', 'theme-list-block')
    list1 = theme.find_all('a', 'theme-list-main')
    # print(list1)
    # print(len)
    if len(list1) == 0:
        error_msg = "找不到此動畫，請輸入其他動畫名稱"
        line_bot_api.push_message(id, TextSendMessage(text = error_msg))
        return "OK"
    else:
        infoblock = theme.find_all('p', 'theme-name')

        # title
        for i in infoblock:
            x = i.getText()
            title.append(x)
        #images
        for i in list1:
            part = i.find('img')
            images.append(part.get("src"))
            
        # total views
        for b in list1:
            view.append(b.find('p').getText())
        # address
        for a in list1:
            address.append("https://ani.gamer.com.tw/" + a['href'])
            
        for des_url in address:
            # print(des_url)
            r = requests.get(des_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"})
            soup1 = BeautifulSoup(r.text,"html.parser")
            # scores 
            score = soup1.find('div', 'score-overall-number').getText()
            scores.append("評分 " + score)

            #types
            datatype = soup1.find('ul', 'data_type')
            category = datatype.find('li').getText()
            x = datatype.find('li').getText()
            x = x[4:]
            types.append("作品類型 " + x)
            
            # times
            time = soup1.find('div', 'anime_info_detail')
            time = time.find('p').text
            time = time[5:15]
            times.append(time)
    
        carousel_group = []
        details = []
        num = min(len(list1), 10)
        for i in range(num):
            detail = times[i] + " " + scores[i] + "\n" + types[i] + "\n" + "總觀看數 " + view[i] + "\n"
            details.append(detail)
            carousel_data = CarouselColumn(
                thumbnail_image_url = images[i],
                title = title[i],
                text = details[i],
                actions=[
                    URIAction(label='詳細內容', uri = address[i]),
                ]
            )
            carousel_group.append(carousel_data)
        
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=CarouselTemplate(
                columns=carousel_group,
                image_size='cover'
            )
        )
        line_bot_api.reply_message(reply_token, buttons_template_message)
        return "OK"

# send type of drama
def send_drama(reply_token, text):
    print('i am in send drama')
    line_bot_api = LineBotApi(channel_access_token)
    if text == 'hot':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20'
    elif text == 'china':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=国产剧&sort=recommend&page_limit=20'
    elif text == 'japan':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=日剧&sort=recommend&page_limit=20'
    elif text == 'korea':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=韩剧&sort=recommend&page_limit=20'
    elif text == 'america':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=20'
    elif text == 'england':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=英剧&sort=recommend&page_limit=20'
    elif text == 'hongkong':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=港剧&sort=recommend&page_limit=20'
    elif text == 'entertain':
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=综艺&sort=recommend&page_limit=20'
    

    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    json_str = r.content.decode()
    dict_ret = json.loads(json_str)
    content_list = dict_ret["subjects"]
    content_list = content_list[:10]
    cc = OpenCC('s2t')
    
    for i in content_list:
        text = i['title']
        text = cc.convert(text)
        i['title'] = text
        if i['rate'] == '':
            i['rate'] = '暫無評分'

    carousel_group = []
    details = []
    for i in range(10):
        detail = '評分:'+ content_list[i]['rate'] + "\n"
        details.append(detail)
        carousel_data = CarouselColumn(
            thumbnail_image_url = content_list[i]['cover'],
            title = content_list[i]['title'],
            text = details[i],
            actions=[
                URIAction(label='詳細內容', uri = content_list[i]['url']),
            ]
        )
        carousel_group.append(carousel_data)
    
    buttons_template_message = TemplateSendMessage(
        alt_text = 'CarouselTemplate',
        template = CarouselTemplate(
            columns = carousel_group,
            image_size = 'cover'
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template_message)
    return "OK"


# send new movie
def send_new_movie(reply_token):
    print('i am in send new movie')
    line_bot_api = LineBotApi(channel_access_token)

    url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
    response = requests.get(url=url) 
    soup = BeautifulSoup(response.text, 'lxml')
    
    imgs = []
    info_items = soup.find_all('div', 'release_info')
    names = []
    english_names = []
    dates = []
    levels = []
    address = []
    imdbs = []
    times = []

    for item in info_items:
        name = item.find('div', 'release_movie_name').a.text.strip()
        names.append(name)
        english_name = item.find('div', 'en').a.text.strip()
        english_names.append(english_name)
        release_time = item.find('div', 'release_movie_time').text.split('：')[-1].strip()
        dates.append(release_time)
        level = item.find('div', 'leveltext').span.text.strip()
        levels.append(level)
                
    fotos = soup.find_all('div', 'release_foto')

    for i in fotos:
        img = i.find('img').get('data-src')
        imgs.append(i.find('img').get('data-src'))
        address.append(i.a.get('href'))
        
    for i in address:
        response2 = requests.get(url=i)
        soup2 = BeautifulSoup(response2.text, 'lxml')
        table2 = soup2.find('div', 'movie_intro_info_r')
        attr = table2.find_all('span')
        imdbs.append(attr[3].text)
        
        time = attr[1].text
        time = time.split('：')[1]
        times.append(time)

    # make carousal button
    carousel_group = []
    details = []

    for i in range(8):
        detail = dates[i]
        carousel_data = CarouselColumn(
            thumbnail_image_url = imgs[i],
            title = names[i],
            text = detail,
            actions=[
                URIAction(label='詳細內容', uri = address[i]),
            ]
        )
        carousel_group.append(carousel_data)
    
    buttons_template_message = TemplateSendMessage(
        alt_text = 'CarouselTemplate',
        template = CarouselTemplate(
            columns = carousel_group,
            image_size = 'cover'
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template_message)
    return "OK"

# send_usa_hot_movie 美國票房
def send_usa_hot_movie(reply_token):
    print('i am in send drama')
    line_bot_api = LineBotApi(channel_access_token)
    url2 = 'https://movies.yahoo.com.tw/chart.html?cate=us'
    response = requests.get(url=url2)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    names = []
    english_names = []
    dates = []
    levels = []
    address = []
    imdbs = []
    times = []
    imgs = []

    movies = soup.find('div', 'rank_list table rankstyle1')
    movies_list = movies.find_all('div', 'tr')

    del(movies_list[0])
    # movies_list = movies_list[:5]

    address.clear()
    for i in movies_list:
        try:
            tmp = i.find('a').get('href')
        except Exception as ee:
            print('cannot find address')
        if(tmp != ""):
            address.append(tmp)
    
    # print('len of address : ' + len(address))
    address = list(dict.fromkeys(address))
    print(len(address))
    
    for i in address:
        response2 = requests.get(url=i)
        soup2 = BeautifulSoup(response2.text, 'lxml')
        # names
        table = soup2.find('div', 'movie_intro_info_r')
        name = table.find('h1').text
        names.append(name)
        english_name = table.find('h3').text
        english_names.append(english_name)
        # img
        table = soup2.find('div', 'movie_intro_info_l')
        img = table.find('img').get('src')
        imgs.append(img)
        # imdb
        table2 = soup2.find('div', 'movie_intro_info_r')
        attr = table2.find_all('span')
        imdb = attr[3].text
        if imdb[0] == 'I':
            imdbs.append(imdb)
        else:
            imdbs.append('no imdb')
        time = attr[1].text
        time = time.split('：')[1]
        times.append(time)
        
        dates.append(attr[0].text)

    # make button
    carousel_group = []
    details = []
    for i in range(5):
        detail = dates[i] + '\n' + imdbs[i] 
        carousel_data = CarouselColumn(
            thumbnail_image_url = imgs[i],
            title = names[i],
            text = detail,
            actions=[
                URIAction(label='詳細內容', uri = address[i]),
            ]
        )
        carousel_group.append(carousel_data)
      
    buttons_template_message = TemplateSendMessage(
        alt_text = 'CarouselTemplate',
        template = CarouselTemplate(
            columns = carousel_group,
            image_size = 'cover'
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template_message)
    return "OK"

# send_taiwan_hot_movie 台灣票房
def send_taiwan_hot_movie(reply_token):
    print('i am in send drama')
    line_bot_api = LineBotApi(channel_access_token)
    
    url = 'https://movies.yahoo.com.tw/chart.html'
    response = requests.get(url=url)
    
    soup = BeautifulSoup(response.text, 'lxml')

    names = []
    english_names = []
    dates = []
    levels = []
    address = []
    imdbs = []
    times = []
    imgs = []

    movies = soup.find('div', 'rank_list table rankstyle1')
    movies_list = movies.find_all('div', 'tr')
    del(movies_list[0])
    movies_list = movies_list[:10]

    for i in movies_list:
        address.append(i.find('a').get('href'))
    
    for i in address:
        response2 = requests.get(url=i)
        soup2 = BeautifulSoup(response2.text, 'lxml')
        # names
        table = soup2.find('div', 'movie_intro_info_r')
        name = table.find('h1').text
        names.append(name)
    
        english_name = table.find('h3').text
        english_names.append(english_name)
        # img
        table = soup2.find('div', 'movie_intro_info_l')
        img = table.find('img').get('src')
        imgs.append(img)
        # imdb
        table2 = soup2.find('div', 'movie_intro_info_r')
        attr = table2.find_all('span')
        imdb = attr[3].text
        if imdb[0] == 'I':
            imdbs.append(imdb)
        else:
            imdbs.append('no imdb')
        time = attr[1].text
        time = time.split('：')[1]
        times.append(time)
        
        dates.append(attr[0].text)

    carousel_group = []
    details = []
    for i in range(10):
        detail = dates[i] + '\n' + imdbs[i] 
        carousel_data = CarouselColumn(
            thumbnail_image_url = imgs[i],
            title = names[i],
            text = detail,
            actions=[
                URIAction(label='詳細內容', uri = address[i]),
            ]
        )
        carousel_group.append(carousel_data)
    
    buttons_template_message = TemplateSendMessage(
        alt_text = 'CarouselTemplate',
        template = CarouselTemplate(
            columns = carousel_group,
            image_size = 'cover'
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template_message)
    return "OK"

def send_back(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TemplateSendMessage(
        alt_text='ConfirmTemplate',
        template=ConfirmTemplate(
            text='回到首頁? 回前一步?',
            actions=[
                MessageAction(
                    label='回到首頁',
                    text='回到首頁'
                ),
                MessageAction(
                    label='回前一步',
                    text='回前一步'
                )
            ]
        )
    ))
    return "OK"