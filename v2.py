from time import sleep
from datetime import datetime
from os import system, name as os_name
from base64 import b64encode
from io import BytesIO
from requests import get, post, Session
from re import findall
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class Zefoy:
    def __init__(self) -> None:
        self.driver = self.setup_browser()
        self.sent = 0
        self.clear = system('cls' if os_name == 'nt' else 'clear')
        self.xpaths = {
            "followers": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
            "hearts": "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
            "comment_hearts": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
            "views": "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
            "shares": "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
            "favorites": "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
        }

    def setup_browser(self) -> webdriver.Chrome:
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    def solve_captcha(self) -> dict:
        session = Session()
        session.headers = {
            'authority': 'www.baidu.com',
            'origin': 'https://www.baidu.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        while True:
            source_code = session.get('https://www.baidu.com').text
            captcha_url = findall(r'img src="([^"]*)"', source_code)[0]
            token_answer = findall(r'type="text" name="(.*)" oninput="this.value', source_code)[0]
            encoded_image = b64encode(BytesIO(session.get('https://zefoy.com' + captcha_url).content).read()).decode('utf-8')

            captcha_answer = post(
                "https://platipus9999.pythonanywhere.com/",
                json={'captcha': encoded_image, 'current_time': datetime.now().strftime("%H:%M:%S")}
            ).json().get("result", "")

            data = {token_answer: captcha_answer}
            response = session.post('https://zefoy.com', data=data).text
            try:
                findall(r'remove-spaces" name="(.*)" placeholder', response)[0]
                return {'name': 'PHPSESSID', 'value': session.cookies.get('PHPSESSID')}
            except IndexError:
                pass

    def send_bot(self, search_button, url_box, vid_info, div):
        element = self.driver.find_element(By.XPATH, url_box)
        element.clear()
        element.send_keys(vid_info)
        self.driver.find_element(By.XPATH, search_button).click()
        sleep(3)

        ratelimit_seconds, full = self.check_submit()
        if "(s)" in str(full):
            self.sleep_with_message(ratelimit_seconds)
            self.driver.find_element(By.XPATH, search_button).click()
            sleep(2)

        send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
        self.driver.find_element(By.XPATH, send_button).click()
        self.sent += 1
        print(f"Sent {self.sent} times.")
        sleep(4)
        self.send_bot(search_button, url_box, vid_info, div)

    def sleep_with_message(self, delay):
        while delay > 0:
            sleep(1)
            delay -= 1
            print(f"Cooldown: {delay}s remaining")

    def check_submit(self):
        remaining_xpath = f'//*[@id="{self.xpaths["views"]}/span"]'
        try:
            element = self.driver.find_element(By.XPATH, remaining_xpath)
        except:
            return None, None

        if "READY" in element.text:
            return True, True

        if "seconds for your next submit" in element.text:
            minutes, seconds = map(int, findall(r'\d+', element.text)[:2])
            return minutes * 60 + seconds, element.text
        return None, None

    def main(self):
        self.clear
        self.driver.get("https://zefoy.com")

        print("Solving Captcha...")
        self.driver.add_cookie(self.solve_captcha())
        self.driver.refresh()

        video_url = input("Enter Video URL: ")
        search_button_xpath = f'/html/body/div[6]/div/form/div/div/button'
        url_box_xpath = f'/html/body/div[6]/div/form/div/input'

        self.send_bot(search_button_xpath, url_box_xpath, video_url, div=6)

if __name__ == "__main__":
    Zefoy().main()
