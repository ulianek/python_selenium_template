import PIL
import shutil

from Modules.Helpers.folders_helper import create_folder_if_not_exists
from Modules.Helpers.javascript_helper import scroll_to_height, get_inner_height, get_entire_height, remove_element
from Tests.config import Config


def get_screenshots_of_entire_page(driver, location, file_name, merge=True, remove_el=None):
    help_location = location

    remove_element(remove_el)

    if merge is True:
        create_folder_if_not_exists(Config.SCREENSHOT_HELP_PATH)

    entire_page_height = get_entire_height(driver)
    windows_height = get_inner_height(driver)
    current_height = 0
    iterator = 0
    images = []
    path = (location + file_name + "_part_" + str(iterator) + ".png")
    driver.get_screenshot_as_file((location + file_name + "_part_" + str(iterator) + ".png"))
    images.append(path)

    while (current_height + windows_height) < entire_page_height:
        iterator += 1
        current_height = current_height + windows_height
        scroll_to_height(driver, current_height)

        path = (location + file_name + "_part_" + str(iterator) + ".png")
        driver.get_screenshot_as_file((location + file_name + "_part_" + str(iterator) + ".png"))
        images.append(path)

    if merge is True:
        merge_images(images, help_location, file_name)


def merge_images(list_im, location, file_name):
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

    shutil.rmtree(Config.SCREENSHOT_HELP_PATH)
