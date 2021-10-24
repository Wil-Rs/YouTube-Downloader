from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar, Combobox
from download import *
import threading
import sys

class Interface():
    def __init__(self, master):
        """
        Cria a janela principal
        """
        self.master = master
        self.master.title("YouTube Downloader")
        self.dow = Download()
        self.criaObjetos()
        self.colocaNaTela()            

    def criaObjetos(self):
        """
        Cria os objetos da tela
        """
        
        self.menu = Menu(self.master)
        self.menu.add_cascade(label="Como fazer download?", command=self.comoFazerDown)
        self.master.config(menu=self.menu)

        self.auxVideo = True
        self.auxPlay = False
        
        self.chVideo = Checkbutton(self.master, text="Video", command=self.seVideoSelecionado)
        self.chVideo.select()
        self.chPlaylist = Checkbutton(self.master, text="Playlist", command=self.sePlaylistSelecionado)

        self.labelURL = Label(self.master, text="Link: ")
        self.entryURL = Entry(self.master, width=45)

        
        self.btVerificar = Button(self.master, text="Verificar", command=self.verificaDown)
        self.btDownload = Button(self.master, text="Download", command=self.download)

        self.barraCarregamento = Progressbar(self.master)
        self.porcentagem = Label(self.master, text="000.00%")

        self.combobox = Combobox(self.master)

        self.labelStatus = Label(self.master, text="Verificando Informações...", fg="blue")

        self.descricao = Text(self.master, width=40, height=5)
        self.desc = Label(self.master, text="Descrição: ")
        
        self.titulo = Label(self.master, text="----------")
        self.title = Label(self.master, text="Titulo: ")

        self.duracao = Label(self.master, text="-- Minutos")
        self.dura = Label(self.master, text="Duração: ")

    def seVideoSelecionado(self):
        """
        Auxilia os checkbox
        """
        self.auxVideo = True
        self.auxPlay = False
        self.chPlaylist.deselect()

    def sePlaylistSelecionado(self):
        """
        Auxilia os checkbox
        """
        self.auxvideo = False
        self.auxPlay = True
        self.chVideo.deselect()
        return messagebox.showinfo("Playlist", "Playlist não está funcionando!")

    def colocaNaTela(self):
        """
        Coloca os objetos na tela
        """
        self.chVideo.grid(row=0, column=0)
        self.chPlaylist.grid(row=0, column=1)
        self.labelURL.grid(row=1, column=0)
        self.entryURL.grid(row=1, column=1, padx=5)
        self.btVerificar.grid(row=2, column=1, sticky="WE", padx=5, pady=5)
        
        
        self.barraCarregamento.grid(row=4, column=1, sticky="WE", padx=5, pady=5 )
        self.porcentagem.grid(row=4, column=2)

        self.titulo.grid(row=48, column=1)
        self.title.grid(row=48, column=0)
        
        self.duracao.grid(row=49, column=1)
        self.dura.grid(row=49, column=0)
        
        self.descricao.grid(row=50, column=1)
        self.desc.grid(row=50, column=0)


    def auxVerificaDown(self):
        """
        Auxilia a self.verificaDown
        """
        self.dow.getLink(self.entryURL, self.reset)
        self.combobox["value"] = self.dow.getResolution()
        self.combobox.grid(row=2, column=1, sticky="WE", padx=5, pady=5)
        self.btDownload.grid(row=3, column=1, sticky="WE", padx=5)
        self.labelStatus.grid_forget()

        self.descricao.insert(END, self.dow.getDescription())
        self.duracao["text"] = "{:.4} Minutos".format(self.dow.getDuration())
        self.titulo["text"] = self.dow.getTitle()
        
    def verificaDown(self):
        """
        Verifica o link para download
        """
        threading.Thread( target=self.auxVerificaDown ).start()
        self.labelStatus.grid(row=2, column=1, sticky="WE", padx=5, pady=5)
        self.btVerificar.grid_forget()

    def auxDownload(self):
        """
        Auxilia a self.download
        """
        if self.auxVideo:
            self.dow.download(self.barraProgress, self.combobox, self.downloadComplete)
    
    def download(self):
        """
        Faz o download do video
        """
        self.btDownload.grid_forget()
        self.labelStatus["text"] = "Iniciando Download!!!"
        self.labelStatus.grid(row=2, column=1, sticky="WE", padx=5, pady=5)
        threading.Thread( target=self.auxDownload ).start()
        print("vai")
        

    def barraProgress(self, stream, chunk, bytes_remaining):
        """
        Add os valores a barra de progresso
        """
        self.barraCarregamento["value"] = 100 - (bytes_remaining * 100 / int(self.dow.streams.filesize))
        self.porcentagem["text"] = "{:4.4}%".format( 100 - (bytes_remaining * 100 / int(self.dow.streams.filesize)) )
        self.master.title("YouTube Downloader {:4.4}%".format( 100 - (bytes_remaining * 100 / int(self.dow.streams.filesize)) ))
        
    def downloadComplete(self, stream, file_handle):
        """
        É chamada quando o download é terminado
        """
        if messagebox.askyesno("Download 100%", "Terminado o download!!!, Deseja fazer outro?") == True:
            self.combobox["value"] = 0
            self.master.title("YouTube Downloader")
            self.reset()
            messagebox.showinfo("Download 100%", "Terminado o download!!!")
        else:
            messagebox.showinfo("Volte sempre", "Te esperaremos, te a proxima")
            sys.exit()

    def reset(self):
        """
        Volta os objetos da tela como no inicio
        """
        self.removeTela()
        self.criaObjetos()
        self.colocaNaTela()

    def removeTela(self):
        """
        Remove os objetos da tela
        """
        self.chVideo.grid_forget()
        self.chPlaylist.grid_forget()
        self.labelURL.grid_forget()
        self.entryURL.grid_forget()
        self.btVerificar.grid_forget()
        self.barraCarregamento.grid_forget()
        self.porcentagem.grid_forget()
        self.titulo.grid_forget()
        self.title.grid_forget()
        self.duracao.grid_forget()
        self.dura.grid_forget()
        self.descricao.grid_forget()
        self.desc.grid_forget()
        self.combobox.grid_forget()
        self.btDownload.grid_forget()

    def comoFazerDown(self):
        """
        
        """
        messagebox.showinfo("Como fazer download", "Basta copiar o link, selecionar o local da url e apertar Ctrl + V e apertar verificar.")

    def inicia(self):
        """
        Inicia o loop da tela principal
        """
        self.master.mainloop()


