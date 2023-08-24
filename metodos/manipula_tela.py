import time
from typing import Optional, Tuple, Union
# import win32api
import manipula_cliente
import manipula_funcoes
import manipula_imagem
import main
import pyautogui as tecla
import numpy as np
import customtkinter

# vida=58,mana=78
# esquerda=38,direita=1194
esquerda=39
direita=509
vida=65
mana=85
nome=1
id=0

corVidaMana=(0,0,148)#vermelho

# def busca_tecla_especifica():
#     a = win32api.GetKeyState(0x01)
#     if a<0:
#         x,y = tecla.position()
#         coordenadas = f'{int(x)},{int(y)}'
#         manipula_cliente.envia_dados_servidor(coordenadas)

def desenhaMiniMapa():
    telaInteira=manipula_funcoes.retorna_atualizacao_tela()
    larguraTela=telaInteira.shape[1]
    alturaTela=telaInteira.shape[0]
    metadeLargura=larguraTela//2
    metadeAltura=alturaTela//2
    pixelInicial=[metadeAltura-150,metadeLargura-50]
    # while pixelInicial!=(0,0,0).all():
    # manipula_imagem.mostra_imagem(0,frameTela,None)

def retornaVidaMana(vidaMana,posicao):
    if vidaMana==85:
        corVidaMana=(148,99,0)#azul
    telaInteira=manipula_funcoes.retorna_atualizacao_tela()
    frameTela=telaInteira[vidaMana:vidaMana+1,posicao:posicao+133]
    contadorPixelVermelho=np.sum(frameTela==corVidaMana)
    return retornaPorcentagemVida(contadorPixelVermelho)

