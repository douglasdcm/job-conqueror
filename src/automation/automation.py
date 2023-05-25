from logging import info
from selenium.webdriver.support import wait
from src.settings import TIMEOUT
from src.exceptions.exceptions import WebDriverError
from os import environ
from caqui import synchronous
from src.settings import DRIVER_URL, CAPABILITIES


class BaseObjects:
    def __init__(self, driver):
        self._driver = driver
        self._wait = wait.WebDriverWait(driver, TIMEOUT)

    def get_all_elements(self, by_type, locator):
        try:
            info("Getting all elements '{}:{}'".format(by_type, locator))
            elements = self._driver.find_elements(by_type, locator)
            if not elements:
                message = "No elements found. Skipping process"
                print(message)
                info(message)
            return elements
        except Exception as error:
            WebDriverError(f"Could not get elements. {str(error)}")

    def get_attribute_from_element(self, element, attribute):
        if environ.get("DEBUG") == "on":
            info("Getting attribute {} from element {}".format(attribute, element))
        return element.get_attribute(attribute)

    def navigate_to(self, url, timeout=TIMEOUT):
        info("Navigate to '{}'".format(url))
        session = synchronous.get_session(DRIVER_URL, CAPABILITIES)
        try:
            synchronous.go_to_page(DRIVER_URL, session, url)
        except Exception as error:
            raise WebDriverError(str(error)) from error
        finally:
            synchronous.close_session(DRIVER_URL, session)

    def get_text(self, by_type, locator):
        session = synchronous.get_session(DRIVER_URL, CAPABILITIES)
        try:
            element = synchronous.find_element(DRIVER_URL, session, by_type, locator)
            return synchronous.get_text(DRIVER_URL, session, element)
        except Exception as error:
            raise WebDriverError(str(error)) from error
        finally:
            synchronous.close_session(DRIVER_URL, session)
