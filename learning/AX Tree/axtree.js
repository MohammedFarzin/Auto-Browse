const puppeteer = require('puppeteer-core');

async function getAxtree(url) {
    const browser = await puppeteer.launch({executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: true });
    const page = await browser.newPage();
    await page.goto(url);

    const client = await page.target().createCDPSession();
    const axtree = await client.send('Accessibility.getFullAXTree');
    console.log(axtree);
    console.log(JSON.stringify(axtree, null, 2));
    await browser.close();
}

getAxtree('https://playwright.dev/python/docs/intro');