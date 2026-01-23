from playwright.async_api import async_playwright
import json
import asyncio

async def get_axtree(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)

        client = await context.new_cdp_session(page)

        axtree = await client.send("Accessibility.getFullAXTree")
        
        print(json.dumps(axtree, indent=4))
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_axtree("https://docs.browser-use.com/quickstart"))