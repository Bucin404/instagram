import os,requests,getpass,json,io,time, random
from datetime import datetime
import re, string, uuid, hashlib, hmac, urllib
from time import sleep
from bs4 import BeautifulSoup as bs
#from PIL import Image, ImageOps
from colorama import init, Fore, Back, Style
current = datetime.now()

init(convert=True)

biru = Fore.BLUE
kuning = Fore.YELLOW
merah = Fore.RED
putih = Fore.WHITE
cyan = Fore.CYAN
hijau = Fore.GREEN
hitam = Fore.BLACK
reset = Style.RESET_ALL
bg_merah = Back.RED
bg_kuning = Back.YELLOW
bg_hijau = Back.GREEN
bg_biru = Back.BLUE
bg_putih = Back.WHITE

header = {"Host": "i.instagram.com",
          'accept' : '*/*',
          'referer': 'https://www.instagram.com/',
          'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
          'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

url = 'https://i.instagram.com/api/v1/'
device = {
'manufacturer'      : 'Xiaomi',
'model'             : 'HM 1SW',
'android_version'   : 18,
'android_release'   : '4.3'
}
useragent = 'Instagram 9.2.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**device)
ig_sig_key = '012a54f51c49aa8c5c322416ab1410909add32c966bbaa0fe3dc58ac43fd7ede'
sig_key_versi = '4'

BASE_URL = "https://www.instagram.com/"
LOGIN_URL = BASE_URL + "accounts/login/ajax/"
USER_AGENT = 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
CHANGE_URL = "https://www.instagram.com/accounts/web_change_profile_picture/"
CHNAGE_DATA = {"Content-Disposition": "form-data", "name": "profile_pic", "filename":"profilepic.jpg","Content-Type": "image/jpeg"}
headers = {
    "Host": "www.instagram.com",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.instagram.com/accounts/edit/",
    "X-IG-App-ID": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive",
}

class igeh:
      def __init__(self, user, pas):
            self.cok = None
            self.status = 0
            self.username_id = None
            self.rank_token = None
            self.token = None
            self.fullname = None
            self.phone = None
            self.username = user
            self.password = pas
            m = hashlib.md5()
            m.update(user.encode('utf-8') + pas.encode('utf-8'))
            self.device_id = self.getDeviceId(m.hexdigest())
            self.uuid = self.getUUID(True)

      def update(self):
            return (self.session, self.status, self.password, self.username, self.token, self.cok)

      def login(self):
            self.session = requests.Session()
            self.session.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : useragent})
            response = self.session.get(f'{url}si/fetch_headers/?challenge_type=signup&guid={self.getUUID(False)}')
            if response.status_code == 200:
                 data = {'phone_id'   : self.getUUID(True),
                        '_csrftoken' : response.cookies['csrftoken'],
                        'username'   : self.username,
                        'guid'       : self.uuid,
                        'device_id'  : self.device_id,
                        'password'   : self.password,
                        'login_attempt_count' : '0'}
                 response = self.session.post(f'{url}accounts/login/', data=self.getSignature(json.dumps(data)))
                 load = json.loads(response.text)
                 if "logged_in_user" in str(response.text):
                         self.id = load["logged_in_user"]["pk"]
                         self.rank_token = "%s_%s" % (self.id, self.uuid)
                         self.token = response.cookies["csrftoken"]
                         self.username_id = self.id
                         self.phone = load["logged_in_user"]["phone_number"]
                         self.fullname = load["logged_in_user"]["full_name"]
                         self.cok = response.cookies
                         self.status = 1

                 elif "checkpoint_required" in str(response.text):
                         self.status = 2
                 elif "Please wait a few minutes before you try again." in str(response.text):
                         self.status = 3
                 elif "ip_block" in str(response.text):
                         self.status = 4
                 else:
                         self.status = 5

      def getSignature(self, data):
             try:
                  parse = urllib.parse.quote(data)
             except AttributeError:
                  parse = urllib.quote(data)

             return f'ig_sig_key_version={sig_key_versi}&signed_body={hmac.new(ig_sig_key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).hexdigest()}.{parse}'

      def getUUID(self, type):
             generated_uuid = str(uuid.uuid4())
             if (type):
                 return generated_uuid
             else:
                 return generated_uuid.replace('-', '')

      def getDeviceId(self, seed):
             volatile_seed = "12345"
             m = hashlib.md5()
             m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
             return 'android-' + m.hexdigest()[:16]

