import ConfigParser
import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


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

        parser = ConfigParser.ConfigParser()
        base_path = os.path.join(os.environ['HOME'], '.mozilla/firefox/')
        parser.read(os.path.join(base_path, "profiles.ini"))
        profile_path = os.path.join(base_path, filter(lambda x: x[0].lower() == 'path', parser.items('Profile0'))[0][1])
        try:
            profile = FirefoxProfile(profile_path)
        except OSError:
            raise Exception("You must execute the following command:\nsudo chmod +r -R %s" % profile_path)
        self.driver = Firefox(profile)

        self.driver.get("file://%s/index.html" % os.getcwdu())

    def get_url_sound(self):
        self.driver.find_element_by_xpath('//*[@id="recaptcha_switch_audio"]').click()
        return self.driver.find_element_by_xpath('//*[@id="recaptcha_audio_download"]').get_attribute('href')

    def get_recaptcha_challenge_field(self):
        return self.driver.find_element_by_xpath('//*[@id="recaptcha_challenge_field"]').get_attribute('value')

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
    pass