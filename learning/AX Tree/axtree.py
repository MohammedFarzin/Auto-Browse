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
        print(axtree['nodes'][0].keys())
        
        for node in axtree['nodes']:
            print("nodeId: ", node['nodeId'])

            print("ignored: ", node.get('ignored', ''))
            if node.get('ignored', ''):
                print("--------------------------------")
                continue
            print("role: ", node.get('role', ''))
            print("chromeRole: ", node.get('chromeRole', ''))
            print("name: ", node.get('name', ''))
            print("properties: ", node.get('properties', ''))
            print("childIds: ", node.get('childIds', ''))
            print("backendDOMNodeId: ", node.get('backendDOMNodeId', ''))
            print("frameId: ", node.get('frameId', ''))
            print("--------------------------------")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_axtree("https://qa-lyncs.pioapp.net/batch-control"))