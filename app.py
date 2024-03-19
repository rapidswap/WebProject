from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import time
import os
import sys
import urllib.request
import json
import deepl

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

def ex_crawl_website():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='org_notice_db',
            user='root',
            password='net110'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query="SELECT title FROM org_notice"
            cursor.execute(query)
            existing_titles=[row[0] for row in cursor.fetchall()]
            resp = requests.get('https://www.anyang.ac.kr/main/communication/notice.do')
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            notice = soup.select('.b-top-box a')

            new_titles = []
            new_urls = []

            for i in notice:
                titles.append(i.text.replace('\t', '').replace('\n', ''))
                urls.append(i['href'])

                if title not in existing_titles:
                    new_titles.append(title)
                    new_urls.append(urls)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # 연결 닫기
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return new_titles, new_urls

def insert_to_org_database(titles):
    connection = None  # 변수 초기화
    try:
        #MYSQL에 연결
        connection = mysql.connector.connect(
            host='localhost',
            database='org_notice_db',
            user='root',
            password='net110'
        )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()

            # titles와 urls를 데이터베이스에 삽입
            for title, in titles:
                insert_query = f"INSERT INTO notice (title) VALUES ('{title}')"
                cursor.execute(insert_query)
                connection.commit()

            print("Records inserted successfully")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # 연결 닫기
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insert_to_database(titles, urls):
    connection = None  # 변수 초기화
    try:
        #MYSQL에 연결
        connection = mysql.connector.connect(
            host='localhost',
            database='notice_db',
            user='root',
            password='net110'
        )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()

            # titles와 urls를 데이터베이스에 삽입
            for title, url in zip(titles, urls):
                insert_query = f"INSERT INTO notice (title, url) VALUES ('{title}', '{url}')"
                cursor.execute(insert_query)
                connection.commit()

            print("Records inserted successfully")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # 연결 닫기
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
def fetch_from_database():
    try:
        # MySQL에 연결
        connection = mysql.connector.connect(
            host='localhost',
            database='notice_db',
            user='root',
            password='net110'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 데이터베이스에서 제목과 URL을 가져옴
            query = "SELECT title, url FROM notice"
            cursor.execute(query)
            results = cursor.fetchall()

            if results:  # 데이터가 존재하는 경우
                titles = [row[0] for row in results]
                urls = [row[1] for row in results]
                return titles, urls, True  # 데이터가 있음을 반환
            else:  # 데이터가 없는 경우
                return None, None, False  # 데이터가 없음을 반환

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None, None, False
    finally:
        # 연결 닫기
        if connection.is_connected():
            cursor.close()
            connection.close()
            
def check_duplicate_title(title):
    connection = None  # 변수 초기화
    try:
        # MySQL에 연결
        connection = mysql.connector.connect(
            host='localhost',
            database='notice_db',
            user='root',
            password='net110'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 데이터베이스에서 제목을 조회하여 중복 여부 확인
            query = "SELECT * FROM notice WHERE title = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()  # 중복된 제목이 없으면 None을 반환

            if result is None:
                return True  # 중복된 제목이 없음
            else:
                return False  # 중복된 제목이 있음

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return False  # 연결 오류 시에도 크롤링을 중단하도록 False 반환
    finally:
        # 연결 닫기
        if connection.is_connected():
            cursor.close()
            connection.close()
            
app = Flask(__name__)

@app.route('/')
def index():
    # save_titles, save_urls, data_exist = fetch_from_database()
    # if data_exist:
    #     translated_titles = []
    #     #안해도 되는 과정
    #     # for title in save_titles:
    #     #     auth_key="ecc2240c-cd14-45fa-995e-16eab245cffe:fx"
    #     #     tranlator=deepl.Translator(auth_key)
    #     #     message = title
    #     #     result = translator.translate_text(message, target_lang="EN-US")
    #     #     translated_titles.append(result.text)
    #     for title,url in zip(save_titles, save_urls):
    #         if check_duplicate_title(title):
    #             #중복된 내용은 크롤링 안하도록 해야함.
    #             titles, urls = crawl_website()
    #             for title in titles:
    #                 auth_key="ecc2240c-cd14-45fa-995e-16eab245cffe:fx"
    #                 translator=deepl.Translator(auth_key)
    #                 message = title
    #                 result = translator.translate_text(message, target_lang="EN-US")
    #                 translated_titles.append(result.text)
    #             insert_to_database(translated_titles,urls)

            

        translated_titles=[]
        titles, urls = crawl_website()
        for title in titles:
            auth_key="ecc2240c-cd14-45fa-995e-16eab245cffe:fx"
            translator=deepl.Translator(auth_key)
            message = title
            result = translator.translate_text(message, target_lang="EN-US")
            translated_titles.append(result.text)
        insert_to_database(translated_titles,urls)
        insert_to_org_database(titles)

        # # 공지사항 번역
            
    # # 8개의 공지사항만 선택
    view_titles = translated_titles[:8]
    view_urls = urls[:8]
    return render_template('index.html', translated_titles=translated_titles, urls=urls)

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
