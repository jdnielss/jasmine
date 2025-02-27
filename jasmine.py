import requests, json, subprocess, os, random, string, urllib.parse, re, time, urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from telethon.sync import TelegramClient, functions
from telethon.tl import types
from termcolor import colored
from dotenv import load_dotenv
from requests_toolbelt import MultipartEncoder
from googlesearch import search

load_dotenv()
TELE_ID = os.getenv("TELE_ID")
TELE_HASH = os.getenv("TELE_HASH")
TELE_NUMBER = os.getenv("TELE_NUMBER")

banks = {"bca": "BCA", "mandiri": "Mandiri", "bni": "BNI", "bri": "BRI", "bsm": "BSI (Bank Syariah Indonesia)", "bca_syr": "BCA Syariah", "btn": "BTN / BTN Syariah", "cimb": "CIMB Niaga / CIMB Niaga Syariah", "dbs": "DBS Bank Indonesia", "btpn": "BTPN / Jenius / BPTN Wow!", "kesejahteraan_ekonomi": "Seabank / Bank BKE", "danamon": "Danamon / Danamon Syariah", "muamalat": "Muamalat", "artos": "Bank Jago", "hana": "LINE Bank / KEB Hana", "royal": "blu by BCA Digital", "nationalnobu": "Nobu (Nationalnobu) Bank", "permata": "Bank Permata", "bii": "Maybank Indonesia", "panin": "Panin Bank", "uob": "TMRW / UOB", "ocbc": "OCBC NISP", "citibank": "Citibank", "artha": "Bank Artha Graha Internasional", "standard_chartered": "Standard Chartered Bank", "anz": "ANZ Indonesia", "hsbc": "HSBC Indonesia", "mayapada": "Bank Mayapada", "bjb": "BJB", "dki": "Bank DKI Jakarta", "daerah_istimewa": "BPD DIY", "jawa_tengah": "Bank Jateng", "jawa_timur": "Bank Jatim", "jambi": "Bank Jambi", "sumut": "Bank Sumut", "sumatera_barat": "Bank Sumbar (Bank Nagari)", "riau_dan_kepri": "Bank Riau Kepri", "sumsel_dan_babel": "Bank Sumsel Babel", "lampung": "Bank Lampung", "kalimantan_selatan": "Bank Kalsel", "kalimantan_barat": "Bank Kalbar", "kalimantan_timur": "Bank Kaltimtara", "kalimantan_tengah": "Bank Kalteng", "sulselbar": "Bank Sulselbar", "sulut": "Bank SulutGo", "nusa_tenggara_barat": "Bank NTB Syariah", "bali": "BPD Bali", "nusa_tenggara_timur": "Bank NTT", "maluku": "Bank Maluku", "papua": "Bank Papua", "bengkulu": "Bank Bengkulu", "sulawesi": "Bank Sulteng", "sulawesi_tenggara": "Bank Sultra", "sinarmas": "Bank Sinarmas", "maspion": "Bank Maspion Indonesia", "ganesha": "Bank Ganesha", "mega": "Bank Mega", "mega_syr": "Bank Mega Syariah", "commonwealth": "Commonwealth Bank", "aceh": "Bank Aceh Syariah"}
wallets = {"ovo": "OVO", "dana": "DANA", "linkaja": "LinkAja", "gopay": "GoPay", "shopeepay": "ShopeePay"}
fids, iids, rids, gids, tids, lids, nids, sids = [], [], [], [], [], [], [], []
ins, gov, docs = [], [], []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Sec-Fetch-Mode": "navigate",
}

class Api:
    def Ewallet(bank, number):
        try: return requests.post('https://cekrekening-api.belibayar.online/api/v1/account-inquiry', json={ "account_bank": bank, "account_number": number }).json()
        except: return None

class Telegram:
    def Auth():
        client = TelegramClient(TELE_NUMBER, TELE_ID, TELE_HASH)
        client.start(phone=TELE_NUMBER)
        return client

    def Get(number):
        try:
            client = Telegram.Auth()
            contact = types.InputPhoneContact(0, number, "", "")
            contacts = client(functions.contacts.ImportContactsRequest([contact]))
            user = contacts.users[0] if contacts.users else None
            if user:
                client(functions.contacts.DeleteContactsRequest([user.id]))
                return f"@{user.username} | {user.first_name} {user.last_name or ''}".strip()
        finally: client.disconnect()

