import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import Sengine.command_processor as cp
import json
import time
import os
import threading
import re
import sys

CommandProcessor = cp.CommandProcessor()

class SengineAI:
    def __init__(self):
        self.config_process()
        self.options = uc.ChromeOptions()
        self.options.add_argument('--disable-notifications')
        if CommandProcessor.headless: self.options.add_argument('--headless')
        self.engine = uc.Chrome(options=self.options, version_main = 120)

        if not os.path.exists("SavedStates"):
            os.makedirs("SavedStates")

    def login(self, username, password):
        # Navigate to the Facebook login page.
        self.engine.get("https://www.facebook.com")

        # Perform a normal login or cookie-based login depending on the existence of cookie file.
        if not os.path.exists("SavedStates/fblogin_cookies.json"):
            self.normal_login(username, password)
            print("Login Success...")
        else:
            self.cookie_login()
            print("Login Success...")

        # get profile id
        if CommandProcessor.profile == "":
            self.engine.get("https://www.facebook.com/profile.php")
            profile = self.engine.current_url
            profile = re.findall(r'\d+', profile)[-1] if re.findall(r'\d+', profile) else None
            CommandProcessor.profile = profile
            self.config_update()

        self.engine.get("https://www.facebook.com/messages/t/")

        time.sleep(5)
        self.thread_process()

    def normal_login(self, username, password):
        for i in range(1, 4):
            try:
                email_box = WebDriverWait(self.engine, 40).until(EC.presence_of_element_located((By.ID, "email")))
                self.engine.execute_script("arguments[0].value = arguments[1];", email_box, username)

                pass_box = self.engine.find_element(By.ID, "pass")
                self.engine.execute_script("arguments[0].value = arguments[1];", pass_box, password)
                pass_box.send_keys(Keys.ENTER)

                cookies = self.engine.get_cookies()
                cookies_json = json.dumps(cookies, indent=4)

                print("Saving Cookies..")
                with open("SavedStates/fblogin_cookies.json", 'w') as file:
                    file.write(cookies_json)

                break
            except:
                print(f"Login fail trying again {i}...")

    def cookie_login(self):
        try:
            with open("SavedStates/fblogin_cookies.json", 'r') as file:
                cookies_json = file.read()

            cookies = json.loads(cookies_json)

            for cookie in cookies:
                self.engine.add_cookie(cookie)

            time.sleep(2)

            print("Cookies Injected Sucessfully...")
        except:
            print("Login Failed...")

    def config_update(self):
        with open('SavedStates/config.json', 'r') as file:
            data = json.load(file)

        data["profile"] = CommandProcessor.profile

        with open('SavedStates/config.json', 'w') as file:
            json.dump(data, file, indent=4)

    def config_process(self):
        if not os.path.exists("SavedStates/config.json"):

            config = {
                "profile": "",
                "admin_uid": "",
                "chat_api": "",
                "On_Login_OTP": False,
                "headless": False,
                "commands": [
                    "help",
                    "info",
                    "img",
                    "joke",
                    "admin",
                    "shutdown"
                ]
            }

            with open('SavedStates/config.json', 'w') as json_file:
                json.dump(config, json_file, indent=4)

            print("JSON file 'config.json' created successfully.")

        with open('SavedStates/config.json', 'r') as json_file:
            data = json.load(json_file)

        CommandProcessor.admin_uid = data["admin_uid"]
        CommandProcessor.On_Login_OTP = data["On_Login_OTP"]
        CommandProcessor.headless = data["headless"]
        CommandProcessor.profile = data["profile"]
        self.commands = data["commands"]

    def thread_process(self):
        print("Starting please wait...")

        thread = threading.Thread(target=CommandProcessor.login_process())
        thread.daemon = True
        thread.start()

        self.process_message()

    def process_message(self):
        print("Running...")

        # Continuously monitor for new messages.
        while True:
            try:
                message = self.engine.find_element(By.XPATH, "//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84']")
                link = self.engine.find_element(By.XPATH, "//a[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']")
                raw_url = link.get_attribute('href')
                url = re.findall(r'\d+', raw_url)[-1] if re.findall(r'\d+', raw_url) else None

                if "/" in message.text:
                    command = message.text[message.text.find('/') + 1:].strip()
                    for instruction in self.commands:
                        if instruction in command:
                            command = f"self.send_command(incoming_url='{url}', command='{command}')"

                    # Sending command to command_processor
                    if command not in CommandProcessor.command_list:
                        CommandProcessor.command_list.append(command)
                        CommandProcessor.command_queue.put(CommandProcessor.evaluation(command))

                if CommandProcessor.shutdown == True:
                    break
            except:
                pass

        sys.exit()
