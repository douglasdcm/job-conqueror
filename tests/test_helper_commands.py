from src.controller import help_, get_jobs_data, sanity_check, overwrite
from tests.settings import DATABASE_STRING
from pytest import fixture
from os import getcwd
from pytest import mark


@mark.functional
class TestHelperCommands:
    @fixture
    def get_crashed_crawlers(self):
        return [
            {
                "locator": "//a",
                "url": "file:///" + getcwd() + "/tests/resources/p_crashed_links.html#",
                "active": "Y",
            },
            {
                "locator": "//a",
                "url": "file:///" + getcwd() + "/tests/resources/p_crashed_links.html#",
                "active": "Y",
            },
            {
                "locator": "//a",
                "url": "file:///" + getcwd() + "/tests/resources/p_crashed_links.html#",
                "active": "Y",
            },
        ]

    @fixture
    def populate_db(self, setup_db):
        db = setup_db
        db.salva_registro(
            "positions",
            "url, description",
            "'https://test_message_1.com', 'test_message_1'",
        )
        db.salva_registro(
            "positions",
            "url, description",
            "'https://test_message_2.com', 'test_message_2'",
        )
        db.salva_registro(
            "positions",
            "url, description",
            "'https://test_message_3.com', 'test_message_3'",
        )
        return db

    @fixture
    def get_companies(self):
        return [
            {
                "active": "Y",
                "locator": "//a",
                "url": "file:///" + getcwd() + "/src/resources/sanity_check.html#",
            }
        ]

    def test_update_get_data_from_many_links(self):
        companies = [
            {
                "active": "Y",
                "locator": "//a",
                "url": "file:///" + getcwd() + "/tests/resources/p_many_links.html#",
            }
        ]
        assert overwrite(DATABASE_STRING, companies) is True

    def test_run_by_db_string(self, get_companies):
        assert get_jobs_data(companies=get_companies) is True

    def test_overwrite_database_returns_true(self, get_companies):
        assert overwrite(DATABASE_STRING, get_companies) is True

    def test_sanity_check_works(self, setup_db, get_companies):
        assert sanity_check(get_companies) is True

    def test_help_is_opened(self):
        actual = help_()
        assert "--help" in actual
        assert "--sanity-check"
