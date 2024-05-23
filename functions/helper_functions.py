from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .credentials import username, password, signin_url, function_url
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import random

    
    
def search_for_functions(function_name, n, wait):
    function_number = str(n)
    input_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchBar.pR.w100p")))
    # input_element.click()
    input_element.clear()
    input_element.send_keys(function_name + function_number)

    
def go_to_functions(driver, actions, function_name, n, wait):
    sleep(1)

    # driver.get(function_url)
    n = str(n)
        
    function_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[text()="{function_name}{n}"]')))
    
    # Hover over the element
    actions.move_to_element(function_element).perform()
    
    print("Hover action performed")
    
    function_element.click()
    
    sleep(0.5)
    
    edit_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Edit Function"]')))
    print(edit_button.text)
    sleep(0.5)
    edit_button.click()
    sleep(0.5)
    return True
    # if wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="info"]'))):
    #     save_and_execute(driver, wait)
    #     return True
        
def save_and_execute(driver, wait):
    sleep(0.5)
    save_button = wait.until(EC.presence_of_element_located((By.XPATH, '//lyte-yield[text()="Save & Execute"]')))
    sleep(0.5)
    save_button.click()
    sleep(0.5)

    
def find_result(driver, wait):
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'openCusFunctOutputCont')))
    result_ = WebDriverWait(element, 20).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Function executed successfully"]')))
    # result_ = WebDriverWait(element, 20).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Failed to execute function"]')))
    if result_:
        print("Function Execution Status:")
        print(result_.text)
        return True
    else:
        return False
    
def login(driver, wait, logger):
    # Navigate to the URL
    driver.get(signin_url) 
    
    u_name = wait.until(EC.presence_of_element_located((By.ID, 'login_id')))
    u_name.send_keys(username)
    u_name.send_keys(Keys.ENTER)
    
    sleep(2)
    
    pass_ = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    pass_.send_keys(password)
    pass_.send_keys(Keys.RETURN)
    
    logger.info("Login Successful")
    
    
def main(function_name, m, n, driver, logger, wait, result_wait, actions, should_login=False, open_tabs=False):
    successful_functions = []
    
    i = 1
    
    tab_diff = n - (m - 1)
    
    if open_tabs:
        # Open multiple tabs
        for _ in range(tab_diff):
            logger.info(f"Opening Tab {_ + 1}")
            driver.execute_script("window.open('');")
            sleep(0.2)
        
    driver.switch_to.window(driver.window_handles[0])
    
    if should_login:    
        try:
            login(driver, wait, logger=logger)
        except:
            print(f"Could'nt Login, Trying again")
            try:
                login(driver, wait, logger=logger)
            except Exception as e:
                print(f"Error: {e}")
                logger.error(e)
                exit()

        
    sleep(3)
    total_tabs = len(driver.window_handles)
    logger.info(f"Total tabs: {total_tabs}")
    
    for index, handle in enumerate(driver.window_handles):
        logger.info(f"Tab index: {index}, Window handle: {handle}")
        
    # print(function_number)
        
    while True:
        function_number = m
        print(function_number)
        
        if i > 1:
            logger.info(f"Failed, Trying {i} time")
        try:   
            for tab_index in range(1, tab_diff + 1):
                driver.switch_to.window(driver.window_handles[tab_index])
                driver.get(function_url)   
                          
            function_number = m
            # Interact with each tab
            for tab_index in range(1, tab_diff + 1):
                driver.switch_to.window(driver.window_handles[tab_index])
                search_for_functions(function_name, function_number, wait)
                function_number += 1
                
            function_number = m
            
            for tab_index in range(1, tab_diff + 1):
                logger.info(f"{function_name}{function_number}")
                # Switch to the tab
                driver.switch_to.window(driver.window_handles[tab_index])
                
                logger.info(f"Switched to Tab {tab_index}")
                go_to_functions(driver, actions, function_name, function_number, wait)
                
                function_number += 1
            
            function_number = m
            
            for tab_index in range(1, tab_diff + 1):
                driver.switch_to.window(driver.window_handles[tab_index])
                if wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="info"]'))):
                    save_and_execute(driver, wait)
                function_number += 1
                
            function_number = m
                
            for tab_index in range(1, tab_diff + 1):
                driver.switch_to.window(driver.window_handles[tab_index])
                sleep(0.5)
                result = find_result(driver, result_wait)
                sleep(0.5)
                if result:
                    function__ = function_name + str(function_number)
                    sleep(0.5)
                    logger.info(f"{function_name}{function_number} Successful")
                    successful_functions.append(function__) 
                else:
                    function__ = function_name + str(function_number)
                    save_and_execute(driver, wait)
                    result = find_result(driver, result_wait)
                    if result:
                        sleep(0.5)
                        logger.info(f"{function_name}{function_number} Successful")
                        successful_functions.append(function__)
                    else:
                        logger.info(f"{function_name}{function_number} Failed")
                        continue
                
                function_number += 1
            logger.info("Run Completed")
            break
        except Exception as e:
            i += 1
            logger.error(f"Exception occurred: {e}")
            sleep(1)
            
    data = {
        "successful_functions": successful_functions,
        "status": "SUCCESSFULL"
    }
    
    logger.info(data)
    
    # for tab_index in reversed(range(1, tab_diff + 1)):
    #     logger.info(f"Closing page {tab_index}")
    #     print(f"Closing page {tab_index + 1}")
    #     driver.switch_to.window(driver.window_handles[tab_index])
    #     sleep(0.5)
    #     driver.close()
    
    return data

            
if __name__ == "__main__":
    main()