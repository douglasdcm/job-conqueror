from logging import error as log_info
from src.exceptions.exceptions import WebDriverError, CrawlerError
from os import environ
from src.helper.helper import save_description_to_database, Connection
from src.automation.automation import BaseObjects
from selenium.webdriver.common.by import By


class Generic:
    def __init__(self, driver, locator):
        """
        This is what the name says: a generic crawler. It is intended to be used if the company's
            page has all the links of positions available in a single page without pagination.
            Take the page bellow:
            (...)
                <div class="menu-container">
                    <a class = "menu" herf="www.fake.com">
                </div>
                <div class="positions-container>
                    <a class = "positions" href="www.fake.com/jobs/position_1">
                    <a class = "positions" href="www.fake.com/jobs/position_2">
                    <a class = "positions" href="www.fake.com/jobs/position_3">
                </div>
            (...)
            The locators a.positions (css locator) are the ones we are looking for.
        Arsg:
            locator (str): the locator of the links of positions, e.g. a.positions
        """
        self._url = None
        self._locator = locator
        self._base_objects = BaseObjects(driver)

    def __get_all_job_links(self, locator):
        try:
            by_type = By.XPATH
            elements = self._base_objects.get_all_elements(by_type, locator)
            links = []
            for element in elements:
                links.append(
                    self._base_objects.get_attribute_from_element(element, "href")
                )
            return links
        except Exception as error:
            raise WebDriverError(f"Could not get element(s). {str(error)}")

    def __go_to_page(self, url):
        try:
            self._base_objects.navigate_to(url)
        except Exception as error:
            raise WebDriverError(f"Could not navidate to page {url}. {str(error)}")

    def __save_job_information(self, links):
        for link in links:
            try:
                print(f"Collecting data from postion '{link}'")
                self.__go_to_page(link)
                save_description_to_database(
                    Connection.get_connection_string(),
                    link,
                    self.__get_job_description(),
                )
            except WebDriverError as error:
                message = f"Skipping process. Failed to get data from {link}"
                print(message)
                log_info(message)
                if environ.get("DEBUG") == "on":
                    raise CrawlerError(str(error)) from error
            except Exception as error:
                raise CrawlerError(str(error))
        return True

    def __get_job_description(self):
        try:
            by_type = By.TAG_NAME
            text = ""
            text += " " + self._base_objects.get_text(by_type, "body")
            text += " " + self._base_objects.get_text(by_type, "head")
            return text
        except Exception as error:
            raise WebDriverError(f"Could not get description from page. {str(error)}")

    def set_url(self, url):
        self._url = url

    def run(self):
        self.__go_to_page(self._url)
        links = self.__get_all_job_links(self._locator)
        return self.__save_job_information(links)
