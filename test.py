try:
    import undetected_chromedriver as uc
    import ctypes, platform, os, time
    import selenium, requests, webbrowser

except ImportError:
    input("You do not have all of the modules required installed.")
    os._exit(1)

class zefoy:

    def __init__(self):
        self.driver = uc.Chrome()
        self.captcha_box = '/html/body/div[5]/div[2]/form/div/div'
        self.clear = "clear"

        if platform.system() == "Windows":
            self.clear = "cls"

        self.sent = 0
        self.xpaths = {
            "followers": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
            "hearts": "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
            "comment_hearts": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
            "views": "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
            "shares": "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
            "favorites": "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
        }

    def main(self):
        os.system(self.clear)
        self.change_title("TikTok Automator using zefoy.com | Github: @xtekky")

        print("Waiting for Zefoy to load... 502 Error = Blocked country or VPN is on")

        self.driver.get("https://zefoy.com")
        self.wait_for_xpath(self.captcha_box)

        print("Site loaded, enter the CAPTCHA to continue.")
        print("Waiting for you...")

        self.wait_for_xpath(self.xpaths["followers"])
        os.system(self.clear)
        status = self.check_status()

        print()
        print(f"Join our Discord Server for exclusive FREE tools.")
        print(f"You can also get updates when Zefoy updates the bots and more.")
        print(f"Select your option below.\n")

        counter = 1
        for thing in status:
            print(f"[{counter}] {thing} {status[thing]}")
            counter += 1

        print(f"[7] Discord / Support")
        option = int(input("\nSelect an option: "))

        if option == 1:
            div = "7"
            self.driver.find_element("xpath", self.xpaths["followers"]).click()

        elif option == 2:
            div = "8"
            self.driver.find_element("xpath", self.xpaths["hearts"]).click()

        elif option == 3:
            div = "9"
            self.driver.find_element("xpath", self.xpaths["comment_hearts"]).click()

        elif option == 4:  # Views
            div = "10"
            self.driver.find_element("xpath", self.xpaths["views"]).click()

        elif option == 5:
            div = "11"
            self.driver.find_element("xpath", self.xpaths["shares"]).click()

        elif option == 6:
            div = "12"
            self.driver.find_element("xpath", self.xpaths["favorites"]).click()

        elif option == 7:
            webbrowser.open('discord.gg/onlp')
            os._exit(1)

        else:
            os._exit(1)

        video_url_box = f'/html/body/div[{div}]/div/form/div/input'
        search_box = f'/html/body/div[{div}]/div/form/div/div/button'
        vid_info = input("\nEnter Username/Video URL: ")

        self.send_bot(search_box, video_url_box, vid_info, div)

    def send_bot(self, search_button, main_xpath, vid_info, div):
        element = self.driver.find_element('xpath', main_xpath)
        element.clear()
        element.send_keys(vid_info)
        self.driver.find_element('xpath', search_button).click()
        time.sleep(3)

        ratelimit_seconds, full = self.check_submit(div)
        if "(s)" in str(full):
            self.main_sleep(ratelimit_seconds)
            self.driver.find_element('xpath', search_button).click()
            time.sleep(2)

        time.sleep(3)

        send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
        self.driver.find_element('xpath', send_button).click()
        self.sent += 1
        print(f"Sent {self.sent} times.")

        time.sleep(4)
        self.send_bot(search_button, main_xpath, vid_info, div)

    def main_sleep(self, delay):
        while delay != 0:
            time.sleep(1)
            delay -= 1
            self.change_title(f"TikTok Zefoy Automator | Cooldown: {delay}s")

    def convert(self, min, sec):
        seconds = 0
        if min != 0:
            seconds += int(min) * 60
        seconds += int(sec) + 5
        return seconds

    def check_submit(self, div):
        remaining = f"/html/body/div[{div}]/div/div/h4"
        try:
            element = self.driver.find_element("xpath", remaining)
        except:
            return None, None

        if "READY" in element.text:
            return True, True

        if "seconds for your next submit" in element.text:
            output = element.text.split("Please wait ")[1].split(" for")[0]
            minutes = element.text.split("Please wait ")[1].split(" ")[0]
            seconds = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration = self.convert(minutes, seconds)
            return sleep_duration, output

        return element.text, None

    def check_status(self):
        statuses = {}
        for thing in self.xpaths:
            value = self.xpaths[thing]
            element = self.driver.find_element('xpath', value)

            if not element.is_enabled():
                statuses.update({thing: "[OFFLINE]"})
            else:
                statuses.update({thing: "[WORKS]"})

        return statuses

    def change_title(self, arg):
        if self.clear == "cls":
            ctypes.windll.kernel32.SetConsoleTitleW(arg)

    def wait_for_xpath(self, xpath):
        while True:
            try:
                self.driver.find_element('xpath', xpath)
                return True
            except selenium.common.exceptions.NoSuchElementException:
                pass


if __name__ == "__main__":
    obj = zefoy()
    obj.main()
    input()