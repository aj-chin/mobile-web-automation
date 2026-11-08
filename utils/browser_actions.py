
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowserActions:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        return element

    def scroll_down(self, times=2, delay=2):
        import time

        for index in range(times):
            before = self.driver.execute_script(
                "return window.scrollY"
            )

            self.driver.execute_script(
                "window.scrollBy(0, window.innerHeight)"
            )

            time.sleep(delay)

            after = self.driver.execute_script(
                "return window.scrollY"
            )

            print(
                f"Scroll {index + 1}/{times}: "
                f"{before} -> {after}"
            )


    def is_in_viewport(self, element):
        return self.driver.execute_script(
            """
            const rect = arguments[0].getBoundingClientRect();

            return (
                rect.width > 0 &&
                rect.height > 0 &&
                rect.bottom > 0 &&
                rect.right > 0 &&
                rect.top < window.innerHeight &&
                rect.left < window.innerWidth
            );
            """,
            element
        )
