import locale  # Yerel zaman için
import os  # İşletim sistemi ile ilgili işlemleri yapmamıza sağlayan kütüphane
import random # Rastgele değer atayabilmek için
import time  # Zaman için
import webbrowser # Tarayıcıyı açabilmek için
from datetime import datetime # Tarihi almak için
from turtle import title

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
import speech_recognition as sr  # Sesi tanımak için
from gtts import gTTS  # Yazıyı sese çevirmek için
from playsound import playsound  # Ses dosyalarını çalmak için
from selenium.webdriver.common.by import By

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
        if "görüşürüz" in voice or "kapan" in voice:
            konus("görüşürüz")
            print("Görüşürüz")
            exit()
        if "bugün ayın kaçı" in voice :
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
        if "saat kaç" in voice:
            secenekler = ["Saat şu an:", "hemen bakıyorum", "saat", "Bir bakayım, saat:"]
            saat = datetime.now().strftime("%H:%M")
            secenekler = random.choice(secenekler)
            konus(str(secenekler + saat)) 
        if "google'a gir" in voice:
            devam_et = True
            konus("Ne aramamı istersin?")
            while devam_et:

                arama = kaydet()
                url = "https://www.google.com/search?q={}".format(arama) # Arama yapmak için
                webbrowser.get().open(url) #Yukarda oluşturduğumuz url'i google'da aratıyorum
                konus("{} için Google'da bulduklarımı listeliyorum".format(arama))
                konus("Tekrar Arama Yapmak ister misin")
                arama = kaydet()
                if arama == "Evet":
                    devam_et = True
                    konus("Ne aramamı istersin?")
                elif arama =="Hayır":
                    devam_et = False
                    konus("Peki")
        if "not et" in voice or "not al" in voice:
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
        if "youtube'u aç" in voice or "müzik aç" in voice or "video aç" in voice:
            devam_et=True
            konus("Ne açmamı istersin")
            while devam_et:
                istek = kaydet()
                try:
                    konus("{} açılıyor".format(istek))
                    url = "https://www.youtube.com/results?search_query={}".format(istek)
                    tarayici = webdriver.Firefox()
                    tarayici.get(url)
                    tarayici.find_element(By.XPATH, "//*[@id='video-title']/yt-formatted-string").click()
                    time.sleep(1)
                    konus("Bir daha {}mak ister misin".format(istek))
                    istek = kaydet()
                    if istek == "Evet":
                        konus("Ne açmamı istersin")
                        continue
                    elif istek == "Hayır":
                        konus("youtube'dan çıkıyorum")
                        break

                except sr.UnknownValueError:  # Söylediğimiz Kelimeleri anlayamazsa diye
                    konus("Anlayamadım")
                    print("Asistan: Anlayamadım")
                    continue








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
