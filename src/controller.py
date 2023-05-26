from logging import info
from src.helper.helper import Connection, initialize_table
from src.driver.driver_factory import DriverFactory
from src.exceptions.exceptions import CommandError
from os import environ
from src.crawler import generic


def __finish_driver(chrome):
    chrome.quit()
    message = "Crawler finished."
    print(message)
    info(message)


def get_jobs_data(database_string, companies):
    if not Connection.get_database_connection():
        return False
    for company in companies:
        if company["active"].upper() != "Y":
            continue
        chrome = DriverFactory().get_driver()
        try:
            url = company["url"]
            message = f"Collecting data of company '{url}'"
            print(message)
            info(message)
            message = "Starting crawler for '{}'...".format(url)
            print(message)
            info(message)
            driver_ = chrome.start(url)
            crawler = generic.Generic(driver_, company["locator"])
            crawler.set_url(url)
            crawler.run()
            __finish_driver(driver_)
        # The execution need to continue even in case of errors
        except Exception as error:
            message = (
                f"Unexpected error occurred while getting position data. {str(error)}"
            )
            info(message)
            if environ.get("DEBUG") == "on":
                raise CommandError(str(error))
        finally:
            try:
                __finish_driver(chrome)
            except Exception:
                pass
    return True


def sanity_check(database_string, companies):
    return get_jobs_data(database_string, companies)


def help_():
    return (
        "Commands:\n"
        "--sanity-check    check the installtion and clean the database\n"
        "--help            open the help documentation\n"
        "--overwrite       get the new positions from companies\n"
        "    --clean-db    clean up the database"
    )


def overwrite(database_string, companies=None, clean_database=False):
    message = "Updating positions"
    print(message)
    info(message)
    if clean_database:
        initialize_table(database_string)
    get_jobs_data(database_string, companies)
    print("Update finished")
    return True
