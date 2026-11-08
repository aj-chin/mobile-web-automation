# Mobile Web Automation with Selenium

An end-to-end mobile web automation project using **Python, Selenium, and pytest**.

The project automates a user journey on Twitch's mobile website using Chrome's Pixel 7 device emulation. It follows the Page Object Model (POM) and separates website-specific interactions from reusable browser utilities.

## Tech Stack

- Python 3.12
- Selenium 4.38.0
- pytest 8.4.2
- Google Chrome with Pixel 7 mobile emulation
- GitHub Codespaces

## Test Scenario

The automated test performs the following workflow:

1. Launch Chrome in headless mode with Pixel 7 mobile emulation.
2. Navigate to Twitch and open the Browse page.
3. Search for `StarCraft II`.
4. Open the StarCraft II category.
5. Wait for streamer cards to appear.
6. Scroll down twice.
7. Identify the first streamer card visible in the viewport.
8. Open the selected stream.
9. Wait for the stream page to load and verify that the video player is displayed.
10. Capture a screenshot when the test passes.

The test validates category and streamer navigation using URL checks.

**Note:** Video player verification checks that the player element is visible and has nonzero dimensions. It does not verify video playback or audio output.

## Project Structure

```text
mobile-web-automation/
├── .devcontainer/
│   └── devcontainer.json
├── pages/
│   └── twitch/
│       └── twitch_page.py
├── utils/
│   └── browser_actions.py
├── tests/
│   ├── conftest.py
│   └── twitch/
│       ├── config.py
│       └── test_twitch_search.py
├── screenshots/
│   ├── success/
│   └── failure/
├── requirements.txt
├── pytest.ini
└── README.md
```

Python package initialization files (`__init__.py`) are omitted for readability.

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `tests/twitch/test_twitch_search.py` | Defines the test workflow and assertions |
| `pages/twitch/twitch_page.py` | Contains Twitch-specific locators and page interactions |
| `utils/browser_actions.py` | Provides reusable browser operations |
| `tests/twitch/config.py` | Stores Twitch test configuration and timing values |
| `tests/conftest.py` | Creates and closes the Selenium WebDriver |

## Setup

### Option 1: GitHub Codespaces

The repository includes a `.devcontainer/devcontainer.json` configuration for the development environment.

1. Open the repository on GitHub.
2. Select **Code → Codespaces → Create codespace on main**.
3. Wait for the environment setup to complete.
4. Open the terminal and run the test.

The devcontainer configuration installs the required dependencies and Google Chrome.

### Option 2: Local Environment

Requirements:

- Python 3.12
- Google Chrome
- pip

Clone the repository and install dependencies:

```bash
git clone https://github.com/aj-chin/mobile-web-automation.git
cd mobile-web-automation
python -m pip install -r requirements.txt
```

Selenium Manager handles ChromeDriver management when a compatible Chrome installation is available.

## Running Tests

Run all tests:

```bash
python -m pytest -v -s
```

Run the Twitch test only:

```bash
python -m pytest tests/twitch/test_twitch_search.py -v -s
```

The `-v` flag enables verbose test output, while `-s` displays console messages.

## Screenshots

After a successful test, a screenshot is saved to:

```text
screenshots/success/<streamer_name>_<timestamp>.png
```

Screenshot files are excluded from Git tracking through `.gitignore`.

The `screenshots/failure/` directory is reserved for potential future failure screenshot support.

## Design Decisions

### Page Object Model

Twitch-specific locators and interactions are encapsulated in `TwitchPage`, keeping the test focused on the user workflow and expected results.

### Reusable Browser Utilities

`BrowserActions` provides common operations such as clicking, entering text, scrolling, and checking whether an element intersects the viewport.

This separation allows additional website Page Objects to reuse browser functionality.

### Mobile Emulation

Chrome is configured to emulate a Pixel 7, allowing the test to exercise Twitch's mobile web interface in a headless environment.

### Explicit and Fixed Waits

Explicit waits are used for element interaction, streamer card availability, and navigation.

Fixed delays are retained for search results, scrolling, and initial player loading, where the interface may update asynchronously.

### Dynamic Streamer Selection

The test selects the first displayed streamer card intersecting the current viewport after scrolling.

This avoids relying on a fixed streamer name, which may become unavailable as live content changes.

## Limitations and Future Improvements

- **Dynamic content:** Twitch's live streamer availability and page structure can change.
- **Timing:** Fixed delays can increase execution time and may be insufficient under slow network conditions.
- **Playback validation:** The test verifies player visibility but does not confirm that video frames are playing.
- **Failure screenshots:** Automatic screenshot capture on failure is not currently implemented.
- **Browser coverage:** The test currently runs on Chrome with Pixel 7 emulation.

Potential improvements include condition-based waits, richer failure diagnostics, additional test scenarios, and broader device coverage.

## Test Execution Demo

The following GIF shows a live Selenium test run using Chrome's Pixel 7 mobile emulation.

![Twitch mobile automation demo](recordings/twitch_test.gif)