class Web:
    def Facebook(email):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get("https://web.facebook.com/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0")
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "identify_email"))).send_keys(email)
            driver.find_element(By.ID, "did_submit").click()
            with open(f"result/{email}/facebook.jpg", 'wb') as f: f.write(requests.get(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "_2qgu"))).get_attribute("src")).content)
            try: return WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "_xku"))).find_element(By.CLASS_NAME, "_50f6").text.split('\n')[0]
            except: return WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "_alwr"))).find_element(By.CLASS_NAME, "fsl").text
        except: return None
        finally: driver.quit()

    def Whatsapp(number):
        try:
            response = requests.get(f"https://api.whatsapp.com/send/?phone={number.replace('08','628') if number.startswith('08') else number}&text&type=phone_number&app_absent=0").text
            with open(f"result/{number}/whatsapp.jpg", 'wb') as f: f.write(requests.get(BeautifulSoup(response, 'html.parser').find('img', class_='_9vx6')['src']).content)
            return BeautifulSoup(response, 'html.parser').find('h3', class_='_9vd5 _9scb _9scr').text.strip()
        except: return None

class Lookup:
    def Title(url):
        try:
            title = BeautifulSoup(requests.get(url, headers=headers, timeout=1).text, 'html.parser').title.string
            if '...' in title: return url.split('//')[1]
            else: return title.strip().replace(" - ", " ").replace(" | ", " ").split("|")[0].split("-")[0].split("–")[0] if 'Berita' not in title and 'Situs' not in title and 'Portal' not in title and 'Site' not in title else None
        except: return None
    def Social(name, func, number): print(f"   {colored('➥', 'cyan')} {name} : {colored(result, 'cyan')}") if (result := func(number)) else None
    def Bank(number):
        print(f"\n {colored('✿', 'magenta')} Bank account")
        for bank in banks:
            if (data := Api.Ewallet(bank, number))['message'] == 'ACCOUNT FOUND':
                print(f"   {colored('➥', 'cyan')} {banks[bank]} : {colored(data['data']['account_holder'])}")
                break

    def Wallet(number):
        print(f"\n {colored('✿', 'magenta')} E-Wallet")
        for wallet in wallets:
            if (data := Api.Ewallet(wallet, number))['message'] == 'ACCOUNT FOUND':
                print(f"   {colored('➥', 'cyan')} {wallets[wallet]} : {colored(data['data']['account_holder'])}")

class Social:
    def Scrape(url):
        try:
            response = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser").find("meta", attrs={"name": "description"})['content']
            nids.extend(re.findall(r'08\d{8,12}', response))
            sids.extend(re.findall(r'@\w+', response))
        except: return None
    def Lookup(number):
        print(f"\n {colored("✿", "magenta")} Social media")
        Lookup.Social("Facebook", Web.Facebook, number)
        Lookup.Social("Whatsapp", Web.Whatsapp, number)
        Lookup.Social("Telegram", Telegram.Get, number)
    def ID():
        print(f"\n {colored("✿", "magenta")} Related accounts")
        for fid in set(fids): print(f"   {colored('➥', 'cyan')} Facebook : {colored(fid, 'cyan')}")
        for iid in set(iids): print(f"   {colored('➥', 'cyan')} Instagram : {colored(iid, 'cyan')}")
        for lid in set(lids): print(f"   {colored('➥', 'cyan')} Linkedin : {colored(lid, 'cyan')}")
        for rid in set(rids): print(f"   {colored('➥', 'cyan')} Reddit : {colored(rid, 'cyan')}")
        for gid in set(gids): print(f"   {colored('➥', 'cyan')} Github : {colored(gid, 'cyan')}")
        for tid in set(tids): print(f"   {colored('➥', 'cyan')} Twitter : {colored(tid, 'cyan')}")
        for nid in set(nids): print(f"   {colored('➥', 'cyan')} Phone : {colored(nid, 'cyan')}")
        for sid in set(sids): print(f"   {colored('➥', 'cyan')} Etc : {colored(sid, 'cyan')}")
    def Docs(query):
        print(f"\n {colored('✿', 'magenta')} Related documents")
        for doc in set(docs):
            if 'pdf' in doc.split('/')[-1].lower() or 'xlsx' in doc.split('/')[-1].lower() or 'csv' in doc.split('/')[-1].lower():
                with open(f"result/{query}/{doc.split('/')[-1]}", 'wb') as f: f.write(requests.get(doc, headers=headers, verify=False).content)
                print(f"   {colored('➥', 'cyan')} {doc.split('/')[-1]} from {doc.split('/')[2]}")
    def Institute():
        print(f"\n {colored('✿', 'magenta')} Related institutions")
        for i in set(ins):
            title = Lookup.Title(f'https://{i}')
            print(f"   {colored('➥', 'cyan')} {title}") if title else None
    def Government():
        print(f"\n {colored('✿', 'magenta')} Related governments")
        for g in set(gov):
            title = Lookup.Title(f'https://{g}')
            print(f"   {colored('➥', 'cyan')} {title}") if title else None

