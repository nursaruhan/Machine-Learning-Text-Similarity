# -*- coding: utf-8 -*-
"""
@author: saruhan
"""
import jpype
import re
from collections import Counter
from nltk.corpus import stopwords


class nlp:
    def zemberek():
        jvmDllPath = r"C:/Program Files/Java/jdk1.8.0_171/jre/bin/server/jvm.dll"
        try:
            jpype.startJVM(jvmDllPath,"-ea", "-Djava.class.path=C:/Users/saruhan/Desktop/Machine Learning Text Similarity/zemberek-tum-2.0.jar")
        except:
            pass
        Tr = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")   
        tr = Tr()
        Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
        zemberek = Zemberek(tr)
        return zemberek

    def frekans(word):
        counts = Counter(word)
        return counts
      
    def clean(text):#Metinden noktalama işaretleri temizlenir  
        text = re.sub(r'[^\w\s]', ' ', text).lower()
        text = ' '.join(text.split())
        return text

    def textClean(text):#Metinden gereksiz kelimeler temizlenir  
        bodyText = nlp.clean(str(text))
        bodyTextSplit = nlp.frekans(bodyText.split())
        stopwordsList = stopwords.words('turkish')      
        words = [word for word in bodyTextSplit if word not in stopwordsList]
        return words
    
    def stemFind(word):#Zemberek kullanılarak kelimekökü bulunur
        zemberek = nlp.zemberek()
        result = zemberek.kelimeCozumle(word)
        stem = result[0].kok().icerik()
        return stem

    def testStemFind(text):# Metin içindeki kökleri bulur
        words = nlp.textClean(text)
        stemList = []
        pointlessStem=[]
        for i, item in enumerate(words):
            try:
                stem = nlp.stemFind(words[i])
                print(stem)
                stemList.append(stem)
            except:
                pointlessStem.append(words[i])
        return stemList
    
