import time
from datetime import datetime
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait

from pages.twitch.twitch_page import TwitchPage
from tests.twitch.config import SEARCH_KEYWORD, CATEGORY_SLUG
from tests.twitch.config import PLAYER_DELAY

def test_twitch_search(driver):
    twitch = TwitchPage(driver)

    # open browser
    twitch.open_twitch()
    twitch.open_browse()
    print(f"Category URL: {driver.current_url}")

    # perform search
    twitch.search_game(SEARCH_KEYWORD)
    twitch.open_category(CATEGORY_SLUG)
    WebDriverWait(driver, 10).until(
        lambda browser: (
            f"/directory/category/{CATEGORY_SLUG}"
            in browser.current_url
        )
    )
    twitch.wait_for_streamers()
    
    # Scroll twice
    twitch.scroll_streamers()

    # choose the first within view
    streamer_card, streamer_name = twitch.get_first_visible_streamer()
    assert streamer_card.is_displayed()
    assert streamer_name
    print(f"Streamer selected: {streamer_name}")

    # click into stream
    twitch.open_streamer(streamer_card)
    assert "twitch.tv" in driver.current_url

    # wait for stream to load
    time.sleep(PLAYER_DELAY)
    print(f"Stream URL: {driver.current_url}")
    assert twitch.is_player_displayed(), (
        f"Video player was not displayed. "
        f"Current URL: {driver.current_url}"
    )

    # take screenshot
    screenshot_dir = Path("screenshots/success")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = (
        screenshot_dir / f"{streamer_name}_{timestamp}.png"
    )
    screenshot_saved = driver.save_screenshot(
        str(screenshot_path)
    )
    assert screenshot_saved, "Failed to save screenshot"
    print(f"Screenshot saved: {screenshot_path}")
