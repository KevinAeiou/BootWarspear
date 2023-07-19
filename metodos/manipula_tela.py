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
        self.temas()
        self.labelsTeste()

        lista=manipula_cliente.consutar_lista('eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem')
        tamanhoLista=len(lista)

        # self.texto=customtkinter.CTkLabel(self.sidebar_frame,text='Personagens', font=customtkinter.CTkFont(size=16, weight="bold"))
        # self.texto.grid(row=0, column=0, padx=20, pady=(20, 10))
        # contadorPersonagem=1
        # for personagem in lista:
        #     self.tabview = customtkinter.CTkTabview(self, width=30)
        #     self.tabview.grid(row=contadorPersonagem, column=0, padx=(20, 0), pady=(20, 0))
        #     self.tabview.add(f"{personagem[nome]}")
        #     contadorPersonagem+=1
        # self.tabview.add("Tab 2")
        # self.tabview.add("Tab 3")
        # self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
        # if tamanhoLista>0:
        #     indice=1
        #     for personagem in lista:
        #         # print(f'Entrou laço.')
        #         # personagemBotao=customtkinter.CTkButton(tela,text=personagem[nome],command=lambda:clique(personagem[id]))
        #         indicePersonagem=f'{indice} - {personagem[nome]}'
        #         # print(indicePersonagem)
        #         self.personagemLabel=customtkinter.CTkLabel(self.sidebar_frame,text=indicePersonagem)
        #         self.personagemLabel.grid(row=indice,column=0,padx=3,pady=3)
        #         # personagemBotao=customtkinter.CTkButton(tela,text=personagem[nome])
        #         # personagemBotao.pack(padx=10,pady=10)
        #         indice+=1
        #     indicePersonagem=f'0 - Voltar'
        #     self.personagemLabel=customtkinter.CTkLabel(self.sidebar_frame,text=indicePersonagem)
        #     self.personagemLabel.grid(row=indice+1,column=0,padx=5,pady=5)
        #     self.personagemInput=customtkinter.CTkEntry(self.sidebar_frame,placeholder_text='Sua escolha')
        #     self.personagemInput.grid(row=indice+2,column=0,padx=5,pady=5)
        #     print(self.personagemInput.get())
        #     self.personagemBotao=customtkinter.CTkButton(self.sidebar_frame,text='Confirma.',command=lambda:self.verificaOpcao(tamanhoLista,self.personagemInput))
        #     self.personagemBotao.grid(row=indice+3,column=0,padx=5,pady=5)
        # else:
        #     self.texto=customtkinter.CTkLabel(self,text='A lista está vazia')
        #     self.texto.grid(row=1,column=0,padx=10,pady=10)

    def labelsTeste(self):
        self.label1=customtkinter.CTkLabel(master=self.frameCentral,text='Teste1',bg_color='transparent',text_color=['#000','#fff'])
        self.label1.grid(row=0,column=0,padx=10,pady=10)
        self.label2=customtkinter.CTkLabel(master=self.frameDireito,text='Teste2',bg_color='transparent',text_color=['#000','#fff'])
        self.label2.grid(row=0,column=0,padx=10,pady=10)

    def configuraLayout(self):
        alturaTela=self.winfo_screenheight()
        larguraTela=self.winfo_screenwidth()
        largura=larguraTela/2
        self.title('Gerenciador boot WarSpear')
        self.geometry(f'{largura}x{alturaTela-50}')
        # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        self.frameEsquerdo = customtkinter.CTkFrame(self, width=largura/3, corner_radius=10)
        self.frameEsquerdo.grid(row=0, column=0,rowspan=4, sticky="nsew")
        # self.frameEsquerdo.grid_rowconfigure(2, weight=1)

        self.frameCentral = customtkinter.CTkFrame(self, width=largura/3, corner_radius=10)
        self.frameCentral.grid(row=0, column=1,rowspan=8, sticky="nsew")
        # self.frameCentral.grid_rowconfigure(2, weight=1)

        self.frameDireito = customtkinter.CTkFrame(self, width=largura/3, corner_radius=10)
        self.frameDireito.grid(row=0, column=3,rowspan=16, sticky="nsew")
        # self.frameDireito.grid_rowconfigure(3, weight=1)

    def temas(self):
        self.labelTema=customtkinter.CTkLabel(master=self.frameEsquerdo,text='Tema:',bg_color='transparent',text_color=['#000','#fff'])
        self.labelTema.grid(row=3,column=0,padx=10,pady=10)
        self.opcoesTema=customtkinter.CTkOptionMenu(master=self.frameEsquerdo,values=['Light','Dark','System'],command=self.mudaTema)
        self.opcoesTema.grid(row=4,column=0,padx=10,pady=10)

    def verificaOpcao(self,tamanhoLista,opcaoPersonagem):
        confirmacao=True
        print(opcaoPersonagem)
        print(tamanhoLista)
        if not opcaoPersonagem.isdigit() or int(opcaoPersonagem)<0 or int(opcaoPersonagem)>tamanhoLista:
            print(f'Opção inválida! Selecione um personagem.')
            manipula_funcoes.linhaSeparacao()
            confirmacao=False
        return confirmacao
    
    def mudaTema(self,novaAparencia):
        customtkinter.set_appearance_mode(novaAparencia)

if __name__=='__main__':
    app=App()
    app.mainloop()
# print(f'{retornaVidaMana(vida,esquerda)}%')
# desenhaMiniMapa()