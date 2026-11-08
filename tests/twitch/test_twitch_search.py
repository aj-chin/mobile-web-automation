
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from selenium.webdriver.support.ui import WebDriverWait

from pages.twitch.twitch_page import TwitchPage
from tests.twitch.config import (
    CATEGORY_SLUG,
    PLAYER_DELAY,
    SEARCH_KEYWORD,
)


def test_twitch_search(driver):
    twitch = TwitchPage(driver)

    # Open Twitch and navigate to Browse
    twitch.open_twitch()
    twitch.open_browse()

    # Search for the category
    twitch.search_game(SEARCH_KEYWORD)
    twitch.open_category(CATEGORY_SLUG)

    expected_category_path = f"/directory/category/{CATEGORY_SLUG}"

    WebDriverWait(driver, 10).until(
        lambda browser: (
            urlparse(browser.current_url).path
            == expected_category_path
        )
    )

    print(f"Category URL: {driver.current_url}")

    # Wait for streamer cards and scroll twice
    twitch.wait_for_streamers()
    twitch.scroll_streamers()

    # Select the first streamer visible in the viewport
    streamer_card, streamer_name = twitch.get_first_visible_streamer()

    assert streamer_card.is_displayed()
    assert streamer_name, "Selected streamer has no name"

    # Open the selected stream
    twitch.open_streamer(streamer_card)

    expected_stream_path = f"/{streamer_name.lower()}"

    WebDriverWait(driver, 10).until(
        lambda browser: (
            urlparse(browser.current_url).path.lower().rstrip("/")
            == expected_stream_path
        )
    )

    print(f"Stream URL: {driver.current_url}")

    # Verify the player is displayed
    time.sleep(PLAYER_DELAY)

    assert twitch.is_player_displayed(), (
        f"Video player was not displayed for {streamer_name}. "
        f"Current URL: {driver.current_url}"
    )

    # Capture the successful test screenshot
    screenshot_dir = Path("screenshots/success")
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = (
        screenshot_dir / f"{streamer_name}_{timestamp}.png"
    )

    assert driver.save_screenshot(str(screenshot_path)), (
        f"Failed to save screenshot: {screenshot_path}"
    )

    print(f"Screenshot saved: {screenshot_path}")
