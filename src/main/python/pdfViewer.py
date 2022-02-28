#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView
from PyQt5 import uic
from os import path, getcwd



class PDFWindow(QMainWindow):
   
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        self.filename = args[1] or "WaterQuality"
        self.urlPath = args[0].ctx.retrieve_pdf(self.filename)

        try:
           
            self.webView = QWebEngineView()
            dir = QDir()
            self.setWindowTitle("Industrial Water Quality Guidelines Background Info")
            self.centralWidget = QWidget(self)
            url = QUrl.fromUserInput(self.urlPath)
            self.webView.setUrl(url)
            
            self.webView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            self.webView.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
            self.setCentralWidget(self.webView)
            

        except Exception as e:
            print(e)
            pass

    def url_changed(self):
        self.setWindowTitle(self.webView.title())

    def go_back(self):
        self.webView.back()
