import cv2
import os
import numpy as np
import pytesseract
from PIL import Image
from manipula_teclado import *
from lista_chaves import *
from keras.models import load_model
# import mahotas
import time

tela = 'atualizacao_tela.png'
testeDigitos='testeDigitos.png'

#cor letras voltar, avançar, fechar, jogar (93,218,254)

# model = load_model("modelos/keras_Model.h5", compile=False)
classes=['Desconhecido','ToBraba']
# data = np.ndarray(shape=(1, 80, 60, 3),dtype=np.float32)

def salvaImagem(caminho,titulo,imagem):
    if os.path.isdir(caminho):
         cv2.imwrite('{caminho}/{}'.format(titulo),imagem)
    else:
        os.makedirs('{caminho}')
        cv2.imwrite('{caminho}/{}'.format(titulo),imagem)

def salvaNovaTela(screenshot):
    imagem = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(tela, imagem)

def recortaFrame(frame):
    imagem = abre_imagem(tela)
    if 'novo_modelo_habilidade' in frame:
        nome_arquivo = f'modelos/{frame}.png'
        fatia_imagem = imagem[719:719+33,85:85+43]
    cv2.imwrite(nome_arquivo, fatia_imagem)
    return fatia_imagem

def reconhece_digito(imagem):
    inicio = time.time()
    # tesseract image.png output --oem 3 --psm 11 -c tessedit_char_whitelist=0123456789
    caminho = r"C:\Program Files\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
    #busca texto das produções
    # texto_reconhecido = pytesseract.image_to_string(imagem, lang="por")
    digitoReconhecido=pytesseract.image_to_string(imagem,
                                                  config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    fim = time.time()
    # print(f'Tempo de reconhece_digito: {fim - inicio}')
    # print(f'____________________________________________________')
    return digitoReconhecido

def reconheceTexto(imagem):
    # inicio = time.time()
    # tesseract image.png output --oem 3 --psm 11 -c tessedit_char_whitelist=0123456789
    texto=None
    caminho = r"C:\Program Files\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
    #busca texto das produções
    texto_reconhecido=pytesseract.image_to_string(imagem, lang="por")
    if len(texto_reconhecido)!=0:
        lista_caracteres_especiais = ['"','',',','.','|','!','@','$','%','¨','&','*','(',')','_','-','+','=','§','[',']','{','}','ª','º','^','~','?','/','°',':',';','>','<','\'','\n']
        # lista_caracteres_numericos = ['0','1','2','3','4','5','6','7','8','9']
        # for numero in lista_caracteres_numericos:
        #     texto_reconhecido = texto_reconhecido.replace(numero,'')
        for especial in lista_caracteres_especiais:
            texto_reconhecido = texto_reconhecido.replace(especial,'')
        texto=texto_reconhecido
        # fim = time.time()
    # print(f'Tempo de reconhece_texto: {fim - inicio}')
    # print(f'____________________________________________________')
    return texto

def trata_frame_nome_inimigo(imagem_original):
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]): 
            if (imagem_original[y,x] == (0,0,255)).all():
                #tranforma pixel em branco
                imagem_tratada[y,x] = (255,255,255)
    return imagem_tratada

def abre_imagem(caminho_imagem):
    imagem = cv2.imread(caminho_imagem)
    return imagem

def mostraImagem(indice,imagem,nome_frame):
    if nome_frame == None:
        nome_frame = 'Janela teste'
    cv2.imshow(nome_frame,imagem)
    cv2.waitKey(indice)
    cv2.destroyAllWindows()

def retorna_histograma(imagem):
    return cv2.calcHist([imagem],[0],None,[256],[0,256])

def retorna_comparacao_histogramas(histograma,histograma1):
    c1=0
    i=0
    while i<len(histograma)and i<len(histograma1):
        c1+=(histograma[i]-histograma1[i])**2
        i+=1 
    return c1**(1/2)

def retorna_imagem_colorida(screenshot):
    imagem = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return imagem

def retornaImagemCinza(screenshot):
    imagem = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    return imagem

def retorna_imagem_concatenada(imagem,imagem2):
    imagem_concatenada = cv2.vconcat([imagem,imagem2])
    return imagem_concatenada

def vconcat_resize(img_list, interpolation  
                   = cv2.INTER_CUBIC): 
      
    w_min = min(img.shape[1]  
                for img in img_list) 
      
    
    im_list_resize = [cv2.resize(img, 
                      (w_min, int(img.shape[0] * w_min / img.shape[1])), 
                                 interpolation = interpolation) 
                      for img in img_list] 
    
    return cv2.vconcat(im_list_resize) 

