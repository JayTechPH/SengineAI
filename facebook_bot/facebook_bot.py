import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

chat = "https://www.messenger.com/t/"


class facebook_bot():
#config function
    def __init__(self, gcid, username, password, morning, evening, afternoon, night):
        
        options = uc.ChromeOptions()
        options.add_argument('--disable-not    ifications')
        self.engine = uc.Chrome(version_main = 95, options=options)
        self.engine.get("https://www.messenger.com/")
        self.login(gcid, username, password)
        self.greetings(gcid, morning, evening, afternoon, night)
        
        
#login function
    def login(self, gcid, username, password):

        email_box = WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.ID, "email")))
        email_box.send_keys(username)

        pass_box = self.engine.find_element(By.ID, "pass")
        pass_box.send_keys(password)

        login_btn = self.engine.find_element(By.ID, "loginbutton")
        login_btn.click()
        
        self.engine.get(chat+gcid)
        message_box = WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[class='xat24cr xdj266r']")))
        message_box.send_keys("Hi! Sengiene AI Activated!")
        message_box.send_keys(Keys.ENTER)
        print("LOGIN SUCCESS")
        
    def greetings(self, gcid, morning, evening, afternoon, night):

        
        
        while True:
    # Get the current time
            current_time = time.strftime("%I:%M:%S %p")
        
            if current_time == morning:
                self.engine.get(chat+gcid)
                
                message_box = WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[class='xat24cr xdj266r']")))
                message_box.send_keys("Good Morning Guys!!!")
                message_box.send_keys(Keys.ENTER)
                print("message success")
            
            if current_time == evening:
                self.engine.get(chat+gcid)
                message_box = WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[class='xat24cr xdj266r']")))
                message_box.send_keys("Good Evening Guys!!!")
                print("message success")
            
            if current_time == afternoon:
                self.engine.get(chat+gcid)
                message_box = WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[class='xat24cr xdj266r']")))
                message_box.send_keys("Good Afternoon Guys!!!")
                print("message success")
            
            if current_time == night:
                self.engine.get(chat+gcid)
                message_box = WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[class='xat24cr xdj266r']")))
                message_box.send_keys("Good Night Guys!!!")
                print("message success")
            



