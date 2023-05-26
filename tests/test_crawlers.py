from src.crawler.generic import Generic
from src.crawler.company import Company
from tests.resources.fake_driver import FakeDriver
from pytest import mark


@mark.functional
class TestCrawler:
    def test_get_all_companies_from_csv(self):
        companies = Company().get_all()[1]

        assert companies.get("locator") == '//a[contains(@title,"Veja detalhes")]'
        assert companies.get("url") == "https://www.dqrtech.com.br/vagas/"
        assert companies.get("active") is not None

    def test_all_crawler_types_run_succesfully(self, setup_db, monkeypatch):
        crawler = Generic(FakeDriver(), "any_locator")
        assert crawler.run() is True
