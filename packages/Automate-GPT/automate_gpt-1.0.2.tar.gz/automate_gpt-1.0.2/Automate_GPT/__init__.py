from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from undetected_chromedriver import Chrome
from time import sleep
from pyperclip import paste

class ChatGPTAutomation:
    Search = "//*[@aria-label='Search']"
    Stop = "//*[@aria-label='Stop streaming']"
    Copy = './/*[@data-testid="copy-turn-action-button"]'
    User_msg = './/*[@data-message-author-role="user"]'
    def __init__(self,driver:Chrome):
        self.driver:Chrome = driver
        self.actions:ActionChains = ActionChains(driver)
        self.driver.get("https://chatgpt.com/")
    def element_is_present(self,rootemem:WebElement,xpath: str):
        try:
            rootemem.find_element(By.XPATH,xpath)
            return True
        except NoSuchElementException:
            return False
    
    def chat(self,prompt: str):
        sleep(1)
        self.actions.key_down(Keys.SHIFT).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).key_up(Keys.SHIFT).perform()
        textarea = self.driver.switch_to.active_element
        self.actions.send_keys_to_element(textarea,prompt).perform()
        textarea.submit()
        sleep(2)
        while True:
            if not self.element_is_present(self.driver,self.Stop):
                sleep(1)
                self.actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('c').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
                sleep(0.5)
                break
            else:
                sleep(1)
        return paste()
    
    def reset_chat(self):
        self.actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('o').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
    def is_search_enable(self):
        return self.driver.find_element(By.XPATH,self.Search).get_attribute("aria-pressed") == "true"
    def search_enable(self,enable_permission:bool=True):
        if not(self.is_search_enable() == enable_permission):
            self.driver.find_element(By.XPATH,self.Search).click()
    def get_conversation(self):
        conv:list[dict[str,str]] = []
        for i in self.driver.find_elements(By.TAG_NAME,"article"):
            if self.element_is_present(i,self.User_msg):
                conv.append({"user":i.text.removeprefix("You said:\n")})
            else:
                copybtn = i.find_element(By.XPATH,self.Copy)
                self.actions.scroll_to_element(copybtn).perform()
                self.actions.click(copybtn).perform()
                sleep(0.5)
                conv.append({"assistant":paste()})
        return conv