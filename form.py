import time
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 

class Form():
    def __init__(self):
        chromedriver_autoinstaller.install(cwd=True)
        warnings.simplefilter("ignore", ResourceWarning)

    def _load_config(self):
        with open('./config.txt', encoding="utf-8") as f:
            lines = f.readlines()
        self.config = [l.replace("\n", "") for l in lines]
    
    def open_browser(self):
        self._load_config()
        options = Options()
        if "headless" in self.config:
            options.headless = True
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options = options)

    def scroll_to_button(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def next_page(self):
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '繼續')]"))).click()

    def run(self):
        self.driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeoWWK8qe8y3PkhirrWaKoNIpirbvZQyKljcZaQKkZAqCnnrw/viewform")
        self.scroll_to_button()
        time.sleep(1)

        # p1
        _input = self.driver.find_elements(By.CLASS_NAME, "whsOnd")
        tsf_num, name = _input[0], _input[1]
        tsf_num.send_keys(f"{self.config[0]}")
        tsf_num.submit()
        name.send_keys(f"{self.config[1]}")
        name.submit()

        self.driver.find_elements(By.CLASS_NAME, "AB7Lab")[0].click()
        self.next_page()

        # p2
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.config[2]}')]"))).click()

        drop_down = self.driver.find_elements(By.CLASS_NAME, "MocG8c")
        drop_down[0].click()

        action_key_down = ActionChains(self.driver).move_to_element(drop_down[0]).key_down(Keys.DOWN).key_up(Keys.DOWN)
        action_key_enter = ActionChains(self.driver).move_to_element(drop_down[0]).key_down(Keys.RETURN)
        action_key_down.perform()
        action_key_enter.perform()
        self.next_page()

        # p3
        self.driver.find_elements(By.CLASS_NAME, "uVccjd")[0].click()

        if "test" not in self.config:
            self.driver.find_elements(By.CLASS_NAME, "uArJ5e")[1].click()
        
        try:
            time.sleep(2)
            self.driver.close()
        except:
            pass
        
if __name__ == '__main__':
    form = Form()
    form.open_browser()
    form.run()
