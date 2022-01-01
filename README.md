# 成語達人
> TOC Project 2021 - Linebot 實作
- Bot Basic ID: @403jptbv

## 構想
「成語達人」旨在讓使用者透過填空遊戲學習成語，並提供查詢成語的功能進一步進行學習，架構主要分成兩大部分：「成語遊戲」、「成語查詢」，「成語遊戲」的部分一次有四題，完成後即會看見自己的成績，也可以在完成後查看所有答案，也可以進一步查詢答案的意思、典故（和成語查詢部分相通）；「成語查詢」部分則是可以自行鍵入成語進行查詢，使用爬蟲取得該成語釋義與典故說明。
- 資料來源：[教育部成語典](https://dict.idioms.moe.edu.tw/search.jsp?webMd=2&la=0)

## 使用示範
- 輸入「主選單」進入列表
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/1.jpeg" img width="450"/>

- 點擊開始遊戲進入「成語填空遊戲」（共4題）
- 第1題
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/2.jpeg" img width="450"/>

- 第2題
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/3.jpeg" img width="450"/>

- 第3題
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/4.jpeg" img width="450"/>
                                                                                           
- 第4題
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/5.jpeg" img width="450"/>

- 完成後即可查看成績，下一步可以選擇「返回主選單」或「查看答案」
- 點擊「查看答案」後即可查看四題題目的答案，並且進一步查詢成語  
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/7.jpeg" img width="450"/>

- 點擊成語可查詢詳情（釋義、典故說明）
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/8.jpeg" img width="450"/>
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/9.jpeg" img width="450"/>

- 回到主選單，換選擇「查詢成語」
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/10.jpeg" img width="450"/>

- 可選擇「返回主選單」，或輸入欲查詢的成語，可查看釋義與典故說明
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/11.jpeg" img width="450"/>
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/12.jpeg" img width="450"/>

### 其他情形
- 若查詢成語時查無資料，則顯示「查無此成語！」，並可以選擇「重新查詢」或「返回主選單」
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/14.jpeg" img width="450"/>

- 若查詢成語典故時無資料，則顯示「查無此成語典故說明！」，並可以選擇「查看釋義」、「重新查詢成語」或「返回主選單」
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/img/16.jpeg" img width="450"/>

## FSM結構圖
<img src="https://github.com/catherine1606/TOC-LineBot/blob/main/fsm.png">

- user: 初始狀態
- menu: 功能列表
- game1: 遊戲第1題
- game2: 遊戲第2題
- game3: 遊戲第3題
- game4: 遊戲第4題
- score: 呈現遊戲成績
- answer: 呈現遊戲答案
- search: 輸入欲查詢成語（或返回主選單）
- not_search: 查無此成語的狀態
- get_idiom: 成功查詢成語，詢問使用者欲查看之內容（釋義、典故說明）
- mean: 呈現成語釋義
- story: 呈現成語典故說明

## 使用教學
1. 使用`pipenv`
```
pip3 install pipenv
pipenv --three
pipenv install
pipenv shell
```

2. 創立`.env`，並填入:
- LINE_CHANNEL_SECRET
- LINE_CHANNEL_ACCESS_TOKEN
<br>

### Local 執行
3. 安裝`ngrok`(MAC)
```
brew install ngrok
```

4. 執行`app.py`
```
python3 app.py
```

5. 執行`ngrok`
```
ngrok http 8000
```
(看執行`app.py`後的`port number`)

6. 將網址填入 **Line Bot webhook URL**

7. 打開 **Line** 使用「成語達人」！
<br>

### 部署至Heroku
8. 創建 **Heroku app**

9. **Push code**
```
# 登入Heroku
heroku login

# 初始化git
git config --global user.name "你的名字"
git config --global user.email 你的信箱
git init


# 連接資料夾與Heroku
heroku git:remote -a {HEROKU_APP_NAME}


# Push Code
git add .
git commit -m "Add code"
git push -f heroku master
```

10. 將 **Heroku** 網址填入 **Line Bot webhook URL**
```
{HEROKU_APP_NAME}.herokuapp.com/callback
```

11. 打開 **Line** 使用「成語達人」！

---

### 問題
- 使用 python3.9 遇到 pygraphviz 無法正常使用的問題 -> 改為使用 python3.6
- pygraphviz 的 Heroku 安裝問題
```
heroku buildpacks:set heroku/python
heroku buildpacks:add --index 1 heroku-community/apt
```

### 資料來源 & 參考資料
- [教育部成語典](https://dict.idioms.moe.edu.tw/search.jsp?webMd=2&la=0)
- [flaticon](https://www.flaticon.com)
- TOC 課程簡報（含範例程式）
- [Line Bot 教學](https://github.com/yaoandy107/line-bot-tutorial)
- [Pipenv 更簡單、更快速的 Python 套件管理工具](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4)
