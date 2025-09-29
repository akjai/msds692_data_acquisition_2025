from playwright.sync_api import sync_playwright
import time


with sync_playwright() as p:
    # Launching a Browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://reddit.com")

    page.wait_for_selector("main")

    # Click the login button and enter id and password.
    page.locator("a", has_text="Log In").click()
    page.locator("#login-username").click()
    page.keyboard.type("ankitjai3000@gmail.com")
    page.keyboard.press("Tab")
    page.keyboard.type("Aj08181999!")
    page.locator("a", has_text="Log In").click()

    # Wheel to go 150 pxl, 1000 pxl
    time.sleep(5)