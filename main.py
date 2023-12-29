import locale  # Yerel zaman için
import os  # İşletim sistemi ile ilgili işlemleri yapmamıza sağlayan kütüphane
import random  # Rastgele değer atayabilmek için
import time  # Zaman için
import webbrowser  # Tarayıcıyı açabilmek için
from datetime import datetime  # Tarihi almak için
import speech_recognition as sr  # Sesi tanımak için
from gtts import gTTS  # Yazıyı sese çevirmek için
from playsound import playsound  # Ses dosyalarını çalmak için
from selenium import webdriver # Webde gezinti için
from selenium.webdriver.common.by import By #Linke tıklatmak için kullandım bunu sadece
import requests # Hava durumu kısmında siteden bu kütüphane sayesinden güncel veri çektik
from bs4 import BeautifulSoup # Hava durumu için
import cv2  # Foto alma için


#tts : text to speech kısaltması bunu ingilizce kullanmayı tercih ettim
#audio genel ses için bunu ,
#voice mikrofondan gelen ses için bunu
#Asistanın sesi için ise voice değişken ismi verdim

locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8') #TR zaman dilimini ekledim

r = sr.Recognizer()# Ses tanıma
current_datetime = datetime.now() # Anlık tarih almak için


def kaydet(soyle=False):
    voice ="" # Aşşağıda dediğimizi anlayamayınca voice değişkenine değer atayamadığı için hata verip sonlanmaması için

    with sr.Microphone() as source: # Sesi varsayılan aygıttan alıyorum
        if soyle:
            print(soyle)
        audio = r.listen(source) # boş değer atıyoruz voice içine
        try:
            voice = r.recognize_google(audio, language="tr-TR") # Bilgileri googlede aratıp sonuç buluyor

        except sr.UnknownValueError: # Söylediğimiz Kelimeleri anlayamazsa diye     
            konus("Anlayamadım") 
            print("Asistan: Anlayamadım")
        return voice
    

