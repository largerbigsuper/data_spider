# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

domain = 'http://www.tskspx.com/indexNew.do'
driver = webdriver.Chrome()
driver.get(domain)
# elem = driver.find_element_by_name('title')
print driver.title



