from re import findall, compile
from time import time, sleep
from json import loads
from random import choices
from base64 import b64encode, b64decode
from requests import Session, get, head, post
from urllib.parse import unquote
from os import execv
from sys import executable, argv
from hashlib import sha256
from threading import Thread
from PIL import Image
from io import BytesIO

config = {
    'cloudflare': 'kAMtbsTqP9nr2zH.dUqsGIlq60hFfRCsoy1WX.bPhiE-1669637072-0-150',
    'mode': 'views'
}

item_id = None
proxies = None  # experimental

endpoints = {
    "views": "c2VuZC9mb2xsb3dlcnNfdGlrdG9V",
    "hearts": "c2VuZE9nb2xsb3dlcnNfdGlrdG9r",
    "followers": "c2VuZF9mb2xsb3dlcnNfdGlrdG9r",
    "favorites": "c2VuZF9mb2xsb3dlcnNfdGlrdG9L",
    "shares": "c2VuZC9mb2xsb3dlcnNfdGlrdG9s",
}

__keys__ = {
    'key_1': None,
    'key_2': None
}

class livecounts:
    @staticmethod
    def video_info(video_id):
        headers = {
            'authority': 'tiktok.livecounts.io',
            'origin': 'https://livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers)
        return req.json()

    @staticmethod
    def link_to_id(video_link):
        return str(
            findall(r"(\d{18,19})", video_link)[0]
            if len(findall(r"(\d{18,19})", video_link)) == 1
            else findall(r"(\d{18,19})", head(video_link, allow_redirects=True, timeout=5).url)[0]
        )

def __decrypt__(data):
    a = unquote(data[::-1])
    return b64decode(a).decode()

def __format__(string):
    return "".join(dict.fromkeys(string))

def __init__(__session__):
    __html__ = str(__session__.get('http://zefoy.com').text).replace('&amp;', '&')
    captcha_token = None
    results = findall(r'name="([A-Za-z0-9]{31,32})">', __html__)
    if results:
        captcha_token = results[0]
    captcha_url = findall(r'img src="([^"]*)"', __html__)[0]
    sessid = __session__.cookies.get('PHPSESSID')
    return captcha_token, captcha_url, sessid

def __solve__(__session__, captcha_token, captcha_url):
    try:
        captcha_image = __session__.get('https://zefoy.com' + captcha_url).content
        response = __session__.post('https://captcha.xtekky.repl.co/', json={
            'captcha': b64encode(captcha_image).decode('utf-8'),
        })
        if response.json()['status_code'] == 0:
            captcha_answer = __format__(response.json()['captcha_answer'])
        else:
            image = Image.open(BytesIO(captcha_image))
            image.show()
            captcha_answer = input('Captcha > ')
        response = __session__.post('https://zefoy.com', data={
            "captcha_secure": captcha_answer,
            captcha_token: ""
        })
        __keys__["key_1"] = findall('(?<="))[a-z0-9]{16}', response.text)[0]
        return True
    except Exception as e:
        print(f'Error solving captcha: {e}')
        __solve__(__session__, captcha_token, captcha_url)

def __search__(__session__, __tiktok_link):
    try:
        req_token = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=16))
        sessionid = __session__.cookies.get('PHPSESSID')
        token = __keys__["key_1"]
        headers = {
            'authority': 'zefoy.com',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{req_token}',
            'cookie': f'PHPSESSID={sessionid}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        data = f'------WebKitFormBoundary{req_token}\r\nContent-Disposition: form-data; name="{token}"\r\n\r\n{__tiktok_link}\r\n------WebKitFormBoundary{req_token}--\r\n'
        __search_link = post(f'https://zefoy.com/{endpoints[config["mode"]]}', headers=headers, data=data)
        __search_link_response = __decrypt__(__search_link.content)
        if "Session expired" in __search_link_response:
            __session__.cookies['PHPSESSID'] = input('Session expired. Enter session ID > ')
            __search__(__session__, __tiktok_link)
        if 'Please try again later' in __search_link_response:
            sleep(60)
            __search__(__session__, __tiktok_link)
        __keys__['key_2'], _ = findall(r'name="(.*)" value="(.*)" hidden', __search_link_response)[0]
    except Exception as e:
        print(f'Error during search: {e}')

def __send__(__session__):
    headers = {
        'authority': 'zefoy.com',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    data = f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="{__keys__["key_2"]}"\r\n\r\n{item_id}\r\n------WebKitFormBoundary--\r\n'
    post(f'https://zefoy.com/{endpoints[config["mode"]]}', headers=headers, data=data)
    print('Request sent successfully.')
    sleep(5)

if __name__ == '__main__':
    with Session() as __session__:
        a, b, c = __init__(__session__)
        if __solve__(__session__, a, b):
            video_link = input('Video link > ')
            item_id = livecounts.link_to_id(video_link)
            while True:
                __search__(__session__, video_link)
                sleep(0.5)
                __send__(__session__)
                sleep(1)
