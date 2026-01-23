import asyncio
from playwright.async_api import async_playwright

async def get_dom_content(url, selector):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')

        await page.wait_for_selector(selector)

        elements = await page.query_selector_all(selector)

        results = []
        for el in elements:
            results.append({
                "text": await el.inner_text(),
                "svg": await el.get_attribute("svg"),
            })
        await browser.close()
        return results