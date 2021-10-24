from tkinter import *
from interface import *

try:
    master = Tk()
    janela = Interface(master)
    janela.inicia()
except:
    print("Erro")
