from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import urllib.request
import json

def crawl_website():
    resp = requests.get('https://www.anyang.ac.kr/main/communication/notice.do')
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    notice = soup.select('.b-top-box a')

    titles = []
    urls = []

    for i in notice:
        titles.append(i.text.replace('\t', '').replace('\n', ''))
        urls.append(i['href'])

    return titles, urls

    

app = Flask(__name__)

@app.route('/')
def index():
    titles, urls = crawl_website()

    # # 8개의 공지사항만 선택
    titles = titles[:8]
    urls = urls[:8]

    # # 네이버 Papago NMT API 사용을 위한 정보
    # client_id = 'h79SZaDW5H6jULO4HUkT'
    # client_secret = 'gAzWayzwTu'

    # # 공지사항 번역
    # translated_titles = []
    # for title in titles:
    #     enc_text = urllib.parse.quote(title)
    #     data = f"source=ko&target=en&text={enc_text}"
    #     url = "https://openapi.naver.com/v1/papago/n2mt"

    #     # HTTP 요청 설정
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id", client_id)
    #     request.add_header("X-Naver-Client-Secret", client_secret)

    #     # 데이터 전송 및 응답 수신
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()

    #     if rescode == 200:
    #         response_body = response.read()
    #         result_json = json.loads(response_body.decode('utf-8'))

    #         # 번역된 텍스트 추출
    #         translated_text = result_json['message']['result']['translatedText']
    #         translated_titles.append(translated_text)
    #     else:
    #         translated_titles.append("Error Code:" + str(rescode)) 

    # HTML 템플릿에 전달
    # return render_template('index.html', translated_titles=translated_titles, urls=urls)
    return render_template('index.html', translated_titles=titles, urls=urls)
@app.route('/objectives')
def objectives():
    return render_template('objectives.html')

@app.route('/Notice')
def Notice():
    titles, urls = crawl_website()
        # 네이버 Papago NMT API 사용을 위한 정보
    # client_id = 'h79SZaDW5H6jULO4HUkT'
    # client_secret = 'gAzWayzwTu'

    # translated_titles = []

    # for title in titles:
    #     encText = urllib.parse.quote(title)
    #     data = "source=ko&target=en&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"

    #     # HTTP 요청 설정
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id", client_id)
    #     request.add_header("X-Naver-Client-Secret", client_secret)

    #     # 데이터 전송 및 응답 수신
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()

    #     if rescode == 200:
    #         response_body = response.read()
    #         result_json = json.loads(response_body.decode('utf-8'))

    #         # 번역된 텍스트 추출
    #         translated_text = result_json['message']['result']['translatedText']
    #         translated_titles.append(translated_text)
    #     else:
    #         translated_titles.append("Error Code:" + str(rescode))

    # HTML 템플릿에 전달
    return render_template('Notice.html', titles=titles, urls=urls)

@app.route('/graduateschool')
def graduateschool():
    return render_template('graduateschool.html')

def main():
    while True:
        crawl_website()
        time.sleep(3600)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    main()
