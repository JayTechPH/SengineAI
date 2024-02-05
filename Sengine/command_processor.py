import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import random
import json
import time
import os
import shutil
import queue
import sys

messagelink = "https://mbasic.facebook.com/messages/t/"

custom_help_list = [
"""
COMMAND LIST (/)
-------------------------------------
-------------------------------------
""",
"joke - generate joke",
"img - search image",
]

custom_chat_list = [
]

def process_command_parameter_full(command, index, mode):
    words = command.split()
    if mode == 0:
        return ' '.join(words[1:]) if len(words) > 1 else None
    elif mode == 1:
        return words[index] if len(words) > index else None
    else: return None

# Add Custom Function Here
class CustomCommand:
    # Example
    def get_random_joke(self):
        url = "https://icanhazdadjoke.com/"

        headers = {
            "Accept": "text/plain"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text.strip()
            else:
                return "Failed to fetch a joke. Please try again later."
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def process_images(self, search, count):
        if not os.path.exists("images"):
            os.makedirs("images")

        search_url = f"https://www.google.com/search?q={search}&tbm=isch"

        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        count = min(count, 10)

        image_tags = soup.find_all('img', limit=count + 1)

        for i, img in enumerate(image_tags):
            image_url = img['src']
            if image_url.startswith('http://') or image_url.startswith('https://'):
                image_response = requests.get(image_url)
                with open(os.path.join("images", f'image_{i}.jpg'), 'wb') as f:
                    f.write(image_response.content)

    # use this if you send image (return images_folder_path, 1) save the image you want to send in these folder /images
    # or use this (return "", 1) if your using (/images) folder this is the default image folder

    # use this if you send message (return mesaage_string, 0)
    # example use below
    def command_processor(self, process_command_text, command_parameter, num, full_command):
        if process_command_text == "joke":
            return self.get_random_joke(), 0
        elif process_command_text == "img":
            if command_parameter is not None:
                query = process_command_parameter_full(full_command, index=1, mode=0)
                self.process_images(search=query, count=num)
                return "", 1
        return 2

class CommandProcessor:
    def __init__(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument('--disable-notifications')
        self.command_queue = queue.Queue()
        self.cp = CustomCommand()
        self.admin_uid = ""
        self.otp_value = ""
        self.profile = ""
        self.command_list = []
        self.help_groups_list = []
        self.On_Login_OTP = False
        self.headless = False
        self.shutdown = False

    def login_process(self):
        if self.headless: self.options.add_argument('--headless')
        self.engine = uc.Chrome(options=self.options, version_main = 120)
        self.engine.get("https://www.facebook.com")
        self.cookie_login()
        self.engine.get("https://www.facebook.com/messages/")
        if self.admin_uid != "" and self.On_Login_OTP == True:
            self.otp()
        self.help_process()
        self.queue_processing()

    def cookie_login(self):
        try:
            with open("SavedStates/fblogin_cookies.json", 'r') as file:
                cookies_json = file.read()

            cookies = json.loads(cookies_json)

            for cookie in cookies:
                self.engine.add_cookie(cookie)

            print("Injecting Cookies...")

            time.sleep(5)
        except:
            print("Login Failed")

    def config_update(self):
        with open('SavedStates/config.json', 'r') as file:
            data = json.load(file)

        data["admin_uid"] = self.admin_uid

        with open('SavedStates/config.json', 'w') as file:
            json.dump(data, file, indent=4)
    # for future use
    def otp(self):
        x = ''.join(random.choices('0123456789', k=6))
        self.otp_value = x
        self.engine.get(messagelink + self.admin_uid)
        self.process_send_message(x)

    def admin_process(self, command, incoming_url, command_parameter):
        if self.admin_uid != "":
            if command_parameter == "set":
                self.process_send_message(message=self.default_chat_list[4])
            elif command_parameter == "free":
                if incoming_url != self.admin_uid:
                    self.process_send_message(message=self.default_chat_list[5])
                else:
                    self.admin_uid = ""
                    self.process_send_message(message=self.default_chat_list[6])
                    self.config_update()
        else:
            if command_parameter == "set":
                num = 3
                self.admin_uid = incoming_url
                self.config_update()
            self.process_send_message(message=self.default_chat_list[num])

    def shtdwn(self):
        self.process_send_message(message=self.default_chat_list[7])
        self.shutdown = True
        sys.exit()

    def shutdown_func(self, incoming_url):
        if self.admin_uid != "":
            if self.admin_uid == incoming_url:
                self.shtdwn()
            else:
                self.process_send_message(message=self.default_chat_list[5])
        else:
            self.shtdwn()

    def help_process(self):
        for i in range(1, len(custom_help_list), 5):
            group_positions = list(range(i, min(i + 5, len(custom_help_list))))
            self.help_groups_list.append(group_positions)

    def help_func(self, num):
        if num == 1:
            self.process_send_message(message=self.default_chat_list[0])
        else:
            x = self.help_groups_list[num - 2]
            z = custom_help_list[0]
            z = z.split('\n')
            for i in x:
                y = custom_help_list[i]
                z.insert(3, y)
            message = '\n'.join(z)
            self.process_send_message(message)

    def evaluation(self, command):
        eval(command)
        if command in self.command_list:
            self.command_list.remove(command)

    def queue_processing(self):
        while not self.command_queue.empty():
            func = self.command_queue.get()
            func()

    def process_send_image(self, incomingurl, images_folder):
        if images_folder == "":
            images_folder_path = os.path.abspath("images")
        else:
            images_folder_path = images_folder

        if incomingurl.startswith("10"):
            link = f"https://mbasic.facebook.com/messages/photo/?ids={incomingurl}&tids%5B0%5D=cid.c.{incomingurl}%3A{self.profile}&message_text&cancel=https%3A%2F%2Fmbasic.facebook.com%2Fmessages%2Ft%2F{incomingurl}"
        else:
            link = f"https://mbasic.facebook.com/messages/photo/?ids&tids%5B0%5D=cid.g.{incomingurl}&message_text&cancel=https%3A%2F%2Fmbasic.facebook.com%2Fmessages%2Ft%2F{incomingurl}"

        for filename in os.listdir(images_folder_path):
            self.engine.get(link)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_path = os.path.join(images_folder_path, filename)
                send = self.engine.find_element(By.XPATH, "//input[@type='file']")
                send.send_keys(image_path)
                button = self.engine.find_element(By.XPATH, "//input[@type='submit']")
                button.click()

        shutil.rmtree(images_folder_path)

    def process_send_message(self, message):
        send = self.engine.find_element(By.ID, "composerInput")
        self.engine.execute_script("arguments[0].value = arguments[1];", send, message)
        button = self.engine.find_element(By.NAME, "send")
        button.click()

    def process_command(self, command):
        process_command_text = command.split()[0]
        return process_command_text

    def process_command_parameter(self, command):
        words = command.split()
        return words[1] if len(words) >= 2 else None

    def process_command_number(self, command):
        proc = command.split()
        if len(proc) >= 2 and proc[-1].isdigit():
            num = proc[-1]
        else: num = "1"
        return int(num)

    default_chat_list = [
"""
COMMAND LIST (/)
-------------------------------------
help - see all command list
info - creator of SengineAI
admin - admin commands
shutdown - (admin only)
usage - command example
-------------------------------------
""",
"Command doesn't exist.",
"SengineAI, developed by Ar Jay Pangilinan \nhttps://jaytechph.github.io",
"Your now the admin of this bot account. ^_^",
"The admin of this is already set. ^_^",
"You are not the admin of this bot. ^_^",
"The bot is free now! and everyone can access the admin command. ^_^",
"Sengine AI is shutting down Bye! ^_^",
"Example Usage \n use (/) to call command example - /help.\nother command use parameter example - /help 1"
]

    def send_command(self, incoming_url, command):
        try:
            self.engine.get(messagelink + incoming_url)
            process_command_text = self.process_command(command)
            num = self.process_command_number(command)
            command_parameter = self.process_command_parameter(command)

            if process_command_text == "help":
                self.help_func(num)
            elif process_command_text == "info":
                self.process_send_message(message=self.default_chat_list[2])
            elif process_command_text == "admin":
                self.admin_process(command, incoming_url, command_parameter)
            elif process_command_text == "shutdown":
                self.shutdown_func(incoming_url)
            elif process_command_text == "usage":
                self.process_send_message(message=self.default_chat_list[8])
            else:
                data, mode = self.cp.command_processor(process_command_text, command_parameter, num, command)
                if mode == 0:
                    self.process_send_message(message=data)
                elif mode == 1:
                    self.process_send_image(incoming_url, data)
                else:
                    self.process_send_message(message=self.default_chat_list[1])
        except:
            pass
