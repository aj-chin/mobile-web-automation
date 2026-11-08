
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_experimental_option(
        "mobileEmulation",
        {"deviceName": "Pixel 7"}
    )

    browser = webdriver.Chrome(options=options)

    try:
        yield browser
    finally:
        browser.quit()
