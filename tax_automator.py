"""
Opens firefox, navigates to Creditkarma.com, waits for you to get to the 1099 investment income page, then fills out
the form with the data in combined_1099.csv, which is in the format that Wealthfront issues their 1099 XLS forms, but
converted in Libreoffice to CSV.
"""

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
import csv
import time

transactions = list()

with open("combined_1099.csv") as wealthfront_1099:
    r = csv.DictReader(wealthfront_1099)
    for row in r:
        transactions.append(row)


browser = webdriver.Firefox()
browser.get("https://www.creditkarma.com/auth/logon")
username = browser.find_element_by_id('username')
username.click()
username.send_keys('mgherm@gmail.com')
# passwd = browser.find_element_by_id('password')
# # passwd_value = input('password: ')
# # passwd.send_keys(passwd_value)
# # passwd.submit()
waiting_element = WebDriverWait(browser, 10000).until(expected_conditions.url_matches("https://tax.creditkarma.com/taxes/CapitalGainsFullListSummary.action"))
time.sleep(3)
counter = 0
for row in transactions:
    counter_string = str(counter)
    try:
        belongs_to = Select(browser.find_element_by_name("capitalGains["+counter_string+"].belongsTo"))
    except:
        add_rows = browser.find_element_by_id('addRows')
        add_rows.click()
        time.sleep(5)
        belongs_to = Select(browser.find_element_by_name("capitalGains[" + counter_string + "].belongsTo"))
    reporting_category = Select(browser.find_element_by_name("capitalGains["+counter_string+"].reportingCategory"))
    description = browser.find_element_by_name("capitalGains["+counter_string+"].description")
    date_acquired = browser.find_element_by_name("capitalGains["+counter_string+"].dateAcquired")
    date_sold = browser.find_element_by_name("capitalGains["+counter_string+"].dateSold")
    sales_price = browser.find_element_by_name("capitalGains["+counter_string+"].salesPrice")
    cost = browser.find_element_by_name("capitalGains["+counter_string+"].cost")
    code = Select(browser.find_element_by_name("capitalGains["+counter_string+"].adjustmentCode"))
    adjustment_amount = browser.find_element_by_name("capitalGains["+counter_string+"].adjustmentAmount")
    # belongs_to.clear()
    belongs_to.select_by_value('tp')
    # reporting_category.clear()
    if row['Holding period'] == "Short-term":
        reporting_category.select_by_value('1')
    else:
        reporting_category.select_by_value('4')
    description.clear()
    description.send_keys(row["Description of property"])
    date_acquired.clear()
    date_acquired.send_keys(row['Date acquired'])
    date_sold.clear()
    date_sold.send_keys(row['Date sold'])
    sales_price.clear()
    sales_price.send_keys(row['Sales price'])
    cost.clear()
    cost.send_keys(row['Cost'])
    # code.clear()
    code.select_by_value(row['Code(s)'])
    adjustment_amount.clear()
    adjustment_amount.send_keys(row["Amount of adjustment"])
    counter += 1