def sessionLog(user, pas):
      sesi = igeh(user, pas)
      sesi.login()
      session, status, password, username, token, cok = sesi.update()
      if status == 1:
           cookies = f'csrftoken={cok["csrftoken"]};ds_user_id={cok["ds_user_id"]};rur={cok["rur"]};sessionid={cok["sessionid"]}'
           return (session, username, password, token, cookies)

      elif status == 2:
           exit("{bg_kuning}{putih}:INFO:{reset} {biru}CHECKPOINT, {hijau}Periksa akun anda!!")
      elif status == 3:
           exit("{bg_merah}{putih}:INFO:{reset} {biru}LIMIT, {hijau}Tunggu beberapa menit lagi / Gunakan akun lain!!{reset}")
      elif status == 4:
           exit("{bg_merah}{putih}:INFO:{reset} {biru}IP BLOCK, {hijau}Tunggu beberapa menit!!")
      else:
           exit("{bg_merah}{putih}:INFO:{reset} {biru}Username / Password salah!!{reset}")

def crop_image(poto, width, height):
      try:
          im = Image.open(poto)
          resize = im.resize((width, height), Image.ANTIALIAS)
          resize.save("tes_crop.jpeg", "JPEG")
          return True
      except:
          return False
px = [
"asecx:sabar123@144.168.227.250:80",
"asecx:sabar123@168.90.199.107:80",
"asecx:sabar123@168.90.199.245:80",
"asecx:sabar123@107.174.248.120:80"
]
server = "http://"+random.choice(px)
class proxies:
    def __init__(self):
        self.http_proxy  = server
        self.https_proxy = server
        self.ftp_proxy   = server
        self.proxyDict = {
                      "http"  : self.http_proxy,
                      "https" : self.https_proxy,
                      "ftp"   : self.ftp_proxy
                    }

    def get_proxy(self):
        return self.proxyDict

