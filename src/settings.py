from os import getcwd

BASE_DIR = getcwd()
ROOT_DIR = BASE_DIR + "/src/"
RESOURCES_DIR = ROOT_DIR + "resources/"
DRIVER_DIR = RESOURCES_DIR + "chromedriver"
LOGS_FOLDER = "/webapp/logs/"
DRIVER_URL = "http://127.0.0.1:9999"
CAPABILITIES = {
    "desiredCapabilities": {
        "browserName": "anydriver",
        "acceptInsecureCerts": True,
        "pageLoadStrategy": "eager",
        "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
    }
}

TIMEOUT = 30
TABLE_NAME = "positions"
LOG_FILE = LOGS_FOLDER + "crawler.log"
DATABASE_STRING_DEFAULT = "postgresql://postgres:postgresql@postgres/postgres"
