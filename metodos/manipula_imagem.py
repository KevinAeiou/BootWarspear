import cv2
import numpy as np
import pytesseract
from PIL import Image
import mahotas
import time
from PIL import ImageChops

tela = 'atualizacao_tela.png'
testeDigitos='testeDigitos.png'

#cor letras voltar, avançar, fechar, jogar (93,218,254)

def salva_nova_tela(screenshot):
    imagem = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(tela, imagem)

def recorta_frame(frame):
    imagem = abre_imagem(tela)
    if 'novo_modelo_habilidade' in frame:
        nome_arquivo = f'modelos/{frame}.png'
        fatia_imagem = imagem[719:719+33,85:85+43]
    #frame especial habilidade
    #fatia_imagem = imagem[33:95,175:189]
    #frame = f'modelos/modelo_menu_{id}.png'
    #recorta frame do centro do menu
    #fatia_imagem = imagem[336:336+117, 280:280+117]
    #recorta frame profissoes e trabalhos atuais
    #fatia_imagem = imagem[242:242+27,248:248+185]
    #recorta frame inferior da esquerda do menu
    #fatia_imagem = imagem[611:611+32,168:168+141]
    #recorta frame inferior direito do menu 611:642,371:512
    #fatia_imagem = imagem[703:703+53,627:627+53]
    cv2.imwrite(nome_arquivo, fatia_imagem)
    return fatia_imagem

def reconhece_digito(imagem):
    inicio = time.time()
    # tesseract image.png output --oem 3 --psm 11 -c tessedit_char_whitelist=0123456789
    caminho = r"C:\Program Files\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
    #busca texto das produções
    # texto_reconhecido = pytesseract.image_to_string(imagem, lang="por")
    digitoReconhecido=pytesseract.image_to_string(imagem, config='outputbase digits')
    fim = time.time()
    print(f'Tempo de reconhece_digito: {fim - inicio}')
    print(f'____________________________________________________')
    return digitoReconhecido

def reconhece_texto(imagem):
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

def transforma_caracteres_preto(imagem_original):
    # inicio = time.time()
    #marrom1 = 48,87,164
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]):
            #se a cor do pixel for diferente de preto ou marrom 
            if (imagem_original[y,x] == (0,255,255)).all()\
                or(imagem_original[y,x] == (139,236,255)).all()\
                or(imagem_original[y,x] == (93,218,254)).all()\
                or(imagem_original[y,x] == (255,255,255)).all()\
                or(imagem_original[y,x] == (255,102,255)).all()\
                or(imagem_original[y,x] == (88,219,255)).all():
                #tranforma pixel em preto
                imagem_tratada[y,x] = (0,0,0)
            else:
                imagem_tratada[y,x] = (255,255,255)
    # fim = time.time()
    # print(f'Tempo de transforma_caracteres_preto: {fim - inicio}')
    # print(f'____________________________________________________')
    return imagem_tratada

def transforma_menu_preto(imagem_original):
    #marrom1 = 48,87,164
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]):
            #se a cor do pixel for diferente de preto ou marrom 
            if (imagem_original[y,x] == (93,218,254)).all():
                #tranforma pixel em preto
                imagem_tratada[y,x] = (0,0,0)
            else:
                imagem_tratada[y,x] = (255,255,255)
    return imagem_tratada

def transforma_branco_preto(imagem_original):
    #marrom1 = 48,87,164
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]):
            #se a cor do pixel for diferente de preto ou marrom 
            if (imagem_original[y,x] == (255,255,255)).all():
                #tranforma pixel em preto
                imagem_tratada[y,x] = (0,0,0)
            else:
                imagem_tratada[y,x] = (255,255,255)
    return imagem_tratada

def trata_frame_nivel_trabalho(imagem_original):#transforma pixels vermelhos em preto e resto em branco
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]):
            #se a cor do pixel for diferente de branco
            if (imagem_original[y,x] == (255,0,0)).all():
                #tranforma pixel em preto
                imagem_tratada[y,x] = (255,255,255)
            else:
                imagem_tratada[y,x] = (0,0,0)

    return imagem_tratada

def trata_frame_menu_profissao(imagem_original):
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]): 
            if (imagem_original[y,x] != (41,49,49)).any() and (imagem_original[y,x] != (41,66,66)).any():
                #tranforma pixel em branco
                imagem_tratada[y,x] = (255,255,255)
    return imagem_tratada

def trata_frame_nome_inimigo(imagem_original):
    imagem_tratada = imagem_original
    for y in range(0,imagem_original.shape[0]):
        for x in range(0, imagem_original.shape[1]): 
            if (imagem_original[y,x] == (0,0,255)).all():
                #tranforma pixel em branco
                imagem_tratada[y,x] = (255,255,255)
    return imagem_tratada

def trata_imagem(imagem_preto_branco):
    for y in range(0,imagem_preto_branco.shape[0]):
        for x in range(0, imagem_preto_branco.shape[1]):
            #se as coordenadas forem menores que 17 pixels
            if y<17 or x<17:
                #transforma o pixel em outra cor
                imagem_preto_branco[y,x] = (255,100,255)
            #se o pixel for diferente de branco,
            if (imagem_preto_branco[y,x] != (255,255,255)).any():
                #transforma o pixel em branco
                imagem_preto_branco[y,x] = (255,255,255)
            #se o pixel é branco
            elif (imagem_preto_branco[y,x] == (255,255,255)).any():
                #transforma o pixel em preto
                imagem_preto_branco[y,x] = (0,0,0)
    return imagem_preto_branco

def abre_imagem(caminho_imagem):
    imagem = cv2.imread(caminho_imagem)
    return imagem

def mostra_imagem(indice,imagem,nome_frame):
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

def retorna_imagem_cinza(screenshot):
    imagem = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    return imagem

def retorna_imagem_concatenada(imagem,imagem2):
    imagem_concatenada = cv2.hconcat([imagem,imagem2])
    return imagem_concatenada

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

def retorna_imagem_equalizada(img_original):
    img = cv2.cvtColor(np.array(img_original), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl2 = clahe.apply(img)
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

def temporario():
    imagem_teste = abre_imagem(testeDigitos)
    digitos=reconhece_digito(imagem_teste)
    print(f'Digitos reconhecidos: {digitos}')

# temporario()