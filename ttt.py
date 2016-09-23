# -*- coding: utf-8 -*-
import time
from selenium import webdriver


_driver = webdriver.Firefox()
_driver.get("http://www.126.com")
_inp = _driver.find_element_by_id("x-URS-iframe")
_driver.switch_to.frame(_inp)
_inp1 = _driver.find_element_by_id("account-box")
time.sleep(10)
print _inp1.is_displayed()
