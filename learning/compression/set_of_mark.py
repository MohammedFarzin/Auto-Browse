import asyncio
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont


async def compress_content(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)


        screenshot_bytes = await page.screenshot()
        with open("screenshot.png", "wb") as f:
            f.write(screenshot_bytes)


        selectors = 'button, a, input, [role="button"], textarea'
        elements = await page.query_selector_all(selectors)

        compressed_text = []

        img = Image.open("screenshot.png").convert("RGB")
        draw = ImageDraw.Draw(img)

        count = 0

        for i, el in enumerate(elements):
            box = await el.bounding_box()
            if not box or box['width'] < 2 or box['height'] < 2:
                continue

            count += 1
            draw.rectangle([box['x'], box['y'], box['x']+box['width'], box['y']+box['height']], outline="red", width=2)
            draw.rectangle([box['x'], box['y']-15, box['x']+20, box['y']], fill="red")
            draw.text((box['x']+2, box['y']-15), str(count), fill="white")

            text_content = (await el.inner_text() or await el.get_attribute("placeholder") or "" ).strip()[:20]
            compressed_text.append(f"[{count}] {el.evaluate('e => e.tagName')}: {text_content} ({int(box['x'])}, {int(box['y'])})")

        
        img.save("compressed_screenshot.png")
        text_output = "\n".join(compressed_text)
        print(f"--- Visual Context Saved to compressed_vision.png ---")
        print(f"--- Text Context ({len(text_output)} bytes) ---")
        print(text_output)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(compress_content("https://docs.browser-use.com/quickstart"))