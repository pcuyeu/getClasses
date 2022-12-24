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

# Web browser opens in the background
options = Options()
options.headless = True
# Points to browser executable and goes to web page specified
browser_driver = Service('<point to your chrome executable on your device>')
page_to_scrape = webdriver.Chrome(service=browser_driver, options = options)
page_to_scrape.implicitly_wait(10)  
page_to_scrape.get("<class website>")

start = time.time()

ignore_list = [ElementNotVisibleException, ElementNotSelectableException]
wait = WebDriverWait(page_to_scrape, timeout = 12, poll_frequency= 3, ignored_exceptions= ignore_list)

# efficient way of waiting for web page to load.
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

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
number.send_keys("310")
time.sleep(1)
keyword_search.send_keys("")


# RADIO BUTTON TO SEARCH FOR ALL CLASSES 
open_classes_btn = page_to_scrape.find_element(By.ID, "search-all")
open_classes_btn.click()
time.sleep(1)

# CLICK ON SEARCH BUTTON
search_btn = page_to_scrape.find_element(By.ID, "search-button")
search_btn.click()
time.sleep(1)

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
                end = time.time()
                print("The time of execution of above program is :", (end-start) * 10**3, "ms")
                break
            else:
                # pop is used remove the full classes from each list
                if counter % 2 == 0:
                    class_info_odd.pop(0)
                else:
                    class_info_even.pop(0)
                counter += 1
    page_to_scrape.quit()