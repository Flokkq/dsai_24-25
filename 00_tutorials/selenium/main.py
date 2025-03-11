#!/usr/bin/env python
# coding: utf-8

# # Webscraping with Selenium
# Selenium Webpage: https://www.selenium.dev/
# 
# documentation for python: https://www.selenium.dev/selenium/docs/api/py/index.html#

# In[ ]:


# install selenium package if not done so far
#!pip install selenium

# ## Attention:
# 
# Selenium needs a WebDriver (specific for the browser you have: Chrome, Firefox, Edge, Safar).
# 
# In many cases it is installed automatically when Selenium is used with Python
# 
# If not, follow this link for manual installation: https://www.selenium.dev/selenium/docs/api/py/index.html#drivers

# In[1]:


import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # Wofür das EC steht weiß ich jetzt nicht :/
 
# Launch Chrome browser
options = webdriver.ChromeOptions()

options.add_argument("headless")
browser = webdriver.Chrome(options=options)
 
# Load web page
browser.get("https://www.yahoo.com")

# Network transport takes time. Wait until the page is fully loaded
def is_ready(browser):
    return browser.execute_script(r"""
        return document.readyState === 'complete'
    """)
WebDriverWait(browser, 30).until(is_ready)

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@name="agree"]'))).click()
 
# Scroll to bottom of the page to trigger JavaScript action
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
WebDriverWait(browser, 30).until(is_ready)
 
# Search for news headlines and print
elements = browser.find_elements(By.XPATH, "//h3/a[u[@class='StretchedBox']]")

for elem in elements:
    print(elem.text)
    print()
 
# Close the browser once finish
browser.close()

# In[ ]:



