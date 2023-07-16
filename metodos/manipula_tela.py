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

def verificaOpcao(tamanhoLista,opcaoPersonagem):
    confirmacao=True
    print(opcaoPersonagem)
    print(tamanhoLista)
    if not opcaoPersonagem.isdigit() or int(opcaoPersonagem)<0 or int(opcaoPersonagem)>tamanhoLista:
        print(f'Opção inválida! Selecione um personagem.')
        manipula_funcoes.linhaSeparacao()
        confirmacao=False
    return confirmacao

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configura tela
        self.title('Gerenciador boot WarSpear')
        self.geometry(f'{500}x{580}')

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.texto=customtkinter.CTkLabel(self,text='Personagens', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.texto.grid(row=0, column=0, padx=20, pady=(20, 10))

        lista=manipula_cliente.consutar_lista('eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem')
        tamanhoLista=len(lista)
        if tamanhoLista>0:
            indice=1
            for personagem in lista:
                # print(f'Entrou laço.')
                # personagemBotao=customtkinter.CTkButton(tela,text=personagem[nome],command=lambda:clique(personagem[id]))
                indicePersonagem=f'{indice} - {personagem[nome]}'
                # print(indicePersonagem)
                self.personagemLabel=customtkinter.CTkLabel(self.sidebar_frame,text=indicePersonagem)
                self.personagemLabel.grid(row=indice,column=0,padx=3,pady=3)
                # personagemBotao=customtkinter.CTkButton(tela,text=personagem[nome])
                # personagemBotao.pack(padx=10,pady=10)
                indice+=1
            indicePersonagem=f'0 - Voltar'
            self.personagemLabel=customtkinter.CTkLabel(self.sidebar_frame,text=indicePersonagem)
            self.personagemLabel.grid(row=indice,column=0,padx=5,pady=5)
            self.personagemInput=customtkinter.CTkEntry(self.sidebar_frame,placeholder_text='Sua escolha')
            self.personagemInput.grid(row=indice+1,column=0,padx=5,pady=5)
            print(self.personagemInput)
            self.personagemBotao=customtkinter.CTkButton(self.sidebar_frame,text='Confirma.',command=lambda:verificaOpcao(tamanhoLista))
            self.personagemBotao.grid(row=indice+2,column=0,padx=5,pady=5)
        else:
            self.texto=customtkinter.CTkLabel(self,text='A lista está vazia.')
            self.texto.pack(padx=10,pady=10)

if __name__=='__main__':
    app=App()
    app.mainloop()
# print(f'{retornaVidaMana(vida,esquerda)}%')
# desenhaMiniMapa()