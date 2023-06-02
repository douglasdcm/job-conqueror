from src.crawler.generic import Generic
from src.crawler.company import Company
from pytest import mark, fixture


@mark.functional
class TestCrawler:
    @fixture
    def setup(self):
        crawler = Generic("any_locator")
        crawler.initialize()
        yield crawler
        crawler.quit()

    def test_get_all_companies_from_csv(self):
        companies = Company().get_all()[1]

        assert companies.get("locator") == '//a[contains(@title,"Veja detalhes")]'
        assert companies.get("url") == "https://www.dqrtech.com.br/vagas/"
        assert companies.get("active") is not None

    def test_all_crawler_types_run_succesfully(self, setup, setup_db):
        crawler = setup
        assert crawler.run() is True
