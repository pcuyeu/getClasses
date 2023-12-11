#IMPORT LIBRARIES

from selenium import webdriver
from selenium.webdriver.common.keys import Keys    # Allows for input into text fields
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By    # Locates elements by their tags
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementNotVisibleException,ElementNotSelectableException)
from selenium.webdriver.chrome.options import Options
import time

# added some more imports
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


##### NEW ADDITIONS TO SELENIUM #####:

# https://www.selenium.dev/blog/2023/headless-is-going-away/
# ^(TITLE OF ARTICLE IS A JOKE... NEW HEADLESS OPTION FOR SELENIUM)

# Selenium v4.6.0 includes built in Manager. No need to use a third party library
# (WebDriverManager). 

###########################################

# headless mode (makes browser window not visible to the user)
options = Options()
options.add_argument("--headless=new")

page_to_scrape = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)
page_to_scrape.get("https://catalog.apps.asu.edu/catalog/classes")

page_to_scrape.maximize_window() # maximize window

ignore_list = [ElementNotVisibleException, ElementNotSelectableException]
wait = WebDriverWait(page_to_scrape, timeout = 12, poll_frequency= 3, ignored_exceptions= ignore_list)

# efficient way of waiting for web page to load.
#wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

# clear Cookie banner 
consent_banner = page_to_scrape.find_element(By.CLASS_NAME, "uds-cookie-consent-faux-close-btn")
consent_banner.click()
time.sleep(3)

# BUTTON FOR ADDITIONAL OPTIONS
moreOptions = page_to_scrape.find_element(By.LINK_TEXT, "Advanced Search")
moreOptions.click() 
time.sleep(1)

# Term drop down menu
drop_down_menu = page_to_scrape.find_element(By.ID, "term")
# TEXT FIELDS
subject = page_to_scrape.find_element(By.NAME, "subject")
number = page_to_scrape.find_element(By.NAME, "catalogNbr")
keyword_search = page_to_scrape.find_element(By.ID, "keyword")

# Waits for element to be displayed on screen
wait.until(EC.element_to_be_clickable(drop_down_menu))
time.sleep(1)

# Types input into the text fields
subject.send_keys("CSE")
time.sleep(1)
number.send_keys("340")
time.sleep(1)
keyword_search.send_keys("")
time.sleep(1)

# Scroll down the page until the search-button is visible
src_btn_flag = page_to_scrape.find_element(By.XPATH, "//*[@id='search-button']")
page_to_scrape.execute_script("arguments[0].scrollIntoView();", src_btn_flag)
time.sleep(3)

# RADIO BUTTON TO SEARCH FOR ALL CLASSES  
#open_classes_btn = page_to_scrape.find_element(By.ID, "search-all")
#open_classes_btn.click()
#time.sleep(3)

# CLICK ON SEARCH BUTTON
search_button = page_to_scrape.find_element(By.ID, "search-button")
search_button.click() 
time.sleep(3)

#################### PAGE WITH WANTED DATA ####################

# all_seats is a list of seats for all sections for the semester (ex: 0 of 100). 
all_seats = page_to_scrape.find_elements(By.CLASS_NAME, "class-results-cell.seats")
class_info_odd = page_to_scrape.find_elements(By.CLASS_NAME, "class-accordion.odd")
class_info_even = page_to_scrape.find_elements(By.CLASS_NAME, "class-accordion.even")
# element is a string of the first element -> convert first index of element into a integer


# Quick Check to see if both lists are empty
if len(all_seats) == 0:
    print("No classes found.")
    page_to_scrape.quit()
else:
# counter variable has a couple of uses...
# 1. counter is used to filter the classes with no available seats for the 1st if statement below.
# 2. counter splits the odd and even accordions, so the order stays the same as displayed in the web page
# 3. Used for grabbing the values from all_seats 
    counter = 0
    for element in all_seats:
        # Get the first number from seats available
        element = all_seats[counter].text
        firstIndex = int(element[0])             
        if firstIndex > 0: 
            if counter % 2 == 0:
                # info_odd is here instead of info_even b/c the first accordion displayed is odd.
                # - Pattern: accordion.odd, accordion.even, accordion.odd, accordion.even, ...  
                info_odd = class_info_odd[0].text
                class_info_odd.pop(0)
                print(info_odd + "\n")
            else:
                info_even = class_info_even[0].text
                class_info_even.pop(0)
                print(info_even + "\n") 
            counter += 1
    
        else:
            if (len(all_seats) - 1) == counter:
                print("All seats are taken or the end of list has been reached.")
                break
            else:
                # pop is used remove the full classes from each list
                if counter % 2 == 0:
                    class_info_odd.pop(0)
                else:
                    class_info_even.pop(0)
                counter += 1
    page_to_scrape.quit()
