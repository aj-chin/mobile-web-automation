
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.twitch.config import (
    TWITCH_URL,
    SEARCH_DELAY,
)
from tests.twitch.config import SCROLL_COUNT, SCROLL_DELAY

from utils.browser_actions import BrowserActions


class TwitchPage:
    BROWSE_LINK = (By.CSS_SELECTOR, 'a[href="/directory"]')
    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        'input[data-a-target="tw-input"]'
    )
    STREAM_CARDS = (
        By.CSS_SELECTOR,
        'article:has(> button):has(a[href$="/home"])'
    )
    VIDEO_PLAYER = (
        By.CSS_SELECTOR,
        '[data-a-target="video-player"]'
    )

    def __init__(self, driver):
        self.driver = driver
        self.actions = BrowserActions(driver)

    def open_twitch(self):
        self.driver.get(TWITCH_URL)

    def open_browse(self):
        self.actions.click(self.BROWSE_LINK)

    def search_game(self, keyword):
        search_input = self.actions.enter_text(
            self.SEARCH_INPUT,
            keyword
        )
        search_input.send_keys(Keys.ENTER)
        time.sleep(SEARCH_DELAY)

    def open_category(self, slug):
        category_locator = (
            By.CSS_SELECTOR,
            f'a[href="/directory/category/{slug}"]'
        )
        self.actions.click(category_locator)

    def scroll_streamers(self):
        self.actions.scroll_down(
            times=SCROLL_COUNT,
            delay=SCROLL_DELAY
        )

    def wait_for_streamers(self, timeout=10):
        from selenium.webdriver.support.ui import WebDriverWait

        WebDriverWait(self.driver, timeout).until(
            lambda browser: len(
                browser.find_elements(*self.STREAM_CARDS)
            ) > 0
        )


    def get_first_visible_streamer(self):
        cards = self.driver.find_elements(*self.STREAM_CARDS)

        print(f"Total streamer cards: {len(cards)}")

        for card in cards:
            if not card.is_displayed():
                continue

            if not self.actions.is_in_viewport(card):
                continue

            streamer_link = card.find_element(
                By.CSS_SELECTOR,
                'a[href$="/home"]'
            )

            streamer_name = streamer_link.text.strip()

            print(f"Selected streamer: {streamer_name}")

            return card, streamer_name

        raise AssertionError(
            "No visible streamer cards found after scrolling"
        )


    def open_streamer(self, streamer_card):
        thumbnail_button = streamer_card.find_element(
            By.CSS_SELECTOR,
            ":scope > button"
        )

        thumbnail_button.click()


    def is_player_displayed(self):
        players = self.driver.find_elements(*self.VIDEO_PLAYER)

        if not players:
            return False

        player = players[0]
        size = player.size

        print(f"Player dimensions: {size}")

        return (
            player.is_displayed()
            and size["width"] > 0
            and size["height"] > 0
        )
