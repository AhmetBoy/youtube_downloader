from __future__ import unicode_literals
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.uix.switch import Switch 
import asa
import pytube
import math
import youtube_dl
import pyautogui
import pywhatkit as kit
import pafy
class Main(BoxLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.sayac = 0
        self.text_number = -1 
    def mp3_dis(self):
        self.text_number += 1
        if self.text_number%2 == 0 :
            self.ids.button_360.disabled = True
            self.ids.button_480.disabled = True
            self.ids.button_720.disabled = True
            self.ids.button_1080.disabled = True
        else:
            self.mp4_dis()
    def mp4_dis(self):
        self.ids.button_360.disabled = False
        self.ids.button_480.disabled = False
        self.ids.button_720.disabled = False
        self.ids.button_1080.disabled = False
    def download_text_kontrol(self , parametre):
        self.ids.dowload_text.text = "[color=#008000]"+parametre+"[/color]"
    def secili_button_kontrol(self):
        if self.ids.mp3.state == "down" :
            if  len(self.ids.link.text) < 1 :
                self.download_text_kontrol("[color=#FF0000]link girinz.[/color]")
            else:
                self.indir()
        elif self.ids.mp4.state == "down" :
            if self.ids.button_360.state == "down" or self.ids.button_480.state == "down" or self.ids.button_720.state == "down" or self.ids.button_1080.state == "down" and len(self.ids.link.text) > 1 :
                self.indir()
            else:
                self.ids.dowload_text.text = "[color=#FF0000]kalite seçiniz.[/color]"
        else: 
            if self.ids.button_360.state == "down" or self.ids.button_480.state == "down" or self.ids.button_720.state == "down" or self.ids.button_1080.state == "down":
                self.ids.dowload_text.text = "[color=#FF0000]format seçiniz.[/color]"
            else:
                self.ids.dowload_text.text = "[color=#FF0000]kalite ve format seçiniz.[/color]"
    def resim_bul(self):
        self.sayac += 1
        c = "dene"+str(self.sayac)+".jpg"
        try:    
            link = self.ids.link.text
            asa.a(link , c)
            self.ids.image.background_normal = c 
        except:
            self.ids.link.hint_text = "geçerli bir youtube linki giriniz"
            self.ids.image.background_normal = "youtube.jpg"
            self.ids.info.text = ""
        self.resim_bilgisi()
    def resim_bilgisi(self):
        try:
            link = self.ids.link.text
            yt = pytube.YouTube(link)
            video = pafy.new(link)
            baslik = video.title
            kanal_adi = yt.author
            izlenme = yt.views
            boyutu = math.ceil(yt.length/60)
            self.ids.info.text = "[color=#000000]Video Adı:"+baslik[:40]+"\n"+baslik[40:]+"\n"+"Kanal Adı:"+kanal_adi+"\n"+"İzlenme:"+str(izlenme)+"\n"+"Boyutu:"+str(boyutu)+"dakika[/color]"
        except:
            pass 
    def connect_youtube(self):
        link = self.ids.link.text
        try:
            kit.playonyt(link)
        except:
            print("No video found.")
    def indir(self):
        try:    
            link = self.ids.link.text
            yt = pytube.YouTube(link)
            if self.ids.mp3.state == "down":
                yt.streams.get_by_itag(140).download("mp3")
                self.download_text_kontrol("mp3 indirilidi.")
            elif self.ids.mp4.state == "down":
                if self.ids.button_360.state == "down":
                    yt.streams.get_by_itag(18).download("mp4")
                elif self.ids.button_480.state == "down":
                    yt.streams.get_highest_resolution().download("mp4")
                elif self.ids.button_720.state == "down":
                    yt.streams.get_highest_resolution().download("mp4")
                elif self.ids.button_1080.state == "down":
                    yt.streams.get_highest_resolution().download("mp4")
                self.ids.dowload_text.text = ""
                self.download_text_kontrol("video indirildi.")
        except:
            self.ids.dowload_text.text = "[color=#FF0000]link'i kontrol ediniz.[/color]"
            
class youtube(App):
    def build(self):
        return Main()
if __name__ == "__main__":
    youtube().run()