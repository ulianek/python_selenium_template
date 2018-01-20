import PIL
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pip._vendor.distlib._backport import shutil
from Modules.config import Config


class WebDriverMobile(WebDriver):
    help_screenshots_path = "Screenshots_help/"

    def __init__(self, url, desired_caps):
        super().__init__(url, desired_caps)


    def wait_for_element_and_click(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        WebDriverWait(self, time).until(
            EC.element_to_be_clickable(element)
        )
        self.find_element(*element).click()

    def wait_for_element_and_send_text(self, element, text, time=Config.DEFAULT_WAIT_TIME, clear=True):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        if clear:
            self.find_element(*element).clear()
        self.find_element(*element).send_keys(text)

    def wait_for_text_in_element(self, element, text, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.text_to_be_present_in_element_value(element, text)
        )



    # def check_if_element_is_visible(self, element, time=15):
    #     try:
    #         WebDriverWait(self, time).until(
    #             EC.presence_of_element_located(element)
    #         )
    #         return True
    #     except TimeoutException:
    #         return False

    def check_if_element_is_invisible(self, element, time=Config.DEFAULT_WAIT_TIME):
        try:
            WebDriverWait(self, time).until(
                EC.invisibility_of_element_located(element)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_and_get_text(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element).text

    def wait_for_element_and_get_text_from_input(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element).get_attribute("value")

    def wait_and_get_element(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element)

    def wait_and_get_elements(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_elements(*element)

    def wait_for_element(self, element, time=Config.DEFAULT_WAIT_TIME):
        try:
            WebDriverWait(self, time).until(
                EC.presence_of_element_located(element)
            )
        except:
            pass

    def wait_for_element_until_invisible(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.invisibility_of_element_located(element)
        )

    def check_if_element_is_visible(self, element, time=15):
        self.wait_for_element(element, 2)
        elements = self.find_elements(*element)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_screenshots_of_entire_page(self, location, file_name, merge=True, remove_element=None):

        help_location = location
        try:
            if remove_element is not None:
                self.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", remove_element)

        except:
            pass

        if merge is True:
            location = self.help_screenshots_path
            if not os.path.exists(location):
                os.makedirs(location)

        entire_page_height = self.execute_script("return document.body.scrollHeight")
        windows_height = self.execute_script("return window.innerHeight")
        current_height = 0
        iterator = 0
        images = []
        path = (location + file_name + "_part_" + str(iterator) + ".png")
        self.get_screenshot_as_file((location + file_name + "_part_" + str(iterator) + ".png"))
        images.append(path)

        while ((current_height + windows_height) < entire_page_height):
            iterator += 1
            current_height = current_height + windows_height
            self.execute_script("window.scrollTo(0, " + str(current_height) + ");")

            path = (location + file_name + "_part_" + str(iterator) + ".png")
            self.get_screenshot_as_file((location + file_name + "_part_" + str(iterator) + ".png"))
            images.append(path)

        if merge is True:
            self.merge_images(images, help_location, file_name)

    def merge_images(self, list_im, location, file_name):

        from PIL import Image
        import numpy as np

        imgs = [PIL.Image.open(i) for i in list_im]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        # imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
        #
        # # save that beautiful picture
        # imgs_comb = PIL.Image.fromarray(imgs_comb)
        # imgs_comb.save('Trifecta.jpg')

        # for a vertical stacking it is simple: use vstack
        imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)

        imgs_comb.save(location + file_name + '.png')

        shutil.rmtree(self.help_screenshots_path)
