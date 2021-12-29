from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
from bs4 import BeautifulSoup

import requests
import pandas as pd
import numpy as np
import random
dataset_q = pd.read_csv('TOC_LineBot.csv')
current_answer = ''
answer_index = []
choice_answer = []
sum = 0

idiom_search = ''
idiom_search_url = ''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        global answer_index
        answer_index = []   # 確認每次返回menu都有清空
        return text.lower() == "主選單"

    def is_going_to_game1(self, event):
        text = event.message.text
        return text.lower() == "開始遊戲"
    
    def is_going_to_game2(self, event):
        text = event.message.text
        return check_answer(text)
    
    def is_going_to_game3(self, event):
        text = event.message.text
        return check_answer(text)
    
    def is_going_to_game4(self, event):
        text = event.message.text
        return check_answer(text)
    
    def is_going_to_score(self, event):
        text = event.message.text
        return check_answer(text)
    
    def is_going_to_answer(self, event):
        text = event.message.text
        return text.lower() == "查看答案"

    def is_going_to_search(self, event):
        text = event.message.text
        return text.lower() == "查詢成語"
    
    def is_going_to_get_idiom(self, event): # 利用爬蟲確定是否有此成語 另寫一個function
        text = event.message.text
        if text != "主選單":
            global idiom_search
            clear_search()  # 第一次取用進行清理
            idiom_search = text
        return search_result()  # 有查詢結果：True, 無：False
    
    def is_going_to_not_search(self, event):
        text = event.message.text
        if text != "主選單":
            global idiom_search
            idiom_search = text
        return not search_result()  # 無查詢結果：False, 有：True
    
    def is_going_to_mean(self, event):
        text = event.message.text
        return text.lower() == "釋義"
    
    def is_going_to_story(self, event):
        text = event.message.text
        return text.lower() == "典故說明"


    def on_enter_menu(self, event):
        title = '成語達人'
        text = '請選擇「開始遊戲」或「查詢成語」\n（遊戲共有4題）'
        btn = [
            MessageTemplateAction(
                label = '開始遊戲',
                text ='開始遊戲'
            ),
            MessageTemplateAction(
                label = '查詢成語',
                text ='查詢成語'
            ),
        ]
        url = 'https://cdn-icons.flaticon.com/png/512/3412/premium/3412644.png?token=exp=1640533159~hmac=249354ac87c22772317fbc7edb3389d6'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_game1(self, event):
        title, text, btn, url = question(1)
        send_button_message(event.reply_token, title, text, btn, url)
    
    def on_enter_game2(self, event):
        title, text, btn, url = question(2)
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_game3(self, event):
        title, text, btn, url = question(3)
        send_button_message(event.reply_token, title, text, btn, url)
    
    def on_enter_game4(self, event):
        title, text, btn, url = question(4)
        send_button_message(event.reply_token, title, text, btn, url)
    
    def on_enter_score(self, event):
        global sum
        title = '完成遊戲！'
        text = '測驗成績：' + str(sum)
        sum = 0
        btn = [
            MessageTemplateAction(
                label = '返回主選單',
                text = '主選單'
            ),
            MessageTemplateAction(
                label = '查看答案',
                text = '查看答案'
            ),
        ]
        url = 'https://cdn-icons-png.flaticon.com/512/2164/2164730.png'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def on_enter_answer(self, event):
        global answer_index
        title = '答案'
        text = ('A1：' + dataset_q.iloc[answer_index[0]][0] + '    ' +
                'A2：' + dataset_q.iloc[answer_index[1]][0] + '\n' +
                'A3：' + dataset_q.iloc[answer_index[2]][0] + '    ' +
                'A4：' + dataset_q.iloc[answer_index[3]][0] + '\n' +
                '點擊各成語查詢或選擇「返回主選單」')
        btn = [
            MessageTemplateAction(
                label = dataset_q.iloc[answer_index[0]][0],
                text = dataset_q.iloc[answer_index[0]][0]
            ),
            MessageTemplateAction(
                label = dataset_q.iloc[answer_index[1]][0],
                text = dataset_q.iloc[answer_index[1]][0]
            ),
            MessageTemplateAction(
                label = dataset_q.iloc[answer_index[2]][0],
                text = dataset_q.iloc[answer_index[2]][0]
            ),
            MessageTemplateAction(
                label = dataset_q.iloc[answer_index[3]][0],
                text = dataset_q.iloc[answer_index[3]][0]
            ),
        ]
        url = 'https://cdn-icons.flaticon.com/png/512/4919/premium/4919257.png?token=exp=1640707897~hmac=3a476f1cb818152c0299bff5fde9bf0b'
        send_button_message(event.reply_token, title, text, btn, url)
        answer_index = []
    
    def on_enter_search(self, event):
        title = '查詢成語'
        text = '請「輸入想查詢的成語」\n或點擊「返回主選單」'
        btn = [
            MessageTemplateAction(
                label = '返回主選單',
                text = '主選單'
            ),
        ]
        url = 'https://cdn-icons.flaticon.com/png/512/3157/premium/3157979.png?token=exp=1640708811~hmac=d29136492e74d80e2e62f239c3163da0'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def on_enter_get_idiom(self, event):
        global idiom_search
        title = idiom_search
        text = '請點選「釋義」或「典故說明」'
        btn = [
            MessageTemplateAction(
                label = '釋義',
                text = '釋義'
            ),
            MessageTemplateAction(
                label = '典故說明',
                text = '典故說明'
            ),
        ]
        url = 'https://cdn-icons.flaticon.com/png/512/3412/premium/3412644.png?token=exp=1640533159~hmac=249354ac87c22772317fbc7edb3389d6'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def on_enter_not_search(self, event):
        title = "查無此成語！"
        text = '請點擊「返回主選單」'
        btn = [
            MessageTemplateAction(
                label = '重新查詢',
                text = '查詢成語'
            ),
            MessageTemplateAction(
                label = '返回主選單',
                text = '主選單'
            ),
        ]
        url = 'https://cdn-icons-png.flaticon.com/512/6134/6134051.png'
        send_button_message(event.reply_token, title, text, btn, url)

    
    def on_enter_mean(self, event):
        request = requests.get(idiom_search_url)
        soup_next = BeautifulSoup(request.content, 'html.parser')

        mean_tag = soup_next.find("td", {"headers":"th_mean"})
        extra_tag = mean_tag.find_all("a")
        mean = mean_tag.text

        if extra_tag != None:   # 後面還有多餘的文字再處理
            for i in range (len(extra_tag)):
                extra = extra_tag[i].text
                if len(extra) != 0:
                    mean = mean.replace(extra, '')
            if mean.find('「」') != -1:
                mean = mean.replace('「」', '')
            if mean.find('、') != -1:
                mean = mean.replace('、', '')
            mean = mean.strip()
        
        text = '釋義：\n' + mean + '\n\n*請輸入「主選單」返回列表\n*輸入「典故說明」查看成語典故'
        send_text_message(event.reply_token, text)
    
    def on_enter_story(self, event):
        request = requests.get(idiom_search_url)
        soup_next = BeautifulSoup(request.content, 'html.parser')

        story_tag = soup_next.find("td", {"headers":"th_annotate"})
        if story_tag != None:
            story = story_tag.text
            text = '典故說明：\n' + story + '\n\n*輸入「主選單」返回列表\n*輸入「釋義」查看成語解釋'
            send_text_message(event.reply_token, text)
        else:
            title = "查無此成語典故說明！"
            text = '請點擊「查看釋義」或「重新查詢成語」或「返回主選單」'
            btn = [
                MessageTemplateAction(
                    label = '查看釋義',
                    text = '釋義'
                ),
                MessageTemplateAction(
                    label = '重新查詢成語',
                    text = '查詢成語'
                ),
                MessageTemplateAction(
                    label = '返回主選單',
                    text = '主選單'
                ),
            ]
            url = 'https://cdn-icons-png.flaticon.com/512/6134/6134051.png'
            send_button_message(event.reply_token, title, text, btn, url)
    

