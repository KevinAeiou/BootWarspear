import time
import win32api
import manipula_cliente
import manipula_funcoes
import manipula_imagem
import pyautogui as tecla
import numpy as np

# vida=58,mana=78
# esquerda=38,direita=1194
esquerda=39
direita=509
vida=65
mana=85

corVidaMana=(0,0,148)#vermelho

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

# print(f'{retornaVidaMana(vida,esquerda)}%')
# desenhaMiniMapa()