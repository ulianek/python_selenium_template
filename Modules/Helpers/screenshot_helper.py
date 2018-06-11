import PIL
import shutil

import os


class ScreenshotHelper(object):

    def __init__(self, driver):
        self.driver = driver

    def get_screenshots_of_entire_page(self, location, file_name, merge=True, remove_element=None):
        help_location = location
        try:
            if remove_element is not None:
                self.driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", remove_element)

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
