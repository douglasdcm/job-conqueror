import time
from src.crawler.generic_async import Generic
from pytest import mark, fixture
from os import getcwd


@mark.functional
class TestCrawler:
    @fixture
    def setup(self, request):
        # crawler = Generic("//a")
        crawler = Generic('//a[contains(@title,"Veja detalhes")]')

        def quit():
            crawler.quit()

        request.addfinalizer(quit)
        return crawler

    @mark.asyncio
    async def test_get_all_links(self, setup):
        start = time.time()

        crawler = setup
        await crawler.initialize()

        BASE_DIR = getcwd()

        crawler.set_url(f"https://www.dqrtech.com.br/vagas/")
        # crawler.set_url(f"file:///{BASE_DIR}/tests/resources/p_many_links.html")
        await crawler.run()

        end = time.time()
        print(f"Time: {end-start:.2f} sec")
