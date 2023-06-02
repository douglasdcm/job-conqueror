import asyncio
from logging import info
from src.crawler.generic_async import Generic
from os import getcwd
from src.exceptions.exceptions import CommandError
from os import environ
from src.helper.helper import initialize_table
from logging import info
from src.helper.helper import Connection, initialize_table
from src.exceptions.exceptions import CommandError
from os import environ
from src.crawler import generic

MAX_CONCURRENCY = 3
sem = asyncio.Semaphore(MAX_CONCURRENCY)


def get_jobs_data(companies):
    if not Connection.get_database_connection():
        return False
    for company in companies:
        if company["active"].upper() != "Y":
            continue
        crawler = generic.Generic(company["locator"])
        try:
            url = company["url"]
            message = f"Collecting data of company '{url}'"
            print(message)
            info(message)
            message = "Starting crawler for '{}'...".format(url)
            print(message)
            info(message)
            crawler.initialize()
            crawler.set_url(url)
            crawler.run()
            crawler.quit()
            print("Crawler finished.")
        # The execution need to continue even in case of errors
        except Exception as error:
            message = f"Unexpected error occurred while getting jobs data. {str(error)}"
            info(message)
            if environ.get("DEBUG") == "on":
                raise CommandError(str(error))
        finally:
            try:
                crawler.quit()
            except Exception:
                pass
    return True


def sanity_check(companies):
    return get_jobs_data(companies)


def help_():
    return (
        "Commands:\n"
        "--sanity-check    check the installtion and clean the database\n"
        "--help            open the help documentation\n"
        "--overwrite       get the new positions from companies\n"
        "    --clean-db    clean up the database"
    )


async def __collect_data(company):
    async with sem:
        try:
            url = company["url"]
            locator = company["locator"]
            crawler = Generic(locator)
            await crawler.initialize()

            crawler.set_url(url)
            await crawler.run()
        # The execution need to continue even in case of errors
        except Exception as error:
            message = f"Unexpected error occurred while getting jobs data. {str(error)}"
            info(message)
            if environ.get("DEBUG") == "on":
                raise CommandError(str(error))
        finally:
            try:
                crawler.quit()
            except Exception:
                pass


# Reference: https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio
async def __schedule_tasks(companies):
    tasks = [asyncio.ensure_future(__collect_data(company)) for company in companies]
    await asyncio.gather(*tasks)


def overwrite(database_string, companies=None, clean_database=False):
    if clean_database:
        initialize_table(database_string)
    if asyncio.get_event_loop().is_closed() is True:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(__schedule_tasks(companies))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        return True
