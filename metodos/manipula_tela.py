import time
import win32api
import manipula_cliente
import manipula_funcoes
import manipula_imagem
import pyautogui as tecla

def busca_tecla_especifica():
    a = win32api.GetKeyState(0x01)
    if a<0:
        x,y = tecla.position()
        coordenadas = f'{int(x)},{int(y)}'
        manipula_cliente.envia_dados_servidor(coordenadas)

def desenhaMiniMapa():
    telaInteira=manipula_funcoes.retorna_atualizacao_tela()
    larguraTela=telaInteira.shape[1]
    alturaTela=telaInteira.shape[0]
    metadeLargura=larguraTela//2
    metadeAltura=alturaTela//2
    pixelInicial=[metadeAltura-150,metadeLargura-50]
    # while pixelInicial!=(0,0,0).all():


    manipula_imagem.mostra_imagem(0,frameTela,None)

desenhaMiniMapa()