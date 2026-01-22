const puppeteer = require('puppeteer-core');

async function scanPage(url) {
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: true 
        });
    const page = await browser.newPage();

    page.on("console", msg => {
        if (msg.text().includes('XSS_SUCCESS')){
            console.log('Vunlerability Found: payload exectued in DOM!');
        }
    });

    const payload = "';console.log('XSS_SUCCESS');//";
    const targetUrl = `${url}#name=${encodeURIComponent(payload)}`;

    console.log(`Scanning: ${targetUrl}`);

    try {
        await page.goto(targetUrl, { waitUntil: 'networkidle0', timeout: 450000 });

        const buttonSelector = '#submit-btn';
        if (await page.$(buttonSelector)) {
            await page.click(buttonSelector);
        }
    } catch (err) {
        console.error("Scan Failed: ", err.message);
    } finally {
        await browser.close();
        console.log("Scan Completed");
    }

}


scanPage('https://docs.browser-use.com/quickstart');