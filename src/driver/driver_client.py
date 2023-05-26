from src.exceptions.exceptions import WebDriverError
from caqui.synchronous import get_session, close_session
from src.settings import DRIVER_URL


class DriverClient:
    def __init__(self):
        self._session = None

    def start(self):
        capabilities = {
            "desiredCapabilities": {
                "browserName": "firefox",
                "marionette": True,
                "acceptInsecureCerts": True,
            }
        }
        try:
            self._session = get_session(DRIVER_URL, capabilities)
            return True
        except Exception as error:
            raise WebDriverError("Session to WebDriver not opened") from error

    def quit(self):
        try:
            close_session(DRIVER_URL, self._session)
            return True
        except Exception as error:
            raise WebDriverError("Session of WebDriver not closed") from error
