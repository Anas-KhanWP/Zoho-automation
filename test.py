import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from .credentials import username, password, signin_url, function_url
from time import sleep
from selenium.webdriver.chrome.options import Options
import random

# # Initialize the undetected Chrome WebDriver with options
# driver = uc.Chrome()
# wait = WebDriverWait(driver, 30)
# actions = ActionChains(driver)


# # Open multiple tabs
# for _ in range(4):
#     print(f"Opening Tab {_}")
#     driver.execute_script("window.open('');")
#     sleep(0.2)
    
# # Interact with each tab
# for tab_index in range(1, 4 + 1):  
#     driver.switch_to.window(driver.window_handles[tab_index])
#     print(f"Switched to Tab {tab_index}")
#     driver.get("https://www.example.com")
#     sleep(0.5)
    
# print("Done")
# sleep(60)

min_num_tabs = 1
max_num_tabs = 99


current_min = min_num_tabs
current_max = min(current_min + 19, max_num_tabs)


while current_min <= max_num_tabs:
    print(f"Current Min: {current_min} | Current Max: {current_max}")
    current_min = current_max + 1
    current_max = min(current_min + 19, max_num_tabs)