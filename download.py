from pytube import YouTube
from tkinter import messagebox
import threading
import os

class Download():
    def __init__(self):
        pass

    def getLink(self, entryLink, start):
        """
        Pega o link e verifica se é valido e add as resolucoes pra self.streams
        """
        try:
            self.link = entryLink.get()
            self.yt = YouTube(self.link)
            self.streams = self.yt.streams.all()
            
        except:
            return messagebox.showinfo("Erro", "Verifique o link")
            start()

    def getTitle(self):
        """
        Pega o titulo do video
        """
        try:
            return self.yt.title
        except:
            print("getTitle")

    def getDescription(self):
        """
        Pega a descricao do video
        """
        try:
            return self.yt.description
        except:
            print("getDescription")

    def getDuration(self):
        """
        Pega +- o duracao do video
        """
        try:
            return int(self.yt.length) / 60
        except:
            print("getDuration")

    def download(self, barraP, Combobox, dowComplet):
        """
        Faz o download
        """
        self.yt.register_on_progress_callback(barraP)
        self.yt.register_on_complete_callback(dowComplet)
        self.streams = self.streams[self.listaResolution.index( Combobox.get() )]

        #Verifica se existe a pasta YouTubeDownloader se nao tiver cria a mesma
        if os.path.exists("YouTubeDownloader") == False:
            os.system("mkdir YouTubeDownloader")
                
        self.streams.download("YouTubeDownloader")
            

    def getResolution(self):
        """
        Pega tudas as resolucoes do video e add a uma lista
        """
        try:
            self.listaResolution = []
            for res in self.yt.streams.all():
                if res.resolution != None:
                    self.listaResolution.append( "Tipo Video:    {}     Resolução:   {}".format( res.mime_type, res.resolution ) )
                else:
                    self.listaResolution.append( "Tipo Audio:    {}     Kbps:   {}".format( res.mime_type, res.abr ) )

            return self.listaResolution
        except:
            print("getResolution")

    def getSelectionResolution(self, Combobox):
        """
        Quando é selecionada no Combobox retorna a resolucao selecionada
        """
        try:
            return self.listaResolution.index( Combobox.get() )
        except:
            print("resolution")

    def streams(self):
        self.streams = self.yt.streams.all()
