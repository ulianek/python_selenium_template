def scroll(driver, scroll_element=None):
    if scroll_element:
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight;', scroll_element)
    else:
        driver.execute_script(
            'document.body.scrollTop = document.body.scrollHeight;')


def scroll_to_height(driver, height):
    driver.execute_script("window.scrollTo(0, " + str(height) + ");")


def remove_element(driver, element=None):
    if element is not None:
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)


def get_entire_height(driver):
    return driver.execute_script("return document.body.scrollHeight")


def get_inner_height(driver):
    return driver.execute_script("return window.innerHeight")