class web:
      def __init__(self, u, p):
           self.username = u
           self.password = p
           self.session = requests.Session()
           self.session.headers.update({
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Host': 'www.instagram.com',
                        'Referer': 'https://www.instagram.com/',
                        'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                        'X-Instagram-AJAX': '1',
                        'X-Requested-With': 'XMLHttpRequest'
                    })

      def login(self):
             enc_pass = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(time.time()), self.password)
             self.session.cookies.update({
                        'sessionid': '', 'mid': '', 'ig_pr': '1',
                        'ig_vw': '1920', 'csrftoken': '',
                        's_network': '', 'ds_user_id': ''
                    })
             self.session.get('https://www.instagram.com/web/__mid')
             self.session.headers.update({'X-CSRFToken': self.session.cookies.get_dict()['csrftoken']})
             login_data = {'username':self.username,"enc_password":enc_pass}
             login_resp = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True)
             if login_resp.json()['authenticated']:
                    return True, self.username
             else:
                    return False, self.username

             self.session.headers.update({'X-CSRFToken': self.session.cookies.get_dict()['csrftoken']})


      def change(self, cookies, pil):
           self.session.get('https://www.instagram.com/web/__mid')
           self.session.headers.update(headers)
           self.session.headers.update({'X-CSRFToken': self.session.cookies.get_dict()['csrftoken']})
           try:
                 if pil == 2:
                    try:
                        cek = open("tes_crop.jpeg", "rb")
                        os.system("rm tes_crop.jpeg")
                    except: pass
                    if crop_image(profile, 320, 320):
                        gambar = open("tes_crop.jpeg", "rb")
                        p_pic = bytes(gambar.read())
                        p_pic_s = len(p_pic)
                 else:
                      resp = requests.get('https://source.unsplash.com/random/320x320').content
                      p_pic = bytes(resp)
                      p_pic_s = len(p_pic)
                 self.session.headers.update({'Content-Length' : str(p_pic_s)})
                 files = {'profile_pic': p_pic}
                 r = self.session.post(CHANGE_URL, files=files, data=CHNAGE_DATA, cookies={"cookie":cookies})
                 if pil == 2:
                      os.system("rm tes_crop.jpeg")
                 if r.json()['changed_profile']:
                      return True
                 else:
                      return False
           except:
                  pass

      def post_photo(self, pil, email_new):
           status = 0
           stop = 0
           total = 1
           try:
               try:
                  cek_akun = [val.split(" | ")[0] for val in open("akun1.txt").read().splitlines()]
               except:
                  cek_akun = ["AseCx"]
               if not self.username in cek_akun:
                   sesi, username, password, token, cookies = sessionLog(self.username, self.password)
                   if len(foto) != 0:
                       total = len(foto)
                   while (stop < total):
                        stop += 1
                        if pil == 2:
                            try:
                                cek = open("tes_crop.jpeg", "rb")
                                os.system("rm tes_crop.jpeg")
                            except: pass
                            if crop_image(foto[stop], 600, 720):
                                gambar = open("tes_crop.jpeg", "rb")
                                p_pic = bytes(gambar.read())
                                p_pic_s = len(p_pic)
                        else:
                             resp = requests.get('https://source.unsplash.com/random/320x320').content
                             p_pic = bytes(resp)
                             p_pic_s = len(p_pic)
                        microtime = int(datetime.now().timestamp())
                        sesi.headers.update({
                             "content-type": "image / jpg",
                             "X-Entity-Name" : f"fb_uploader_{microtime}",
                             "Offset": "0",
                             "User-Agent": useragent,
                             "x-entity-length": str(p_pic_s),
                             "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {microtime}, "upload_media_height": 1080, "upload_media_width": 1080}}',
                             "x-csrftoken": token,
                             "x-ig-app-id": "1217981644879628"
                        })
                        upload = sesi.post(f"https://i.instagram.com/rupload_igphoto/fb_uploader_{microtime}", data=p_pic).json()
                        if upload["status"] == "ok":
                              sesi.headers.update({
                                  'Content-Length': str(p_pic_s),
                                  'content-type': 'application/x-www-form-urlencoded',
                                  "origin": "https://www.instagram.com",
                                  "referer": "https://www.instagram.com/create/details/",
                                  'user-agent': useragent,
                                  "x-csrftoken": token,
                                  "x-ig-app-id": "1217981644879628",
                                  "X-Requested-With": "XMLHttpRequest"
                              })
                              data = {
                                  "source_type":"library",
                                  "caption":"",
                                  "upcoming_event":"",
                                  "upload_id":microtime,
                                  "usertags":"",
                                  "custom_accessibility_caption":"",
                                  "disable_comments":"0",
                              }
                              config = sesi.post("https://i.instagram.com/api/v1/media/configure/", data=data).json()
                              if pil == 2:
                                   os.system("rm tes_crop.jpeg")
                              if config["status"] == "ok":
                                    status += 1

                   if status != 0:
                       if self.change(cookies, pil):
                            with open("akun.txt","a") as f:
                                f.write(username+" | sabar123\n")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Status   {merah}: {putih}LOGIN{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Username {merah}: {cyan}{username}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Password {merah}: {cyan}sabar123{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Email    {merah}: {cyan}{email_new}{reset}")
                            print(f"{bg_hijau}{hitam}:INFO:{Style.RESET_ALL} {Fore.BLUE}Profile picture changed {Fore.GREEN}& {Fore.BLUE}Uploaded {Fore.GREEN}{status} {Fore.BLUE}photos  {Fore.WHITE}({Fore.GREEN}DONE{Fore.WHITE}){Style.RESET_ALL}")
                       else:
                            with open("akun.txt","a") as f:
                                 f.write(username+" | sabar123\n")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Status   {merah}: {putih}LOGIN{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Username {merah}: {cyan}{username}") 
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Password {merah}: {cyan}sabar123{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Email    {merah}: {cyan}{email_new}{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Uploaded {hijau}{status} {biru}photos {putih}({hijau}DONE{putih}){reset}")
                   else:
                       if self.change(cookies, pil):
                            with open("akun.txt","a") as f:
                                f.write(username+" | sabar123\n")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Status   {merah}: {putih}LOGIN{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Username {merah}: {cyan}{username}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Password {merah}: {cyan}sabar123{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Email    {merah}: {cyan}{email_new}{reset}")
                            print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Profile picture changed {putih}({hijau}DONE{putih}){reset}")
                       else:
                            print(f"{bg_merah}{hitam}:INFO:{reset} {merah}Something went wrong{reset}")

           except: pass

list_mail = ["vintomaper.com","tovinit.com","mentonit.net"]
url_ = "https://cryptogmail.com/"
header_ = {'Connection' : 'close',
           'Accept' : '*/*',
           'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
           'Cookie2' : '$Version=1',
           'Accept-Language' : 'en-US',
           'User-Agent' : useragent}

def banner():
     os.system("clear")
     print(f"""{reset}
     {biru}__________________  __
    /  _/ ____/ ____/ / / /{reset}{bg_kuning}{hitam}M{reset}{hijau}ass
    {biru}/ // / __/ __/ / /_/ /{reset}{bg_kuning}{hitam}C{reset}{hijau}reate
  {biru}_/ // /_/ / /___/ __  /{reset}{bg_kuning}{hitam}A{reset}{hijau}ccount
 {biru}/___/\____/_____/_/ /_/{reset}{bg_kuning}{hitam}I{reset}{hijau}nstagram
{bg_kuning}{hitam}::{reset} {bg_merah}{putih}Coded by AseCx From XiuzCode{reset} {bg_kuning}{hitam}::{reset}
{merah}──────────────────────────────{reset}""")

def get_teks(accept, key):
        cek = requests.get(url_+"api/emails/"+key, headers={"accept": accept}).text
        if "error" in cek:
                return "-"
        else:
                return cek

def get_random(digit):
        lis = list("abcdefghijklmnopqrstuvwxyz0123456789")
        dig = [random.choice(lis) for _ in range(digit)]
        return "".join(dig), random.choice(list_mail)

def run(email):
        result = []
        no = 0
        while True:
                no += 1
                if no >= 50:
                     break
                try:
                        raun = requests.get(url_+"api/emails?inbox="+email).text
                        if "404" in raun:
                                continue
                        elif "data" in raun:
                                z = json.loads(raun)
                                for data in z["data"]:
                                        res = get_teks("text/html,text/plain",data["id"])
                                        sc = bs(res.encode("utf-8"), "html.parser")
                                        cs = sc.find("td", attrs={"style":"padding:10px;color:#565a5c;font-size:32px;font-weight:500;text-align:center;padding-bottom:25px;"}).text
                                        result.append(str(cs))
                                        requests.delete(url_+"api/emails/"+data["id"])
                                break
                        else:
                                continue
                except (KeyboardInterrupt,EOFError):
                                break
        return result

ambil = requests.Session()
ambil.headers.update({
"Host": "www.fakemail.net",
"Connection": "keep-alive",
"User-Agent": "Mozilla/5.0 (Linux; Android 5.1; A1601) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36",
"Accept": "application/json, text/javascript, */*; q=0.01",
"X-Requested-With": "XMLHttpRequest",
"Origin": "https://www.fakemail.net",
"Referer": "https://www.fakemail.net/",
})

def get_mail(name):
    email = None
    data1 = {
            "email":name,
            "format":"json"
           }
    cek_mail = ambil.post("https://www.fakemail.net/index/email-check/", data=data1).text
    if "ok" in str(cek_mail):
        data2 = {
            "emailInput":name,
            "format":"json"
        }
        new_mail = ambil.post("https://www.fakemail.net/index/new-email/", data=data2).text
        if "ok" in str(new_mail):
             new = ambil.get("https://www.fakemail.net/index/index").text
             email = re.findall('\"email\":\"(.*?)\",', str(new))[0]

    return email

def get_code():
    code = None
    no = 0
    while True:
        no += 1
        if no >= 100:
            break
        inbox = ambil.get("https://www.fakemail.net/index/refresh").text
        if "is your Instagram" in str(inbox):
             get_code = re.findall('\"predmetZkraceny\":\"(.*?)\",', str(inbox))
             code = re.findall('(\d+)', str(get_code))
             break

    return code

def create(pil):
            session = requests.Session()
            sesi = requests.Session()
            session.headers.update(header_)
            #serve = proxies().get_proxy()
            #sesi.proxies = serve
            #session.proxies = serve
            while True:
              try:
                 set_name, set_email = get_random(3)
                 ran = requests.get("https://randomuser.me/api/").json()
                 set_name = f'{str(ran["results"][0]["name"]["first"])}_{set_name}'.upper()
                 headerr = {
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Host': 'www.instagram.com',
                        'Referer': 'https://www.instagram.com/',
                        'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                        'X-Instagram-AJAX': '1',
                        'X-Requested-With': 'XMLHttpRequest'
                        }
                 sesi.headers.update(headerr)
                 sesi.cookies.update({
                        'sessionid': '', 'mid': '', 'ig_pr': '1',
                        'ig_vw': '1920', 'csrftoken': '',
                        's_network': '', 'ds_user_id': ''
                       })
                 sesi.get('https://www.instagram.com/web/__mid')
                 sesi.headers.update({'X-CSRFToken': sesi.cookies.get_dict()['csrftoken']})
                 email_new = get_mail(set_name)
                 suges = sesi.post("https://www.instagram.com/accounts/username_suggestions/", data={"email": email_new, "name": str(ran["results"][0]["name"]["first"]).upper()}).json()
                 usernam = suges["suggestions"][0]
                 uudi = random.choice(["YCMpBgABAAEI3BpsACCjB0aLRmYC"])
                 dat = {
                     "device_id": str(uudi),
                     "email": email_new
                     }
                 send = session.post(f"{url}accounts/send_verify_email/", data=dat).json()
                 try:
                     if send["email_sent"]:
                         try:
                             codec = get_code()[0]
                         except:
                             break
                         print (f"{bg_biru}{putih}:INFO:{reset} {hijau}Waiting for OTP code....{reset}")
                         check = session.post(f"{url}accounts/check_confirmation_code/", data={"code":codec,"device_id": str(uudi),"email":email_new}).json()
                         print (f"{bg_biru}{putih}:INFO:{reset} {cyan}Verification successful with code{hijau}({putih}{codec}{hijau}){reset}")
                         enc_pass = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(time.time()), "sabar123")
                         sesi.post("https://www.instagram.com/web/consent/check_age_eligibility/", data={"day":"14", "mont":"5", "year":"1998"})
                         data = {
                                  "email": email_new,
                                  "enc_password": enc_pass,
                                  "username": usernam,
                                  "first_name": str(ran["results"][0]["name"]["first"]).upper(),
                                  "month": "5",
                                  "day": "14",
                                  "year": "1998",
                                  "client_id": str(uudi),
                                  "seamless_login_enabled":"1",
                                  "tos_version":"row",
                                  "force_sign_up_code": check["signup_code"],
                                  }
                         buat = sesi.post("https://www.instagram.com/accounts/web_create_ajax/", data=data).json()
                         try:
                               if buat["account_created"] == True:
                                   if pil == 99:
                                        with open("akun.txt","a") as f:
                                              f.write(usernam+" | sabar123\n")
                                        print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Status   {merah}: {putih}LOGIN{reset}")
                                        print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Username {merah}: {cyan}{usernam}")
                                        print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Password {merah}: {cyan}sabar123{reset}")
                                        print (f"{bg_hijau}{hitam}:INFO:{reset} {biru}Email    {merah}: {cyan}{email_new}{reset}")
                                   elif pil == 1:
                                       web(usernam, "sabar123").post_photo(pil, email_new)
                                   elif pil == 2:
                                       web(usernam, "sabar123").post_photo(pil, email_new)
                                   print (f"{merah}──────────────────────────────{reset}\n")
                                   break

                         except KeyError:
                               if "checkpoint_required" in str(buat):
                                   print (f"{bg_kuning}{hitam}:INFO:{reset} {biru}Status   {merah}: {kuning}CHECKPOINT{reset}")
                                   print (f"{bg_kuning}{hitam}:INFO:{reset} {biru}Username {merah}: {cyan}{usernam}{reset}")
                                   print (f"{bg_kuning}{hitam}:INFO:{reset} {biru}Password {merah}: {cyan}sabar123{reset}")
                                   print (f"{bg_kuning}{hitam}:INFO:{reset} {biru}Email    {merah}: {cyan}{email_new}{reset}")
                                   print (f"{merah}──────────────────────────────{reset}\n")
                                   with open("akun-cp.txt","a") as f:
                                        f.write(usernam+" | "+email_new+" | sabar123"+" | "+buat['checkpoint_url']+"\n") 
                                   break

                               else:
                                   print ("{bg_merah}{putih}:INFO:{reset} {biru}Status   {putih}: {merah}FAILLED{reset}")
                                   #print (buat)
                                   print (f"{merah}──────────────────────────────{reset}\n")
                                   sleep(15)
                                   break

                 except KeyError:
                       break

              except json.decoder.JSONDecodeError:
                     break
              except requests.exceptions.ConnectionError:
                     print (f"{bg_merah}{putih}:INFO:{reset} {merah}Jaringan Tidak Stabil ....{reset}")
                     sleep(3)
                     break
              except: pass

            create(pil)

def menu_app():
    global profile, foto
    profile = None
    foto = []
    banner()
    #print (f"{hijau}({merah}1{hijau}) {putih}Mass Create Account Instagram Normal")
    print (f"{hijau}({merah}1{hijau}) {putih}Mass Create Account Instagram + Random photos{reset}")
    print (f"{hijau}({merah}2{hijau}) {putih}Mass Create Account Instagram + Own photos{reset}")
    pil = int(input(f"{kuning}>>> {putih}"))
    if pil == 100:
       banner()
       create(pil)
    elif pil == 1:
       banner()
       create(pil)
    elif pil == 2:
       stop = 0
       banner()
       profile = input("\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mMasukan foto profile \x1b[32;1m(\x1b[37;1mprofile.jpg\x1b[32;1m) \x1b[31;1m: \x1b[32;1m")
       count = int(input("\x1b[32;1m(\x1b[31;1m?\x1b[32;1m) \x1b[36;1mMau upload foto berapa? \x1b[31;1m: \x1b[32;1m"))
       while (stop < count):
           stop += 1
           foto.append(input(f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mMasukan gambar Ke-\x1b[37;1m{stop} \x1b[32;1m(\x1b[37;1m{stop}.jpg\x1b[32;1m) \x1b[31;1m: \x1b[32;1m"))
       print (f"\x1b[31;1m──────────────────────────────\n")
       create(pil)
    else:
       print (f"{hijau}({merah}!{hijau}) {merah}Pilihan tidak ada..!{reset}")
       sleep(3)
       menu_app()

if __name__ == "__main__":
    tahun = current.year
    bulan = current.month
    hari = current.day
    batas = f'{bulan}{hari}{tahun}'
    exp = requests.get("https://ase-xc.com/tools/ig/apikey.php", headers={"user-agent": "Mozilla/5.0 (Linux; Android 6.0; A1601) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"}).json()
    for i in exp["data"]:
            if int(i["no"]) == 1:
                if int(batas) >= int(i["exp"]):
                    exit('{bg_merah}{putih}:INFO:{reset} {merah}Maaf masa aktif sudah habis..{reset}')
                else:
                    #banner()
                    #create(1)
                    menu_app()



