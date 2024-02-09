import requests

request=requests.get('https://www.anyang.ac.kr/main/communication/notice.do')
html=request.text
print(html)