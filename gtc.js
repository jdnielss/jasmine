const { Gtc } = require('gtc-js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const phoneNumber = process.argv[2];

const gtc = new Gtc({
  cookiePath: process.env.GTC_COOKIES,
  showQr: false,
  puppeteer: {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    ignoreDefaultArgs: ['--disable-extensions'],
  },
});

gtc.on('qrcode', (value) => qrcode.generate(value, { small: true }));
gtc.on('logged', async (logged) => {
  if (logged) {
    const tags = await gtc.find('ID', phoneNumber);
    fs.writeFileSync(`./result/${phoneNumber}/getcontact.json`, JSON.stringify(tags, null, 2), 'utf-8');
  } else console.log('Scan QR code first');
});
gtc.on('error', console.error);
(async () => await gtc.init())();