class Caller:
    def Info(number):
        print(f"\n {colored("✿", "magenta")} Caller info")
        if not os.path.exists(f'result/{number}/getcontact.json'): subprocess.run(['node', 'gtc.js', number], check=True)
        data = json.load(open(f'result/{number}/getcontact.json'))
        with open(f"result/{number}/getcontact.jpg", 'wb') as f: f.write(requests.get(data['picture']).content)
        print(f"   {colored("➥", "cyan")} Name     : {colored(data['name'], "cyan")}")
        print(f"   {colored("➥", "cyan")} Carrier  : {colored(data['provider'], "cyan")}")
        print(f"   {colored("➥", "cyan")} Country  : {colored(data['country'], "cyan")}")

    def Tags(number):
        print(f"\n {colored("✿", "magenta")} Also known as")
        if not os.path.exists(f'result/{number}/getcontact.json'): subprocess.run(['node', 'gtc.js', number], check=True)
        try:
            for tag in json.load(open(f'result/{number}/getcontact.json'))['tags']: print(f"   {colored("➥", "cyan")} {tag}")
        except: print(f"   {colored("➥", "cyan")} {json.load(open(f'result/{number}/getcontact.json'))['name']}")

class Image:
    def Search(image):
        links = []
        with requests.Session() as session:
            session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            
            data = MultipartEncoder(fields={
                'encoded_image': (f"{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}.jpg", open(image, 'rb'), 'image/jpeg'),
                'processed_image_dimensions': (None, '608,879'),
            }, boundary=boundary)

            session.headers.update({
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Cookie': '; '.join([f'{key}={value}' for key, value in session.cookies.items()]),
                'Content-Length': str(data.len),
            })

            response = session.post(f'https://lens.google.com/v3/upload?hl=in&stcs={int(time.time() * 1000)}&vpw=1280&vph=585&ep=subb', data=data)

            try:
                url_finder = re.findall(r'<a href="(https://.*?)"', response.text)
                if url_finder:
                    for encoded_url in url_finder:
                        decoded_url = urllib.parse.unquote(encoded_url).replace("amp;", "")
                        if 'google' not in decoded_url: links.append(decoded_url)
                return links
            except: return None

class Ext:
    def Search(query):
        print(f"\n {colored("✿", "magenta")} Links related to {colored(query, "cyan")}")
        for url in search(query, stop=50):
            print(f"   {colored("➥", "cyan")} {url}")
            fids.append(url.split('&id=')[1]) if '&id=' in url and '&' not in url.split('&id=')[1] and 'facebook' in url else fids.append(url.split('/')[3]) if 'facebook' in url and '?' not in url and '/public/' not in url else None
            iids.append(url.split('/')[3]) if 'instagram' in url else None
            lids.append(url.split('/')[4]) if 'linkedin' in url and '/dir/' not in url else None
            rids.append(url.split('/')[4]) if 'reddit' in url and 'user' in url else None
            gids.append(url.split('/')[3]) if 'github' in url else None
            tids.append(url.split('/')[3]) if 'twitter' in url else None
            docs.append(url) if 'pdf' in url.lower() or 'xlsx' in url.lower() or 'csv' in url.lower() else None
            ins.append(url.split('/')[2]) if '.ac.id' in url else None
            gov.append(url.split('/')[2]) if '.go.id' in url else None
            Social.Scrape(url)
    def Image(image):
        print(f"\n {colored("✿", "magenta")} Links related to {colored(image, "cyan")}")
        for link in Image.Search(image): print(f"   {colored("➥", "cyan")} {link}")

# Just Another Search Module In-case-of Nearly Everything
print(f"\n {colored("✿", "magenta")} Jasmine")
query = input(f"   {colored("➥", "cyan")} Search   : ")
if not os.path.exists(f'result/{query}'): os.makedirs(f'result/{query}')
if query.startswith('08'):
    #Caller.Info(query)
    Lookup.Wallet(query)
    Social.Lookup(query)
    #Caller.Tags(query)
elif query.isnumeric(): Lookup.Bank(query)
elif "@" in query:
    Social.Lookup(query)
    Ext.Search(query.split('@')[0])
Ext.Search(query)
Social.ID()
Social.Institute()
Social.Government()
Social.Docs(query)
for image in [f for f in os.listdir(f'result/{query}') if f.endswith('.jpg')]: Ext.Image(f'result/{query}/{image}')
