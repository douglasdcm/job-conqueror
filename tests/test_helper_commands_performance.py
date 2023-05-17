from src.helper.commands import overwrite
from tests.settings import DATABASE_STRING
from pytest import fixture, mark
from src.crawler.generic import Generic
from os import getcwd


@mark.nonfunctional
class TestPerformanceCommands:

    def test_update_get_data_from_1500_links(self):
        companies = [
            {
                "crawler": Generic("//a"),
                "url": "file:///" + getcwd() + "/tests/resources/p_15000_links.html#",
            }
        ]
        assert overwrite(DATABASE_STRING, companies) is True
