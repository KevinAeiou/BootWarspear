import cv2
import numpy as np
import manipula_arquivo
import manipula_imagem
import manipula_teclado
import manipula_navegador
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

def verifica_menu_referencia(menu_referencia):
    tela_inteira = retorna_atualizacao_tela()
    tamanho_referencia = menu_referencia.shape[:2]
    frame_tela = tela_inteira[712:712+menu_referencia.shape[0],1312:1312+menu_referencia.shape[1]]
    tamanho_frame_tela = frame_tela.shape[:2]
    if tamanho_frame_tela == tamanho_referencia:
        diferenca = cv2.subtract(frame_tela, menu_referencia)
        b, g, r = cv2.split(diferenca)
        if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
            return True
    else:
        print(f'Tamanho do menu referência e frame da tela diferentes!')
        linha_separacao()

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

def verifica_habilidade_ativa(tela_inteira,lista):
    for x in range(len(lista)):
        imagem_lista = lista[x]
        frame_tela = tela_inteira[668:668+imagem_lista[1].shape[0],661:661+imagem_lista[1].shape[1]]
        if frame_tela.shape[:2] == imagem_lista[1].shape[:2]:
            diferenca = cv2.subtract(frame_tela, imagem_lista[1])
            b, g, r = cv2.split(diferenca)
            if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                posicao_habilidade = retorna_posicao_habilidade(imagem_lista[0])
                manipula_teclado.click_especifico_habilidade(1,posicao_habilidade)
        else:
            print(f'Tamanho do frame diferente do modelo!')
            linha_separacao()
#Codigo modificado 23/01 11:20
def verifica_trabalho_concluido():
    #icone do primeiro espaço de produç 181,295 228,342
    tela_inteira = retorna_atualizacao_tela()
    frame_trabalho_concluido = tela_inteira[311:311+43, 233:486]
    texto = manipula_imagem.reconhece_texto(frame_trabalho_concluido)
    string_trabalho="Trabalho concluído"
    if texto != '' and texto == string_trabalho:
        print(f'Trabalho concluído!')
        return True
    print(f'Em produção...')
    return False
#modificado 10/01
def verifica_licenca(licenca_trabalho_lista_desejo):
    licenca_reconhecida = retorna_licenca_reconhecida()
    print(f"Buscando {licenca_trabalho_lista_desejo}")
    linha_separacao()
    while licenca_reconhecida != licenca_trabalho_lista_desejo:
        manipula_teclado.click_especifico(1,"right")
        licenca_reconhecida = retorna_licenca_reconhecida()
        if licenca_reconhecida.replace(' ','') == "Nenhumitem":
            if licenca_trabalho_lista_desejo != "Licençadeproduçãodoiniciante":
                licenca_trabalho_lista_desejo = "Licençadeproduçãodoiniciante"
            elif licenca_trabalho_lista_desejo == "Licençadeproduçãodoiniciante":
                licenca_trabalho_lista_desejo = "Licençadeproduçãodoaprendiz"
            elif licenca_trabalho_lista_desejo == "Licençadeproduçãodoaprendiz":
                licenca_trabalho_lista_desejo = "Licençadeproduçãodomestre"
            elif licenca_trabalho_lista_desejo == "Licençadeproduçãodomestre":
                print(f"Parando programa...")
                exit()
    else:
        manipula_teclado.click_especifico(2,"f2")

def retorna_licenca_reconhecida():
    tela_inteira = retorna_atualizacao_tela()
    frame_tela = tela_inteira[275:317,169:512]
    frame_tela_equalizado = manipula_imagem.retorna_imagem_equalizada(frame_tela)
    licenca_reconhecida = manipula_imagem.reconhece_texto(frame_tela_equalizado)
    return licenca_reconhecida
