from tkinter import *
from tkinter.ttk import *
from ctkinder import *
from typing import Optional, Tuple, Union

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.configuraLayout()
        self.configuraLabels()
        self.configuraWidgets()
        self.configuraPosicaoLabels()
        self.configuraRadioButton()

    def configuraRadioButton(self):
        v=StringVar(self.label4,'1')
        style=Style(self)
        style.configure('RadioButton',background='light blue',
                        foreground='orange',font=('arial',14,'bold'))
        valores={'Radiobutton1':'1',
                 'Radiobutton2':'2',
                 'Radiobutton3':'3'}
        cont=0
        for (chave,valor) in valores.items():
            self.radioButtom=Radiobutton(self.label4,text=chave,variable=v,value=valor)
            self.radioButtom.grid(row=cont,column=0)
            cont+=1

    def configuraWidgets(self):
        self.widget1=customtkinter.CTkToplevel(self.label2,fg_color='blue')

    def configuraLabels(self):
        self.label1=customtkinter.CTkLabel(self,bg_color='blue')
        self.label2=customtkinter.CTkLabel(self,bg_color='red')
        self.label3=customtkinter.CTkLabel(self.label2,bg_color='green')
        self.label4=customtkinter.CTkLabel(self.label2,bg_color='pink')
    
    def configuraPosicaoLabels(self):
        self.label1.grid(row=0,column=0,padx=10,pady=(10,0),sticky=('ew'))
        self.label2.grid(row=1,column=0,padx=10,pady=10,sticky=('nsew'))
        self.label2.rowconfigure(0,weight=0)
        self.label2.rowconfigure(1,weight=1)
        self.label3.grid(row=0,column=0,padx=10,pady=(10,0),sticky=('ew'))
        self.label4.grid(row=1,column=0,padx=10,pady=10,sticky=('nsew'))
    
    def configuraLayout(self):
        alturaTela=self.winfo_screenheight()
        larguraTela=self.winfo_screenwidth()
        largura=larguraTela//2
        self.title('Tela teste')
        self.geometry(f'{largura}x{alturaTela}+{largura-5}+0')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=0)
        self.rowconfigure(1,weight=1)

if __name__=='__main__':
    app=App()
    app.mainloop()