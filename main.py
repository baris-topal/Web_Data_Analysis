
#Veri Çekmek için;
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#Duygu Analizi için;
from textblob import TextBlob
#Kelime Tekrarı için;
from collections import Counter
from string import punctuation, digits
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#Tekrarı Görselleştirmek için;
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#Arayüz için;
from PyQt5.QtGui import QPixmap,QIcon,QFont
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QTableWidget

tekrar_Kelime=[]
tekrar_Sayisi=[]

def vericekme():
     file = open('Tüm_Link.txt', 'w', encoding='utf-8')
     file2 = open('Duyuru.txt', 'w', encoding='utf-8')
     file3 = open('Tüm_Link.txt', 'r', encoding='utf-8')
     file4 = open('Analiz_Link.txt', 'w', encoding='utf-8')

     browser = webdriver.Firefox()
     url = requests.get('https://duzce.edu.tr/site-haritasi')
     soup = BeautifulSoup(url.content,'html.parser')
     for linkler in soup.find_all('a'):
          linkler=linkler.get('href')
          if linkler != ' ' and linkler is not None:
               index = linkler.find('http')
               index2 = linkler.find('https')
               if index == -1 and index2 == -1:
                    linkler='http://www.duzce.edu.tr/'+linkler
                    file.write(linkler+'\n')
     dizi=file3.readlines()
     browser.minimize_window()
     a = int(input("Son kaç yıldaki duyuruları görmek istiyorsunuz?(En fazla 3 yılı gösterir!) : "))
     while a<1 or a>3 or a==str:
          print("Yanlış değer girdiniz lütfen tekrar deneyiniz!")
          a = int(input("Son kaç yıldaki duyuruları görmek istiyorsunuz?(En fazla 3 yılı gösterir!) : "))
     if a==1:
          dizi = dizi[26:2362]
     elif a == 2:
          dizi = dizi[2362:3997]
     elif a == 3:
          dizi = dizi[3997:5456]
     for item in dizi:
          file4.write(item)
     browser.maximize_window()
     random.shuffle(dizi)
     yenidizi=dizi[0:20]
     for i in yenidizi:
          browser.get(i)
          etiket=browser.find_elements_by_class_name('blog-content')
          for etiket2 in etiket:
               file2.write(etiket2.text.strip()+'\n')
     browser.close()

def kelime_sıklığı():

     with open('Duyuru.txt','r',encoding='utf-8') as dosya:
          metin=dosya.read()
     cevirici = str.maketrans('', '', punctuation)
     metin = metin.translate(cevirici)
     cevirici = str.maketrans('', '', digits)
     metin = metin.translate(cevirici)
     metin = metin.lower()
     stopWords = set(stopwords.words('turkish'))
     alist = [line.rstrip() for line in open('turkce-stop-words.txt', 'r', encoding='utf-8')]
     stopWords.update(alist)
     words = word_tokenize(metin)

     kelimeler = []
     for w in words:
          if w not in stopWords:
               kelimeler.append(w)
     kelime_Sayi = Counter(kelimeler)
     for kelime in kelime_Sayi.most_common():
          tekrar_Kelime.append(kelime[0])
          tekrar_Sayisi.append(kelime[1])

     wordcloud = WordCloud(stopwords=stopWords,background_color='white',collocations=False)\
          .generate(' '.join(kelimeler))
     wordcloud.to_file("img/first_review.png")
     plt.imshow(wordcloud, interpolation='bilinear')
     plt.axis("off")

def duygu_analizi():
     file2=open('Duyuru.txt','r',encoding='utf-8')
     file5=open('Duyuru_Analiz.txt','w',encoding='utf-8')
     for duyuru in file2.readlines():
          blob1=TextBlob(duyuru)
          try:
               blob_eng=blob1.translate(to = "en")
               file5.write(str(blob1.strip())+"\
                    \n(Kutupluk: "+str(blob_eng.sentiment.polarity)+ \
                         " Öznellik: "+str(blob_eng.sentiment.subjectivity)+')\n')
          except :
               continue

def ara_yuz():
     vericekme()

     kelime_sıklığı()

     duygu_analizi()

     uygulama = QApplication([])
     uygulama.setWindowIcon(QIcon('img/icon.png'))


     foto=QLabel()
     pixmap = QPixmap('img/first_review.png')
     foto.setPixmap(pixmap)
     foto.setGeometry(0,50,400,200)
     foto.setWindowTitle("Kelime Bulutu")
     foto.show()

     liste=QListWidget()
     file6=open('Duyuru_Analiz.txt','r',encoding='utf-8')
     for list in file6.readlines():
          liste.addItem(list)
     liste.setFont(QFont('Times',24))
     liste.setGeometry(0,100,1250,750)
     liste.setWindowTitle("Duyuru Analizi")
     liste.show()

     tablo = QTableWidget()
     tablo.setRowCount(10)
     tablo.setColumnCount(2)
     tablo.setHorizontalHeaderLabels(['Kelime','Tekrar Sayısı'])
     for i in range(tablo.rowCount()):
          for j in range(tablo.columnCount()):
               if j == 0:
                    tablo.setItem(i, j, QtWidgets.QTableWidgetItem(str(tekrar_Kelime[i])))
               else:
                    tablo.setItem(i, j, QtWidgets.QTableWidgetItem(str(tekrar_Sayisi[i])))

     tablo.setGeometry(0,150,240,326)
     tablo.setWindowTitle("Kelime Sıklığı")
     tablo.show()

     uygulama.exec_()

ara_yuz()