def retorna_subtracao_imagem(imagem1,imagem2):
    tamanho_imagem1 = imagem1.shape[:2]
    tamanho_imagem2 = imagem2.shape[:2]
    if tamanho_imagem1 == tamanho_imagem2:
        diferenca = cv2.subtract(imagem1, imagem2)
        #mostra_imagem('Subtração', diferenca)
        b, g, r = cv2.split(diferenca)
        if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
            return True
    else:
        print(f'Imagens com tamanhos diferentes.{tamanho_imagem1}:{tamanho_imagem2}')
    return False

def retornaImagemEqualizada(img):
    inicio = time.time()
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl2 = clahe.apply(img)
    fim = time.time()
    # print(f'{D}:{fim-inicio}.')
    return cl2

def retorna_modelo_nivel_tratado(modelo_original):
    lista_cores = [[21,74,114],[55,88,106],[33,70,104],[71,99,113],[66,113,133],[25,61,98],[62,108,128],[32,81,115],[9,54,101],[26,87,124],[10,86,131],[23,60,96],[41,80,105],[82,90,107],[74,82,90],[60,89,109],[77,91,110],[69,83,103],[64,94,111],[84,92,100],[72,84,94]]
    modelo_tratado = modelo_original
    for altura in range(0,modelo_original.shape[0]):
        for largura in range(0,modelo_original.shape[1]):
            for x in range(len(lista_cores)):
                if (modelo_original[altura,largura] == lista_cores[x]).any():
                    modelo_tratado[altura,largura] = (255,255,255)
    return modelo_tratado

def retorna_imagem_redimensionada(imagem_original,porcentagem):
    imagem_original = cv2.cvtColor(np.array(imagem_original), cv2.COLOR_RGB2BGR)
    largura = imagem_original.shape[1]
    altura = imagem_original.shape[0]
    nova_largura = int(largura*porcentagem)
    nova_altura = int(altura*porcentagem)
    novo_tamanho = (nova_largura,nova_altura)
    imagem_redimensionada = cv2.resize(imagem_original,
                                        novo_tamanho,interpolation=cv2.INTER_AREA)
    return imagem_redimensionada
