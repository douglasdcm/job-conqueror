from logging import info
from src.exceptions.exceptions import WebDriverError
from os import environ
from caqui import synchronous
from src.settings import DRIVER_URL, CAPABILITIES


class BaseObjects:
    def __init__(self, session):
        self._session = session

    def get_all_elements(self, by_type, locator):
        try:
            info("Getting all elements '{}:{}'".format(by_type, locator))
            elements = synchronous.find_elements(
                DRIVER_URL, self._session, by_type, locator
            )
            if not elements:
                message = "No elements found. Skipping process"
                print(message)
                info(message)
            return elements
        except Exception as error:
            WebDriverError(f"Could not get elements. {str(error)}")

    def get_attribute_from_element(self, element, property):
        if environ.get("DEBUG") == "on":
            info("Getting attribute {} from element {}".format(property, element))
        return synchronous.get_property(DRIVER_URL, self._session, element, property)

    def navigate_to(self, url):
        info("Navigate to '{}'".format(url))
        try:
            synchronous.go_to_page(DRIVER_URL, self._session, url)
        except Exception as error:
            raise WebDriverError(str(error)) from error

    def get_text(self, by_type, locator):
        try:
            element = synchronous.find_element(
                DRIVER_URL, self._session, by_type, locator
            )
            return synchronous.get_text(DRIVER_URL, self._session, element)
        except Exception as error:
            raise WebDriverError(str(error)) from error
