from re import findall
from io import BytesIO
from PIL import Image
from time import sleep, time
from base64 import b64decode
from random import choices
from string import ascii_letters, digits
from requests import Session, post
from datetime import datetime
from urllib.parse import unquote, quote


def fmt(string) -> str:
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO __main__ -> {string}"


def decode(text: str) -> str:
    return b64decode(unquote(text[::-1])).decode()


def get_client() -> Session:
    client = Session()
    client.headers = {
        'authority': 'zefoy.com',
        'origin': 'https://zefoy.com',
        'cp-extension-installed': 'Yes',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    return client


def solve_captcha(client: Session) -> str:
    try:
        html = client.get('https://zefoy.com').text.replace('&amp;', '&')

        captcha_token = findall(r'<input type="hidden" name="(.*)">', html)[0]
        captcha_url = findall(r'img src="([^"]*)"', html)[0]
        captcha_token_v2 = findall(r'type="text" maxlength="50" name="(.*)" oninput="this.value', html)[0]

        print(fmt(f'captcha_token: {captcha_token}'))
        print(fmt(f'captcha_url: {captcha_url}'))

        captcha_image = client.get('https://zefoy.com' + captcha_url).content
        image = Image.open(BytesIO(captcha_image))
        image.show()

        captcha_answer = input('Solve captcha: ')

        response = post('https://zefoy.com', headers={
            'authority': 'zefoy.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': client.headers['user-agent'],
        }, data={
            captcha_token_v2: captcha_answer,
            captcha_token: ""
        })

        key_1 = findall(r'remove-spaces" name="(.*)" placeholder', response.text)[0]
        print(fmt(f'key_1: {key_1}'))

        return key_1
    except Exception as e:
        print(fmt(f'Failed to solve captcha (zefoy may have blocked you) [{e}]'))
        return ""


def send(client: Session, key: str, aweme_id: str) -> None:
    token = ''.join(choices(ascii_letters + digits, k=16))
    data = f'------WebKitFormBoundary{token}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{aweme_id}\r\n------WebKitFormBoundary{token}--\r\n'

    response = post('https://zefoy.com/c2VuZF9mb2xsb3dlcnNfdGlrdG9L', data=data, cookies=client.cookies.get_dict(),
                    headers={
                        'authority': 'zefoy.com',
                        'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{token}',
                        'user-agent': client.headers['user-agent'],
                    }).text

    response = decode(response)
    print(response)

    if 'Session expired' in response:
        print(fmt('Session expired'))
    elif 'views sent' in response:
        print(fmt(f'Views sent to {aweme_id}'))
    else:
        print(fmt(f'Failed to send views to {aweme_id}'))


def search_link(client: Session, key_1: str, tiktok_url: str) -> None:
    data = f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="{key_1}"\r\n\r\n{tiktok_url}\r\n------WebKitFormBoundary--\r\n'

    response = decode(post('https://zefoy.com/c2VuZF9mb2xsb3dlcnNfdGlrdG9L', data=data,
                           headers={
                               'authority': 'zefoy.com',
                               'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary',
                               'user-agent': client.headers['user-agent'],
                           }).text)

    if "onsubmit=\"showHideElements('.w1r','.w2r')" in response:
        token, aweme_id = findall(r'name="(.*)" value="(.*)" hidden', response)[0]
        print(fmt(f'Sending to: {aweme_id} | key_2: {token}'))
        sleep(3)
        send(client, token, aweme_id)
    else:
        timer = int(findall(r'ltm=(\d*);', response)[0])
        print(fmt(f'Time to sleep: {timer}'), end="\r")
        sleep(timer)
        print(fmt('Sending views...'), end="\r")


if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@minniehouse16/video/7214847085642812714'
    client = get_client()
    key_1 = solve_captcha(client)

    if not key_1:
        print(fmt('Failed to solve captcha (zefoy may have blocked you)'))
        exit()

    while True:
        search_link(client, key_1, tiktok_url)
        sleep(5)