#modifica 16/01
def verifica_producao_recursos(nome_trabalho_lista_desejo):
    lista_producao_recursos = ['Grande coleção de recursos comuns','Melhoria da substância comum','Melhorar licença comum','Licença de produção do aprediz','Melhoria da substância composta','Coleta em massa de recursos avançados']
    for x in lista_producao_recursos:
        if nome_trabalho_lista_desejo in x:
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
def verifica_posicoes_trabalhos(personagem_id,coluna_lista_profissao_necessaria,conteudo_lista_desejo):
    indice_nome_profissao = 1
    yinicial_nome=285
    #xinicial=233, xfinal=478, yinicial=285, yfinal=324 altura=70
    #sempre faz três verificações
    time.sleep(1)
    for x in range(4):
        nome_trabalho = retorna_nome_trabalho_reconhecido(yinicial_nome,0)
        #enquanto não comparar toda lista
        for linha_lista_desejo in range (len(conteudo_lista_desejo)):
            conteudo_linha_lista_desejo = conteudo_lista_desejo[linha_lista_desejo]
            #retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
            id_trabalho_lista_desejo = conteudo_linha_lista_desejo[0]
            nome_trabalho_lista_desejo = conteudo_linha_lista_desejo[1]
            nome_profissao_lista_desejo = conteudo_linha_lista_desejo[2]
            raridade_trabalho_lista_desejo = conteudo_linha_lista_desejo[5]
            nome_licenca_lista_desejo = conteudo_linha_lista_desejo[4]
            if raridade_trabalho_lista_desejo == 'Comum':
                print(f'Verificando trabalho comum...')
                linha_separacao()
                return verifica_trabalho_comum(conteudo_linha_lista_desejo,coluna_lista_profissao_necessaria[indice_nome_profissao],personagem_id)
            #se o trabalho na lista de desejo NÃO for da profissão verificada no momento, passa para o proximo trabalho na lista
            elif coluna_lista_profissao_necessaria[indice_nome_profissao]==nome_profissao_lista_desejo:
                if nome_trabalho == '':
                    break
                print(f'Nome do trabalho disponível: {nome_trabalho}')
                print(f'Nome do trabalho na lista: {nome_trabalho_lista_desejo}')
                linha_separacao()
                if nome_trabalho.replace(' ','') in nome_trabalho_lista_desejo.replace(' ',''):
                    entra_trabalho_encontrado(x)
                    if not verifica_producao_recursos(nome_trabalho_lista_desejo):
                        #confima o nome do trabalho
                        manipula_teclado.click_especifico(1,'down')
                        manipula_teclado.click_especifico(1,'enter')
                        if not confirma_nome_trabalho(nome_trabalho_lista_desejo):
                            sai_trabalho_encontrado(x)
                            return False
                        else:
                            manipula_teclado.click_especifico(1,'f1')
                            entra_licenca()
                            #verifica tipo de licença de produção
                            verifica_licenca(nome_licenca_lista_desejo)
                            #antes de modificar qualquer araquivo, verifica erros
                            while not verifica_erro(nome_licenca_lista_desejo):
                                continue
                            manipula_teclado.click_especifico(2,'f2')
                            manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id,nome_trabalho_lista_desejo,1)
                            return True
        yinicial_nome = yinicial_nome+70
    else:
        print(f'Nem um trabalho disponível está na lista de desejos.')
        linha_separacao()
    return False

def verifica_trabalho_comum(trabalho_lista_desejo,nome_profissao_verificada,personagem_id):
    manipula_teclado.click_especifico(5,'down')
    while True:
        nome_trabalho_reconhecido = retorna_nome_trabalho_reconhecido(530,1)
        nome_trabalho = trabalho_lista_desejo[1]
        nome_profissao = trabalho_lista_desejo[2]
        nome_licenca = trabalho_lista_desejo[4]
        print(f'Trabalho reconhecido: {nome_trabalho_reconhecido}')
        print(f'Trabalho na lista: {nome_trabalho}')
        linha_separacao()
        if nome_profissao_verificada==nome_profissao:
            if nome_trabalho_reconhecido == '':
                manipula_teclado.click_especifico(1,'f1')
                manipula_teclado.click_especifico(8,'up')
                return False
            elif nome_trabalho_reconhecido.replace(' ','') in nome_trabalho.replace(' ',''):
                manipula_teclado.click_especifico(2,'enter')
                #verifica tipo de licença de produção
                verifica_licenca(nome_licenca)
                #antes de modificar qualquer araquivo, verifica erros
                verifica_erro(nome_licenca)
                manipula_teclado.click_especifico(2,'f2')
                manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id,nome_trabalho,1)
                return True
        manipula_teclado.click_especifico(1,'down')

