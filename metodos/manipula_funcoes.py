import cv2
import numpy as np
import manipula_imagem
import manipula_teclado
import manipula_cliente
import time
import os.path
from unidecode import unidecode

xinicial=181
xfinal = 228
yinicial = 295
yfinal = 342

yinicial_nivel = 285
yfinal_nivel = 285 + 69

cont_voltas = 0
contador_paracima=4
personagem_id=''
altura_frame = 70
porcentagem_vida = 25

usuario_id = 'eEDku1Rvy7f7vbwJiVW7YMsgkIF2'
tela = 'atualizacao_tela.png'

def atualiza_nova_tela():
    imagem = manipula_teclado.tira_screenshot()
    manipula_imagem.salva_nova_tela(imagem)
    print(f'Atualizou a tela.')
    linha_separacao()

def adiciona_trabalho(personagem_id,trabalho,licenca):
    manipula_cliente.adiciona_trabalho(personagem_id,trabalho,licenca)
    linha_separacao()
#modificado16/01
def atualiza_lista_profissao(personagem_id):
    #285,355
    manipula_teclado.click_atalho_especifico('alt','tab')
    yinicial_profissao = 285
    #altura frame: 35 pixel
    #altura entre os frames: 70 pixel
    print(f'Atualizando lista de profissões...')
    linha_separacao()
    #limpa o arquivo lista_profissoes
    manipula_cliente.excluir_lista_profissoes(personagem_id)
    linha_separacao()
    for x in range(8):
        #print(f'Teste: {x}')
        #se x==4
        if x == 4:
            #clica 5x para baixo
            manipula_teclado.click_especifico(5,'down')
            #yinicial_profissao recebe valor fixo=529
            yinicial_profissao = 529
        #se x>4
        elif x > 4:
            #clica 1x para baixo
            manipula_teclado.click_especifico(1,'down')
            #yinicial_profissao recebe valor fixo=529
            yinicial_profissao = 529
        #atualiza tela
        tela_inteira = retorna_atualizacao_tela()
        #recorta frame do nome da profissao
        frame_nome_profissao = tela_inteira[yinicial_profissao:yinicial_profissao+35,233:456]
        #reconhece a profissao do frame
        nome_reconhecido = manipula_imagem.reconhece_texto(frame_nome_profissao)
        if nome_reconhecido == '':
            nome_reconhecido = 'Desconhecido'
        #grava o nome na lista de profissoes
        manipula_cliente.adicionar_profissao(personagem_id,unidecode(nome_reconhecido))
        #manipula_arquivo.inclui_linha(f'{unidecode(nome_reconhecido)},',caminho_arquivo_lista_profissoes)
        #incrementa o yinicial_profissao
        yinicial_profissao+=70
    print(f'Processo concluído!')
    linha_separacao()
    manipula_teclado.click_especifico(8,'up')
    return

def atualiza_referencias():
    tela_inteira = retorna_atualizacao_tela()
    largura_tela = tela_inteira.shape[1]
    frame_referencia1 = tela_inteira[705-50:705,0:50]
    frame_referencia2 = tela_inteira[705-50:705,largura_tela-50:largura_tela]
    return frame_referencia1, frame_referencia2

def pega_centro(x, y, largura, altura):
    """
    :param x: x do objeto
    :param y: y do objeto
    :param largura: largura do objeto
    :param altura: altura do objeto
    :return: tupla que contém as coordenadas do centro de um objeto
    """
    x1 = largura // 2
    y1 = altura // 2
    cx = x + x1
    cy = y + y1
    return cx, cy
#modificado 16/01
def cadastra_nome_trabalho(tipo_raridade_trabalho,nome_profissao):
    nivel_trabalho = input(f'Nivel do trabalho: ')
    linha_separacao()
    while not nivel_trabalho.isdigit() or int(nivel_trabalho)<0 or int(nivel_trabalho)>32:
        print(f'Opção inválida! Selecione uma das opções.')
        nivel_trabalho = input(f'Sua escolha: ')
        linha_separacao()
    else:
        nivel_trabalho = int(nivel_trabalho)
        if nivel_trabalho==0:
            print(f'Voltar...')
            linha_separacao()
            return
        while True:
            tela_inteira = retorna_atualizacao_tela()
            frame_nome_trabalho = tela_inteira[280:280+33,169:169+303]#frame nome trabalho menu especifico
            # frame_nome_trabalho = tela_inteira[273:273+311,167:167+347]
            nome_trabalho_reconhecido = manipula_imagem.reconhece_texto(frame_nome_trabalho)
            confirma_cadastro = input(f'Cadastrar {nome_trabalho_reconhecido}? Sim ou não(S/N): ')
            linha_separacao()
            while not confirma_cadastro.isalpha() or (str(confirma_cadastro).lower().replace('\n','')!='s' and str(confirma_cadastro).lower().replace('\n','')!='n'):
                print(f'Opção inválida! Cadastrar {nome_trabalho_reconhecido}?')
                confirma_cadastro = input(f'Sim ou não(S/N): ')
                linha_separacao()
            else:
                confirma_cadastro = str(confirma_cadastro).lower().replace('\n','')
                if confirma_cadastro == 's':
                    atributos_trabalho = f'{nome_trabalho_reconhecido},{tipo_raridade_trabalho},{nivel_trabalho},{nome_profissao},'
                    manipula_cliente.cadastrar_trabalho(atributos_trabalho)
                    #manipula_arquivo.inclui_linha(linha,tipo_raridade_trabalho)
                    print(f'{nome_trabalho_reconhecido} foi cadastrado!')
                    linha_separacao()
                novo_cadastro = str(input(f'Deseja cadastrar novo trabalho? Sim ou não(S/N): '))
                linha_separacao()
                while not novo_cadastro.isalpha() or (str(novo_cadastro).lower().replace('\n','')!='s' and str(novo_cadastro).lower().replace('\n','')!='n'):
                    print(f'Opção inválida! Cadastrar novo trabalho?')
                    novo_cadastro = input(f'Sim ou não(S/N): ')
                    linha_separacao()
                else:
                    novo_cadastro = str(novo_cadastro).lower().replace('\n','')
                    if novo_cadastro == 'n':
                        print(f'Voltar.')
                        linha_separacao()
                        break

