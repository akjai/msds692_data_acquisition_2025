from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Step 1. Create a browser
    # Can use chromium/firefox/webkit
    browser = p.chromium.launch(headless=False)
    # Step 2. Create a new BrowserContext
    context = browser.new_context()
    # Step 3. Open a page
    page = context.new_page()
    page.goto("https://www.youtube.com/channel/UCA61H4fWOMHikLcUFKyQUog")
    time.sleep(2)
    page.click("#thumbnail")
    time.sleep(10)
    browser.close()