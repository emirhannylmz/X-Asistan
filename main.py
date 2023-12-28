from playsound import playsound #Ses dosyalarını çalmak için
from gtts import gTTS # Yazıyı sese çevirmek için
import speech_recognition as sr # Sesi tanımak için
import pyaudio #
import os # İşletim sistemi ile ilgili işlemleri yapmamıza sağlayan kütüphane
import time # Zaman için
import locale # Yerel zaman için
from datetime import datetime
import random
from random import choice 
import webbrowser
from random import randint
#tts : text to speech kısaltması bunu ingilizce kullanmayı tercih ettim
#audio genel ses için bunu ,
#Asistanın sesi için ise voice değişken ismi verdim
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8') #TR zamanını ekledim

r = sr.Recognizer()# Ses tanıma
current_datetime = datetime.now() # Anlık tarih almak için


def kaydet(soyle=False):
    voice ="" # Aşşağıda dediğimizi anlayamayınca voice değişkenşne değer atayamadığı için hata verip sonlanmaması için 

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
    if "x Asistan" in voice:
        voice = kaydet()
        
            
        if "merhaba" in voice:
            konus("merhaba")
        if "selam" in voice:
            konus("selam")
        if  "nasılsın" in voice:
            konus("İyiyim sen nasılsın")
        if "teşekkür ederim" in voice or "teşekkürler" in voice :
            konus("rica ederim")
        if "görüşürüz" in voice:
            konus("görüşürüz")
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
        if "google'da ara" in voice:

            konus("Ne aramamı istersin?")
            arama = kaydet()
            url = "https://www.google.com/search?q={}".format(arama) # Arama yapmak için
            webbrowser.get().open(url) #Yukarda oluşturduğumuz url'i google'da aratıyorum
            konus("{} için Google'da bulduklarımı listeliyorum".format(arama))
        if "sayı tahmin oyunu oluştur" in voice:
            tahmin_oyunu()

        
        


kolaySeviyeHak = 10
zorSeviyeHak = 5

def zorluk():
    konus("Kolay mı yoksa Zor seviye mi tercih edersiniz")
    tercih = kaydet()
    if tercih =="kolay":
        konus("Oyunu kazanabilmek için 10 hakkın var")
        return kolaySeviyeHak
    elif tercih == "zor":
        konus("oyunu kazanabilmek için 5 hakkın var")
        return zorSeviyeHak

def tahmin_oyunu():
    konus("1 ile 100 arasından bir sayıyı aklımdan tuttum")
    rastgele_sayi = randint(1,100)
    devam_et = True
    kalan_hak = zorluk()
    while devam_et:
        konus("Aklımdan tuttuğum sayıyı tahmin et")
        tahmin = int(kaydet())
        if tahmin > rastgele_sayi:
            kalan_hak -=1
            konus("Fazla attın,daha küçük bir sayı seç. {} adet hakkın kaldı".format(kalan_hak))
        elif tahmin < rastgele_sayi:
            kalan_hak -=1
            konus("Ufak attın, daha büyük bir sayı seç. {} adet hakkın kaldı".format(kalan_hak))
        if kalan_hak == 0:
            konus("Hakkın doldu, kaybettin")
            devam_et = False 
            konus("Yeni oyun oynamak ister misin") 
            yeni_oyun = kaydet()
            if yeni_oyun == "evet":
                tahmin_oyunu()
            else:
                devam_et = False      





def konus(metin):
     tts = gTTS(text=metin, lang="tr", slow=False) # fonksiyona gönderilen metni temsil ediyor bu parametre
     dosya = "cevap.mp3" # Ses dosyamız 
     tts.save(dosya) # Ses dosyasını kaydediyorum
     playsound(dosya) # Ses dosyasını çalıyorum
     os.remove(dosya) # İşimiz bitince ses dosyasını silmesi için bu da

playsound("giris.mp3")
konus("Hoşgeldin")


while True:
    voice = kaydet() # Mikrofoondan aldığım sesi voice değişkeninin içine attım
    if voice != '':
        voice = voice.lower() # Bizden duyduğu sese karşılık cevap alacağımız zaman büyük harf olmasını istememesi için
        print(voice.capitalize()) # Mikrofona gelen sesi yazdırıyo ve Yazdırırken ilk harfi büyütüyor
        yanitla(voice) 
