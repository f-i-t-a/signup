# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re

class TestSet(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_singup(self):
        driver = self.driver
        print "\n**** TEST - SIGNUP ***"
        driver.get("https://signup.insly.com")
        timestamp = int(time.time()) 
        company_name = "forinslytestassignment" + str(timestamp)

        driver.find_element_by_id("broker_name").send_keys(company_name)
        print "\n'" + company_name + "' was set as Company name"
        Select(driver.find_element_by_id("broker_address_country")).select_by_visible_text("Switzerland")
        driver.find_element_by_id("broker_tag").click()
        for i in range(10):
            try:
                self.assertEqual(company_name, driver.find_element_by_id("broker_tag").get_attribute("value"))
                break
            except: pass 
        else: self.fail("FAIL! --Demo URL was not correspondent to Company name or not filled")     
        print "\n'" + company_name + ".insly.com' was set as Demo URL"
        driver.find_element_by_id("prop_company_profile").click()
        Select(driver.find_element_by_id("prop_company_profile")).select_by_visible_text("Other")
        driver.find_element_by_id("prop_company_no_employees").click()
        Select(driver.find_element_by_id("prop_company_no_employees")).select_by_visible_text("1-5")
        driver.find_element_by_id("prop_company_person_description").click()
        Select(driver.find_element_by_id("prop_company_person_description")).select_by_visible_text("I am doing something else")
        
        driver.find_element_by_id("broker_admin_email").send_keys("forinslytestassignment+" + str(timestamp) + "@gmail.com")    
        print "\n'forinslytestassignment+" + str(timestamp) + "@gmail.com was set as work e-mail"
        driver.find_element_by_id("broker_admin_name").send_keys("Accountant Manager")
        driver.find_element_by_link_text("suggest a secure password").click()
        password = driver.find_element_by_xpath("//div[@id='insly_alert']/b").text
        print "\n'" + password + "' was suggested and taken into use as a password"
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button.primary").click()
        driver.find_element_by_id("broker_admin_phone").send_keys(timestamp)
        
        driver.find_element_by_link_text("terms and conditions").click()
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button.primary").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Terms and conditions'])[2]/following::span[1]").click()
        print "\n'Term and conditions' was opened and set as 'agreed'"
        driver.find_element_by_link_text("privacy policy").click()
        element = driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='XII. AMENDMENTS TO THE PRIVACY POLICY'])[1]/following::div[1]")
        element.location_once_scrolled_into_view
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Privacy Policy'])[1]/following::span[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='privacy policy'])[1]/preceding::span[1]").click()
        print "\n'Privacy and policy' was opened, scrolled and set as 'agreed'"
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='privacy policy'])[1]/following::span[1]").click()
        print "\n'Processing of personal data' was set as 'agreed'"
        
        WebDriverWait(driver, 90).until(EC.element_to_be_clickable((By.ID, "submit_save")))
        driver.find_element_by_id("submit_save").click()
        
        WebDriverWait(driver, 900).until(EC.title_contains(company_name))
        print "\nDemo page with '" + company_name + "' in title was opened" 
        print "\n  TEST IS PASSED"


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
