import time
import win32api
import manipula_cliente
import pyautogui as tecla

def busca_tecla_especifica():
    a = win32api.GetKeyState(0x01)
    if a<0:
        x,y = tecla.position()
        coordenadas = f'{int(x)},{int(y)}'
        manipula_cliente.envia_dados_servidor(coordenadas)