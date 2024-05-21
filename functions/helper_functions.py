import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from .credentials import username, password, signin_url, function_url
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
import logging
from datetime import datetime


def login(driver, wait):
    # Navigate to the URL
    driver.get(signin_url) 
    
    u_name = wait.until(EC.presence_of_element_located((By.ID, 'login_id')))
    u_name.send_keys(username)
    u_name.send_keys(Keys.ENTER)
    
    sleep(2)
    
    pass_ = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    pass_.send_keys(password)
    pass_.send_keys(Keys.RETURN)
    
def go_to_functions(driver, actions, function_name, n, wait):
    sleep(1)

    driver.get(function_url)
    
    function_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[text()="{function_name}{n}"]')))
    
    # Hover over the element
    actions.move_to_element(function_element).perform()
    
    print("Hover action performed")
    
    input_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchBar.pR.w100p")))
    input_element.click()
    input_element.clear()
    input_element.send_keys(function_name + n)
    
    # Get the next sibling of the test_function_element
    next_sibling = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="{function_name}{n}"]/following-sibling::*[1]')))
    
    if next_sibling:
        next_sibling.click()
        sleep(0.5)
        edit_button = wait.until(EC.presence_of_element_located((By.XPATH, '//lyte-menu-label[text()="Edit"]')))
        sleep(0.5)
        edit_button.click()
        sleep(0.5)
        if wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="info"]'))):
            # save_button = wait.until(EC.presence_of_element_located((By.XPATH, '//lyte-yield[text()="Save & Execute"]')))
            # sleep(0.5)
            # save_button.click()
            # sleep(0.5)
            save_and_execute(driver, wait)
            return True
    else:
        return False
    
def save_and_execute(driver, wait):
    save_button = wait.until(EC.presence_of_element_located((By.XPATH, '//lyte-yield[text()="Save & Execute"]')))
    sleep(0.5)
    save_button.click()
    sleep(0.5)

    
def find_result(driver, wait):
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'openCusFunctOutputCont')))
    result_ = WebDriverWait(element, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Function executed successfully"]')))
    if result_:
        return True
    else:
        return False
    
def main(function_name, n):
    # Setup logging
    today_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"log_{today_date}.log"
    logging.basicConfig(
        filename=log_filename, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Setup Chrome options to prevent bot detection
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("start-maximized")

    # Random user agent
    # user_agents = [
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    #     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    # ]
    # user_agent = random.choice(user_agents)
    # chrome_options.add_argument(f'user-agent={user_agent}')

    # Initialize the undetected Chrome WebDriver with options
    driver = uc.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    i = 1
    # Open multiple tabs
    for _ in range(4):
        logger.info(f"Opening Tab {_}")
        driver.execute_script("window.open('');")
        sleep(0.2)

    login(driver, wait)
    sleep(3)
    while True:
        if i > 1:
            logger.info(f"Failed, Trying {i} time")
        try:
            # Open multiple tabs
            # for _ in range(n):
            #     logger.info(f"Opening Tab {_ + 1}")
            #     driver.execute_script("window.open('');")
            #     sleep(0.2)
                
            # Interact with each tab
            for tab_index in range(1, n + 1):
                logger.info(f"{function_name}{tab_index}")
                # Switch to the tab
                driver.switch_to.window(driver.window_handles[tab_index])
                logger.info(f"Switched to Tab {tab_index}")
                # boolean = go_to_functions(driver, actions, function_name, tab_index, wait)
                go_to_functions(driver, actions, function_name, tab_index, wait)
                # if boolean:
                #     sleep(0.5)
                #     logger.info(boolean)
                #     # sleep(10)
                #     sleep(0.5)
                #     result = find_result(driver, wait)
                #     sleep(0.5)
                #     if result:
                #         sleep(0.5)
                #         logger.info(result.text)
                #     else:
                #         logger.info("Do Something")
                # else:
                #     logger.info("No Bool")
                #     i += 1
                
            for tab_index in range(1, n + 1):
                sleep(0.5)
                result = find_result(driver, wait)
                sleep(0.5)
                if result:
                    sleep(0.5)
                    logger.info(f"{function_name}{tab_index} Successful => {result.text}")
                else:
                    save_and_execute(driver, wait)
                    result = find_result(driver, wait)
                    if result:
                        sleep(0.5)
                        logger.info(f"{function_name}{tab_index} Successful => {result.text}")
                    else:
                        logger.info(f"{function_name}{tab_index} Failed => {result.text}")
            break
        except Exception as e:
            i += 1
            logger.error(f"Exception occurred: {e}")
            sleep(1)

            
if __name__ == "__main__":
    main()