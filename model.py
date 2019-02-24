# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import os
import nlp as n
from scipy.io import arff
   

class Model:
    global textList
    textList=[]
    
    def fileName(path, k):
        file = os.listdir(path)
        for i, item in enumerate(file): 
            if (i==k):
                return(file[i])
   
    def read(path):
        files = os.listdir(path)
        textList.clear()
        for file in files:
            if file.endswith(".txt"):             
                print(file)
                
        for i, item in enumerate(files):
            fileRead = open(path +"/"+ files[i], "r") 
            text = fileRead.read()
            textList.append(n.nlp.testStemFind(text))
        return(textList)
    
    #Yeni Eğitim setinin matrisi oluşturulup arff olarak kaydedilir.
    def newTrain(trainName, pathTrain):
        #Eğitim Verisi
        trainSet = []
        trainTextList = []
        trainTextList = Model.read(pathTrain)
        #Çift boyutlu diziyi tek boyutlu diziye çevirdik (vectorizer için)
        for row in trainTextList:
            trainSet.append(' '.join([str(elem) for elem in row]))
        print (trainSet)
        
        vectorizer= CountVectorizer()   
        trainVectorizerArray= vectorizer.fit_transform(trainSet).toarray()    
        print ('TrainVectorizerArray', trainVectorizerArray)
             
        transformer = TfidfTransformer()
        transformer.fit(trainVectorizerArray)
        train = transformer.transform(trainVectorizerArray).toarray()
        print("Train Transform", train)
        
        wordList = vectorizer.get_feature_names()
        print(wordList)        
        Model.arffCreate(trainName, pathTrain, train, wordList)

    
    #Yeni test verisini eğitim setinde bulunan kelimelere bağlı olarak oluşturması gerekir.
    def newTest(name, pathTest, pathTrainArff):
        data, meta = Model.loadArff(pathTrainArff)

        #Bağlı olduğu eğitim verisini alıyoruz.Dizi uzunluğu için gerekli        
        trainList = []
        attributeList = [] 
        attributeList =  meta.names()
        for i in range(len(attributeList)-1):
            trainList.append(attributeList[i])
        print(trainList)
    
        vectorizer = CountVectorizer()   
        trainVectorizerArray= vectorizer.fit_transform(trainList).toarray()    
        print ('TrainVectorizerArray', trainVectorizerArray)
             
        transformer = TfidfTransformer()
        
        testSet = []
        testTextList = []
        #read() Metinleri kelime kökleri bulunmuş sekilde getirir
        testTextList = Model.read(pathTest) 
        for row in testTextList:
            testSet.append(' '.join([str(elem) for elem in row]))
        print (testSet)
        
        testVectorizerArray = vectorizer.transform(testSet).toarray()
        print("testVectorizerArray", testVectorizerArray)
        
        transformer.fit(testVectorizerArray)
        test = transformer.transform(testVectorizerArray).toarray()
        print ('Test Transform',test)
   
        wordList = vectorizer.get_feature_names()
        print(wordList)
        
        Model.arffCreate(name, pathTest, test, wordList)
        
    #Arff uzantılı dosyayı oluşturur.    
    def arffCreate(name, path, text, wordList):
        read = open("C:/Users/saruhan/Desktop/"+name+".arff","w+")
        
        read.write("@RELATION " + name + "\n\n")
        for i, item in enumerate(wordList):
            read.write("@ATTRIBUTE " + wordList[i] + " NUMERIC\n" )
    
        files = os.listdir(path)
        read.write("@ATTRIBUTE class { ")
                          
        for i, item in enumerate(files):
            if files[i].endswith(".txt"):   
                if(i != len(files)-1):  
                    read.write(files[i] + ", ")  
                else:
                    read.write(files[i])        
        read.write("}\n" )    
        read.write("\n@DATA\n")
        for i, item in enumerate(text):
            for j, item in enumerate (text[i]):
                read.write(str(text[i][j]) +", " )
            read.write(files[i] + "\n")    
        print(name+ ".arff dosyası oluşturuldu.")    
        read.close()  
            
        
    def loadArff(path):  
        
        data, meta=arff.loadarff(path)
        
        n = len(data)
        m = len(data[0])-1
        dizi = [[0] * m for i in range(n)]
        for i in range(n):
            for j in range(m):
                dizi[i][j] = (data[i][j])       
        print("Yüklenen", dizi) 
        return (dizi, meta)
        
    def knn(pathTrain, pathTest, n):
        
        dataTrain, metaTrain = Model.loadArff(pathTrain)      
        dataTest, metaTest=Model.loadArff(pathTest)
            
        result = []        
        knn = NearestNeighbors(n_neighbors=n,  metric='cosine')
        knn.fit(dataTrain)
        kneighbors = knn.kneighbors(dataTest)
        print(kneighbors)

        for i, item in enumerate(kneighbors[0]):
            for j, item in enumerate(kneighbors[0][i]):
                print("Test", (metaTest['class'][1][i]), "Egitim",(metaTrain['class'][1][kneighbors[1][i][j]]) ,"Benzerlik Oranı:", round((1-kneighbors[0][i][j])*100, 3))
                result.append([(metaTest['class'][1][i]),(metaTrain['class'][1][kneighbors[1][i][j]]) ,round((1-kneighbors[0][i][j])*100, 3)])
        return (result)


