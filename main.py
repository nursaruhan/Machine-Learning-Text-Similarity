# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 03:10:02 2019

@author: saruhan
"""

import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import math
import os
import nlp as n
import model as m

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        #Yeni eğitim seti 
        self.labelNewTrainName = QLabel("Arff uzantılı yeni eğitim setinin adı:", self)
        self.labelNewTrainName.setGeometry(20, 40, 265, 28)
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelNewTrainName.setFont(font)
        self.labelNewTrainName.setObjectName("label")
        
        self.editNewTrainName = QLineEdit(self)
        self.editNewTrainName.setGeometry(290, 40, 100, 23)
        
        self.buttonNewTrain = QPushButton("Yeni Eğitim Seti Oluştur", self)
        self.buttonNewTrain.setGeometry(420, 40, 360, 28)
        self.buttonNewTrain.clicked.connect(self.newTrainUpload)
        
        #Yeni test seti     
        self.labelNewTestName = QLabel("Arff uzantılı yeni test setinin adı:", self)
        self.labelNewTestName.setGeometry(20, 80, 265, 28)
        self.labelNewTestName.setFont(font)
        self.labelNewTestName.setObjectName("label")
        
        self.editNewTestName = QLineEdit(self)
        self.editNewTestName.setGeometry(290, 80, 100, 23)
       
        self.buttonTrainArff = QPushButton("Bağlı Eğitim Setini Seç", self)
        self.buttonTrainArff.setGeometry(420, 80, 170, 28)
        self.buttonTrainArff.clicked.connect(self.trainArff)
        
        self.buttonNewTest = QPushButton("Yeni Test Seti Oluştur", self)
        self.buttonNewTest.setGeometry(609, 80, 170, 28)
        self.buttonNewTest.clicked.connect(self.newTestUpload)
        
        #Benzerlik Hesaplama
        self.labelSimilarity = QLabel("Benzerlik Hesaplama İşlemleri:", self)
        self.labelSimilarity.setGeometry(20, 150, 251, 28)
        self.labelSimilarity.setFont(font)
        self.labelSimilarity.setObjectName("label")
        
        self.buttonTrainSelect = QPushButton("Eğitim Setini Seç", self)
        self.buttonTrainSelect.setGeometry(20, 190, 370, 28)
        self.buttonTrainSelect.clicked.connect(self.trainArff)
        
        self.buttonTestSelect = QPushButton("Test Setini Seç", self)
        self.buttonTestSelect.setGeometry(20, 230, 370, 28)
        self.buttonTestSelect.clicked.connect(self.testArff)
                
        self.label = QLabel("K sayısı:", self)
        self.label.setGeometry(20, 270, 251, 28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.n = QLineEdit(self)
        self.n.setGeometry(90, 270, 300, 23)
        
        self.listView = QListWidget(self)
        self.listView.setGeometry(20, 310, 370, 400) 
        
        self.buttonSimilarity = QPushButton("Benzerlik Hesapla",self)
        self.buttonSimilarity.setGeometry(420, 270, 360, 28)
        self.buttonSimilarity.clicked.connect(self.similarityFind)     
        
        self.listViewSimilarity = QListWidget(self)
        self.listViewSimilarity.setGeometry(420, 310, 360, 400)

    def newTrainUpload(self):
        self.listView.clear()
        option= QFileDialog.DirectoryOnly

        pathTrain = QFileDialog.getExistingDirectory(self, "Open Directory", "C:/Users/saruhan/Desktop")        
        files = os.listdir(pathTrain)
        self.listView.addItem("Egitim verileri:")
        for i, item in enumerate(files): 
            self.listView.addItem(files[i])
            
        m.Model.newTrain(self.editNewTrainName.text(), pathTrain)
   
    def trainArff(self):
        global pathTrainArff
        pathTrainArff = QFileDialog.getOpenFileName(self, "Dosya Aç", "C:/Users/saruhan/Desktop", "Image file(*.arff)")
        print(pathTrainArff[0])
           
    def newTestUpload(self):
        self.listView.clear()
        self.listView.addItem(pathTrainArff[0])
        option= QFileDialog.DirectoryOnly

        pathTest = QFileDialog.getExistingDirectory(self, "Open Directory", "C:/Users/saruhan/Desktop")
        files = os.listdir(pathTest)
        self.listView.addItem("Test verileri:")
        for i, item in enumerate(files): 
            self.listView.addItem(files[i])
        #Arff Dosyası Oluşturulacak    
        m.Model.newTest(self.editNewTestName.text(), pathTest, pathTrainArff[0])    
            
    #Benzerlik Bulmak İçin    
    def testArff(self):
        global pathTestArff
        pathTestArff = QFileDialog.getOpenFileName(self, "Dosya Aç", "C:/Users/saruhan/Desktop", "Image file(*.arff)")
        print(pathTestArff[0])    

    def similarityFind(self):
        self.listView.clear()
        self.listViewSimilarity.clear()
        result = m.Model.knn(pathTrainArff[0], pathTestArff[0], int(self.n.text()))
        self.listView.addItem(pathTrainArff[0])
        self.listView.addItem(pathTestArff[0])
        for i, item in enumerate(result): 
            self.listViewSimilarity.addItem(str(result[i]))
      
def window():
    app = QApplication(sys.argv)
    window = Main()
    window.setWindowTitle("Text Similarity")
    window.setGeometry(500,100, 800,750)
    window.show()
    sys.exit(app.exec())
        
if __name__ == "__main__":
    window()        
        

    
    
        