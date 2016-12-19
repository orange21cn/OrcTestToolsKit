from selenium import webdriver

# driver = webdriver.Firefox()
# driver.get("http://www.ch.com")
# driver.set_script_timeout(2)
# driver.maximize_window()
# driver.find_element_by_xpath("//body/div[13]/div[2]/div[1]/div[1]/a").click()
#
# for handle in driver.window_handles:
#     driver.switch_to.window(handle)
#     print driver.title
#!/usr/bin/python

from selenium import webdriver

driver = webdriver.Firefox()

driver.get("...")

driver.find_element_by_id("account").sendkeys("testaccount")
driver.find_element_by_id("passwd").sendkeys("password")
driver.find_element_by_id("submit").submit()