def yanitla(voice):
                  
        if "merhaba" in voice:
            konus("merhaba")
            print("Asistan:Merhaba")

        elif "selam" in voice:
            konus("selam")
            print("Asistan: Selam")

        if  "nasılsın" in voice:
            konus("İyiyim sen nasılsın")
            print("Asistan: İyiyim sen nasılsın")

        if "teşekkür ederim" in voice or "teşekkürler" in voice :
            konus("rica ederim")
            print("Asistan: Rica Ederim")

        elif "görüşürüz" in voice or "kapan" in voice:
            konus("görüşürüz")
            print("Görüşürüz")
            exit()

        elif "bugün ayın kaçı" in voice :
            gun = current_datetime.day  
            konus(str(gun)) #konus fonksiyonumuz metin ifadeleri sese çevirdiği için stringe dönüştürüyorum

        elif "bugün hangi gün" in voice or "bugün günlerden ne" in voice or "hangi gündeyiz" in voice:
        
            
            today= time.strftime("%A") # modülün türkçeye çevirisi sıkıntılı olduğu için aşşağıdaki koşulları yaptım

            today.capitalize()
            if today == "Monday":
                today = "Pazartesi"

            elif today == "Tuesday":
                today = "Salı"

            elif today == "Wednesday":
                today = "Çarşamba"

            elif today == "Thursday":
                today = "Perşembe"

            elif today == "Friday":
                today = "Cuma"

            elif today == "Saturday":
                today = "Cumartesi"

            elif today == "Sunday":
                today = "Pazar"

            konus(today)
        elif "saat kaç" in voice:
            secenekler = ["Saat şu an:", "hemen bakıyorum", "saat", "Bir bakayım, saat:"]
            saat = datetime.now().strftime("%H:%M")
            secenekler = random.choice(secenekler)
            konus(str(secenekler + saat)) 
        elif "google'a gir" in voice or "arama yap" in voice:
            devam_et = True
            konus("Ne aramamı istersin?")
            while devam_et:

                try:
                    arama = kaydet()
                    konus("{} ile ilgili  bulduklarımı listeliyorum".format(arama))
                    url = "https://www.google.com/search?q={}".format(arama) # Arama yapmak için
                    webbrowser.get().open(url) #Yukarda oluşturduğumuz url'i google'da sadece aratmak için
                    time.sleep(3)
                    konus("Tekrar Arama Yapmak ister misin")
                    arama = kaydet()
                    if arama == "Evet":
                        konus("Ne aramamı istersin?")
                        continue
                    elif arama =="Hayır":
                        devam_et = False
                        konus("Peki")
                except sr.UnknownValueError:
                    konus("Anlayamadım")
                    print("Asistan: Anlayamadım")
                    continue
        elif "not et" in voice or "not al" in voice:
            konus("Dosya ismi ne olsun")
            txtdosyasi = kaydet() + ".txt"
            konus("Ne kaydetmek istiyorsun")
            txt = kaydet()
            d = open(txtdosyasi, "w", encoding="utf-8") # Ascii veya başka bir şey olarak çalıştırmaması
            # için ve türkçe karakterler olduğu için utf-8 ekliyorum
            konus("Notunu kaydettim")
            d.writelines(txt)
            d.close()
            return
        elif "youtube'u aç" in voice or "müzik aç" in voice or "video aç" in voice:
            devam_et=True
            konus("Ne açmamı istersin")
            while devam_et:
                istek = kaydet()
                try:
                    konus("{} açılıyor".format(istek))
                    url = "https://www.youtube.com/results?search_query={}".format(istek)
                    tarayici = webdriver.Chrome()
                    tarayici.get(url)
                    tarayici.find_element(By.XPATH, "//*[@id='video-title']/yt-formatted-string").click()
                    time.sleep(7)
                    konus("Bir daha açmak ister misin".format(istek))
                    istek = kaydet()
                    if istek == "Evet":
                        konus("Ne açmamı istersin")
                        continue
                    elif istek == "Hayır":
                        konus("youtube'dan çıkıyorum")
                        return

                except sr.UnknownValueError:  # Söylediğimiz Kelimeleri anlayamazsa diye
                    konus("Anlayamadım")
                    print("Asistan: Anlayamadım")
        elif "film aç" in voice:
            try:
                konus("hangi filmi açayım")
                film = kaydet()
                konus("{} filmini açıyorum")
                tarayici = webdriver.Chrome()
                url = "https://www.google.com/search?q={} filmini full izle".format(film)
                tarayici.get(url)
                tarayici.find_element(By.XPATH,"//*[@id='rso']/div[2]/div/div/div[1]/div/div/span/a/h3").click()
                time.sleep(300) # Sebebini bilmediğim bir şekilde tarayıcıyı açık bırakna komutu normalde çalışmasına rağmen burda çalışmadığı için bunu kullandım
            except sr.UnknownValueError:
                konus("Anlayamadım")
                return
        elif "film izlemek istiyorum" in voice:
            konus("hangi tür film istersin")

            filmtur = kaydet()

            try:
                konus("{} türü için bulduğum filmler bunlar")
                tarayici = webdriver.Chrome()
                url = "https://filmmodutv.com/film-kategori/{}".format(filmtur)
                tarayici.get(url)
                konus("Eğer kararsızsan sana film önerisinde bulunmak istiyorum")
                cevap = kaydet()
                print(cevap)
                if cevap =="evet" or "tamam" or "olur":
                    konus("Filmini hemen seçiyorum")
                    tarayici.find_element(By.XPATH, "//*[@id='listehizala']/div[1]/div/div[3]/a/div").click()
                    konus("keyifli seyirler")

                else:
                    konus("Keyifli seyirler")
                tarayici.quit()
            except sr.UnknownValueError:
                    konus("Anlayamadım")
                    print("Asistan: Anlayamadım")
        elif "hava durumu tahmini" in voice or "hava durumu" in voice or "bugün hava nasıl" in voice:
            konus("Hangi şehrin hava durumunu istersin")
            cevap = kaydet()
            print(cevap)

            def HavaRaporlari(gununIndexi):

                url = "https://havadurumu15gunluk.xyz/havadurumu/630/{}-hava-durumu-15-gunluk.html".format(cevap)

                response = requests.get(url) # Belirtilen şehrin hava durumu bilgilerini çekmek için

                if response.status_code == 200:
                    # print("İŞLEM BAŞARILI")
                    soup = BeautifulSoup(response.text, "html.parser")
                    # print(soup)

                    tumVeriler = soup.find_all("tr")[gununIndexi].text # Belirli  güne ait hava durumu bilgilerini atıyorm
                    tumVeriler = tumVeriler.replace("Saatlik", "").strip()
                    print(tumVeriler)

                    gunluk_hava = ""

                    gunduz_sicaklik = tumVeriler[-6:-4]
                    gece_sicaklik = tumVeriler[-3:-1]
                    print("Gunduz Sıcaklık: " + gunduz_sicaklik)
                    print("Gece Sıcaklık: " + gece_sicaklik)

                    tumVeriler = tumVeriler[6:-6].strip()

                    gunun_ismi = tumVeriler[:3]

                    gunKisaltma = ["Sal", "Çar", "Per", "Cum", "Cmt", "Paz", "Pzt"]

                    for x in gunKisaltma:
                        if x in tumVeriler:
                            gunluk_hava = tumVeriler.replace(x, "")

                    print("Hava Durumu: " + gunluk_hava)

                    gununIsimleri = {"Paz": "Pazartesi", "Pzt": "Pazartesi", "Sal": "Salı", "Çar": "Çarşamba",
                                     "Per": "Perşembe", "Cum": "Cuma", "Cmt": "Cumartesi"}
                    gunun_ismi = gununIsimleri[gunun_ismi]
                    print("Gunun Adı: " + gunun_ismi)

                    return "{} için {} günün hava raporları şu şekilde: Hava: {} Gündüz Sıcaklığı: {} derece Gece Sıcaklığı: {} derece". \
                        format(cevap, gunun_ismi, gunluk_hava, gunduz_sicaklik, gece_sicaklik)

                else:
                    print("Hata meydana geldi")

            konus("{} şehir için yarının mı yoksa 5 günlük raporlarını mı istersiniz".format(cevap))
            cevap2 = kaydet().lower()
            print(cevap2)

            if cevap2 in "yarının":

                konus(HavaRaporlari(2))
            else:
                sayac = 1

                while sayac < 6:
                    konus(HavaRaporlari(sayac))
                    sayac += 1
        elif "fotoğraf çek" in voice:
            konus("Kameranı hemen açıyorum")

            kamera = cv2.VideoCapture(0) #  Bilgisayardaki kameradan görüntü almak için cv2 kütüphanesinin VideoCapture fonksiyonu kullanılıyor. 0, bilgisayardaki ilk kamerayı temsil eder.

            kontrol, resim = kamera.read() # Kamera değişkeninden görüntü alarak resim değişkenine kaydediyom

            konus("Gülümse çekiyorum...")

            cv2.imwrite("deneme.jpg", resim) # resim değişkenindeki görüntüyü deneme.jpg adında bir dosyaya kaydediyorum

            kamera.release() # Kamera kaynağı serbest bırakılıyor.

            cv2.destroyAllWindows() #Açık olan tüm OpenCV pencereleri kapatılıyor.

            time.sleep(2)

            konus("fotoğrafınızı görmek istiyor musunuz")
            cevap = kaydet()

            if cevap in "Evet":
                resim = cv2.imread("deneme.jpg") # "deneme.jpg" dosyasındaki resim resim değişkenine okunuyor.
                cv2.imshow("Deneme Resim 1", resim) # Okunan resim, "Deneme Resim 1" adıyla bir pencerede gösteriliyor.
                cv2.waitKey(0)
                cv2.destroyAllWindows()

def konus(metin):
     tts = gTTS(text=metin, lang="tr", slow=False) # fonksiyona gönderilen metni temsil ediyor bu parametre
     dosya = "cevap.mp3" # Ses dosyamız 
     tts.save(dosya) # Ses dosyasını kaydediyorum
     playsound(dosya) # Ses dosyasını çalıyorum
     os.remove(dosya) # İşimiz bitince ses dosyasını silmesi için bu da

playsound("giris.mp3")



while True:
    voice = kaydet() # Mikrofoondan aldığım sesi voice değişkeninin içine attım
    if voice != '':
        voice = voice.lower() # Bizden duyduğu sese karşılık cevap alacağımız zaman büyük harf olmasını istememesi için
        print(voice.capitalize()) # Mikrofona gelen sesi yazdırıyo ve Yazdırırken ilk harfi büyütüyor
        yanitla(voice)