def detecta_movimento():
    detec = []
    print(f'Atualizou o background.')
    backgroud = cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=255,detectShadows=False)
    referencia_anterior1, referencia_anterior2 = atualiza_referencias()
    while True:
        if not verifica_referencia_tela(referencia_anterior1):
        # if not verifica_referencia_tela(referencia_anterior1,referencia_anterior2):
            print(f'Atualizou o background.')
            backgroud = cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=255,detectShadows=False)
        tela_inteira = retorna_atualizacao_tela()
        altura_tela = tela_inteira.shape[0]
        frame_tela = tela_inteira[0:altura_tela,0:674]
        frame_tela = cv2.resize(frame_tela,(0,0),fx=0.9,fy=0.9)
        frame_tela_cinza = cv2.cvtColor(frame_tela,cv2.COLOR_BGR2GRAY)
        frame_tela_borado = cv2.GaussianBlur(frame_tela_cinza,(3,3),5)
        bg_frame = backgroud.apply(frame_tela_borado)
        frame_tela_dilatado = cv2.dilate(bg_frame,np.ones((5,5)))
        nucleo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        dilatado = cv2.morphologyEx(frame_tela_dilatado,cv2.MORPH_CLOSE,nucleo)

        contorno, imagem = cv2.findContours(dilatado, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for (i, c) in enumerate(contorno):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = (w >= 40) and (h >= 40)
            if not validar_contorno:
                continue
            cv2.rectangle(frame_tela, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame_tela, centro, 4, (0, 0, 255), -1)
        #Clicar no centro do objeto em movimento

        referencia_anterior1, referencia_anterior2 = atualiza_referencias()
        # cv2.imshow('Teste',dilatado)
        cv2.imshow('Teste2',frame_tela)
        print(centro)
        manipula_teclado.click_mouse_esquerdo(1,centro[0],centro[1])
        frame_nome_objeto = frame_tela[32:32+30,frame_tela.shape[1]-164:frame_tela.shape[1]]
        nome_objeto_reconhecido = manipula_imagem.reconhece_texto(frame_nome_objeto)
        print(f'Nome reconhecido: {nome_objeto_reconhecido}')
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.3)
    cv2.destroyAllWindows()

