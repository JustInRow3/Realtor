import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#Chromedriver Options
options = Options()
options.page_load_strategy = 'eager' # Webdriver waits until DOMContentLoaded event fire is returned.
options.headless = False #Show browser?

#Open tab
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wd.implicitly_wait(10)

#Enter URL
wd.get('https://www.realtor.com/realestateagents/')
wd.maximize_window()

#Wait
# wait = WebDriverWait(wd, 20)  # setup wait
# wait.until(EC.presence_of_element_located((By.ID, 'user_email'))).send_keys('*********') #Enter email
# wait.until(EC.presence_of_element_located((By.ID, 'user_password'))).send_keys('********') #Enter Password
# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sign_in_form"]/div[3]/label/div'))).click() #click checkbox
# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sign_in_form"]/p[1]/input'))).click() #click Sign In

time.sleep(1)

#<a href="">Sign In</a>

