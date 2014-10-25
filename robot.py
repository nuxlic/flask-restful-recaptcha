from time import sleep
import urllib
from selenium.webdriver import Firefox

class Element(object):
    def __init__(self, element):
        print "Initializing Element"
        self.element = element

class Textbox(Element):
    def set_text(self, value):
        print "Setting Text to Element"
        self.element.send_keys(value)

class Button(Element):
    def click(self):
        print "Clicking Element"
        self.element.click()

class CaptchaPage():
    def __init__(self):
        print "Captcha Page Initializing"
        self.driver = Firefox()
        self.driver.get("http://localhost:5000/captcha/")

    def download_sound(self, path):
        print "Downloading Sound to: "  + path
        self.driver.find_element_by_xpath('//*[@id="recaptcha_switch_audio"]').click()
        url = self.driver.find_element_by_xpath('//*[@id="recaptcha_audio_download"]').get_attribute('href')
        urllib.urlretrieve(url, path)

    def get_captcha_textbox(self):
        print "Getting Captcha Textbox"
        return Textbox(self.driver.find_element_by_xpath('//*[@id="recaptcha_response_field"]'))

    def get_submit_button(self):
        print "Getting Submit Form Button"
        return Button(self.driver.find_element_by_xpath("/html/body/form/input"))

    def close(self):
        print "Closing Captcha Page"
        self.driver.close()


if __name__ == "__main__":
    captcha_page = CaptchaPage()
    captcha_page.download_sound("/tmp/captcha.mp3")
    captcha_page.get_captcha_textbox().set_text("HOLAA")
    captcha_page.get_submit_button().click()
    captcha_page.close()