def retorna_nome_trabalho_reconhecido(yinicial_nome,identificador):
    #tira novo print da tela
    imagem_inteira = retorna_atualizacao_tela()
    #recorta frame para reconhecimento de texto
    if identificador == 0:
        altura = 39
    elif identificador == 1:
        altura = 68
    frame_nome_trabalho = imagem_inteira[yinicial_nome:yinicial_nome+altura,233:478]
    #retorna texto encontrado
    return manipula_imagem.reconhece_texto(frame_nome_trabalho)

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
#modificado 23/01
def verifica_erro(nome_licenca_lista_desejo):
    tela_inteira = retorna_atualizacao_tela()
    erro = retorna_tipo_erro(tela_inteira)
    if erro == 1:
        manipula_teclado.click_especifico(2,"enter")
        verifica_licenca(nome_licenca_lista_desejo)
        return True
    elif erro == 2:
        print(f'Tentando reconectar.')
        linha_separacao()
        manipula_teclado.click_especifico(2,'enter')
        return True
    elif erro == 3:
        print(f'Retirando trabalho da lista.')
        print(f'Voltando para o menu profissões.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(2,'f1')
        manipula_teclado.click_especifico(8,'up')
        return True
    elif erro == 4:
        print(f'Escolhendo item.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(2,'f2')
        return True
    elif erro == 5:
        time.sleep(3)
        return True
    elif erro == 6:
        print(f'Voltando para o menu profissões.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(4,'up')
        manipula_teclado.click_especifico(2,'left')
        return True
    elif erro == 7:
        print(f'Recuperar presente depois.')
        linha_separacao()
        manipula_teclado.click_especifico(2,'f1')
        return True
    elif erro == 8:
        print(f'Espera trabalho ser concluido.')
        linha_separacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(4,'up')
        manipula_teclado.click_especifico(1,'left')
        trabalho_concluido = verifica_trabalho_concluido()
        print(f'Esperando trabalho ser concluído...')
        linha_separacao()
        while not trabalho_concluido:
            trabalho_concluido = verifica_trabalho_concluido()
        return False
    elif erro == 9:
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(8,'up')
        return True
    elif erro == 10:
        manipula_teclado.click_especifico(2,'enter')
        print(f'Voltando para a tela inicial.')
        linha_separacao()
        return True
    elif erro == 11:
        manipula_teclado.click_especifico(2, 'enter')
        print(f'Voltando para a tela inicial.')
        linha_separacao()
        time.sleep(300)
        return True
    elif erro == 12:
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(1,'up')
        manipula_teclado.click_especifico(1,'left')
        print(f'Ignorando trabalho concluído!')
        linha_separacao()
        return True
    elif erro == 13:
        manipula_teclado.click_especifico(1,'enter')
        print(f'Erro ao conectar...')
        linha_separacao()
        return True
    elif erro == 14:
        manipula_teclado.click_especifico(1,'f1')
        linha_separacao()
        return True
    elif erro == 15:
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        print(f'Login ou senha incorreta...')
        linha_separacao()
        return True
    return False
#modificado 12/01
def retorna_tipo_erro(tela_inteira):
    frame_erro = tela_inteira[335:335+100,150:526]
    erro_encontrado = manipula_imagem.reconhece_texto(frame_erro)

    tipo_erro_trabalho = ['precisoumalicençadeproduçãoparainiciarotrabalho','Nãofoipossívelseconectaraoservidor','Vocênãotemosrecursosnecessáriasparaessetrabalho',
    'Vocêprecisaescolherumitemparainiciarumtrabalhodeprodução','Conectando','precisomaisexperiênciaprofissionalparainiciarotrabalho',
    'GostariadeiràLojaMilagrosaparaveralistadepresentes','Vocênãotemespaçoslivresparaotrabalho','agorapormoedas','OservidorestáemmanutençãoEstamosfazendodetudoparaconcluílaomaisrápvidopossível',
    'Foidetectadaoutraconexãousandoseuperfil','Gostanadecomprar','conexão com o servidor foi interrompida','Você precisa de mais moedas','Login ou senha incorreta']

    print(erro_encontrado)
    for tamanho_tipo_erro in range(len(tipo_erro_trabalho)):
        if tipo_erro_trabalho[tamanho_tipo_erro].replace(' ','') in erro_encontrado.replace(' ',''):
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
    posicao_nome = [[197,354,170,27],[2,33,169,21]]
    tela_inteira = retorna_atualizacao_tela()
    for indice in range(len(posicao_nome)):
        frame_nome_personagem = tela_inteira[posicao_nome[indice][1]:posicao_nome[indice][1]+posicao_nome[indice][3],posicao_nome[indice][0]:posicao_nome[indice][0]+posicao_nome[indice][2]]
        frame_nome_personagem_tratado = manipula_imagem.transforma_amarelo_preto(frame_nome_personagem)
        nome_personagem_reconhecido = manipula_imagem.reconhece_texto(frame_nome_personagem_tratado)
        # manipula_imagem.mostra_imagem(0,frame_nome_personagem,nome_personagem_reconhecido)
        print(nome_personagem_reconhecido)
        if nome_personagem_reconhecido.replace(' ','').lower()\
            in nome_personagem.replace(' ','').lower():
            return True
    return False

def verifica_email_personagem(email_personagem):
    lista_caracter = ['.','@','_']
    for caracter in lista_caracter:
        email_personagem.replace(caracter,'')
    tela_inteira = retorna_atualizacao_tela()
    frame_nome_personagem = tela_inteira[534:534+32,208:208+264]
    frame_nome_personagem_tratado = manipula_imagem.transforma_amarelo_preto(frame_nome_personagem)
    nome_personagem_reconhecido = manipula_imagem.reconhece_texto(frame_nome_personagem_tratado)
    manipula_imagem.mostra_imagem(0,frame_nome_personagem,nome_personagem_reconhecido)
    print(nome_personagem_reconhecido)
    if nome_personagem_reconhecido.replace(' ','').lower()\
        in email_personagem.replace(' ','').lower():
        return True
    return False

def retorna_lista_profissao_verificada(personagem_id):
    #cria lista vazia
    lista_profissao_verificada = []
    #abre o arquivo lista de profissoes
    conteudo_lista_profissoes = manipula_cliente.consutar_lista(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_profissoes')
    #abre o arquivo lista de desejos
    conteudo_lista_desejo = manipula_cliente.consultar_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo')
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
    lista_habilidade_encontrada = []
    lista_imagem_habilidade = retorna_lista_imagem_habilidade()
    tela_inteira = retorna_atualizacao_tela()
    altura_modelo = lista_imagem_habilidade[0].shape[0]
    largura_modelo = lista_imagem_habilidade[0].shape[1]
    for x in range(382,983):
        frame_habilidade = tela_inteira[728:728+altura_modelo, x:x+largura_modelo]
        tamanho_frame_habilidade = frame_habilidade.shape[:2]
        for y in range(len(lista_imagem_habilidade)):
            tamanho_modelo = lista_imagem_habilidade[y].shape[:2]
            if tamanho_frame_habilidade == tamanho_modelo:
                diferenca = cv2.subtract(lista_imagem_habilidade[y], frame_habilidade)
                b, g, r = cv2.split(diferenca)
                if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                    lista_habilidade_encontrada.append([x,lista_imagem_habilidade[y]])
                    break
            else:
                print(f'Modelos com tamanhos diferentes. {tamanho_frame_habilidade}:{tamanho_modelo}')
                linha_separacao()
                break
    return lista_habilidade_encontrada

def passa_proxima_posicao():
    global yinicial, yfinal, altura_frame
    #passa para a proxima posição de produção
    yinicial = yfinal+23
    yfinal = yfinal+altura_frame

def entra_personagem_ativo(nome):
    manipula_teclado.click_especifico(1,'enter')
    while verifica_erro(''):
        continue
    else:
        menu = retorna_menu()
        while menu != 2:
            if menu == 0:#se estiver no menu jogar
                manipula_teclado.click_especifico(1,'enter')
            elif menu == 1:#se estiver no menu noticias
                manipula_teclado.click_especifico(1,'f2')
            menu = retorna_menu()
        else:
            manipula_teclado.vai_inicio_fila()                
            while not verifica_nome_personagem(nome):
                manipula_teclado.click_especifico(1,'right')
            else:
                manipula_teclado.click_especifico(1,'f2')
                while verifica_erro(''):
                    continue
                else:
                    if not retorna_menu():
                        print(f'Login efetuado com sucesso!')
                        return True
                    else:
                        print(f'Erro ao tentar entrar...')
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
def prepara_personagem(personagem_id):
    #lista_profissao_necessaria é uma matrix onde o indice 0=posição da profissão
    #e o indice 1=nome da profissão    
    dados_personagem = manipula_cliente.consulta_dados_personagem(usuario_id,personagem_id)
    nome = dados_personagem[0][1]
    email = dados_personagem[0][2]
    senha = dados_personagem[0][3]
    estado = dados_personagem[0][4]
    if estado!=1:#se o personagem estiver inativo, troca o estado
        manipula_cliente.muda_estado_personagem(usuario_id,personagem_id)
    else:
        #verificar em que menu está
        encontra_menu_especifico(nome,email,senha)
        #verificar qual personagem está logado
        if verifica_nome_personagem(nome):
            #iniciar busca por trabalho
            inicia_busca_trabalho(personagem_id, dados_personagem, estado)
        else:#se o nome do personagem for diferente
            while True:
                while verifica_erro(''):
                    continue
                else:
                    while retorna_menu() != False:
                        manipula_teclado.click_mouse_esquerdo(1,2,35)
                    else:
                        manipula_teclado.encerra_secao()
                        loga_email_entra_personagem(nome, email, senha)
    return

def loga_email_entra_personagem(nome, email, senha):
    manipula_teclado.entra_secao(email,senha)
    while verifica_erro(''):
        manipula_teclado.entra_secao(email,senha)
    else:
        while not entra_personagem_ativo(nome):
            continue

def inicia_busca_trabalho(personagem_id, dados_personagem, estado):
    posicao_profissao = 0
    lista_profissao_necessaria = retorna_lista_profissao_verificada(personagem_id)
    print('Inicia busca...')
    if len(lista_profissao_necessaria)>0:
        conteudo_lista_desejo= manipula_cliente.consultar_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo')
        manipula_teclado.click_atalho_especifico('alt','tab')
        while len(conteudo_lista_desejo)>0:
                    #percorre toda lista de indice de profissao
            for indice_lista_profissao_necessaria in range(len(lista_profissao_necessaria)):
                menu = retorna_menu()
                while menu != 3:
                    trata_menu(menu)
                    menu = retorna_menu()
                        #retorna a profissão eespecífica
                posicao_nome_profissao = lista_profissao_necessaria[indice_lista_profissao_necessaria]
                manipula_teclado.retorna_menu_profissao_especifica(posicao_nome_profissao[posicao_profissao])
                if verifica_posicoes_trabalhos(personagem_id,lista_profissao_necessaria[indice_lista_profissao_necessaria],conteudo_lista_desejo):
                    lista_profissao_necessaria = retorna_lista_profissao_verificada(personagem_id)
                    manipula_teclado.click_especifico(1,'left')
                    break
                lista_profissao_necessaria = retorna_lista_profissao_verificada(personagem_id)
                manipula_teclado.click_especifico(3,'up')
                manipula_teclado.click_especifico(1,'left')
                        #verifca se existe trabalho concluido
                trabalho_concluido = verifica_trabalho_concluido()
                if trabalho_concluido:
                    tela_inteira = retorna_atualizacao_tela()
                    frame_nome_trabalho = tela_inteira[285:285+37, 233:486]
                    nome_trabalho_concluido = manipula_imagem.reconhece_texto(frame_nome_trabalho)
                    manipula_teclado.click_especifico(1,'down')
                    manipula_teclado.click_especifico(1,'f2')
                    if not verifica_erro(''):
                        manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id,nome_trabalho_concluido,2)
                    manipula_teclado.click_especifico(1,'up')
                    manipula_teclado.click_especifico(1,'left')
                else:
                    manipula_teclado.click_especifico(1,'left')
            dados_personagem = manipula_cliente.consulta_dados_personagem(usuario_id,personagem_id)
            estado = dados_personagem[4]
            if estado!=1:
                prepara_personagem(manipula_teclado.retorna_idpersonagem_ativo(usuario_id))
            conteudo_lista_desejo = manipula_cliente.consultar_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo')
        else:
            print(f'Todos os trabalhos desejados foram iniciados.')
            print(f'Voltando...')
    else:
        print(f'Lista de trabalhos desejados vazia.')
        print(f'Voltando.')
        linha_separacao()

def encontra_menu_especifico(nome,email,senha):
    menu_reconhecido = retorna_menu()
    print(menu_reconhecido)
    if menu_reconhecido == 1:#menu notícias
        manipula_teclado.click_especifico(1,'f1')
    menu_reconhecido = retorna_menu()
    if menu_reconhecido == 0:#menu jogar
        if not verifica_email_personagem(email):
            loga_email_entra_personagem(nome,email,senha)            

def usa_habilidade():
    #719:752, 85:128 137:180 189:232
    #muda p/ outra janela
    manipula_teclado.click_atalho_especifico('alt','tab')
    manipula_teclado.click_atalho_especifico('win','up')
    modelo_menu_referencia = manipula_imagem.abre_imagem('modelos/modelo_menu_9.png')
    #cria lista com habilidades a serem usadas
    lista = retorna_lista_habilidade_verificada()
    if len(lista)==0:
        return
    print(f'Buscando referência!')
    linha_separacao()
    while True:
        if verifica_menu_referencia(modelo_menu_referencia):
            #verifica se está em modo de ataque
            tela_inteira = retorna_atualizacao_tela()
            if verifica_modo_ataque() or verifica_alvo():
                #percorre a lista de habilidades
                for indice_habilidade in range(len(lista)):
                    #atualiza a tela
                    conteudo_coluna = lista[indice_habilidade]
                    #recorta frame na posição da habilidade específica
                    frame_habilidade = tela_inteira[728:728+conteudo_coluna[1].shape[0], conteudo_coluna[0]:conteudo_coluna[0]+conteudo_coluna[1].shape[1]]
                    #define o tamanho do frame
                    tamanho_frame_habilidade = frame_habilidade.shape[:2]
                    #define o tamanho do modelo
                    tamanho_modelo = conteudo_coluna[1].shape[:2]
                    if verifica_porcentagem_vida() and verifica_menu_referencia(modelo_menu_referencia):
                        manipula_teclado.click_especifico_habilidade(1,'t')
                    #compara os tamanhos das imagens
                    if tamanho_frame_habilidade == tamanho_modelo:
                        #subtrai as imgagens de comparação
                        diferenca = cv2.subtract(conteudo_coluna[1], frame_habilidade)
                        #divide os canais de cores
                        b, g, r = cv2.split(diferenca)
                        #se cada cor subtraida for igual a zero
                        if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                            #clica a tecla específica de cada habilidade
                            posicao_habilidade = retorna_posicao_habilidade(conteudo_coluna[0])
                            manipula_teclado.click_especifico_habilidade(1,posicao_habilidade)
                    else:
                        print(f'Modelos com tamanhos diferentes. {tamanho_frame_habilidade}-{tamanho_modelo}')
                        linha_separacao()
            else:
                verifica_habilidade_ativa(tela_inteira,lista)

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
    if menu == 1:
        #menu principal
        manipula_teclado.click_especifico(1,'num1')
        manipula_teclado.click_especifico(1,'num7')
    elif menu == 2:
        #menu secundario
        manipula_teclado.click_especifico(1,'num7')
    elif menu == 4:
        #menu trabalhos atuais
        manipula_teclado.click_especifico(1,'left')
    elif menu == 5:
        #menu trabalhos disponiveis
        manipula_teclado.click_especifico(2,'left')
    elif menu == 6:
        #menu trabalho específico
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_especifico(3,'up')
        manipula_teclado.click_especifico(2,'left')
    elif menu == 7:
        #menu notícias
        manipula_teclado.click_especifico(2,'f2')
    elif menu == 8:
        #menu seleção de perssonagem
        manipula_teclado.click_especifico(1,'f2')
    elif menu == 9:
        #tela principal
        manipula_teclado.click_especifico(1,'f2')
        manipula_teclado.click_especifico(1,'num1')
        manipula_teclado.click_especifico(1,'num7')
    elif menu == 10:
        #Tela inicial do jogo
        manipula_teclado.click_especifico(1,'enter')
    
def retorna_menu():
    #0 MENU JOGAR

    #1 NOTICIAS VOLTAR/AVANÇAR
    #4 PERSONAGEM VOLTAR
    #13 PRODUZIR/TRABALHOS DISPONIVEIS VOLTAR
    #14 TRABALHO ESPECIFICO VOLTAR/INICIAR

    #2 ESCOLHA DE PERSONAGEM FECHAR/JOGAR
    #4 PRINCIPAL FECHAR
    #11 PRODUZIR/PROFISSÕES FECHAR
    #12 PRODUZIR/TRABALHOS ATUAIS FECHAR

    #15 LICENÇA CANCELAR/AVANÇAR
    #16 TRABALHO ATRIBUTOS CANCELAR/BATEPAPO

    #3TELA INICIAL
    print(f'Reconhecendo menu.')
    linha_separacao()
    texto_jogar = retorna_texto_sair()
    if texto_jogar.replace(' ','').lower() == 'sair':
        print(f'Menu jogar...')
        return 0
    else:
        texto_menu = retorna_texto_menu_reconhecido()
        print(texto_menu)
        if 'voltar' in texto_menu and'notícias' in texto_menu\
            and'avancar' in texto_menu:
            print(f'Menu notícias...')
            return 1
        elif ('voltar'in texto_menu and'conquistas'in texto_menu):
            print(f'Menu personagem...')
            return 4
        elif ('voltar'in texto_menu and'profissões'in texto_menu):
            print(f'Menu trabalhos diponíveis...')
            return 13
        elif ('voltar'in texto_menu and'iniciar'in texto_menu):
            print(f'Menu trabalho específico...')
            return 14
        elif ('fechar'in texto_menu and'jogar'in texto_menu):
            print(f'Menu escolha de personagem...')
            return 2
        elif ('fechar'in texto_menu and'interagir'in texto_menu):
            print(f'Menu principal...')
            return 4
        elif ('fechar'in texto_menu and'profissões'in texto_menu):
            print(f'Menu produzir...')
            return 11
        elif ('fechar'in texto_menu and'trabalhosatuais'in texto_menu):
            print(f'Menu trabalhos atuais...')
            return 12
        elif ('cancelar'in texto_menu and'avançar'in texto_menu):
            print(f'Menu licenças...')
            return 15
        elif ('cancelar'in texto_menu and'batepapo'in texto_menu):
            print(f'Menu atributo do trabalho...')
            return 16
        elif ('fechar'in texto_menu and'ofertadiária'in texto_menu):
            print(f'Menu oferta diária...')
            return 40
        else:
            print(f'Menu não reconhecido...')
            return False

def retorna_texto_menu_reconhecido():
    tela_inteira = retorna_atualizacao_tela()
    frame_menu = tela_inteira[187:187+450,140:140+400]
    frame_menu_tratado = manipula_imagem.transforma_amarelo_preto(frame_menu)
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

def funcao_teste(personagem_id):
    # atualiza_nova_tela()
    # retorna_menu()
    # entra_personagem_ativo('tolinda')
    # verifica_email_personagem('gunsa')
    modelo_menu_referencia = manipula_imagem.abre_imagem('modelos/modelo_menu_9.png')
    verifica_menu_referencia(modelo_menu_referencia)
    # menu = retorna_menu()
    # print(menu)
#funcao_teste()