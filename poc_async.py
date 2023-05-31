import asyncio
import time
from logging import info
from src.crawler.generic_async import Generic
from src.crawler.company import Company
from os import getcwd
from src.exceptions.exceptions import CommandError
from os import environ

BASE_DIR = getcwd()
ROOT_DIR = BASE_DIR + "/caqui/src"
TEST_DIR = BASE_DIR + "/tests"


async def collect_data():
    companies = Company().get_all()
    for company in companies:
        # if company["active"].upper() != "Y":
        #     continue
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


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        collect_data(),
        collect_data(),
        collect_data(),
    )


start = time.time()

asyncio.run(main())

end = time.time()
print(f"Time: {end-start:.2f} sec")