def retornaPorcentagemVida(pixelVermelho):
    porcentagem=0
    if pixelVermelho!=0:
        porcentagem=(pixelVermelho*100)//399
    return porcentagem

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.configuraLayout()
        self.configuraWidget()
        self.configuraGridWidgets()

    def configuraLayout(self):
        alturaTela=self.winfo_screenheight()
        larguraTela=self.winfo_screenwidth()
        largura=larguraTela//2
        self.title('Gerenciador boot WarSpear')
        self.geometry(f'{largura}x{alturaTela}+{largura-5}+0')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=0)
        self.rowconfigure(1,weight=1)

    def configuraWidget(self):
        self.labelPersonagem=customtkinter.CTkLabel(self,text='Personagens', font=customtkinter.CTkFont(size=16, weight="bold"))
        self.frameCentro = customtkinter.CTkFrame(self,corner_radius=10)
        self.tabPersonagens = customtkinter.CTkTabview(self.frameCentro)
        self.botaoIniciar=customtkinter.CTkButton(self.frameCentro,text='Iniciar')
        self.labelTema=customtkinter.CTkLabel(self.frameCentro,text='Tema:',bg_color='transparent',text_color=['#000','#fff'])
        self.opcoesTema=customtkinter.CTkOptionMenu(self.frameCentro,values=['Light','Dark','System'],command=self.mudaTema)

        listaTabs=[]
        lista=manipula_cliente.retornaDicionarioUsuario('eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem')
        for personagem in lista:
            self.tabPersonagens.add(f"{personagem[nome]}")
            self.tabPersonagens.tab(f"{personagem[nome]}").columnconfigure(0,weight=1)
            self.tabPersonagens.tab(f"{personagem[nome]}").rowconfigure(0,weight=1)
            listaTabs.append(self.tabPersonagens)
        for personagem in lista:
            caminhoListaDesejo=f'eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem[id]}/Lista_desejo'  
            listaToDo = manipula_cliente.retornaListaDicionarioTrabalhoDesejado(caminhoListaDesejo,0)
            print(f'Lista to do do personagem {personagem[nome]}.')
            listaDoing = manipula_cliente.retornaListaDicionarioTrabalhoDesejado(caminhoListaDesejo,1)
            print(f'Lista doing do personagem {personagem[nome]}.')
            listaDone = manipula_cliente.retornaListaDicionarioTrabalhoDesejado(caminhoListaDesejo,2)
            print(f'Lista done do personagem {personagem[nome]}.')
            for tabs in listaTabs:
                self.tabEstadosTrabalho=customtkinter.CTkTabview(tabs.tab(personagem[nome]))
                self.tabEstadosTrabalho.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")
                self.tabEstadosTrabalho.add(f'To do')
                self.tabEstadosTrabalho.add(f'Doing')
                self.tabEstadosTrabalho.add(f'Done')
                self.tabEstadosTrabalho.tab('To do').columnconfigure(0,weight=1)
                self.tabEstadosTrabalho.tab('To do').rowconfigure(0,weight=1)
                self.tabEstadosTrabalho.tab('Doing').columnconfigure(0,weight=1)
                self.tabEstadosTrabalho.tab('Doing').rowconfigure(0,weight=1)
                self.tabEstadosTrabalho.tab('Done').columnconfigure(0,weight=1)
                self.tabEstadosTrabalho.tab('Done').rowconfigure(0,weight=1)

                self.frameRolante=customtkinter.CTkScrollableFrame(self.tabEstadosTrabalho.tab('To do'))
                self.frameRolante.grid(row=0,column=0,padx=5,pady=(5,0),sticky='nsew')

                self.frameRolanteLista=[]
                contadorTrabalho=0
                if len(listaToDo)!=0:
                    for toDo in listaToDo:
                        self.labelTrabalho=customtkinter.CTkLabel(self.frameRolante,text=toDo[nome])
                        self.labelTrabalho.grid(row=contadorTrabalho,column=0,padx=5,pady=(5,0))
                        self.frameRolanteLista.append(self.labelTrabalho)
                        contadorTrabalho+=1
                else:
                    self.labelTrabalho=customtkinter.CTkLabel(self.frameRolante,text='Lista vazia')
                    self.labelTrabalho.grid(row=contadorTrabalho,column=0,padx=5,pady=(5,0))

                self.frameRolante=customtkinter.CTkScrollableFrame(self.tabEstadosTrabalho.tab('Doing'))
                self.frameRolante.grid(row=0,column=0,padx=5,pady=(5,0),sticky='nsew')
                self.frameRolanteLista=[]
                contadorTrabalho=0
                if len(listaDoing)!=0:
                    for doing in listaDoing:
                        self.labelTrabalho=customtkinter.CTkLabel(self.frameRolante,text=doing[nome])
                        self.labelTrabalho.grid(row=contadorTrabalho,column=0,padx=5,pady=(5,0))
                        contadorTrabalho+=1
                else:
                    self.labelTrabalho=customtkinter.CTkLabel(self.frameRolante,text='Lista vazia')
                    self.labelTrabalho.grid(row=contadorTrabalho,column=0,padx=5,pady=(5,0))
                
                self.frameRolante=customtkinter.CTkScrollableFrame(self.tabEstadosTrabalho.tab('Done'))
                self.frameRolante.grid(row=0,column=0,padx=5,pady=(5,0),sticky='nsew')
                self.frameRolanteLista=[]
                contadorTrabalho=0
                if len(listaDone)!=0:
                    for done in listaDone:
                        self.labelTrabalho=customtkinter.CTkLabel(self.frameRolante,text=done[nome])
                        self.labelTrabalho.grid(row=contadorTrabalho,column=0,padx=5,pady=(5,0))
                        contadorTrabalho+=1
                else:
                    self.labelTrabalho=customtkinter.CTkLabel(self.frameRolante,text='Lista vazia')
                    self.labelTrabalho.grid(row=contadorTrabalho,column=0,padx=5,pady=(5,0))
                
    def configuraGridWidgets(self):
        self.labelPersonagem.grid(row=0, column=0, padx=20, pady=(10, 0),sticky=('we'))
        self.frameCentro.grid(row=1, column=0,padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.frameCentro.columnconfigure(0,weight=1)
        self.frameCentro.rowconfigure(0,weight=1)
        self.frameCentro.rowconfigure((1,2,3),weight=0)
        self.tabPersonagens.grid(row=0, column=0, padx=10, pady=(10,0),sticky="nsew")
        self.botaoIniciar.grid(row=1,column=0,padx=10,pady=(10,0))
        self.labelTema.grid(row=2,column=0,padx=10,pady=(10,0),sticky="sw")
        self.opcoesTema.grid(row=3,column=0,padx=10,pady=(5,20),sticky="sw")
    
    def mudaTema(self,novaAparencia):
        customtkinter.set_appearance_mode(novaAparencia)

if __name__=='__main__':
    app=App()
    app.mainloop()
# print(f'{retornaVidaMana(vida,esquerda)}%')
# desenhaMiniMapa()