def detecta_movimento_teste():
    detec = []
    lista = []
    x=0
    print(f'Atualizou o background.')
    backgroud = cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=255,detectShadows=False)
    referencia_anterior1, referencia_anterior2 = atualiza_referencias()    
    while True:
        if not verifica_referencia_tela(referencia_anterior1):
            backgroud = cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=255,detectShadows=False)
        tela_inteira = retorna_atualizacao_tela()
        altura_tela = tela_inteira.shape[0]
        frame_tela = tela_inteira[0:altura_tela,0:674]
        #frame_tela = cv2.resize(frame_tela,(0,0),fx=0.9,fy=0.9)
        frame_tela_cinza = cv2.cvtColor(frame_tela,cv2.COLOR_BGR2GRAY)
        frame_tela_borado = cv2.GaussianBlur(frame_tela_cinza,(3,3),5)
        bg_frame = backgroud.apply(frame_tela_borado)
        frame_tela_dilatado = cv2.dilate(bg_frame,np.ones((5,5)))
        nucleo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        dilatado = cv2.morphologyEx(frame_tela_dilatado,cv2.MORPH_CLOSE,nucleo)

        contorno, imagem = cv2.findContours(dilatado, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for (i, c) in enumerate(contorno):
            (x, y, largura_objeto, altura_objeto) = cv2.boundingRect(c)
            validar_contorno = ((largura_objeto >= 42) and (altura_objeto >= 42))and((largura_objeto <= 90) and (altura_objeto <= 90))
            if not validar_contorno:
                continue
            cv2.rectangle(frame_tela, (x, y), (x + largura_objeto, y + altura_objeto), (0, 255, 0), 2)
            centro_objeto = pega_centro(x, y, largura_objeto, altura_objeto)
            detec.append(centro_objeto)
            cv2.circle(frame_tela, centro_objeto, 4, (0, 0, 255), -1)
        if len(detec)>0:
            largura_tela = tela_inteira.shape[1]
            raio_posicao = largura_tela/56
            ajuste_y = x+altura_objeto-int(raio_posicao)
            #manipula_teclado.click_mouse_esquerdo(1,centro_objeto[0],ajuste_y)
            tela_inteira = retorna_atualizacao_tela()
            nome_objeto_reconhecido=retorna_nome_inimigo(tela_inteira)
            if nome_objeto_reconhecido!='':
                print(nome_objeto_reconhecido)
                lista.append(nome_objeto_reconhecido)
            # while verifica_lista_inimigo(nome_objeto_reconhecido):
            #     tela_inteira=retorna_atualizacao_tela()
            #     nome_objeto_reconhecido=retorna_nome_inimigo(tela_inteira)
            #     verifica_lista_inimigo(nome_objeto_reconhecido)
        cv2.imshow('Teste',frame_tela)
        if cv2.waitKey(5)==27:
            break
        referencia_anterior1, referencia_anterior2 = atualiza_referencias()
        x+=1
    cv2.destroyAllWindows()
    print(lista)
#modificado16/01
def excluir_trabalho(trabalho_id):
    manipula_cliente.excluir_trabalho(trabalho_id)
#modificado 16/01
def mostra_lista(tipo_lista):
    lista = manipula_cliente.consutar_lista(tipo_lista)
    tamanho_lista = len(lista)
    if tamanho_lista>0:
        for x in range(tamanho_lista):
            print(f'{x+1} - {lista[x][1]}')
        print(f'0 - Voltar.')
    else:
        print(f'A lista está vazia.')
        linha_separacao()
        lista = 0
    return lista

def mostra_lista_desejo(tipo_lista):
    lista_desejo = manipula_cliente.consutar_lista(tipo_lista)
    tamanho_lista = len(lista_desejo)
    if tamanho_lista>0:
        for x in range(tamanho_lista):
            print(f'{lista_desejo[x][1]}')
        linha_separacao()
    else:
        print(f'A lista está vazia.')
        linha_separacao()
        lista_desejo = 0
    return lista_desejo

#modificado 16/01
def mostra_lista_trabalho(nome_profissao,raridade_trabalho):
    lista = manipula_cliente.consulta_lista_trabalho(nome_profissao,raridade_trabalho)
    tamanho_lista = len(lista)
    if tamanho_lista>0:
        for x in range(tamanho_lista):
            print(f'{x+1} - {lista[x][0]}')
        print(f'0 - Voltar.')
    else:
        print(f'A lista está vazia.')
        linha_separacao()
        lista = 0
    return lista

def verifica_lista_inimigo(nome_reconhecido):
    lista_inimigos = ['Sombradapodridãofuriosa','Mineradorlouco','Lobocego','adecãoebuliente','Chamadasprofundezas','Párialouco','Harpialadra','Sombradapodridão','Goblinmestreminério','ChifraçoAncião']
    for indice in range(len(lista_inimigos)):
        if lista_inimigos[indice]==nome_reconhecido:
            print(f'Encontrou: {lista_inimigos[indice]}')
            return True
    return False

def verifica_referencia_tela(referencia_anterior1):
# def verifica_referencia_tela(referencia_anterior1,referencia_anterior2):
    frame_referencia1, frame_referencia2 = atualiza_referencias() 
    histograma_referencia1 = manipula_imagem.retorna_histograma(frame_referencia1)
    histograma_referencia_anterior1 = manipula_imagem.retorna_histograma(referencia_anterior1)
    histograma_referencia2 = manipula_imagem.retorna_histograma(frame_referencia2)
    # histograma_referencia_anterior2 = manipula_imagem.retorna_histograma(referencia_anterior2)
    comparacao_histogramas1 = manipula_imagem.retorna_comparacao_histogramas(histograma_referencia1,histograma_referencia_anterior1)
    # comparacao_histogramas2 = manipula_imagem.retorna_comparacao_histogramas(histograma_referencia2,histograma_referencia_anterior2)
    if comparacao_histogramas1!=0:
    # if comparacao_histogramas1!=0 and comparacao_histogramas2!=0:
        print(f'Referencias não comferem.')
        return False
    return True

def verifica_menu_referencia():
    menu_referencia=manipula_imagem.abre_imagem('modelos/modelo_menu_0.png')
    tela_inteira=retorna_atualizacao_tela()
    tamanho_tela = tela_inteira.shape[:2]
    tamanho_referencia = menu_referencia.shape[:2]
    for x in range(420,tamanho_tela[1]):
        if x+tamanho_referencia[1]<=tamanho_tela[1]:
            for y in range(700,tamanho_tela[0]):
                if y+tamanho_referencia[0]<=tamanho_tela[0]:
                    frame_tela=tela_inteira[y:y+tamanho_referencia[0],x:x+tamanho_referencia[1]]
                    tamanho_frame_tela = frame_tela.shape[:2]
                    if tamanho_frame_tela==tamanho_referencia:
                        diferenca = cv2.subtract(frame_tela, menu_referencia)
                        b, g, r = cv2.split(diferenca)
                        if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                            # print(f'x: {posicao[0]}, y: {posicao[1]}')
                            return True
                    else:
                        print(f'Tamanho do menu referência e frame da tela diferentes!')
                        linha_separacao()
                else:
                    break
        else:
            break
    return False

def verifica_alvo():
    tela_inteira = retorna_atualizacao_tela()
    pixel_vida_alvo = tela_inteira[67,1194]
    return (pixel_vida_alvo == [33,25,255]).all()

def verifica_modo_ataque():
    #atualiza a tela
    tela_inteira = retorna_atualizacao_tela()
    pixel_modo_ataque = tela_inteira[55,0]
    return (pixel_modo_ataque != [66,197,230]).all()

def verifica_porcentagem_vida():
    tela_inteira = retorna_atualizacao_tela()
    xvida = int(38+(133*(porcentagem_vida/100)))
    if (tela_inteira[67,xvida]!=[33,25,255]).all() and (tela_inteira[67,xvida]!=[0,0,205]).all():
        print(f'Vida abaixo de {porcentagem_vida}%.')
        return True
    return False
#Codigo modificado 23/01 11:20
def verifica_trabalho_concluido():
    #icone do primeiro espaço de produç 181,295 228,342
    tela_inteira = retorna_atualizacao_tela()
    frame_trabalho_concluido = tela_inteira[311:311+43, 233:486]
    texto = manipula_imagem.reconhece_texto(frame_trabalho_concluido)
    string_trabalho="Trabalho concluído"
    if texto != '' and texto == string_trabalho:
        print(f'Trabalho concluído!')
        linha_separacao()
        return True
    elif texto !='' and 'adicionarnovo' in texto.replace(' ','').lower():
        print(f'Nem um trabalho!')
    else:
        print(f'Em produção...')
    linha_separacao()
    return False
#modificado 10/01
def verifica_licenca(licenca_trabalho):
    licenca_reconhecida = retorna_licenca_reconhecida()
    print(f"Buscando: {licenca_trabalho}")
    linha_separacao()
    if 'licençasdeproduçaomaspode'in licenca_reconhecida.replace(' ','').lower():
        print(f"Parando programa...")
        exit()
    while not licenca_reconhecida.replace(' ','').lower()in licenca_trabalho.replace(' ','').lower():
        manipula_teclado.click_especifico(1,"right")
        licenca_reconhecida=retorna_licenca_reconhecida()
        print(f'Licença reconhecida: {licenca_reconhecida}.')
        if 'nenhumitem'in licenca_reconhecida.replace(' ','').lower():
            licenca_trabalho='licençadeproduçãodoiniciante'
    else:#se encontrou a licença buscada
        manipula_teclado.click_especifico(1,"f2")

def retorna_licenca_reconhecida():
    tela_inteira = retorna_atualizacao_tela()
    frame_tela = tela_inteira[275:317,169:512]
    frame_tela_equalizado = manipula_imagem.retorna_imagem_equalizada(frame_tela)
    licenca_reconhecida = manipula_imagem.reconhece_texto(frame_tela_equalizado)
    return licenca_reconhecida
#modifica 16/01
def retorna_producao_recursos(nome_trabalho_lista_desejo):
    lista_producao_recursos = ['Grande coleção de recursos comuns','Melhoria da substância comum','Melhorar licença comum','Licença de produção do aprediz','Melhoria da substância composta','Coleta em massa de recursos avançados']
    for x in lista_producao_recursos:
        if nome_trabalho_lista_desejo.replace(' ','').lower() in x.replace(' ','').lower():
            return True
    return False

def confirma_nome_trabalho(nome_trabalho_lista):
    #tira novo print da tela
    imagem_inteira = retorna_atualizacao_tela()
    frame_nome_trabalho = imagem_inteira[280:280+33,169:169+303]
    nome_trabalho = manipula_imagem.reconhece_texto(frame_nome_trabalho)
    if nome_trabalho.replace(' ','')[1:len(nome_trabalho)-1] in nome_trabalho_lista.replace(' ',''):
        print(f'Trabalho confirmado! {nome_trabalho}')
        return True
    print(f'Trabalho negado! {nome_trabalho}')
    return False
#modificado 16/01
def verifica_posicoes_trabalhos(profissao,conteudo_lista_desejo):
    yinicial_nome=285
    #xinicial=233, xfinal=478, yinicial=285, yfinal=324 altura=70
    #sempre faz três verificações
    time.sleep(1)
    for posicao_trabalho_reconhecido in range(4):
        nome_trabalho = retorna_nome_trabalho_reconhecido(yinicial_nome,0)
        print(f'Nome do trabalho disponível: {nome_trabalho}')
        #enquanto não comparar toda lista
        for trabalho_lista_desejo in conteudo_lista_desejo:
            #retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
            nome_trabalho_lista_desejo = trabalho_lista_desejo[1]
            nome_profissao_lista_desejo = trabalho_lista_desejo[2]
            raridade_trabalho_lista_desejo = trabalho_lista_desejo[5]
            #se o trabalho na lista de desejo NÃO for da profissão verificada no momento, passa para o proximo trabalho na lista
            if profissao==nome_profissao_lista_desejo:
                if raridade_trabalho_lista_desejo == 'Comum':
                    print(f'Verificando trabalho comum...')
                    linha_separacao()
                    return 0,trabalho_lista_desejo
                if nome_trabalho == '':
                    break
                print(f'Nome do trabalho na lista: {nome_trabalho_lista_desejo}')
                if nome_trabalho.replace(' ','').lower() in nome_trabalho_lista_desejo.replace(' ','').lower():
                    return posicao_trabalho_reconhecido,trabalho_lista_desejo
        linha_separacao()
        yinicial_nome = yinicial_nome+70
    else:
        manipula_teclado.click_especifico(4,'up')
        manipula_teclado.click_especifico(1,'left')
        print(f'Nem um trabalho disponível está na lista de desejos.')
        linha_separacao()
        return 0,None

def verifica_trabalho_comum(trabalho_lista_desejo,nome_profissao_verificada):
    manipula_teclado.click_especifico(5,'down')
    global contador_paracima
    contador_paracima=5
    while True:
        nome_trabalho_reconhecido = retorna_nome_trabalho_reconhecido(530,1)
        nome_trabalho = trabalho_lista_desejo[1]
        nome_profissao = trabalho_lista_desejo[2]
        print(f'Trabalho reconhecido: {nome_trabalho_reconhecido}')
        print(f'Trabalho na lista: {nome_trabalho}')
        linha_separacao()
        if nome_profissao_verificada==nome_profissao:
            if nome_trabalho_reconhecido=='':
                manipula_teclado.click_especifico(1,'f1')
                manipula_teclado.click_especifico(contador_paracima,'up')
                manipula_teclado.click_especifico(1,'left')
                break
            elif nome_trabalho_reconhecido.replace(' ','').lower() in nome_trabalho.replace(' ','').lower():
                manipula_teclado.click_especifico(1,'enter')
                contador_paracima+=1
                break
        manipula_teclado.click_especifico(1,'down')
        contador_paracima+=1
        # print(f'Teste de contador: {contador_paracima}')

def retorna_nome_trabalho_reconhecido(yinicial_nome,identificador):
    #tira novo print da tela
    imagem_inteira = retorna_atualizacao_tela()
    #recorta frame para reconhecimento de texto
    if identificador == 0:
        altura = 39
    elif identificador == 1:
        altura = 68
    frame_nome_trabalho = imagem_inteira[yinicial_nome:yinicial_nome+altura,233:478]
    #teste trata frame trabalho comum
    frame_nome_trabalho_tratado = manipula_imagem.transforma_branco_preto(frame_nome_trabalho)
    # manipula_imagem.mostra_imagem(0,frame_nome_trabalho_tratado,'teste')
    #retorna texto encontrado
    return manipula_imagem.reconhece_texto(frame_nome_trabalho_tratado)

def sai_trabalho_encontrado(x):
    manipula_teclado.click_especifico(2,'f1')
    manipula_teclado.click_especifico(x+1,'up')

def entra_licenca():
    manipula_teclado.click_especifico(1,'up')
    manipula_teclado.click_especifico(1,'enter')

def entra_trabalho_encontrado(x):
    manipula_teclado.click_especifico(3,'up')
    manipula_teclado.click_especifico(x+1,'down')
    manipula_teclado.click_especifico(1,'enter')

def verifica_erro(nome_licenca):
    print(f'Verificando erro...')
    erro = retorna_tipo_erro()
    #erros processo de inicio de produção: 1,3,4,6,8
    if erro == 1:
        manipula_teclado.click_especifico(2,"enter")
        verifica_licenca(nome_licenca)
        return 1
    elif erro == 2:
        print(f'Tentando reconectar.')
        linha_separacao()
        manipula_teclado.click_especifico(2,'enter')
        return 2
    elif erro == 3:
        print(f'Retirando trabalho da lista.')
        print(f'Voltando para o menu profissões.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(contador_paracima,'up')
        manipula_teclado.click_especifico(1,'left')
        return 3
    elif erro == 4:
        print(f'Escolhendo item.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(2,'f2')
        manipula_teclado.click_especifico(9,'up')
        return 4
    elif erro == 5:
        time.sleep(3)
        return 5
    elif erro == 6:
        print(f'Voltando para o menu profissões.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(4,'up')
        manipula_teclado.click_especifico(1,'left')
        return 6
    elif erro == 7:
        print(f'Recuperar presente depois.')
        linha_separacao()
        manipula_teclado.click_especifico(2,'f1')
        return 7
    elif erro == 8:
        print(f'Espera trabalho ser concluido.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(4,'up')
        manipula_teclado.click_especifico(1,'left')
        print(f'Esperando trabalho ser concluído...')
        linha_separacao()
        while not verifica_trabalho_concluido():
            continue
        return 8
    elif erro == 9:
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(8,'up')
        return 9
    elif erro == 10:
        manipula_teclado.click_especifico(2,'enter')
        print(f'Voltando para a tela inicial.')
        linha_separacao()
        return 10
    elif erro == 11:
        manipula_teclado.click_especifico(2, 'enter')
        print(f'Voltando para a tela inicial.')
        linha_separacao()
        time.sleep(300)
        return 11
    elif erro == 12:
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(1,'up')
        manipula_teclado.click_especifico(1,'left')
        print(f'Ignorando trabalho concluído!')
        linha_separacao()
        return 12
    elif erro == 13:
        manipula_teclado.click_especifico(1,'enter')
        print(f'Erro ao conectar...')
        linha_separacao()
        return 13
    elif erro == 14:
        manipula_teclado.click_especifico(1,'f1')
        linha_separacao()
        return 14
    elif erro == 15:
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        print(f'Login ou senha incorreta...')
        linha_separacao()
        return 15
    print(f'Nem um erro encontrado!')
    linha_separacao()
    return 0
#modificado 12/01
def retorna_tipo_erro():
    tela_inteira = retorna_atualizacao_tela()
    frame_erro = tela_inteira[335:335+100,150:526]
    erro_encontrado = manipula_imagem.reconhece_texto(frame_erro)
    tipo_erro_trabalho = ['precisoumalicençadeproduçãoparainiciarotrabalho','Nãofoipossívelseconectaraoservidor','Vocênãotemosrecursosnecessáriasparaessetrabalho',
    'Vocêprecisaescolherumitemparainiciarumtrabalhodeprodução','Conectando','precisomaisexperiênciaprofissionalparainiciarotrabalho',
    'GostariadeiràLojaMilagrosaparaveralistadepresentes','Vocênãotemespaçoslivresparaotrabalho','agorapormoedas','OservidorestáemmanutençãoEstamosfazendodetudoparaconcluílaomaisrápvidopossível',
    'Foidetectadaoutraconexãousandoseuperfil','Gostanadecomprar','conexão com o servidor foi interrompida','Você precisa de mais moedas','Login ou senha incorreta']
    for tamanho_tipo_erro in range(len(tipo_erro_trabalho)):
        if tipo_erro_trabalho[tamanho_tipo_erro].replace(' ','').lower() in erro_encontrado.replace(' ','').lower():
            erro_encontrado=''
            return tamanho_tipo_erro+1
    return 0

def retorna_nome_inimigo(tela_inteira):
    altura_tela = tela_inteira.shape[0]
    frame_tela = tela_inteira[0:altura_tela,0:674]
    frame_nome_objeto = frame_tela[32:32+30,frame_tela.shape[1]-164:frame_tela.shape[1]]
    frame_nome_objeto_tratado = manipula_imagem.trata_frame_nome_inimigo(frame_nome_objeto)
    return manipula_imagem.reconhece_texto(frame_nome_objeto_tratado)

def retorna_lista_histograma_menu():
    lista_histograma = []
    print(f'Reconhecendo histograma dos menus.')
    linha_separacao()
    for x in range(10):
        #abre a imagem do modelo
        modelo = manipula_imagem.abre_imagem(f'modelos/modelo_menu_{x}.png')
        #calcula histograma do modelo
        histograma_modelo = manipula_imagem.retorna_histograma(modelo)
        lista_histograma.append(histograma_modelo)
    return lista_histograma

def retorna_posicao_habilidade(x_habilidade):
    xinicial=320
    distancia_habilidade=62
    for x in range(1,11):
        if int(x_habilidade)>=(xinicial+distancia_habilidade*x)-5 and int(x_habilidade)<=(xinicial+distancia_habilidade*x)+5:
            if x==6:
                posicao_habilidade='q'
            elif x==7:
                posicao_habilidade='w'
            elif x==8:
                posicao_habilidade='e'
            elif x==9:
                posicao_habilidade='r'
            elif x==10:
                posicao_habilidade='t'
            else:
                posicao_habilidade=f'num{x}'
            print(f'Posição encontrada: {posicao_habilidade}')
            break
    return posicao_habilidade

def retorna_lista_imagem_habilidade():
    lista_imagem_habilidade = []
    x=0
    while verifica_arquivo_existe(f'modelos/novo_modelo_habilidade_{x}.png'):
        modelo = manipula_imagem.abre_imagem(f'modelos/novo_modelo_habilidade_{x}.png')
        lista_imagem_habilidade.append(modelo)
        x+=1
    return lista_imagem_habilidade

def verifica_arquivo_existe(caminho_arquivo):
    if(os.path.exists(caminho_arquivo)):
          return True
    return False
#modificado 23/01
def verifica_nome_personagem(nome_personagem):
    print(f'Verificando nome personagem...')
    posicao_nome = [[197,354,170,27],[2,33,169,21]]
    tela_inteira = retorna_atualizacao_tela()
    for indice in range(len(posicao_nome)):
        frame_nome_personagem = tela_inteira[posicao_nome[indice][1]:posicao_nome[indice][1]+posicao_nome[indice][3],posicao_nome[indice][0]:posicao_nome[indice][0]+posicao_nome[indice][2]]
        frame_nome_personagem_tratado = manipula_imagem.transforma_amarelo_preto(frame_nome_personagem)
        nome_personagem_reconhecido = manipula_imagem.reconhece_texto(frame_nome_personagem_tratado)
        nome_personagem_reconhecido_tratado = unidecode(nome_personagem_reconhecido)
        # concatenado = manipula_imagem.retorna_imagem_concatenada(frame_nome_personagem,frame_nome_personagem_tratado)
        # manipula_imagem.mostra_imagem(0,concatenado,nome_personagem_reconhecido_tratado)
        print(f'Personagem reconhecido: {nome_personagem_reconhecido_tratado}')
        if nome_personagem_reconhecido_tratado!='' and nome_personagem_reconhecido_tratado.replace(' ','').lower()\
            in nome_personagem.replace(' ','').lower():
            print(f'Nome personagem confirmado!')
            linha_separacao()
            return True
    print(f'Nome personagem diferente!')
    linha_separacao()
    return False

def retorna_lista_profissao_verificada():
    print(f'Verificando profissões necessárias...')
    #cria lista vazia
    lista_profissao_verificada = []
    #abre o arquivo lista de profissoes
    conteudo_lista_profissoes = manipula_cliente.consutar_lista(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_profissoes')
    #abre o arquivo lista de desejos
    conteudo_lista_desejo = manipula_cliente.consulta_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo')
    #percorre todas as linha do aquivo profissoes
    for linhaProfissao in range(len(conteudo_lista_profissoes)):
        nome_profissao = conteudo_lista_profissoes[linhaProfissao]
        nome_profissao = nome_profissao[1]
        #percorre todas as linhas do aquivo lista de desejos
        for linhaDesejo in range(len(conteudo_lista_desejo)):
            atributos = conteudo_lista_desejo[linhaDesejo]
            nome_profissao_desejo = atributos[2]
            if(nome_profissao.lower()==nome_profissao_desejo.lower()):
                #verifca se o indice já está na lista
                lista_profissao_verificada.append([linhaProfissao+1,nome_profissao_desejo])
                break
    else:
        mostra_profissoes_necessarias(lista_profissao_verificada)
    return lista_profissao_verificada

def mostra_profissoes_necessarias(lista_profissao_verificada):
    for x in range(len(lista_profissao_verificada)):
        nome_profissao_necessaria = lista_profissao_verificada[x]
        print(f'Profissão necessária: {nome_profissao_necessaria[1]}')
    linha_separacao()

def retorna_lista_habilidade_verificada():
    print(f'Criando lista de habilidades...')
    lista_habilidade_encontrada = []
    lista_imagem_habilidade = retorna_lista_imagem_habilidade()
    tela_inteira = retorna_atualizacao_tela()
    altura_modelo = lista_imagem_habilidade[0].shape[0]
    largura_modelo = lista_imagem_habilidade[0].shape[1]
    for x in range(380,980):
        for y in range(726,730):
            frame_habilidade = tela_inteira[y:y+altura_modelo, x:x+largura_modelo]
            tamanho_frame_habilidade = frame_habilidade.shape[:2]
            for indice in lista_imagem_habilidade:
                tamanho_modelo = indice.shape[:2]
                if tamanho_frame_habilidade == tamanho_modelo:
                    diferenca = cv2.subtract(indice, frame_habilidade)
                    b, g, r = cv2.split(diferenca)
                    if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                        lista_habilidade_encontrada.append([x,indice])
                        # print(f'Habilidade reconhecida em: {x},{y}')
                        retorna_posicao_habilidade(x)
                        break
                else:
                    print(f'Modelos com tamanhos diferentes. {tamanho_frame_habilidade}:{tamanho_modelo}')
                    linha_separacao()
                    break
    else:
        print(f'Processo concluído!')
        linha_separacao()
    return lista_habilidade_encontrada

def passa_proxima_posicao():
    global yinicial, yfinal, altura_frame
    #passa para a proxima posição de produção
    yinicial = yfinal+23
    yfinal = yfinal+altura_frame

def entra_personagem_ativo(nome):
    print(f'Buscando personagem ativo...')
    menu=retorna_menu(None)
    while menu!=2:
        if menu==0:#se estiver no menu jogar
            manipula_teclado.click_especifico(1,'enter')
            menu=retorna_menu(None)
        elif menu==1:#se estiver no menu noticias
            manipula_teclado.click_especifico(1,'f2')
            menu=2
    else:#menu seleção de personagem
        manipula_teclado.vai_inicio_fila()                
        for x in range(13):
            if not verifica_nome_personagem(nome):
                manipula_teclado.click_especifico(1,'right')
            else:
                manipula_teclado.click_especifico(1,'f2')
                time.sleep(1)
                erro=verifica_erro('')
                if erro==0 or erro==5:
                    if retorna_menu(None)==41:
                        print(f'Login efetuado com sucesso!')
                        linha_separacao()
                        return True
                print(f'Erro ao tentar entrar...')
                linha_separacao()
                break
        else:
            print(f'Personagem não encontrado!')
            linha_separacao()
            manipula_teclado.click_especifico(1,'f1')
    return False

def retorna_medidas_modelos():
    lista_modelos = [1,2,5,9]
    lista_medidas = []
    print(f'Reconhecendo medidas dos tipos de menus.')
    linha_separacao()
    for x in range(len(lista_modelos)):
        nome_modelo = f'modelos/modelo_menu_{lista_modelos[x]}.png'
        modelo = manipula_imagem.abre_imagem(nome_modelo)
        lista_medidas.append(modelo.shape[:2])
    return lista_medidas
#modificado 16/01
def prepara_personagem(id_personagem):
    global personagem_id
    #lista_profissao_necessaria é uma matrix onde o indice 0=posição da profissão
    #e o indice 1=nome da profissão
    manipula_teclado.click_atalho_especifico('alt','tab')
    personagem_id=id_personagem
    lista_personagem_ativo = manipula_cliente.consulta_lista_personagem(usuario_id)#cria uma lista de personagens ativos
    nome, email, senha, estado = configura_atributos()
    if estado!=1:#se o personagem estiver inativo, troca o estado
        manipula_cliente.muda_estado_personagem(usuario_id,personagem_id)
    for personagem in lista_personagem_ativo:#percorre a lista de personagens ativos
        if personagem==personagem_id:#verifica se personagem selecionado está na lista
            if verifica_nome_personagem(nome):#verificar qual personagem está logado
                print('Inicia busca...')
                linha_separacao()
                while inicia_busca_trabalho():
                    continue
            else:#se o nome do personagem for diferente
                if configura_login_personagem(email, senha):
                    while not entra_personagem_ativo(nome):
                        continue
                    else:
                        manipula_teclado.click_atalho_especifico('alt','tab')
                        prepara_personagem(personagem_id)
            break

def configura_login_personagem(email, senha):
    menu=retorna_menu(None)
    while menu==1 or menu==2:
        manipula_teclado.click_especifico(1,'f1')
        menu=retorna_menu(None)
    if menu==0:
        loga_personagem(email,senha)
        return True
    else:
        while menu!=41:
            manipula_teclado.click_mouse_esquerdo(1,2,35)
            linha_separacao()
            menu=retorna_menu(None)
        if menu==41:
            manipula_teclado.encerra_secao()
            linha_separacao()
            loga_personagem(email,senha)
            return True
    return False

def configura_atributos():
    dados_personagem = manipula_cliente.consulta_dados_personagem(usuario_id,personagem_id)
    nome = dados_personagem[1]
    email = dados_personagem[2]
    senha = dados_personagem[3]
    estado = dados_personagem[4]
    return nome,email,senha,estado
    
def loga_personagem(email, senha):
    print(f'Tentando logar conta personagem...')
    manipula_teclado.entra_secao(email,senha)
    linha_separacao()
    while verifica_erro('')!=0:
        manipula_teclado.entra_secao(email,senha)
        linha_separacao()
    print(f'Login efetuado com sucesso!')
    linha_separacao()

def inicia_busca_trabalho():
    posicao=0
    nome=1
    lista_profissao_necessaria=retorna_lista_profissao_verificada()
    if len(lista_profissao_necessaria)>0:#verifica se a lista está vazia
        conteudo_lista_desejo=manipula_cliente.consulta_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo')
        if len(conteudo_lista_desejo)>0:#verifica se a lista está vazia
            for profissao_necessaria in lista_profissao_necessaria:#percorre lista de profissao
                menu=retorna_menu(None)
                while menu!=11:
                    trata_menu(menu)
                    menu=retorna_menu(None)
                nome_profissao = profissao_necessaria[nome]
                manipula_teclado.retorna_menu_profissao_especifica(profissao_necessaria[posicao])
                posicao_trabalho,trabalho_lista_desejo = verifica_posicoes_trabalhos(nome_profissao,conteudo_lista_desejo)
                if posicao_trabalho!=0 and trabalho_lista_desejo!=None:#inicia processo de produção
                    nome_trabalho_lista_desejo=trabalho_lista_desejo[nome]
                    entra_trabalho_encontrado(posicao_trabalho)
                    verifica_producao_recursos(posicao_trabalho, nome_trabalho_lista_desejo)
                    inicia_producao(trabalho_lista_desejo)
                elif posicao_trabalho==0 and trabalho_lista_desejo!=None:#inicia processo busca por trabalho comum
                    verifica_trabalho_comum(trabalho_lista_desejo,nome_profissao)
                    inicia_producao(trabalho_lista_desejo)
                if verifica_trabalho_concluido():
                    nome_trabalho_concluido=recupera_trabalho_concluido()
                    muda_estado_trabalho_concluido(nome_trabalho_concluido)
                else:
                    manipula_teclado.click_especifico(1,'left')
            return True
    print(f'Lista de trabalhos desejados vazia.')
    print(f'Voltando.')
    linha_separacao()
    return False

def muda_estado_trabalho_concluido(nome_trabalho_concluido):
    if verifica_erro('')==0:
        manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id,nome_trabalho_concluido,2)
    manipula_teclado.click_especifico(1,'up')
    manipula_teclado.click_especifico(1,'left')

def recupera_trabalho_concluido():
    tela_inteira = retorna_atualizacao_tela()
    frame_nome_trabalho = tela_inteira[285:285+37, 233:486]
    nome_trabalho_concluido = manipula_imagem.reconhece_texto(frame_nome_trabalho)
    manipula_teclado.click_especifico(1,'down')
    manipula_teclado.click_especifico(1,'f2')
    return nome_trabalho_concluido

def inicia_producao(trabalho):
    entra_licenca()
    verifica_licenca(trabalho[4])#verifica tipo de licença de produção
    manipula_teclado.click_especifico(1,'f2')#click que definitivamente começa a produção
    erro=verifica_erro(trabalho[4])
    if erro==0:
        if retorna_menu(trabalho)==17:#menu escolha equipamento
            manipula_teclado.click_especifico(2,'f2')
        menu=retorna_menu(trabalho)
        if menu==14:#trabalho especifico
            manipula_teclado.click_especifico(1,'f2')
            manipula_teclado.click_especifico(9,'up')
            manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id,trabalho[1],1)
        elif menu==12:#trabalhos atuais
            manipula_teclado.click_especifico(9,'up')
            manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id,trabalho[1],1)
        while verifica_erro(trabalho[4])!=0:
            continue
    elif erro==3:
        caminho_trabalho=f'{personagem_id}/Lista_desejo/{trabalho[0]}'
        manipula_cliente.excluir_trabalho(caminho_trabalho)
    
def verifica_producao_recursos(posicao_trabalho, nome_trabalho_lista_desejo):
    if not retorna_producao_recursos(nome_trabalho_lista_desejo):
        manipula_teclado.click_especifico(1,'down')
        manipula_teclado.click_especifico(1,'enter')
        if not confirma_nome_trabalho(nome_trabalho_lista_desejo):
            sai_trabalho_encontrado(posicao_trabalho)
        else:
            manipula_teclado.click_especifico(1,'f1')

def usa_habilidade():
    #719:752, 85:128 137:180 189:232
    #muda p/ outra janela
    manipula_teclado.click_atalho_especifico('alt','tab')
    manipula_teclado.click_atalho_especifico('win','up')
    #cria lista com habilidades a serem usadas
    lista_habilidade = retorna_lista_habilidade_verificada()
    if len(lista_habilidade)==0:
        print(f'Erro!')
        linha_separacao()
    else:
        print(f'Buscando referência!')
        linha_separacao()
        while True:
            if verifica_menu_referencia():
                #verifica se está em modo de ataque
                if verifica_modo_ataque() or verifica_alvo():
                    #percorre a lista de habilidades
                    for habilidade in lista_habilidade:
                        #atualiza a tela
                        tela_inteira = retorna_atualizacao_tela()
                        #recorta frame na posição da habilidade específica
                        frame_habilidade = tela_inteira[728:728+habilidade[1].shape[0], habilidade[0]:habilidade[0]+habilidade[1].shape[1]]
                        #define o tamanho do frame
                        tamanho_frame_habilidade = frame_habilidade.shape[:2]
                        #define o tamanho do modelo
                        tamanho_modelo = habilidade[1].shape[:2]
                        if verifica_porcentagem_vida() and verifica_menu_referencia():
                            manipula_teclado.click_especifico_habilidade(1,'t')
                        #compara os tamanhos das imagens
                        if tamanho_frame_habilidade == tamanho_modelo:
                            #subtrai as imgagens de comparação
                            diferenca = cv2.subtract(habilidade[1], frame_habilidade)
                            #divide os canais de cores
                            b, g, r = cv2.split(diferenca)
                            #se cada cor subtraida for igual a zero
                            if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                                #clica a tecla específica de cada habilidade
                                lista_habilidade_clicada = []
                                posicao_habilidade = retorna_posicao_habilidade(habilidade[0])
                                manipula_teclado.click_especifico_habilidade(1,posicao_habilidade)
                                linha_separacao()
                                #verica se a habilidade clicada precisa de click do mouse
                                lista_habilidade_clicada.append(habilidade)
                                if verifica_habilidade_central(lista_habilidade_clicada)!=0:
                                    x,y = manipula_teclado.retorna_posicao_mouse()
                                    manipula_teclado.click_mouse_esquerdo(1,x,y)
                                    linha_separacao()
                        else:
                            print(f'Modelos com tamanhos diferentes. {tamanho_frame_habilidade}-{tamanho_modelo}')
                            linha_separacao()
                posicao_habilidade=verifica_habilidade_central(lista_habilidade)
                if posicao_habilidade!=0:
                    manipula_teclado.click_especifico_habilidade(1,posicao_habilidade)
                    linha_separacao()

def verifica_habilidade_central(lista_habilidade):
    tela_inteira = retorna_atualizacao_tela()
    for indice in range(len(lista_habilidade)):
        habilidade=lista_habilidade[indice]
        for x in range(658,662):
            for y in range(666,670):
                frame_habilidade_central = tela_inteira[y:y+habilidade[1].shape[0],x:x+habilidade[1].shape[1]]
                if frame_habilidade_central.shape[:2]==habilidade[1].shape[:2]:
                    diferenca=cv2.subtract(frame_habilidade_central, habilidade[1])
                    b,g,r=cv2.split(diferenca)
                    # frame_concatenado = manipula_imagem.retorna_imagem_concatenada(frame_habilidade_central,diferenca)
                    # manipula_imagem.mostra_imagem(0,frame_concatenado,'Teste')
                    if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                        print(f'Habilidade central encontrada!')
                        # print(f'x: {x}, y: {y}')
                        linha_separacao()
                        return retorna_posicao_habilidade(habilidade[0])
                else:
                    print(f'Tamanho do frame diferente do modelo!')
                    linha_separacao()
    return 0

def recorta_novo_modelo_habilidade():
    lista_imagem_habilidade = retorna_lista_imagem_habilidade()
    indice = len(lista_imagem_habilidade)
    opcao = input(f'Recortar modelo: nº{indice}? Sim ou não. S/N: ')
    linha_separacao()
    while not opcao.isalpha() or (str(opcao).lower().replace('\n','')!='s' and str(opcao).lower().replace('\n','')!='n'):
        print(f'Opção inválida! Recortar modelo: nº {indice}?')
        opcao = input(f'Sim ou não. S/N: ')
        linha_separacao()
    else:
        opcao = str(opcao).lower().replace('\n','')
        while opcao!='n':
            atualiza_nova_tela()
            fatia = manipula_imagem.recorta_frame(f'novo_modelo_habilidade_{indice}')
            lista_imagem_habilidade = retorna_lista_imagem_habilidade()
            indice = len(lista_imagem_habilidade)
            opcao = input(f'Recortar modelo: nº{indice}? Sim ou não. S/N: ')
            linha_separacao()
            while not opcao.isalpha() or (str(opcao).lower().replace('\n','')!='s' and str(opcao).lower().replace('\n','')!='n'):
                print(f'Opção inválida! Recortar modelo: nº {indice}?')
                opcao = input(f'Sim ou não. S/N: ')
                linha_separacao()
        else:
            print(f'Voltar.')
            linha_separacao()

def modifica_quantidade_personagem_ativo():
    nova_quantidade = input(f'Digite a nova quantidade: ')
    linha_separacao()
    while not nova_quantidade.isdigit() or int(nova_quantidade)<=0:
        print(f'Quantidade inválida! Tente novamente...')
        nova_quantidade = input(f'Sua escolha: ')
        linha_separacao()
    else:
        if (manipula_cliente.muda_quantidade_personagem(usuario_id,nova_quantidade)):
            print(f'Quantidade de personagens ativos modificada com sucesso!')
            linha_separacao()
def retorna_lista_menus_reconhecidos():
    x=0
    y=1
    lista_menus_reconhecidos = []
    lista_coordenadas_menus = [[169,600],[371,600]]
    tela_inteira = retorna_atualizacao_tela()
    
    for coordenada in lista_coordenadas_menus:
        frame_tela = tela_inteira[coordenada[y]:coordenada[y]+50,coordenada[x]:coordenada[x]+160]
        frame_tela_tratado = manipula_imagem.transforma_menu_preto(frame_tela)
        texto_reconhecido = manipula_imagem.reconhece_texto(frame_tela_tratado)
        # manipula_imagem.mostra_imagem(0,frame_tela_tratado,texto_reconhecido)   
        lista_menus_reconhecidos.append(texto_reconhecido)
    return lista_menus_reconhecidos

def retorna_atualizacao_tela():
    screenshot = manipula_teclado.tira_screenshot()
    return manipula_imagem.retorna_imagem_colorida(screenshot)

def trata_menu(menu):
    #0 MENU JOGAR

    #1 NOTICIAS VOLTAR/AVANÇAR
    #4 PERSONAGEM VOLTAR
    #13 PRODUZIR/TRABALHOS DISPONIVEIS VOLTAR
    #14 TRABALHO ESPECIFICO VOLTAR/INICIAR

    #2 ESCOLHA DE PERSONAGEM FECHAR/JOGAR
    #3 PRINCIPAL FECHAR
    #11 PRODUZIR/PROFISSÕES FECHAR
    #12 PRODUZIR/TRABALHOS ATUAIS FECHAR

    #15 LICENÇA CANCELAR/AVANÇAR
    #16 TRABALHO ATRIBUTOS CANCELAR/BATEPAPO

    #3TELA INICIAL
    if menu == 0:
        #Tela inicial do jogo
        manipula_teclado.click_especifico(1,'enter')
    elif menu == 1:
        #menu notícias
        manipula_teclado.click_especifico(2,'f2')
    elif menu == 2:
        #menu seleção de perssonagem
        manipula_teclado.click_especifico(1,'f2')
    elif menu == 3:
        #menu principal
        manipula_teclado.click_especifico(1,'num1')
        manipula_teclado.click_especifico(1,'num7')
    elif menu == 4:
        #menu secundario
        manipula_teclado.click_especifico(1,'num7')
    elif menu == 12:
        #menu trabalhos atuais
        manipula_teclado.click_especifico(1,'left')
    elif menu == 13:
        #menu trabalhos disponiveis
        manipula_teclado.click_especifico(2,'left')
    elif menu == 14:
        #menu trabalho específico
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(3,'up')
        manipula_teclado.click_especifico(2,'left')
    elif menu==40:
        #Tela inicial do jogo
        manipula_teclado.click_especifico(1,'f1')
    elif menu==41:
        #tela principal
        manipula_teclado.click_especifico(1,'f2')
        manipula_teclado.click_especifico(1,'num1')
        manipula_teclado.click_especifico(1,'num7')
    
def retorna_menu(trabalho):
    id=0
    #0 MENU JOGAR

    #1 NOTICIAS VOLTAR/AVANÇAR
    #3 PERSONAGEM VOLTAR
    #13 PRODUZIR/TRABALHOS DISPONIVEIS VOLTAR
    #14 TRABALHO ESPECIFICO VOLTAR/INICIAR

    #2 ESCOLHA DE PERSONAGEM FECHAR/JOGAR
    #4 PRINCIPAL FECHAR
    #11 PRODUZIR/PROFISSÕES FECHAR
    #12 PRODUZIR/TRABALHOS ATUAIS FECHAR

    #15 LICENÇA CANCELAR/AVANÇAR
    #16 TRABALHO ATRIBUTOS CANCELAR/BATEPAPO

    #false TELA INICIAL
    licenca = configura_licenca(trabalho)
    erro=verifica_erro(licenca)
    while erro!=0:#enquanto reconhecer algum erro
        if erro==3:
            excluir_trabalho(f'{personagem_id}/Lista_desejo/{trabalho[id]}')
        erro=verifica_erro(licenca)
    else:
        print(f'Reconhecendo menu.')
        if retorna_texto_sair().replace(' ','').lower()=='sair':
            print(f'Menu jogar...')
            return 0
        else:
            if verifica_menu_referencia():
                print(f'Menu tela inicial...')
                linha_separacao()
                return 41
            texto_menu=retorna_texto_menu_reconhecido()
            print(texto_menu)
            if 'voltar' in texto_menu and'notícias' in texto_menu\
                and'avancar' in texto_menu:
                print(f'Menu notícias...')
                linha_separacao()
                return 1
            elif ('fechar'in texto_menu and'jogar'in texto_menu):
                print(f'Menu escolha de personagem...')
                linha_separacao()
                return 2
            elif ('voltar'in texto_menu and'conquistas'in texto_menu):
                print(f'Menu personagem...')
                linha_separacao()
                return 3
            elif ('fechar'in texto_menu and'interagir'in texto_menu):
                print(f'Menu principal...')
                linha_separacao()
                return 4
            elif ('fechar'in texto_menu and'profissões'in texto_menu):
                print(f'Menu produzir...')
                linha_separacao()
                return 11
            elif ('fechar'in texto_menu and'trabalhosatuais'in texto_menu) or ('fechar'in texto_menu and'produzir'in texto_menu and'concluir'in texto_menu):
                print(f'Menu trabalhos atuais...')
                linha_separacao()
                return 12
            elif ('voltar'in texto_menu and'profissões'in texto_menu):
                print(f'Menu trabalhos diponíveis...')
                linha_separacao()
                return 13
            elif ('voltar'in texto_menu and'iniciar'in texto_menu and 'temponecessário'in texto_menu):
                print(f'Menu trabalho específico...')
                linha_separacao()
                return 14
            elif ('cancelar'in texto_menu and'avançar'in texto_menu and'permiteexecutartrabalhos'in texto_menu):
                print(f'Menu licenças...')
                linha_separacao()
                return 15
            elif ('cancelar'in texto_menu and'batepapo'in texto_menu and'requisitosparâmetros'in texto_menu):
                print(f'Menu atributo do trabalho...')
                linha_separacao()
                return 16
            elif ('cancelar'in texto_menu and'avançar'in texto_menu):
                print(f'Menu escolha de equipamento...')
                linha_separacao()
                return 17
            elif ('fechar'in texto_menu and'ofertadiária'in texto_menu):
                print(f'Menu oferta diária...')
                linha_separacao()
                return 40
            else:
                print(f'Menu não reconhecido...')
                linha_separacao()
                return False

def configura_licenca(trabalho):
    licenca=4
    if trabalho==None:
        return ''
    return trabalho[licenca]

def retorna_texto_menu_reconhecido():
    tela_inteira=retorna_atualizacao_tela()
    frame_menu=tela_inteira[187:187+450,165:165+330]
    frame_menu_tratado=manipula_imagem.transforma_amarelo_preto(frame_menu)
    # manipula_imagem.mostra_imagem(0,frame_menu_tratado,'Teste')
    texto_menu = manipula_imagem.reconhece_texto(frame_menu_tratado)
    return texto_menu.lower().replace(' ','')

def retorna_texto_sair():
    tela_inteira = retorna_atualizacao_tela()
    frame_jogar = tela_inteira[768-70:768,0:0+160]
    frame_jogar_tratado = manipula_imagem.transforma_menu_preto(frame_jogar)
    # manipula_imagem.mostra_imagem(0,frame_jogar_tratado,'teste')
    return manipula_imagem.reconhece_texto(frame_jogar_tratado)

def retorna_texto_produzir():
    tela_inteira = retorna_atualizacao_tela()
    frame_produzir = tela_inteira[240:240+30,250:250+180]
    frame_produzir_tratado = manipula_imagem.transforma_amarelo_preto(frame_produzir)
    return manipula_imagem.reconhece_texto(frame_produzir_tratado)

def salva_imagem_envia_servidor():
    tela_inteira = retorna_atualizacao_tela()
    imagem_trabalho = tela_inteira[273:273+311,167:167+347]
    cv2.imwrite('imagem_trabalho.png', imagem_trabalho)

def salva_imagem():
    tela_inteira = retorna_atualizacao_tela()
    imagem_trabalho = tela_inteira[486:486+45,181:181+43]
    cv2.imwrite('imagem_produzir.png', imagem_trabalho)

def verifica_valor_numerico(valor):
    return valor.isdigit()

def verifica_valor_alfabetico(valor):
    return valor.isalpha()

def linha_separacao():
    print(f'____________________________________________________')

def entra_usuario():
    email = input(f'Email: ')
    senha = input(f'Senha: ')
    if manipula_cliente.autenticar_usuario(email,senha):
        return True
    return False

def funcao_teste(id_personagem):
    global personagem_id
    personagem_id=id_personagem
    manipula_teclado.click_atalho_especifico('alt','tab')
    # retorna_menu(None)
    # retorna_texto_menu_reconhecido()
    # verifica_erro('')
    # manipula_teclado.click_atalho_especifico('win','up')
    if verifica_menu_referencia():
        print('Achei!')
    else:
        print('Não achei...')
    # lista_habilidade = retorna_lista_habilidade_verificada()
    # lista_ativos = manipula_cliente.consulta_lista_personagem(usuario_id)
    # print(lista_ativos)
    # modifica_quantidade_personagem_ativo()
    # while True:
    #     verifica_habilidade_central(lista_habilidade)
    # verifica_licenca('Licença de produção do principiante')
    # trabalho = 'trabalhoid','Apêndice de jade ofuscada','profissaoteste','comum','Licença de produção do iniciante'
    # inicia_producao(trabalho)
    # verifica_trabalho_comum(trabalho,'profissaoteste')
    # atualiza_nova_tela()
    # while inicia_busca_trabalho():
    #     continue
    # entra_personagem_ativo('mrninguem')
    # verifica_nome_personagem('Axe')
    manipula_teclado.click_atalho_especifico('alt','tab')
#funcao_teste()