#não funciona
def retorna_imagem_contorno():
    imagem_original = cv2.imread(tela)
    img = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2GRAY)
    suave = cv2.blur(img, (7, 7))

    T = mahotas.thresholding.otsu(suave)
    bin = suave.copy()
    bin[bin > T] = 255
    bin[bin < 255] = 0
    bin = cv2.bitwise_not(bin)
    bordas = cv2.Canny(bin, 0, 10)
    objetos,_ = cv2.findContours(bordas.copy(),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imgC2 = imagem_original.copy()
    # cv2.drawContours(imgC2, objetos, -1, (255, 0, 0), 2)
    for i in objetos:
        M = cv2.moments(i)
        if M['m00'] != 0:
            largura = int(M['m10']-M['m00'])
            x = int(largura+M['m00'])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            area = cv2.contourArea(i)
            if int(area)>1:
                cv2.drawContours(imgC2, [i], -1, (0, 255, 0), 2)
                cv2.circle(imgC2, (cx, cy), 4, (0, 0, 255), -1)
                # cv2.circle(imagem_original, (cx, cy), 7, (0, 0, 255), -1)
                # cv2.putText(imagem_original, "center", (cx - 20, cy - 20),
                #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                # print(f"x: {cx} y: {cy}")
                print(area)
    return imgC2

def retornaImagemCoresInvertidas(imagem):
    return cv2.bitwise_not(imagem)

def mostra_video(caminho_video):
    cap = cv2.VideoCapture(caminho_video)
    if (cap.isOpened() == False):
        print(f'Erro ao abrir o video.')
    while(cap.isOpened()):
        ret, frame = cap.read() 
        if ret == True: 
            cv2.imshow('Frame', frame) 
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break
        else:  
            break
    cap.release() 
    cv2.destroyAllWindows() 

def retorna_fundo_branco():
    return np.ones((200,200,3))*255

def retornaImagemBinarizada(image):
    inicio = time.time()
    blur = cv2.GaussianBlur(image, (1, 1), 
                        cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blur, 180, 255,
                            cv2.THRESH_BINARY_INV)
    # ret, thresh = cv2.threshold(blur,180, 255,
    #                         cv2.THRESH_BINARY)
    fim = time.time()
    # print(f'{D}:Tempo de salvaLimiarImagem: {fim - inicio}')
    return thresh

def retornaImagemDitalata(imagem,kernel,iteracoes):
    return cv2.dilate(imagem,kernel,iterations=iteracoes)

def retornaImagemErodida(imagem,kernel,iteracoes):
    return cv2.erode(imagem,kernel,iterations=iteracoes)

def preProcessamento(imagem):
    imagem=retornaImagemCinza(imagem)
    # imagem=cv2.GaussianBlur(imagem,(1,1),0)
    # t_lower = 254  # Lower Threshold
    # t_upper = 255  # Upper threshold
    imagem=cv2.GaussianBlur(imagem,(5,5),0)
    t_lower = 180  # Lower Threshold
    t_upper = 255  # Upper threshold
    imagem=cv2.Canny(imagem,t_lower,t_upper)
    # kernel=np.ones((2,2),np.uint8)
    # imagem=cv2.dilate(imagem,kernel,iterations=7)
    # imagem=cv2.erode(imagem,kernel,iterations=7)
    kernel=np.ones((3,3),np.uint8)
    imagem=retornaImagemDitalata(imagem,kernel,4)
    imagem=retornaImagemErodida(imagem,kernel,4)
    return imagem

def detectarPersonagem(imagem):
    index=0
    coresToBraba=[(255,0,197),(66,247,255),(170,66,70),(58,206,239),(173,0,148),(58,0,58),(16,74,140)]
    if encontraPixelCor(imagem,coresToBraba):
        index=1
    # imagemPersonagem=cv2.resize(imagem,(60,80))
    # imagemPersonagem=np.asarray(imagemPersonagem)
    # imagemNormalizada=(imagemPersonagem.astype(np.float32)/127.0)-1
    # data[0]=imagemNormalizada
    # predicao=model.predict(data)
    # index=np.argmax(predicao)
    # porcentagem=predicao[0][index]
    classe=classes[index]
    return classe

def encontraPixelCor(imagem,cores):
    for y in range(0,imagem.shape[0]):
        for x in range(0, imagem.shape[1]):
            for cor in cores:
                if (imagem[y,x]==cor).all():
                    return True
    return False

def encontraPersonagem():
    while True:
        screenshot=tira_screenshot()
        telaInteira=retorna_imagem_colorida(screenshot)
        metadeTela=telaInteira[0:telaInteira.shape[0],0:telaInteira.shape[1]//2]
        imagemPreprocessada=preProcessamento(metadeTela)
        contornos,h1=cv2.findContours(imagemPreprocessada,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area=cv2.contourArea(cnt)
            if area>1600 and area<3000:#2400/2600 area personagem de boa
                x,y,l,a=cv2.boundingRect(cnt)
                recorte=metadeTela[y:y+a,x:x+l]
                classe=detectarPersonagem(recorte)
                cv2.putText(metadeTela,str(classe),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
                # cv2.imwrite(f'modelos/personagemTeste/imagem{contador}.png',recorte)
                cv2.rectangle(metadeTela,(x,y),(x+l,y+a),(0,255,0),2)
        cv2.imshow('Metade da tela processada',imagemPreprocessada)
        # cv2.imshow('Metade da tela',metadeTela)
        if cv2.waitKey(3) &0xFF==ord('q'):
            break
    cv2.destroyAllWindows()

def encontraMenu():
    # 
    #  nucleoBlur=1,nucleoDilate=2,interation=1,t_lower = 70  # Lower Threshold,t_upper = 180  # Upper threshold
    nucleoBlur=1
    nucleoDilate=2
    interation=1
    t_lower = 150  # Lower Threshold
    t_upper = 180  # Upper threshold
    while True:
        screenshot=tira_screenshot()
        telaInteira=retorna_imagem_colorida(screenshot)
        metadeTela=telaInteira[0:telaInteira.shape[0],0:telaInteira.shape[1]//2]
        imagem=retornaImagemCinza(metadeTela)
        imagem=cv2.GaussianBlur(imagem,(nucleoBlur,nucleoBlur),0)
        imagem=cv2.Canny(imagem,t_lower,t_upper)
        kernel=np.ones((nucleoDilate,nucleoDilate),np.uint8)
        imagem=retornaImagemDitalata(imagem,kernel,interation)
        imagem=retornaImagemErodida(imagem,kernel,interation)
        contornos,h1=cv2.findContours(imagem,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area=cv2.contourArea(cnt)
            if area>500:#2400/2600 area personagem de boa
                # print(f'Area: {area}.')
                x,y,l,a=cv2.boundingRect(cnt)
                # print(f'Largura: {l}.')
                # print(f'Altura: {a}.')
                # recorte=metadeTela[y:y+a,x:x+l]
                # cv2.imwrite(f'modelos/personagemTeste/imagem{contador}.png',recorte)
                cv2.rectangle(metadeTela,(x,y),(x+l,y+a),(0,255,0),2)
        cv2.imshow('Metade da tela processada',imagem)
        cv2.imshow('Metade da tela',metadeTela)
        if cv2.waitKey(25) &0xFF==ord('q'):
            break
        # nucleoBlur=int(input(f'nucleoblur: '))
        # nucleoDilate=int(input(f'nucleoDilate: '))
        # interation=int(input(f'interation: '))
        # t_lower = int(input(f't_lower: '))
        # t_upper = int(input(f't_upper: '))
        # print(f'_____________________________________________')
    cv2.destroyAllWindows()

def temporario():
    cap = cv2.VideoCapture('C:/Users/Kevin/Videos/Captures/DG_MINAS_ABANDONADAS.mp4') 
    porcentagem=50
    nucleoBlur=1
    nucleoDilate=3
    interation=9
    t_lower=254
    t_upper=255
    if (cap.isOpened()== False):  
        print("Error opening video  file") 
    while(cap.isOpened()): 
        ret, frame = cap.read()
        alturaDesejada=frame.shape[0]*porcentagem/100
        larguraDesejada=frame.shape[1]*porcentagem/100
        frame=cv2.resize(frame,(int(larguraDesejada),int(alturaDesejada)))
        imagem=retornaImagemCinza(frame)
        imagem=cv2.GaussianBlur(imagem,(nucleoBlur,nucleoBlur),0)
        imagem=cv2.Canny(imagem,t_lower,t_upper)
        kernel=np.ones((nucleoDilate,nucleoDilate),np.uint8)
        imagem=cv2.dilate(imagem,kernel,iterations=interation)
        imagem=cv2.erode(imagem,kernel,iterations=interation)
        # imagemPreprocessada=preProcessamento(frame)
        contornos,h1=cv2.findContours(imagem,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area=cv2.contourArea(cnt)
            if area>300 and area<1000:#14500 de boa
                x,y,l,a=cv2.boundingRect(cnt)
                cv2.rectangle(frame,(x,y),(x+l,y+a),(0,255,0),2)
        # frameConcatenado=vconcat_resize([frame,imagemPreprocessada])
        if ret == True: 
            cv2.imshow('Frame', frame) 
            cv2.imshow('Frame tratado', imagem) 
            # cv2.imshow('Frame limiar', frameLimiar) 
            if cv2.waitKey(25) & 0xFF == ord('q')or 0xFF == 27: 
                break
        else:  
            break
    cap.release() 
    cv2.destroyAllWindows() 

def temporario2():
    porcentagem=50
    imagem=abre_imagem('/Users/Kevin/Videos/Captures/DG_MINAS_ABANDONADAS - frame.jpg')
    alturaDesejada=imagem.shape[0]*porcentagem/100
    larguraDesejada=imagem.shape[1]*porcentagem/100
    imagem=cv2.resize(imagem,(int(larguraDesejada),int(alturaDesejada)))
    while True:
        nucleoBlur=int(input(f'Núcleo de desfoque:'))
        nucleoDilate=int(input(f'Núcleo de dilate:'))
        mix=int(input(f'Mínimo threshhold:'))
        imagemCinza=retornaImagemCinza(imagem)
        blur = cv2.GaussianBlur(imagemCinza, (nucleoBlur,nucleoBlur), 
                        cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blur,mix, 255,
                                cv2.THRESH_BINARY)
        kernel=np.ones((nucleoDilate,nucleoDilate),np.uint8)
        imagemPreProcessada=cv2.dilate(thresh,kernel,iterations=4)
        imagemPreProcessada=cv2.erode(imagemPreProcessada,kernel,iterations=3)
        # imagemPreprocessada=preProcessamento(frame)
        contornos,h1=cv2.findContours(imagemPreProcessada,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area=cv2.contourArea(cnt)
            # if area>400 and area<800:#14500 de boa
            x,y,l,a=cv2.boundingRect(cnt)
            cv2.rectangle(imagemCinza,(x,y),(x+l,y+a),(0,255,0),2)

        concatenada=retorna_imagem_concatenada(imagemCinza,imagemPreProcessada)
        mostraImagem(0,concatenada,None)
        # mostraImagem(0,imagemPreProcessada,None)
        if cv2.waitKey(25) & 0xFF == ord('q')or 0xFF == 27: 
            break

# encontraMenu()