def question(num): # 出題目、回傳文字
    global current_answer
    global answer_index
    global choice_answer

    choice_index = random.sample(range(0, len(dataset_q.index)), 4)
    choice_answer = []

    which = np.random.randint(0, len(choice_index)) # 表示確切答案是選項中的第幾個
    index = choice_index[which]
    answer_index.append(index)

    for i in range (4): # 建立選項
        choice_answer.append((dataset_q.iloc[choice_index[i]][0])[1] + '、' + (dataset_q.iloc[choice_index[i]][0])[3])

    question = ('Q' + str(num) + '：' + (dataset_q.iloc[index][0])[0] + ' __ ' + (dataset_q.iloc[index][0])[2] + ' __ ' + '\n' +
                '語意：' + dataset_q.iloc[index][1])
    current_answer = choice_answer[which]
    title = '請選出正確答案'
    text = question
    btn = [
        MessageTemplateAction(
            label = choice_answer[0],
            text = choice_answer[0]
        ),
        MessageTemplateAction(
            label = choice_answer[1],
            text = choice_answer[1]
        ),
        MessageTemplateAction(
            label = choice_answer[2],
            text = choice_answer[2]
        ),
        MessageTemplateAction(
            label = choice_answer[3],
            text = choice_answer[3]
        ),
    ]
    if num == 1:
        url = 'https://cdn-icons.flaticon.com/png/512/3840/premium/3840653.png?token=exp=1640707119~hmac=02f8eb1e8c18ae9ef045778bd59d513d'
    elif num == 2:
        url = 'https://cdn-icons.flaticon.com/png/512/3840/premium/3840738.png?token=exp=1640707360~hmac=ff8455724ab0740d6a368a7c7d0f330e'
    elif num == 3:
        url = 'https://cdn-icons.flaticon.com/png/512/3840/premium/3840739.png?token=exp=1640707403~hmac=371d8b3822ed8b630e6d935406bb7dcb'
    elif num == 4:
        url = 'https://cdn-icons.flaticon.com/png/512/3840/premium/3840753.png?token=exp=1640707438~hmac=919ddfa0938aa86e29f0947351c8d5b7'
    else:
        url = 'https://cdn-icons.flaticon.com/png/512/3412/premium/3412644.png?token=exp=1640533159~hmac=249354ac87c22772317fbc7edb3389d6'
    return title, text, btn, url

def count_sum(text): # 計算得分
    global sum
    if text == current_answer:
        sum += 25   # 一題25分

def check_answer(text):
    global choice_answer
    for i in range (4): # 檢查選項
        if choice_answer[i] == text:
            count_sum(text)
            return True
    return False

def search_result():
    global idiom_search
    global idiom_search_url
    url = 'https://dict.idioms.moe.edu.tw/idiomList.jsp?idiom=' + idiom_search + '&qMd=0&qTp=1&qTp=2'
    request = requests.get(url)

    soup = BeautifulSoup(request.content, 'html.parser')
    elements = soup.find_all("div", {"role":"cell"})

    for element in elements:
        if element.a != None:
            idiom_search_url = "https://dict.idioms.moe.edu.tw/" + element.a['href']
            break
    if idiom_search_url == '' or (element.a.text != idiom_search):
        clear_search()
        return False
    return True

def clear_search():
    global idiom_search 
    global idiom_search_url
    idiom_search = ''
    idiom_search_url = ''