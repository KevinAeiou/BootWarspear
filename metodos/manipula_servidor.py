import socket
import time
import manipula_teclado

servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind(('',55555))
print(f'Esperando conecção...')
servidor.listen(1)
coneccao,endereco = servidor.accept()
while True:
    coordenadas = coneccao.recv(1024).decode()
    coordenada = coordenadas.split(',')
    manipula_teclado.click_mouse_esquerdo(1,int(coordenada[0]),int(coordenada[1]))
    time.sleep(0.5)