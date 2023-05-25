from src.driver.driver_client import DriverClient
from pytest import mark


@mark.skip()
class TestDriverClient:
    def test_client_close_session(self):
        DriverClient().start()
        assert DriverClient().quit() is True

    def test_client_open_session(self):
        assert DriverClient().start() is True
