const puppeteer = require('puppeteer-core');

async function getDomContent(url, selector) {
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: true 
        });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 450000 });

    const data = await page.$$eval(selector, (elements) => {
        return elements.map(el => ({
            text: el.innerText.trim(),
            html: el.innerHTML,
            tag: el.tagName,
            attributes: Array.from(el.attributes).reduce((acc, attr) => {
                acc[attr.name] = attr.value;
                return acc;

            }, {}),
        }))
    })

    await browser.close();
    return data;

}



getDomContent('https://docs.browser-use.com/quickstart', 'h2').then(console.log);