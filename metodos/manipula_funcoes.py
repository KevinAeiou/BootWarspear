import cv2
import numpy as np
from manipula_imagem import *
from manipula_teclado import *
from manipula_cliente import *
from lista_chaves import *
import time
import datetime
import os.path
import re
from unidecode import unidecode

xinicial=181
xfinal = 228
yinicial = 295
yfinal = 342
yinicial_nivel = 285
yfinal_nivel = 285 + 69

cont_voltas = 0
contadorParaCima=4
personagem_id_global=''
altura_frame = 70
porcentagem_vida = 25

menu_jogar=0
menu_noticias=1
menu_escolha_p=2
menu_personagem=3
menu_principal=4
menu_produzir=11
menu_trab_atuais=12
menu_trab_disponiveis=13
menu_trab_especifico=14
menu_licencas=15
menu_trab_atributos=16
menu_esc_equipamento=17
menu_loja_milagrosa=38
menu_rec_diarias=39
menu_ofe_diaria=40
menu_inicial=41
menu_meu_perfil=42
menu_bolsa=43
menu_desconhecido=None

erroPrecisaLicenca=1
erroFalhaConectar=2
erroSemRecursos=3
erroPrecisaEscolherItem=4
erroConectando=5
erroSemExperiencia=6
erroReceberRecompensas=7
erroSemEspacosProducao=8
erroConcluirTrabalho=9
erroManutencaoServidor=10
erroOutraConexao=11
erroSemEspacosBolsa=12
erroConexaoInterrompida=13
erroSemMoedas=14
erroEmailSenhaIncorreta=15
erroTempoProducaoExpirou=16
erroReinoIndisponivel=17
erroAtualizaJogo=18
erroRestaurandoConexao=19
erroUsarObjetoParaProduzir=20

lista_personagem_ativo=[]

para_produzir=0
produzindo=1
concluido=2

dicionarioPersonagem = 'eEDku1Rvy7f7vbwJiVW7YMsgkIF2'
tela = 'atualizacao_tela.png'

def atualiza_nova_tela():
    imagem = tira_screenshot()
    salvaNovaTela(imagem)
    print(f'Atualizou a tela.')
    linhaSeparacao()

def profissaoExiste(profissaoReconhecida,listaProfissao):
    confirmacao=False
    for profissao in listaProfissao:
        if profissao[CHAVE_NOME].lower()in profissaoReconhecida.lower():
            confirmacao=True
            break
    return confirmacao

def atualizaListaProfissao(dicionarioPersonagem):
    yinicialProfissao=285
    print(f'Atualizando lista de profissões...')
    linhaSeparacao()
    for x in range(8):
        if ehQuartaVerificacao(x):
            clickEspecifico(5,'down')
            yinicialProfissao=529
        elif ehMaisQueQuartaVerificacao(x):
            clickEspecifico(1,'down')
            yinicialProfissao=529
        telaInteira=retornaAtualizacaoTela()
        frameNomeProfissao=telaInteira[yinicialProfissao:yinicialProfissao+35,232:232+237]
        profissaoReconhecida=reconheceTexto(frameNomeProfissao)
        if variavelExiste(profissaoReconhecida):
            if textoReconhecidoPertenceTextoDicionario(profissaoReconhecida,dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO][x]):
                print(f'Profissão: {profissaoReconhecida} OK')
                yinicialProfissao+=70
                continue
            else:
                idA = encontraPrimeiroId(dicionarioPersonagem, profissaoReconhecida)
                if variavelExiste(idA):
                    profissaoB=dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO][x][CHAVE_NOME]
                    dicionarioProfissao={CHAVE_ID:dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO][x][CHAVE_ID],
                                        CHAVE_NOME:profissaoReconhecida}
                    modificaProfissao(dicionarioPersonagem,dicionarioProfissao)
                    dicionarioProfissao={CHAVE_ID:idA,
                                        CHAVE_NOME:profissaoB}
                    modificaProfissao(dicionarioPersonagem,dicionarioProfissao)
                    print(f'Trocando posições: {profissaoReconhecida} x {profissaoB}')
                    linhaSeparacao()
                    dicionarioPersonagem=retornaListaDicionariosProfissoesNecessarias(dicionarioPersonagem)
                    yinicialProfissao+=70
                else:
                    print(f'Erro ao buscar id na lista de profissões de: {profissaoReconhecida}.')
        else:
            print(f'Processo interrompido!')
            break
    else:
        clickContinuo(8,'up')
        print(f'Processo concluído!')
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA]=retornaListaDicionariosProfissoesNecessarias(dicionarioPersonagem)
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]=False
    linhaSeparacao()
    return dicionarioPersonagem

def encontraPrimeiroId(dicionarioPersonagem, profissaoReconhecida):
    idA=None
    for profissao in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if textoReconhecidoPertenceTextoDicionario(profissaoReconhecida,profissao):
            idA=profissao[CHAVE_ID]
            break
    return idA

def ehMaisQueQuartaVerificacao(x):
    return x>4

def ehQuartaVerificacao(x):
    return x==4

def atualiza_referencias():
    tela_inteira = retornaAtualizacaoTela()
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
def defineNovoTrabalho(raridade,profissao,nivel):
    confirmacao='s'
    while confirmacao.replace(' ','').lower()=='s':
        nome=input(f'Novo trabalho: ')
        if len(nome.replace(' ',''))!=0:
            print(f'Confirma novo trabalho:(S/N)?')
            confirmaTrabalho=input(f'Escolha: ')
            if confirmaTrabalho.replace(' ','').lower()=='s':
                dicionarioTrabalho={CHAVE_NOME:nome,
                                    CHAVE_PROFISSAO:profissao,
                                    CHAVE_RARIDADE:raridade,
                                    CHAVE_NIVEL:nivel,
                                    CHAVE_LICENCA:'',
                                    CHAVE_RECORRENCIA:False,
                                    CHAVE_ESTADO:0}
                # print(f'{D}:dicionarioTrablho{dicionarioTrabalho}.')
                linhaSeparacao()
                cadastraNovoTrabalho(dicionarioTrabalho)
        else:
            print(f'Nome vazio!')
            linhaSeparacao()
        confirmacao=input(f'Cadastra novo trabalho:(S/N)?')

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
        tela_inteira = retornaAtualizacaoTela()
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
        clickMouseEsquerdo(1,centro[0],centro[1])
        frame_nome_objeto = frame_tela[32:32+30,frame_tela.shape[1]-164:frame_tela.shape[1]]
        nome_objeto_reconhecido=reconheceTexto(frame_nome_objeto)
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
        tela_inteira = retornaAtualizacaoTela()
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
            #click_mouse_esquerdo(1,centro_objeto[0],ajuste_y)
            tela_inteira = retornaAtualizacaoTela()
            nome_objeto_reconhecido=retorna_nome_inimigo(tela_inteira)
            if nome_objeto_reconhecido!=None:
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
#modificado 16/01
def mostraLista(listaDicionarios):
    x=1
    for dicionario in listaDicionarios:
        print(f'{x} - {dicionario[CHAVE_NOME]}.')
        x+=1
    print(f'0 - Voltar.')

def defineListaDesejo(dicionarioUsuario):
    dicionarioUsuario[CHAVE_LISTA_DESEJO]=retornaListaDicionariosTrabalhosDesejados(dicionarioUsuario)
    return dicionarioUsuario

def mostraListaDesejo(dicionarioUsuario):
    for trabalhoDesejado in dicionarioUsuario[CHAVE_LISTA_DESEJO]:
        if estadoTrabalhoEParaProduzir(trabalhoDesejado):
            print(f'{trabalhoDesejado[CHAVE_PROFISSAO]}: {trabalhoDesejado[CHAVE_NOME]}')
    linhaSeparacao()

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
    histograma_referencia1 = retorna_histograma(frame_referencia1)
    histograma_referencia_anterior1 = retorna_histograma(referencia_anterior1)
    histograma_referencia2 = retorna_histograma(frame_referencia2)
    # histograma_referencia_anterior2 = retorna_histograma(referencia_anterior2)
    comparacao_histogramas1 = retorna_comparacao_histogramas(histograma_referencia1,histograma_referencia_anterior1)
    # comparacao_histogramas2 = retorna_comparacao_histogramas(histograma_referencia2,histograma_referencia_anterior2)
    if comparacao_histogramas1!=0:
    # if comparacao_histogramas1!=0 and comparacao_histogramas2!=0:
        print(f'Referencias não comferem.')
        return False
    return True

def verificaMenuReferencia():
    confirmacao=False
    posicao_menu=[[703,627],[712,1312]]
    tela_inteira=retornaAtualizacaoTela()
    for posicao in posicao_menu:
        frame_tela=tela_inteira[posicao[0]:posicao[0]+53,posicao[1]:posicao[1]+53]
        contadorPixelPreto=np.sum(frame_tela==(85,204,255))
        if contadorPixelPreto==1720:
            confirmacao=True
            break
    return confirmacao

def verifica_alvo():
    tela_inteira = retornaAtualizacaoTela()
    pixel_vida_alvo = tela_inteira[67,1194]
    return (pixel_vida_alvo == [33,25,255]).all()

def verifica_modo_ataque():
    #atualiza a tela
    tela_inteira = retornaAtualizacaoTela()
    pixel_modo_ataque = tela_inteira[55,0]
    return (pixel_modo_ataque != [66,197,230]).all()

def verifica_porcentagem_vida():
    tela_inteira = retornaAtualizacaoTela()
    xvida = int(38+(133*(porcentagem_vida/100)))
    if (tela_inteira[67,xvida]!=[33,25,255]).all() and (tela_inteira[67,xvida]!=[0,0,205]).all():
        print(f'Vida abaixo de {porcentagem_vida}%.')
        return True
    return False
#Codigo modificado 23/01 11:20
def retornaEstadoTrabalho():
    estadoTrabalho=para_produzir
    #icone do primeiro espaço de produç 181,295 228,342
    tela_inteira = retornaAtualizacaoTela()
    frame_trabalho_concluido = tela_inteira[311:311+43, 233:486]
    texto=reconheceTexto(frame_trabalho_concluido)
    if texto!=None:
        texto=texto.replace(' ','').lower()
        if "trabalhoconcluído"==texto:
            print(f'Trabalho concluído!')
            estadoTrabalho=concluido
        elif 'adicionarnovo' in texto:
            print(f'Nem um trabalho!')
            estadoTrabalho=para_produzir
        else:
            print(f'Em produção...')
            estadoTrabalho=produzindo
    else:
        print(f'Ocorreu algum erro ao verificar o espaço de produção!')
    linhaSeparacao()
    return estadoTrabalho
#modificado 10/01
def verificaLicenca(licencaTrabalho):
    confirmacao=False
    print(f"Buscando: {licencaTrabalho}")
    linhaSeparacao()
    licenca_reconhecida=retorna_licenca_reconhecida()
    if licenca_reconhecida!=None and licencaTrabalho!=None:
        licencaTrabalho=licencaTrabalho.replace(' ','').lower()
        print(f'Licença reconhecida: {licenca_reconhecida}.')
        linhaSeparacao()
        if 'licençasdeproduçaomaspode' not in licenca_reconhecida:
            primeira_busca=True
            lista_ciclo=[]
            while not licenca_reconhecida in licencaTrabalho:
                primeira_busca=False
                clickEspecifico(1,"right")
                lista_ciclo.append(licenca_reconhecida)
                licenca_reconhecida=retorna_licenca_reconhecida()
                if licenca_reconhecida!=None:
                    print(f'Licença reconhecida: {licenca_reconhecida}.')
                    linhaSeparacao()
                    print(f'Licença reconhecida: {licenca_reconhecida}.')
                    if verifica_ciclo(lista_ciclo)or licenca_reconhecida in 'nenhumitem':
                        licencaTrabalho='licençadeproduçãodoiniciante'
                        print(f'Licença para trabalho agora é: {licencaTrabalho}.')
                else:
                    print(f'Erro ao reconhecer licença!')
                    linhaSeparacao()
                    break
            else:#se encontrou a licença buscada
                if primeira_busca:
                    clickEspecifico(1,"f1")
                else:
                    clickEspecifico(1,"f2")
                confirmacao=True
    else:
        print(f'Erro ao reconhecer licença!')
        linhaSeparacao()
    return confirmacao

def retorna_licenca_reconhecida():
    licencaRetornada=None
    lista_licencas=['iniciante','principiante','aprendiz','mestre','nenhumitem','licençasdeproduçaomaspode']
    tela_inteira=retornaAtualizacaoTela()
    frame_tela=tela_inteira[275:317,169:512]
    frame_tela_equalizado=retorna_imagem_equalizada(frame_tela)
    licenca_reconhecida=reconheceTexto(frame_tela_equalizado)
    if licenca_reconhecida!=None:
        licenca_reconhecida=licenca_reconhecida.replace(' ','').lower()
        for licenca in lista_licencas:
            if licenca in licenca_reconhecida:
                licencaRetornada=licenca_reconhecida
                break            
    return licencaRetornada
    
def verifica_ciclo(lista):
    if len(lista)>=4:
        if lista[0]==lista[-1]:
            return True
    return False

def confirmaNomeTrabalho(dicionarioTrabalho,tipoTrabalho):
    dicionarioTrabalho[CHAVE_CONFIRMACAO]=True
    print(f'Confirmando nome do trabalho...')
    x=0
    y=1
    largura=2
    altura=3
    listaFrames=[[169,280,303,33],[183,195,318,31]]
    posicao=listaFrames[tipoTrabalho]
    telaInteira=retornaAtualizacaoTela()#tira novo print da tela
    frameNomeTrabalho=telaInteira[posicao[y]:posicao[y]+posicao[altura],posicao[x]:posicao[x]+posicao[largura]]
    frameNomeTrabalhoTratado=retornaImagemBinarizada(frameNomeTrabalho)
    nomeTrabalhoReconhecido=reconheceTexto(frameNomeTrabalhoTratado)
    # mostraImagem(0,frameNomeTrabalhoTratado,nomeTrabalhoReconhecido)
    if variavelExiste(nomeTrabalhoReconhecido):
        for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
            if textoReconhecidoPertenceTextoDicionario(nomeTrabalhoReconhecido,dicionarioTrabalhoDesejado):
                dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]=dicionarioTrabalhoDesejado
                print(f'Trabalho confirmado: {nomeTrabalhoReconhecido}!')
                linhaSeparacao()
                break
        else:
            dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]=None
            print(f'Trabalho negado: {nomeTrabalhoReconhecido}!')
            linhaSeparacao()
    else:
        dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
    return dicionarioTrabalho

def verificaPosicoesTrabalhos(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]=None
    yinicial_nome=(dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]*70)+285
    #xinicial=233, xfinal=478, yinicial=285, yfinal=324 altura=70
    time.sleep(2)
    nomeTrabalhoReconhecido=retornaNomeTrabalhoReconhecido(yinicial_nome,0)
    if nomeTrabalhoReconhecido!=None and dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]==None:
        print(f'Nome do trabalho disponível: {nomeTrabalhoReconhecido}')
        #enquanto não comparar toda lista
        for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
            #retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
            if estadoTrabalhoEParaProduzir(dicionarioTrabalhoDesejado)and profissaoEIgual(dicionarioTrabalho,dicionarioTrabalhoDesejado):
                print(f'Nome do trabalho na lista: {dicionarioTrabalhoDesejado[CHAVE_NOME]}')
                if textoReconhecidoPertenceTextoDicionario(nomeTrabalhoReconhecido,dicionarioTrabalhoDesejado):
                    print(f'{dicionarioTrabalhoDesejado[CHAVE_NOME]} reconhecido...')
                    linhaSeparacao()
                    dicionarioTrabalho=entraTrabalhoEncontrado(dicionarioTrabalho,dicionarioTrabalhoDesejado)
                    if chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                        dicionarioTrabalho=confirmaNomeTrabalho(dicionarioTrabalho,1)
                        if variavelExiste(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]):
                            break
                        else:    
                            clickEspecifico(1,'f1')
                            clickContinuo(dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]+1,'up')
                    else:
                        print(f'Erro ao entrar no trabalho encontrado...')
                        linhaSeparacao()
        else:
            linhaSeparacao()
    else:
        dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
    return dicionarioTrabalho

def retornaListaDicionarioTrabalhoComum(dicionarioTrabalho):
    listaDicionariosTrabalhosComunsDesejados=[]
    print(f'Buscando trabalho comum na lista...')
    for trabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:#retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
        #se o trabalho na lista de desejo NÃO for da profissão verificada no momento, passa para o proximo trabalho na lista
        if raridadeTrabalhoEComum(trabalhoDesejado):
            print(f'Trabalho comum encontado: {trabalhoDesejado[CHAVE_NOME]}.')
            linhaSeparacao()
            listaDicionariosTrabalhosComunsDesejados.append(trabalhoDesejado)
    if tamanhoIgualZero(listaDicionariosTrabalhosComunsDesejados):
        print(f'Nem um trabaho comum na lista!')
        linhaSeparacao()
    dicionarioTrabalho[CHAVE_LISTA_TRABALHO_COMUM]=listaDicionariosTrabalhosComunsDesejados
    return dicionarioTrabalho

def retornaListaDicionariosTrabalhosBuscados(listaDicionariosTrabalhos,profissao,raridade):
    listaDicionariosTrabalhosBuscados=[]
    for dicionarioTrabalho in listaDicionariosTrabalhos:
        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO],profissao)and
            textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE],raridade)):
            listaDicionariosTrabalhosBuscados.append(dicionarioTrabalho)
    return listaDicionariosTrabalhosBuscados

def defineChaveDicionarioTrabalhoComum(dicionarioTrabalho):
    print(f'Buscando trabalho comum.')
    global contadorParaCima
    if not primeiraBusca(dicionarioTrabalho):
        contadorParaCima=dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]
        clickEspecifico(contadorParaCima,'down')
        if dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]==3:
            yinicialNome=(2*70)+285
            nomeTrabalhoReconhecido=retornaNomeTrabalhoReconhecido(yinicialNome,1)
    while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
        if primeiraBusca(dicionarioTrabalho):
            clicks=3
            contadorParaCima=3
            clickEspecifico(clicks,'down')
            yinicialNome=(2*70)+285
            nomeTrabalhoReconhecido=retornaNomeTrabalhoReconhecido(yinicialNome,1)
        elif contadorParaCima==4:
            yinicialNome=(3*70)+285
            nomeTrabalhoReconhecido=retornaNomeTrabalhoReconhecido(yinicialNome,1)
        elif contadorParaCima>4:
            nomeTrabalhoReconhecido=retornaNomeTrabalhoReconhecido(530,1)
        if variavelExiste(nomeTrabalhoReconhecido):
            print(f'Trabalho reconhecido: {nomeTrabalhoReconhecido}')
            for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_TRABALHO_COMUM]:
                if requisitoRaridadecomumProfissaoEstadoproduzirSatisteito(dicionarioTrabalho, dicionarioTrabalhoDesejado):
                    print(f'Trabalho na lista: {dicionarioTrabalhoDesejado[CHAVE_NOME]}')
                    if textoEhIgual(nomeTrabalhoReconhecido, dicionarioTrabalhoDesejado[CHAVE_NOME]):
                        linhaSeparacao()
                        clickEspecifico(1,'enter')
                        dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]=contadorParaCima
                        dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]=dicionarioTrabalhoDesejado
                        contadorParaCima+=1
                        break
            else:
                linhaSeparacao()
                clickEspecifico(1,'down')
                contadorParaCima+=1
        else:
            dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
            vaiParaMenuTrabalhoEmProducao()
            print(f'Trabalho comum não reconhecido!')
            linhaSeparacao()
            break
    return dicionarioTrabalho

def vaiParaMenuTrabalhoEmProducao():
    clickEspecifico(1,'f1')
    clickContinuo(9,'up')
    clickEspecifico(1,'left')

def textoReconhecidoPertenceTextoDicionario(textoReconhecido, dicionario):
    return texto1PertenceTexto2(textoReconhecido[3:-3],dicionario[CHAVE_NOME].replace('-',''))

def requisitoRaridadecomumProfissaoEstadoproduzirSatisteito(dicionarioTrabalho, trabalhoListaDesejo):
    return raridadeTrabalhoEComum(trabalhoListaDesejo)and profissaoEIgual(dicionarioTrabalho, trabalhoListaDesejo)and estadoTrabalhoEParaProduzir(trabalhoListaDesejo)

def estadoTrabalhoEParaProduzir(trabalhoListaDesejo):
    return trabalhoListaDesejo[CHAVE_ESTADO]==para_produzir

def profissaoEIgual(dicionarioTrabalho, trabalhoListaDesejo):
    return textoEhIgual(trabalhoListaDesejo[CHAVE_PROFISSAO],dicionarioTrabalho[CHAVE_PROFISSAO])

def raridadeTrabalhoEComum(trabalhoListaDesejo):
    return textoEhIgual(trabalhoListaDesejo[CHAVE_RARIDADE],'comum')

def texto1PertenceTexto2(texto1,texto2):
    # print(f'{D}:{texto1} pertence a {texto2}?')
    return limpaRuidoTexto(texto1)in limpaRuidoTexto(texto2)

def textoEhIgual(texto1,texto2):
    return limpaRuidoTexto(texto1)==limpaRuidoTexto(texto2)

def variavelExiste(variavelVerificada):
    return variavelVerificada!=None

def primeiraBusca(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]==-1

def limpaRuidoTexto(texto):
    return unidecode(texto).replace(' ','').lower()

def retiraDigitos(texto):
    listaDigitos=['0','1','2','3','4','5','6','7','8','9']
    for digito in listaDigitos:
        texto=texto.replace(digito,'')
    return texto

def trabalhoEProducaoRecursos(dicionarioTrabalhoLista):
    confirmacao=False
    listaProducaoRecurso=[
        'melhorarlicençacomum',
        'licençadeproduçãodoaprendiz',
        'grandecoleçãoderecursoscomuns',
        'grandecoleçãoderecursosavançados',
        'coletaemmassaderecursosavançados',
        'melhoriadaessênciacomum',
        'melhoriadasubstânciacomum',
        'melhoriadocatalizadorcomum',
        'melhoriadaessênciacomposta',
        'melhoriadasubtânciacomposta',
        'melhoriadocatalizadoramplificado',
        'criaresferadoaprendiz','produzindoavarinhademadeira','produzindocabeçadocajadodejade',
        'produzindocabeçadecajadodeônix','criaresferadoneófito','produzindoavarinhadeaço',
        'extraçãodelascas','manipulaçãodelascas','fazermódoaprendiz',
        'preparandolascasdequartzo','manipulaçãodeminériodecobre','fazermódoprincipiante',
        'adquirirtesouradoaprendiz','produzindofioresistente','fazendotecidodelinho',
        'fazendotecidodecetim','comprartesouradoprincipiante','produzindofiogrosso',
        'adquirirfacadoaprendiz','recebendoescamasdaserpente','concluindocouroresistente',
        'adquirirfacadoprincipiante','recebendoescamasdolagarto','curtindocourogrosso',
        'adquirirmarretãodoaprendiz','forjandoplacasdecobre','fazendoplacasdebronze',
        'adquirirmarretãodoprincipiante','forjandoplacasdeferro','fazendoanéisdeaço',
        'adquirirmoldedoaprendiz','extraçãodepepitasdecobre','recebendogemadassombras',
        'adquirirmoldedoprincipiante','extraçãodepepitasdeprata','recebendogemadaluz',
        'adquirirpinçadoaprendiz','extraçãodejadebruta','recebendoenergiainicial',
        'adquirirpinçasdoprincipiante','extraçãodeônixextraordinária','recebendoéterinicial',
        'adquirirfuradordoaprendiz','produzindotecidodelicado','extraçãodesubstânciainstável',
        'adquirirfuradordoprincipiante','produzindotecidodenso','extraçãodesubstânciaestável']
    for recurso in listaProducaoRecurso:
        if textoEhIgual(recurso,dicionarioTrabalhoLista[CHAVE_NOME]):
            confirmacao=True
            break
    return confirmacao

def retornaNomeTrabalhoReconhecido(yinicial_nome,identificador):
    nomeTrabalhoReconhecido=None
    if identificador==0:
        altura=39
    elif identificador==1:
        altura=68
    #tira novo print da tela
    telaInteira=retornaAtualizacaoTela()
    frameTelaInteira=telaInteira[yinicial_nome:yinicial_nome+altura,233:478]
    #teste trata frame trabalho comum
    frameNomeTrabalhoTratado=retornaImagemBinarizada(frameTelaInteira)
    contadorPixelPreto=np.sum(frameNomeTrabalhoTratado==0)
    # print(f'{D}:Quantidade de pixels pretos: {contadorPixelPreto}')
    # mostraImagem(0,frameNomeTrabalhoTratado,None)
    if contadorPixelPreto>0:
        nomeTrabalhoReconhecido=reconheceTexto(frameNomeTrabalhoTratado)
    # print(f'{D}:Trabalho reconhecido {nomeTrabalhoReconhecido}.')
    return nomeTrabalhoReconhecido

def sai_trabalho_encontrado(x,tipo_trabalho):
    clicks=[2,1]
    clickEspecifico(clicks[tipo_trabalho],'f1')
    clickContinuo(x+1,'up')
    clickEspecifico(2,'left')

def verificaErro(dicionarioTrabalho):
    licenca=configuraLicenca(dicionarioTrabalho)
    time.sleep(0.5)
    print(f'Verificando erro...')
    erro=retornaTipoErro()
    if erro==erroPrecisaLicenca or erro==erroFalhaConectar or erro==erroConexaoInterrompida or erro==erroManutencaoServidor or erro==erroReinoIndisponivel:
        clickEspecifico(2,"enter")
        if erro==erroPrecisaLicenca:
            verificaLicenca(licenca)
        elif erro==erroFalhaConectar:
            print(f'Erro na conexão...')
        elif erro==erroConexaoInterrompida:
            print(f'Erro ao conectar...')
        elif erro==erroManutencaoServidor:
            print(f'Servidor em manutenção!')
        elif erro==erroReinoIndisponivel:
            print(f'Reino de jogo indisponível!')
        linhaSeparacao()
    elif erro==erroOutraConexao:
        clickEspecifico(1,'enter')
        print(f'Voltando para a tela inicial.')
        linhaSeparacao()
    elif erro==erroSemRecursos or erro==erroTempoProducaoExpirou or erro==erroSemExperiencia or erro==erroSemEspacosProducao:
        clickEspecifico(1,'enter')
        clickEspecifico(1,'f1')
        clickContinuo(contadorParaCima,'up')
        clickEspecifico(1,'left')
        if erro==erroSemRecursos:
            print(f'Retirrando trabalho da lista.')
        elif erro==erroSemExperiencia:
            print(f'Voltando para o menu profissões.')
        elif erro==erroSemEspacosProducao:
            print(f'Sem espaços livres para produção....')
        elif erro==erroTempoProducaoExpirou:
            print(f'O trabalho não está disponível.')
        linhaSeparacao()
    elif erro==erroPrecisaEscolherItem:
        print(f'Escolhendo item.')
        linhaSeparacao()
        clickEspecifico(1,'enter')
        clickEspecifico(1,'f2')
        clickContinuo(9,'up')
    elif erro==erroConectando or erro==erroRestaurandoConexao:
        if erro==erroConectando:
            print(f'Conectando...')
        elif erro==erroRestaurandoConexao:
            print(f'Restaurando conexão...')
        linhaSeparacao()
        time.sleep(1)
    elif erro==erroReceberRecompensas or erro==erroAtualizaJogo or erro==erroUsarObjetoParaProduzir:
        clickEspecifico(1,'f2')
        if erro==erroReceberRecompensas:
            print(f'Recuperar presente.')
        elif erro==erroUsarObjetoParaProduzir:
            print(f'Usa objeto para produzir outro.')
        elif erro==erroAtualizaJogo:
            print(f'Atualizando jogo...')
            clickEspecifico(1,'f1')
            exit()
        linhaSeparacao()
    elif erro==erroConcluirTrabalho:
        print(f'Trabalho não está concluido!')
        clickEspecifico(1,'f1')
        clickContinuo(8,'up')
        linhaSeparacao()
    elif erro==erroSemEspacosBolsa:
        clickEspecifico(1,'f1')
        clickContinuo(8,'up')
        print(f'Ignorando trabalho concluído!')
        linhaSeparacao()
    elif erro==erroSemMoedas:
        clickEspecifico(1,'f1')
        linhaSeparacao()
    elif erro==erroEmailSenhaIncorreta:
        clickEspecifico(1,'enter')
        clickEspecifico(1,'f1')
        print(f'Login ou senha incorreta...')
        linhaSeparacao()
    else:
        print(f'Nem um erro encontrado!')
        linhaSeparacao()
    return erro

def entraLicenca(dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    erro=verificaErro(None)
    if erro==0:
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
        clickEspecifico(1,'up')
        clickEspecifico(1,'enter')
    elif erro==erroOutraConexao:
        dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
    return dicionarioPersonagem

def entraTrabalhoEncontrado(dicionarioTrabalho,trabalhoListaDesejo):
    dicionarioTrabalho[CHAVE_CONFIRMACAO]=True
    erro=verificaErro(trabalhoListaDesejo)
    print(f'Entra trabalho na posição: {dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]+1}.')
    if erroEncontrado(erro):
        if erro==erroOutraConexao or erro==erroConectando or erro==erroRestaurandoConexao:
            dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
            if erro==erroOutraConexao:
                dicionarioTrabalho[CHAVE_UNICA_CONEXAO]
    clickContinuo(3,'up')
    clickEspecifico(dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]+1,'down')
    clickEspecifico(1,'enter')
    linhaSeparacao()
    return dicionarioTrabalho

#modificado 12/01
def retornaTipoErro():
    erro=0
    telaInteira=retornaAtualizacaoTela()
    frameErro=telaInteira[335:335+100,150:526]
    textoErroEncontrado=reconheceTexto(frameErro)
    # print(f'{D}:{textoErroEncontrado}')
    linhaSeparacao()
    if variavelExiste(textoErroEncontrado):
        textoErroEncontrado=limpaRuidoTexto(textoErroEncontrado)
        textoErroEncontrado=retiraDigitos(textoErroEncontrado)
        tipoErro=['precisoumalicençadeproduçãoparainiciarotrabalho','Nãofoipossívelseconectaraoservidor',
                    'Vocênãotemosrecursosnecessáriasparaessetrabalho','Vocêprecisaescolherumitemparainiciarumtrabalhodeprodução',
                    'Conectando','precisomaisexperiênciaprofissionalparainiciarotrabalho','GostariadeiràLojaMilagrosaparaveralistadepresentes',
                    'Vocênãotemespaçoslivresparaotrabalho','agorapormoedas','Oservidorestáemmanutenção',
                    'Foidetectadaoutraconexãousandoseuperfil','Gostanadecomprar','conexãocomoservidorfoiinterrompida',
                    'Vocêprecisademaismoedas','Loginousenhaincorreta','otempodevidada',
                    'reinodejogoselecionado','jogoestadesatualizada','restaurandoconexão','paraatarefadeprodução']
        for posicaoTipoErro in range(len(tipoErro)):
            textoErro=limpaRuidoTexto(tipoErro[posicaoTipoErro])
            if textoErro in textoErroEncontrado:
                # print(f'{D}:"{textoErro}" encontrado em "{textoErroEncontrado}".')
                linhaSeparacao()
                erro=posicaoTipoErro+1
    return erro

def retorna_nome_inimigo(tela_inteira):
    altura_tela = tela_inteira.shape[0]
    frame_tela = tela_inteira[0:altura_tela,0:674]
    frame_nome_objeto = frame_tela[32:32+30,frame_tela.shape[1]-164:frame_tela.shape[1]]
    frame_nome_objeto_tratado = trata_frame_nome_inimigo(frame_nome_objeto)
    nomeInimigo=reconheceTexto(frame_nome_objeto_tratado)
    if nomeInimigo!=None:
        nomeInimigo=nomeInimigo.replace(' ','').lower()
    else:
        print(f'Ocorreu algumm erro ao verificar o nome do inimigo!')
        linhaSeparacao()
    return nomeInimigo

def retorna_lista_histograma_menu():
    lista_histograma = []
    print(f'Reconhecendo histograma dos menus.')
    linhaSeparacao()
    for x in range(10):
        #abre a imagem do modelo
        modelo = abre_imagem(f'modelos/modelo_menu_{x}.png')
        #calcula histograma do modelo
        histograma_modelo = retorna_histograma(modelo)
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
        modelo = abre_imagem(f'modelos/novo_modelo_habilidade_{x}.png')
        lista_imagem_habilidade.append(modelo)
        x+=1
    return lista_imagem_habilidade

def verifica_arquivo_existe(caminho_arquivo):
    if(os.path.exists(caminho_arquivo)):
          return True
    return False

def retornaListaDicionariosProfissoesNecessarias(dicionarioPersonagem):
    print(f'Verificando profissões necessárias...')
    #cria lista vazia
    lista_profissao_verificada=[]
    #abre o arquivo lista de profissoes
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]=retornaListaDicionarioProfissao(dicionarioPersonagem)
    #abre o arquivo lista de desejos
    dicionarioPersonagem[CHAVE_LISTA_DESEJO]=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
    #percorre todas as linha do aquivo profissoes
    posicao=1
    for profissao in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        #percorre todas as linhas do aquivo lista de desejos
        for trabalhoDesejado in dicionarioPersonagem[CHAVE_LISTA_DESEJO]:
            if profissaoENecessaria(profissao, trabalhoDesejado)and estadoTrabalhoEParaProduzir(trabalhoDesejado):
                #verifca se o indice já está na lista
                dicionarioProfissao={CHAVE_ID:profissao[CHAVE_ID],
                                     CHAVE_NOME:profissao[CHAVE_NOME],
                                     CHAVE_POSICAO:posicao}
                lista_profissao_verificada.append(dicionarioProfissao)
                break
        posicao+=1
    else:
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA]=lista_profissao_verificada
        mostraProfissoesNecessarias(dicionarioPersonagem)
    return dicionarioPersonagem

def profissaoENecessaria(profissao, trabalhoDesejado):
    return unidecode(profissao[CHAVE_NOME]).replace(' ','').lower()==unidecode(trabalhoDesejado[CHAVE_PROFISSAO]).replace(' ','').lower()

def mostraProfissoesNecessarias(dicionarioPersonagem):
    for profissao in dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA]:
        print(f'Profissão necessária: {profissao[CHAVE_NOME]}')
    linhaSeparacao()

def retorna_lista_habilidade_verificada():
    print(f'Criando lista de habilidades...')
    lista_habilidade_encontrada = []
    lista_imagem_habilidade = retorna_lista_imagem_habilidade()
    tela_inteira = retornaAtualizacaoTela()
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
                    linhaSeparacao()
                    break
    else:
        print(f'Processo concluído!')
        linhaSeparacao()
    return lista_habilidade_encontrada

def passa_proxima_posicao():
    global yinicial, yfinal, altura_frame
    #passa para a proxima posição de produção
    yinicial = yfinal+23
    yfinal = yfinal+altura_frame

def entraPersonagemAtivo(dicionarioPersonagem):
    personagem=None
    contadorPersonagem=0
    print(f'Buscando personagem ativo...')
    clickEspecifico(1,'enter')
    time.sleep(1)
    while verificaErro(None)!=0:
        continue
    else:
        clickEspecifico(1,'f2')
        clickContinuo(8,'left')   
        personagemReconhecido=retornaNomePersonagem(1)
        # print(f'{D}:personagem reconhecido: {personagemReconhecido}.')
        dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=None
        while variavelExiste(personagemReconhecido) and contadorPersonagem<13:
            dicionarioPersonagem=confirmaNomePersonagem(personagemReconhecido,dicionarioPersonagem)
            if variavelExiste(dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                ativaAtributoUso(dicionarioPersonagem)
                clickEspecifico(1,'f2')
                time.sleep(1)
                erro=verificaErro(None)
                while erro!=0:
                    if erro==erroOutraConexao:
                        personagem=personagemReconhecido
                        personagemReconhecido=None
                        break
                    erro=verificaErro(None)
                else:
                    print(f'Login efetuado com sucesso!')
                    linhaSeparacao()
                    break
            else:
                clickEspecifico(1,'right')
                personagemReconhecido=retornaNomePersonagem(1)
                # print(f'{D}:personagem reconhecido: {personagemReconhecido}.')
            contadorPersonagem+=1
        else:
            print(f'Personagem não encontrado!')
            linhaSeparacao()
            if retornaMenu()==menu_escolha_p:
                clickEspecifico(1,'f1')
    return personagem

def confirmaNomePersonagem(personagemReconhecido,dicionarioPersonagem):
    for dicionarioPersonagemAtivo in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
        # print(f'{D}:{personagemReconhecido} e {dicionarioPersonagemAtivo[CHAVE_NOME]}.')
        if textoEhIgual(personagemReconhecido,dicionarioPersonagemAtivo[CHAVE_NOME]):
            print(f'Personagem {personagemReconhecido} confirmado!')
            linhaSeparacao()
            dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=dicionarioPersonagemAtivo
            break
    return dicionarioPersonagem

def defineListaIdPersonagemMesmoEmail(dicionarioPersonagem,personagemEmail):
    listaIdPersonagemMesmoEmail=[]
    for dicionarioPersonagemAtivo in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        if textoEhIgual(dicionarioPersonagemAtivo[CHAVE_EMAIL],personagemEmail):
            listaIdPersonagemMesmoEmail.append(dicionarioPersonagemAtivo[CHAVE_ID])
    return listaIdPersonagemMesmoEmail

def ativaAtributoUso(dicionarioPersonagem):
    listaPersonagemIdMesmoEmail=defineListaIdPersonagemMesmoEmail(dicionarioPersonagem,dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_EMAIL])
    if not verificaListaVazia(listaPersonagemIdMesmoEmail):
        modificaAtributoPersonagem(dicionarioPersonagem,listaPersonagemIdMesmoEmail,CHAVE_USO,True)
#modificado 16/01
def preparaPersonagem(dicionarioUsuario):
    #lista_profissao_necessaria é uma matrix onde o indice 0=posição da profissão
    #e o indice 1=nome da profissão
    click_atalho_especifico('alt','tab')
    click_atalho_especifico('win','left')
    dicionarioDadosPersonagem=retornaDicionarioDadosPersonagem(dicionarioUsuario)
    if len(dicionarioDadosPersonagem)!=0:
        if not dicionarioDadosPersonagem[CHAVE_USO]:#se o personagem estiver inativo, troca o estado
            listaPersonagemId=[dicionarioUsuario[CHAVE_ID_PERSONAGEM]]
            modificaAtributoPersonagem(dicionarioUsuario,listaPersonagemId,CHAVE_ESTADO,True)
        buscaListaPersonagemAtivo(dicionarioUsuario)
    else:
        print(f'Erro ao configurar atributos do personagem!')
        linhaSeparacao()

def defineListaDicionarioPersonagemAtivo(dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]=[]
    for personagem in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        # print(f'Verificando estado do personagem: {personagem}.')
        if (personagem[CHAVE_ESTADO]or
            personagem[CHAVE_ESTADO]==1):
            # print(f'{D}:{personagem[CHAVE_NOME]} é ativo.')
            dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO].append(personagem)
    return dicionarioPersonagem

def buscaListaPersonagemAtivo(dicionarioUsuario):
    dicionarioPersonagem={CHAVE_ID_USUARIO:dicionarioUsuario[CHAVE_ID_USUARIO],
                          CHAVE_LISTA_DICIONARIO_PERSONAGEM:dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]}
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]=[]
    dicionarioPersonagem=defineListaDicionarioPersonagemAtivo(dicionarioPersonagem)
    # print(f'CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO: {dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]}.')
    while True:
        if verificaListaVazia(dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
            dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]=[]
            dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=defineListaDicionarioPersonagem(dicionarioUsuario)
            dicionarioPersonagem=defineListaDicionarioPersonagemAtivo(dicionarioPersonagem)
            print(f'Lista de personagens ativos atualizada...')
            linhaSeparacao()
        else:#se houver pelo menos um personagem ativo
            dicionarioPersonagemReconhecido=verificaNomePersonagemAtivoReconhecido(dicionarioPersonagem)
            if not tamanhoIgualZero(dicionarioPersonagemReconhecido):
                dicionarioPersonagem[CHAVE_ID_PERSONAGEM]=dicionarioPersonagemReconhecido[CHAVE_ID]
                dicionarioPersonagem[CHAVE_NOME_PERSONAGEM]=dicionarioPersonagemReconhecido[CHAVE_NOME]
                dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=dicionarioPersonagemReconhecido[CHAVE_ESPACO_PRODUCAO]
                dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=True
                dicionarioPersonagem[CHAVE_ESPACO_BOLSA]=True
                dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]=False
                print('Inicia busca...')
                linhaSeparacao()
                dicionarioPersonagem=iniciaBuscaTrabalho(dicionarioPersonagem)
                if dicionarioPersonagem[CHAVE_UNICA_CONEXAO]:
                    if verificaErro(None)!=0 or len(dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO])==1:
                        dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=defineListaDicionarioPersonagem(dicionarioUsuario)
                        dicionarioPersonagem=defineListaDicionarioPersonagemAtivo(dicionarioPersonagem)
                        print(f'Lista de personagens ativos atualizada...')
                        linhaSeparacao()
                        continue
                    else:
                        clickMouseEsquerdo(1,2,35)
                        deslogaPersonagem(dicionarioPersonagemReconhecido[CHAVE_EMAIL],dicionarioPersonagem)
                        dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemReconhecido)
                        dicionarioPersonagem=retiraDicionarioPersonagemListaAtivo(dicionarioPersonagem)
                else:
                    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemReconhecido)
                    dicionarioPersonagem=retiraDicionarioPersonagemListaAtivo(dicionarioPersonagem)
                    continue
            else:#se o nome reconhecido não estiver na lista de ativos
                if (not tamanhoIgualZero(dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO])and
                    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1][CHAVE_EMAIL]==dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][0][CHAVE_EMAIL]):
                    nome=entraPersonagemAtivo(dicionarioPersonagem)
                    print(nome)
                elif configuraLoginPersonagem(dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
                    nome=entraPersonagemAtivo(dicionarioPersonagem)
                    print(nome)
                    if nome!=None and dicionarioPersonagemReconhecido!=None:
                        dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemReconhecido)
                        dicionarioPersonagem=retiraDicionarioPersonagemListaAtivo(dicionarioPersonagem)

def retornaTextoMenuReconhecido(x,y,largura):
    telaInteira=retornaAtualizacaoTela()
    # print(centroAltura,centroMetade)# 384 341
    alturaFrame=30
    texto=None
    frameTela=telaInteira[y:y+alturaFrame,x:x+largura]
    if y>30:
        frameTela=retornaImagemBinarizada(frameTela)
    # mostraImagem(0,frameTela,None)
    # print(f'Quantidade de pixels pretos: {np.sum(frameTela==0)}')
    contadorPixelPreto=np.sum(frameTela==0)
    if existePixelPretoSuficiente(contadorPixelPreto):
        texto=reconheceTexto(frameTela)
        if variavelExiste(texto):
            texto=limpaRuidoTexto(texto)
            # print(f'{D}:Texto reconhecimento de menus: {texto}.')
    # print(f'{D} :{texto}')
    return texto

def existePixelPretoSuficiente(contadorPixelPreto):
    return contadorPixelPreto>250 and contadorPixelPreto<3000

def retornaMenu():
    # 1050,1077,3006,1035,1251,1092,1215,1854,1863,1617,1377,2637,1344,
    # 1947,2721
    inicio = time.time()
    print(f'Reconhecendo menu.')
    textoMenu=retornaTextoMenuReconhecido(26,1,150)
    if variavelExiste(textoMenu):
        if texto1PertenceTexto2('spearonline',textoMenu):
            textoMenu=retornaTextoMenuReconhecido(216,194,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('notícias',textoMenu):
                    print(f'Menu notícias...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_noticias
                elif texto1PertenceTexto2('seleçãodepersonagem',textoMenu):
                    print(f'Menu escolha de personagem...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_escolha_p
                elif texto1PertenceTexto2('produzir',textoMenu):
                    textoMenu=retornaTextoMenuReconhecido(266,242,150)
                    if variavelExiste(textoMenu):
                        if texto1PertenceTexto2('profissões',textoMenu):
                            textoMenu=retornaTextoMenuReconhecido(191,609,100)
                            if variavelExiste(textoMenu):
                                if texto1PertenceTexto2('fechar',textoMenu):
                                    print(f'Menu produzir...')
                                    linhaSeparacao()
                                    fim = time.time()
                                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                                    linhaSeparacao()
                                    return menu_produzir
                                elif texto1PertenceTexto2('voltar',textoMenu):
                                    print(f'Menu trabalhos diponíveis...')
                                    linhaSeparacao()
                                    fim = time.time()
                                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                                    linhaSeparacao()
                                    return menu_trab_disponiveis
                        elif texto1PertenceTexto2('trabalhosatuais',textoMenu):
                            print(f'Menu trabalhos atuais...')
                            linhaSeparacao()
                            fim = time.time()
                            # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                            linhaSeparacao()
                            return menu_trab_atuais
            textoMenu=retornaTextoSair()
            if variavelExiste(textoMenu):
                if textoEhIgual(textoMenu,'sair'):
                    print(f'Menu jogar...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_jogar
            if verificaMenuReferencia():
                print(f'Menu tela inicial...')
                linhaSeparacao()
                fim = time.time()
                # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                linhaSeparacao()
                return menu_inicial
            textoMenu=retornaTextoMenuReconhecido(291,409,100)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('conquistas',textoMenu):
                    print(f'Menu personagem...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_personagem
                elif texto1PertenceTexto2('interagir',textoMenu):
                    print(f'Menu principal...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_principal
            textoMenu=retornaTextoMenuReconhecido(191,319,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('parâmetros',textoMenu):
                    if texto1PertenceTexto2('requisitos',textoMenu):
                        print(f'Menu atributo do trabalho...')
                        linhaSeparacao()
                        fim = time.time()
                        # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                        linhaSeparacao()
                        return menu_trab_atributos
                    else:
                        print(f'Menu licenças...')
                        linhaSeparacao()
                        fim = time.time()
                        # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                        linhaSeparacao()
                        return menu_licencas
            textoMenu=retornaTextoMenuReconhecido(281,429,120)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('profissional',textoMenu):
                    print(f'Menu trabalho específico...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_trab_especifico
            textoMenu=retornaTextoMenuReconhecido(266,269,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('ofertadiária',textoMenu):
                    print(f'Menu oferta diária...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_ofe_diaria
            textoMenu=retornaTextoMenuReconhecido(181,71,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('lojamilagrosa',textoMenu):
                    print(f'Menu loja milagrosa...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_loja_milagrosa
            textoMenu=retornaTextoMenuReconhecido(180,40,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('recompensasdiárias',textoMenu):
                    # print(f'{D}:Menu recompensas diárias...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_rec_diarias
            textoMenu=retornaTextoMenuReconhecido(180,60,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('recompensasdiárias',textoMenu):
                    print(f'Menu recompensas diárias...')
                    linhaSeparacao()
                    fim = time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_rec_diarias
            textoMenu=retornaTextoMenuReconhecido(310,338,57)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('meu',textoMenu):
                    print(f'Menu meu perfil...')
                    linhaSeparacao()
                    fim=time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_meu_perfil
            
            textoMenu=retornaTextoMenuReconhecido(169,97,75)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('bolsa',textoMenu):
                    print(f'Menu bolsa...')
                    linhaSeparacao()
                    fim=time.time()
                    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_bolsa

    print(f'Menu não reconhecido...')
    linhaSeparacao()
    fim = time.time()
    # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
    linhaSeparacao()
    click_atalho_especifico('win','left')
    click_atalho_especifico('win','left')
    verificaErro(None)
    return menu_desconhecido

def deslogaPersonagem(personagemEmail,dicionarioPersonagem):
    menu=retornaMenu()
    while menu!=menu_jogar:
        if menu==menu_inicial:
            encerra_secao()
            break
        elif menu==menu_jogar:
            break
        else:
            clickMouseEsquerdo(1,2,35)
        menu=retornaMenu()
    if personagemEmail!=None or dicionarioPersonagem!=None:
        listaPersonagemId=defineListaIdPersonagemMesmoEmail(dicionarioPersonagem,personagemEmail)
        modificaAtributoPersonagem(dicionarioPersonagem,listaPersonagemId,CHAVE_USO,False)

def retiraDicionarioPersonagemListaAtivo(dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=defineListaDicionarioPersonagem(dicionarioPersonagem)
    dicionarioPersonagem=defineListaDicionarioPersonagemAtivo(dicionarioPersonagem)
    print(f'Lista de personagens ativos atualizada!')
    linhaSeparacao()
    for dicionarioPersonagemRemovido in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]:#percorre lista de personagem retirado
        posicao=0
        for dicionarioPersonagemAtivo in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:#percorre lista de personagem ativo
            if dicionarioPersonagemAtivo[CHAVE_NOME] in dicionarioPersonagemRemovido[CHAVE_NOME]:#compara nome na lista de ativo com nome na lista de retirado
                print(f'{dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][posicao][CHAVE_NOME]} foi retirado da lista de ativos!')
                linhaSeparacao()
                del dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][posicao]
                posicao-=1
            else:
                posicao+=1
    return dicionarioPersonagem

def verificaListaVazia(lista_personagem_ativo):
    if len(lista_personagem_ativo)==0:
        print(f'Lista vazia. Buscando nova lista no servidor.')
        linhaSeparacao()
        return True
    return False

def verificaNomePersonagemAtivoReconhecido(dicionarioPersonagem):
    dicionarioPersonagemReconhecido={}
    nomePersonagemReconhecidoTratado=retornaNomePersonagem(0)
    # print(f'{D}:Nome personagem na posição 0:{nomePersonagemReconhecidoTratado}')
    if variavelExiste(nomePersonagemReconhecidoTratado):
        for dicionarioPersonagemVerificado in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
            if textoEhIgual(nomePersonagemReconhecidoTratado,dicionarioPersonagemVerificado[CHAVE_NOME]):
                print(f'Personagem {nomePersonagemReconhecidoTratado} confirmado!')
                linhaSeparacao()
                dicionarioPersonagemReconhecido=dicionarioPersonagemVerificado
    else:
        print(f'Nome personagem diferente!')
        linhaSeparacao()
    return dicionarioPersonagemReconhecido

def configuraLoginPersonagem(listaDicionarioPersonagensAtivos):
    login=False
    menu=retornaMenu()
    while menu!=menu_jogar:
        if menu==menu_noticias or menu==menu_escolha_p:
            clickEspecifico(1,'f1')
        elif menu!=menu_inicial:
            clickMouseEsquerdo(1,2,35)
        else:
            encerra_secao()
        linhaSeparacao()
        menu=retornaMenu()
    else:
        login=logaContaPersonagem(listaDicionarioPersonagensAtivos)
    return login
    
def logaContaPersonagem(listaDicionarioPersonagensAtivos):
    confirmacao=False
    email=listaDicionarioPersonagensAtivos[0][CHAVE_EMAIL]
    senha=listaDicionarioPersonagensAtivos[0][CHAVE_SENHA]
    print(f'Tentando logar conta personagem...')
    preencheCamposLogin(email,senha)
    erro=verificaErro(None)
    while erro!=0:
        if erro==erroConectando or erro==erroRestaurandoConexao:
            time.sleep(1)
        elif erro==erroEmailSenhaIncorreta:
            break
        else:
            print('Erro ao tentar logar...')
        erro=verificaErro(None)
    else:
        print(f'Login efetuado com sucesso!')
        confirmacao=True
    linhaSeparacao()
    return confirmacao

def defineListaDicionariosTrabalhosPriorizados(dicionarioTrabalho):
    listaDicionariosTrabalhosDesejadosPriorizados=[]
    for dicionarioTrabalhoLista in dicionarioTrabalho[CHAVE_LISTA_DESEJO]:
        if (estadoTrabalhoEParaProduzir(dicionarioTrabalhoLista)and
            textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO],dicionarioTrabalhoLista[CHAVE_PROFISSAO])):
            if textoEhIgual(dicionarioTrabalhoLista[CHAVE_RARIDADE],'especial'):
                dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=1
                listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
            elif textoEhIgual(dicionarioTrabalhoLista[CHAVE_RARIDADE],'raro'):
                if trabalhoEProducaoRecursos(dicionarioTrabalhoLista):
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=3
                    listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
                else:
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=2
                    listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
            else:
                if trabalhoEProducaoRecursos(dicionarioTrabalhoLista):
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=5
                    listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
                else:
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=4
                    listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
    else:
        listaDicionariosTrabalhosDesejadosPriorizadosOrdenada=sorted(listaDicionariosTrabalhosDesejadosPriorizados,key=lambda dicionario:(dicionario[CHAVE_PRIORIDADE],dicionario[CHAVE_NOME]))
        # for trabalho in listaDicionariosTrabalhosDesejadosPriorizadosOrdenada:
        #     print(f'{D}:{trabalho[CHAVE_NOME]}:{trabalho[CHAVE_PRIORIDADE]}')
    dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]=listaDicionariosTrabalhosDesejadosPriorizadosOrdenada
    return dicionarioTrabalho

def defineDicionarioTrabalhoRaroEspecial(dicionarioTrabalho):
    nomeTrabalhoReconhecido=reconheceTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
    print(f'Nome trabalho raro/especial reconhecido: {nomeTrabalhoReconhecido}.')
    # print(f'{D}:Posição trabalho raro/especial: {dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]}.')
    if variavelExiste(nomeTrabalhoReconhecido):
        for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
            if texto1PertenceTexto2(nomeTrabalhoReconhecido,dicionarioTrabalhoDesejado[CHAVE_NOME]):
                dicionarioTrabalho=entraTrabalhoEncontrado(dicionarioTrabalho,dicionarioTrabalhoDesejado)
                if chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                    dicionarioTrabalho=confirmaNomeTrabalho(dicionarioTrabalho,1)
                break
    else:
        dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]=4
    return dicionarioTrabalho

def iniciaBuscaTrabalho(dicionarioPersonagem):
    listaDicionariosTrabalhosDesejados=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
    dicionarioTrabalho={CHAVE_LISTA_DESEJO:listaDicionariosTrabalhosDesejados,
                        CHAVE_DICIONARIO_TRABALHO_DESEJADO:None}
    if not tamanhoIgualZero(listaDicionariosTrabalhosDesejados):#verifica se a lista está vazia
        dicionarioPersonagem=retornaListaDicionariosProfissoesNecessarias(dicionarioPersonagem)
        for profissaoVerificada in dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA]:#percorre lista de profissao
            if not chaveUnicaConexaoForVerdadeira(dicionarioPersonagem):
                continue
            erro=verificaErro(None)
            if not erroEncontrado(erro):
                menu=retornaMenu()
                if estaMenuInicial(menu):
                    if existePixelCorrespondencia():
                        vaiParaMenuCorrespondencia()
                        recuperaCorrespondencia(dicionarioPersonagem)
                while naoEstiverMenuProduzir(menu):
                    dicionarioPersonagem=trataMenu(menu,dicionarioPersonagem)
                    if not chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
                        return dicionarioPersonagem
                    menu=retornaMenu()
                else:
                    # print(f'CHAVE_LISTA_PROFISSAO_MODIFICADA:{dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]}')
                    if listaProfissoesFoiModificada(dicionarioPersonagem):
                        dicionarioPersonagem=atualizaListaProfissao(dicionarioPersonagem)
                    print(f'Verificando profissão: {profissaoVerificada[CHAVE_NOME]}')
                    linhaSeparacao()
                    dicionarioTrabalho[CHAVE_PROFISSAO]=profissaoVerificada[CHAVE_NOME]
                    dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]=-1
                    dicionarioTrabalho[CHAVE_CONFIRMACAO]=True
                    while chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                        entraProfissaoEspecifica(profissaoVerificada[CHAVE_POSICAO])
                        dicionarioTrabalho=defineListaDicionariosTrabalhosPriorizados(dicionarioTrabalho)
                        dicionarioTrabalho=retornaListaDicionarioTrabalhoComum(dicionarioTrabalho)
                        if not textoEhIgual(dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA][0][CHAVE_RARIDADE],'comum'):
                            dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]=0
                            while naoFizerQuatroVerificacoes(dicionarioTrabalho)and dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]==None:
                                dicionarioTrabalho=defineDicionarioTrabalhoRaroEspecial(dicionarioTrabalho)
                                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                    dicionarioTrabalho,dicionarioPersonagem=iniciaProducao(dicionarioTrabalho,dicionarioPersonagem)
                                if not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                    break
                                incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                                linhaSeparacao()
                            else:
                                if dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]==None:
                                    if tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_TRABALHO_COMUM]):
                                        saiProfissaoVerificada(dicionarioTrabalho)
                                    else:
                                        dicionarioPersonagem,dicionarioTrabalho=buscaTrabalhoComum(dicionarioPersonagem, dicionarioTrabalho)
                        else:
                            dicionarioPersonagem,dicionarioTrabalho=buscaTrabalhoComum(dicionarioPersonagem, dicionarioTrabalho)
                        if chaveUnicaConexaoForVerdadeira(dicionarioPersonagem):
                            if chaveEspacoBolsaForVerdadeira(dicionarioPersonagem):
                                if retornaEstadoTrabalho()==concluido:
                                    dicionarioPersonagem=verificaTrabalhoConcluido(dicionarioPersonagem)
                                elif not chaveEspacoProducaoForVerdadeira(dicionarioPersonagem):
                                    break
                            dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]=None
                            clickEspecifico(1,'left')
                            linhaSeparacao()
                        else:
                            break
                    if not chaveEspacoProducaoForVerdadeira(dicionarioPersonagem):
                        break
            elif existeOutraConexao(erro):
                dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
            else:
                print(f'Erro ao percorrer lista de profissões...')
                linhaSeparacao()
                break
        else:
            # print(f'CHAVE_LISTA_PROFISSAO_MODIFICADA:{dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]}')
            if listaProfissoesFoiModificada(dicionarioPersonagem):
                dicionarioPersonagem=atualizaListaProfissao(dicionarioPersonagem)
            print(f'Fim da lista de profissões...')
            linhaSeparacao()
    else:
        print(f'Lista de trabalhos desejados vazia.')
        linhaSeparacao()
    return dicionarioPersonagem

def saiProfissaoVerificada(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
    print(f'Nem um trabalho disponível está na lista de desejos.')
    clickContinuo(4,'up')
    clickEspecifico(1,'left')
    linhaSeparacao()

def buscaTrabalhoComum(dicionarioPersonagem, dicionarioTrabalho):
    dicionarioTrabalho=defineChaveDicionarioTrabalhoComum(dicionarioTrabalho)
    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
        dicionarioTrabalho,dicionarioPersonagem=iniciaProducao(dicionarioTrabalho,dicionarioPersonagem)
        linhaSeparacao()
    return dicionarioPersonagem,dicionarioTrabalho

def reconheceTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho):
    yinicialNome=(dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]*70)+285
    nomeTrabalhoReconhecido=retornaNomeTrabalhoReconhecido(yinicialNome,0)
    return nomeTrabalhoReconhecido

def chaveEspacoProducaoForVerdadeira(dicionarioPersonagem):
    # print(f'{D}:CHAVE_ESPACO_PRODUCAO={dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]}.')
    return dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]

def incrementaChavePosicaoTrabalho(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]+=1

def chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
    # print(f'{D}:CHAVE_DICIONARIO_TRABALHO_DESEJADO: {dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]}.')
    return dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]!=None

def naoFizerQuatroVerificacoes(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]<4

def chaveEspacoBolsaForVerdadeira(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_ESPACO_BOLSA]

def existeOutraConexao(erro):
    return erro==erroOutraConexao

def listaProfissoesFoiModificada(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]

def tamanhoIgualZero(lista):
    return len(lista)==0

def chaveUnicaConexaoForVerdadeira(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_UNICA_CONEXAO]

def chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_CONFIRMACAO]

def naoEstiverMenuProduzir(menu):
    return menu!=menu_produzir

def erroEncontrado(erro):
    return erro!=0

def vaiParaMenuCorrespondencia():
    clickEspecifico(1,'f2')
    clickEspecifico(1,'1')
    clickEspecifico(1,'9')

def estaMenuInicial(menu):
    return menu==menu_inicial

def verificaTrabalhoConcluido(dicionarioPersonagem):
    dicionarioPersonagem,dicionarioTrabalho=recuperaTrabalhoConcluido(dicionarioPersonagem)
    if not tamanhoIgualZero(dicionarioTrabalho):
        listaPersonagem=[dicionarioPersonagem[CHAVE_ID_PERSONAGEM]]
        if dicionarioTrabalho[CHAVE_RECORRENCIA]:
            print(f'Trabalho recorrente.')
            excluiTrabalho(dicionarioPersonagem,dicionarioTrabalho)
            linhaSeparacao()
        else:
            print(f'Trabalho sem recorrencia.')
            modificaEstadoTrabalho(dicionarioPersonagem,
                                    dicionarioTrabalho,
                                    2)
            linhaSeparacao()
        if not dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]:
            modificaAtributoPersonagem(dicionarioPersonagem,listaPersonagem,CHAVE_ESPACO_PRODUCAO,True)
            dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=True
    return dicionarioPersonagem

def recuperaTrabalhoConcluido(dicionarioPersonagem):
    dicionarioTrabalho={}
    tela_inteira=retornaAtualizacaoTela()
    frameNomeTrabalho=tela_inteira[285:285+37, 233:486]
    if verificaErro(None)==0:
        nomeTrabalhoConcluido=reconheceTexto(frameNomeTrabalho)
        clickEspecifico(1,'down')
        clickEspecifico(1,'f2')
        # print(f'{D}:Trabalho concluido reconhecido: {nomeTrabalhoConcluido}.')
        if variavelExiste(nomeTrabalhoConcluido):
            if verificaErro(None)==0:
                if not dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]:
                    dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]=True
                    # print(f'{D}:CHAVE_LISTA_PROFISSAO_MODIFICADA:{dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]}')
                listaDicionarioTrabalhoDesejado=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
                if not tamanhoIgualZero(listaDicionarioTrabalhoDesejado):
                    for dicionarioTrabalhoProduzindo in listaDicionarioTrabalhoDesejado:
                        if (texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1],dicionarioTrabalhoProduzindo[CHAVE_NOME])and
                            dicionarioTrabalhoProduzindo[CHAVE_ESTADO]==produzindo):
                            dicionarioTrabalho=dicionarioTrabalhoProduzindo
                            print(f'{dicionarioTrabalhoProduzindo[CHAVE_NOME]} recuperado.')
                            break
                clickContinuo(1,'up')
                linhaSeparacao()
            else:
                dicionarioPersonagem[CHAVE_ESPACO_BOLSA]=False
                clickContinuo(1,'up')
                clickEspecifico(1,'left')
    return dicionarioPersonagem,dicionarioTrabalho

def trataErros(dicionarioTrabalho,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
    erro=verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
    while erroEncontrado(erro):
        if erro==erroSemRecursos:
            excluiTrabalho(dicionarioPersonagem,dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
            dicionarioTrabalho[CHAVE_LISTA_DESEJO]=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
            if tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_DESEJO]):
                dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
                # print(f'{D}:trataErros:CHAVE_CONFIRMACAO=False')
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        elif erro==erroSemEspacosProducao or erro==erroOutraConexao or erro==erroConectando or erro==erroRestaurandoConexao:
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
            dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
            if erro==erroSemEspacosProducao:
                listaPersonagem=[dicionarioPersonagem[CHAVE_ID_PERSONAGEM]]
                modificaAtributoPersonagem(dicionarioPersonagem,listaPersonagem,CHAVE_ESPACO_PRODUCAO,False)
                dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=False
            elif erro==erroOutraConexao:
                dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
        erro=verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
    return dicionarioTrabalho,dicionarioPersonagem

def trataMenus(dicionarioTrabalho,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    while True:
        menu=retornaMenu()
        if naoReconheceMenu(menu):
            continue
        elif menuTrabalhoEspecificoReconhecido(menu):
            clickEspecifico(1,'f2')
            if naoHaRecursosSuficientes(dicionarioTrabalho):
                excluiTrabalho(dicionarioPersonagem,dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
                break
        elif menuEscolhaEquipamentoReconhecido(menu):
            clickEspecifico(1,'f2')
            time.sleep(1)
            verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
        elif menuTrabalhosAtuais(menu):
            if trabalhoERecorrente(dicionarioTrabalho):
                print(f'Recorrencia está ligada.')
                cloneDicionarioTrabalho = defineCloneDicionarioTrabalho(dicionarioTrabalho)
                cloneDicionarioTrabalho=adicionaTrabalhoDesejo(dicionarioPersonagem,cloneDicionarioTrabalho)
                linhaSeparacao()
            elif not trabalhoERecorrente(dicionarioTrabalho):
                print(f'Recorrencia está desligada.')
                modificaEstadoTrabalho(dicionarioPersonagem,dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO],1)
                linhaSeparacao()
            clickContinuo(12,'up')
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
            break
        else:
            break
    return dicionarioPersonagem

def defineCloneDicionarioTrabalho(dicionarioTrabalho):
    cloneDicionarioTrabalho={CHAVE_ID:None,
                            CHAVE_NOME:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_NOME],
                            CHAVE_ESTADO:1,
                            CHAVE_NIVEL:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_NIVEL],
                            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_PROFISSAO],
                            CHAVE_RARIDADE:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_RARIDADE],
                            CHAVE_RECORRENCIA:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_RECORRENCIA],
                            CHAVE_LICENCA:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_LICENCA]}
                            
    return cloneDicionarioTrabalho

def trabalhoERecorrente(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_RECORRENCIA]

def menuTrabalhosAtuais(menu):
    return menu==menu_trab_atuais

def naoHaRecursosSuficientes(dicionarioTrabalho):
    return verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])==erroSemRecursos

def menuEscolhaEquipamentoReconhecido(menu):
    return menu==menu_esc_equipamento

def menuTrabalhoEspecificoReconhecido(menu):
    return menu==menu_trab_especifico

def naoReconheceMenu(menu):
    return menu==menu_desconhecido

def iniciaProducao(dicionarioTrabalho,dicionarioPersonagem):
    dicionarioPersonagem=entraLicenca(dicionarioPersonagem)
    if chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
        if verificaLicenca(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_LICENCA]):#verifica tipo de licença de produção
            clickEspecifico(1,'f2')#click que definitivamente começa a produção
            dicionarioTrabalho,dicionarioPersonagem=trataErros(dicionarioTrabalho,dicionarioPersonagem)
            # print(f'{D}:CHAVE_CONFIRMACAO depois de sair da função trataErros:{dicionarioTrabalho[CHAVE_CONFIRMACAO]}.')
            linhaSeparacao()
            if chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
                dicionarioPersonagem=trataMenus(dicionarioTrabalho,dicionarioPersonagem)
                if chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
                    erro=verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
                    while erroEncontrado(erro):
                        erro=verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
                    dicionarioTrabalho[CHAVE_LISTA_DESEJO]=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
                    if tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_DESEJO]):
                        dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
                    print(f'Atualizou a CHAVE_LISTA_DESEJO.')
                    linhaSeparacao()
        else:
            dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
            print(f'Erro ao busca licença...')
            linhaSeparacao()
    else:
        print(f'Erro ao entrar na licença...')
        linhaSeparacao()
    return dicionarioTrabalho,dicionarioPersonagem

def retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado):
    if tamanhoIgualZero(listaPersonagemPresenteRecuperado):
        print(f'Limpou a lista...')
        linhaSeparacao()
        listaPersonagemPresenteRecuperado=[]
    nomePersonagemReconhecido=retornaNomePersonagem(0)
    if variavelExiste(nomePersonagemReconhecido):
        print(f'{nomePersonagemReconhecido} foi adicionado a lista!')
        linhaSeparacao()
        listaPersonagemPresenteRecuperado.append(nomePersonagemReconhecido)
    else:#ocorreu algum erro
        print(f'Erro ao reconhecer nome...')
        linhaSeparacao()
    return listaPersonagemPresenteRecuperado

def recebeTodasRecompensas(menu):
    listaPersonagemPresenteRecuperado=retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado=[])
    while True:
        reconheceMenuRecompensa(menu)
        print(f'Lista: {listaPersonagemPresenteRecuperado}.')
        linhaSeparacao()
        deslogaPersonagem(None,None)
        if entraPersonagem(listaPersonagemPresenteRecuperado):
            listaPersonagemPresenteRecuperado=retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado)
        else:
            print(f'Todos os personagens foram verificados!')
            linhaSeparacao()
            break
        menu=retornaMenu()

def recuperaPresente():
    evento=0
    print(f'Buscando recompensa diária...')
    while evento<1:
        telaInteira=retornaAtualizacaoTela()
        metadeAltura=telaInteira.shape[0]//2
        metadeLargura=telaInteira.shape[1]//4
        alturaFrame=80
        y=123
        y=95
        aux=metadeAltura-y
        y=metadeAltura-aux
        larguraFrame=150
        for x in range(8):
            frameTela=telaInteira[y:y+alturaFrame,metadeLargura:metadeLargura+larguraFrame]
            frameTratado=retornaImagemBinarizada(frameTela)
            contadorPixelPreto=np.sum(frameTratado==0)
            # print(f'Contador pixel preto: {contadorPixelPreto}.')
            # mostraImagem(0,frameTratado,None)
            if existemPixelsSuficientes(contadorPixelPreto):
                textoReconhecido=reconheceTexto(frameTratado)
                # mostra_imagem(0,frameTratado,None)
                if variavelExiste(textoReconhecido):
                    print(f'Texto reconhecido: {textoReconhecido}.')
                    if textoEhIgual(textoReconhecido,'pegar'):
                        centroX=metadeLargura+larguraFrame//2
                        centroY=y+alturaFrame//2
                        clickMouseEsquerdo(1,centroX,centroY)
                        posicionaMouseEsquerdo(telaInteira.shape[1]//2,metadeAltura)
                        if verificaErro(None)!=0:
                            evento=2
                            break
                        clickEspecifico(1,'f2')
                        clickContinuo(8,'up')
                        clickEspecifico(1,'left')
                        linhaSeparacao()
                        break
                    elif texto1PertenceTexto2('pegarem',textoReconhecido):
                        clickContinuo(8,'up')
                        clickEspecifico(1,'left')
                        linhaSeparacao()
                        break
                else:
                    print(f'Ocorreu algum erro ao reconhecer presente!')
                    linhaSeparacao()
            y+=80
        evento+=1
    clickEspecifico(2,'f1')

def existemPixelsSuficientes(contadorPixelPreto):
    return contadorPixelPreto>500 and contadorPixelPreto<1100

def reconheceMenuRecompensa(menu):
    print(f'Entrou em recuperaPresente.')
    linhaSeparacao()
    if menu==menu_loja_milagrosa:
        clickEspecifico(1,'down')
        clickEspecifico(1,'enter')
        recuperaPresente()
    elif menu==menu_rec_diarias:
        recuperaPresente()
    else:
        print(f'Recompensa diária já recebida!')
        linhaSeparacao()

def retornaNomePersonagem(posicao):
    nome=None
    print(f'Verificando nome personagem...')
    posicaoNome=[[2,33,169,27],[190,351,177,30]]
    telaInteira=retornaAtualizacaoTela()
    frameNomePersonagem=telaInteira[posicaoNome[posicao][1]:posicaoNome[posicao][1]+posicaoNome[posicao][3],posicaoNome[posicao][0]:posicaoNome[posicao][0]+posicaoNome[posicao][2]]
    frameNomePersonagemTratado=retornaImagemBinarizada(frameNomePersonagem)
    contadorPixelPreto=np.sum(frameNomePersonagemTratado==0)
    # print(f'{D}:{contadorPixelPreto}')
    # mostraImagem(0,frameNomePersonagemTratado,None)
    if contadorPixelPreto>50:
        nomePersonagemReconhecido=reconheceTexto(frameNomePersonagemTratado)
        # print(f'{D}:{nomePersonagemReconhecido}.')
        if variavelExiste(nomePersonagemReconhecido):
            nome=limpaRuidoTexto(nomePersonagemReconhecido)
            # print(f'{D}:Personagem reconhecido: {nomePersonagemReconhecidoTratado}')
            # linhaSeparacao()
        elif contadorPixelPreto>50:
            nome='provisorioatecair'
    return nome

def entraPersonagem(listaPersonagemPresenteRecuperado):
    confirmacao=False
    print(f'Buscando próximo personagem...')
    clickEspecifico(1,'enter')
    time.sleep(1)
    erro=verificaErro(None)
    while erro!=0:
        if erro==5:
            time.sleep(1)
        erro=verificaErro(None)
    else:
        clickEspecifico(1,'f2')
        if len(listaPersonagemPresenteRecuperado)==1:
            clickContinuo(8,'left')
        else:
            clickEspecifico(1,'right')
        nomePersonagem=retornaNomePersonagem(1)               
        while True:
            nomePersonagemPresenteado=None
            for nomeLista in listaPersonagemPresenteRecuperado:
                if nomePersonagem==nomeLista and nomePersonagem!=None:
                    nomePersonagemPresenteado=nomeLista
                    break
            if nomePersonagemPresenteado!=None:
                clickEspecifico(1,'right')
                nomePersonagem=retornaNomePersonagem(1)
            if nomePersonagem==None:
                print(f'Fim da lista de personagens!')
                linhaSeparacao()
                clickEspecifico(1,'f1')
                break
            else:
                clickEspecifico(1,'f2')
                time.sleep(1)
                erro=verificaErro(None)
                while erro!=0:
                    if erro==7:
                        break
                    time.sleep(1.5)
                    erro=verificaErro(None)
                confirmacao=True
                print(f'Login efetuado com sucesso!')
                linhaSeparacao()
                break
    return confirmacao
    
def usa_habilidade():
    #719:752, 85:128 137:180 189:232
    #muda p/ outra janela
    click_atalho_especifico('alt','tab')
    click_atalho_especifico('win','up')
    #cria lista com habilidades a serem usadas
    lista_habilidade = retorna_lista_habilidade_verificada()
    if len(lista_habilidade)==0:
        print(f'Erro!')
        linhaSeparacao()
    else:
        print(f'Buscando referência!')
        linhaSeparacao()
        while True:
            if verificaMenuReferencia():
                #verifica se está em modo de ataque
                if verifica_modo_ataque() or verifica_alvo():
                    #percorre a lista de habilidades
                    for habilidade in lista_habilidade:
                        #atualiza a tela
                        tela_inteira = retornaAtualizacaoTela()
                        #recorta frame na posição da habilidade específica
                        frame_habilidade = tela_inteira[728:728+habilidade[1].shape[0], habilidade[0]:habilidade[0]+habilidade[1].shape[1]]
                        #define o tamanho do frame
                        tamanho_frame_habilidade = frame_habilidade.shape[:2]
                        #define o tamanho do modelo
                        tamanho_modelo = habilidade[1].shape[:2]
                        if verifica_porcentagem_vida() and verificaMenuReferencia():
                            click_especifico_habilidade(1,'t')
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
                                click_especifico_habilidade(1,posicao_habilidade)
                                linhaSeparacao()
                                #verica se a habilidade clicada precisa de click do mouse
                                lista_habilidade_clicada.append(habilidade)
                                if verifica_habilidade_central(lista_habilidade_clicada)!=0:
                                    x,y = retorna_posicao_mouse()
                                    clickMouseEsquerdo(1,x,y)
                                    linhaSeparacao()
                        else:
                            print(f'Modelos com tamanhos diferentes. {tamanho_frame_habilidade}-{tamanho_modelo}')
                            linhaSeparacao()
                posicao_habilidade=verifica_habilidade_central(lista_habilidade)
                if posicao_habilidade!=0:
                    click_especifico_habilidade(1,posicao_habilidade)
                    linhaSeparacao()

def verifica_habilidade_central(lista_habilidade):
    tela_inteira = retornaAtualizacaoTela()
    for indice in range(len(lista_habilidade)):
        habilidade=lista_habilidade[indice]
        for x in range(658,662):
            for y in range(666,670):
                frame_habilidade_central = tela_inteira[y:y+habilidade[1].shape[0],x:x+habilidade[1].shape[1]]
                if frame_habilidade_central.shape[:2]==habilidade[1].shape[:2]:
                    diferenca=cv2.subtract(frame_habilidade_central, habilidade[1])
                    b,g,r=cv2.split(diferenca)
                    # frame_concatenado = retorna_imagem_concatenada(frame_habilidade_central,diferenca)
                    # mostra_imagem(0,frame_concatenado,'Teste')
                    if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                        print(f'Habilidade central encontrada!')
                        # print(f'x: {x}, y: {y}')
                        linhaSeparacao()
                        return retorna_posicao_habilidade(habilidade[0])
                else:
                    print(f'Tamanho do frame diferente do modelo!')
                    linhaSeparacao()
    return 0

def recorta_novo_modelo_habilidade():
    lista_imagem_habilidade = retorna_lista_imagem_habilidade()
    indice = len(lista_imagem_habilidade)
    opcao = input(f'Recortar modelo: nº{indice}? Sim ou não. S/N: ')
    linhaSeparacao()
    while not opcao.isalpha() or (str(opcao).lower().replace('\n','')!='s' and str(opcao).lower().replace('\n','')!='n'):
        print(f'Opção inválida! Recortar modelo: nº {indice}?')
        opcao = input(f'Sim ou não. S/N: ')
        linhaSeparacao()
    else:
        opcao = str(opcao).lower().replace('\n','')
        while opcao!='n':
            atualiza_nova_tela()
            fatia = recortaFrame(f'novo_modelo_habilidade_{indice}')
            lista_imagem_habilidade = retorna_lista_imagem_habilidade()
            indice = len(lista_imagem_habilidade)
            opcao = input(f'Recortar modelo: nº{indice}? Sim ou não. S/N: ')
            linhaSeparacao()
            while not opcao.isalpha() or (str(opcao).lower().replace('\n','')!='s' and str(opcao).lower().replace('\n','')!='n'):
                print(f'Opção inválida! Recortar modelo: nº {indice}?')
                opcao = input(f'Sim ou não. S/N: ')
                linhaSeparacao()
        else:
            print(f'Voltar.')
            linhaSeparacao()

def modifica_quantidade_personagem_ativo():
    nova_quantidade = input(f'Digite a nova quantidade: ')
    linhaSeparacao()
    while not nova_quantidade.isdigit() or int(nova_quantidade)<=0:
        print(f'Quantidade inválida! Tente novamente...')
        nova_quantidade = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        if (muda_quantidade_personagem(dicionarioPersonagem,nova_quantidade)):
            print(f'Quantidade de personagens ativos modificada com sucesso!')
            linhaSeparacao()

def retornaAtualizacaoTela():
    screenshot = tira_screenshot()
    return retorna_imagem_colorida(screenshot)

def trataMenu(menu,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
    if menu==menu_desconhecido:
        pass
    elif menu==menu_trab_atuais:
        estado_trabalho=retornaEstadoTrabalho()
        if estado_trabalho==concluido:
            dicionarioPersonagem=verificaTrabalhoConcluido(dicionarioPersonagem)
        elif estado_trabalho==produzindo:
            # lista_profissao.clear()
            if not dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]:
                print(f'Todos os espaços de produção ocupados.')
                linhaSeparacao()
                dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
            else:
               clickEspecifico(1,'left')
        elif estado_trabalho==0:
            clickEspecifico(1,'left')
    elif menu==menu_rec_diarias or menu==menu_loja_milagrosa:
        recebeTodasRecompensas(menu)
        dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=False
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    elif menu==menu_principal:
        #menu principal
        clickEspecifico(1,'num1')
        clickEspecifico(1,'num7')
    elif menu==menu_personagem:
        #menu personagem
        clickEspecifico(1,'num7')
    elif menu==menu_trab_disponiveis:
        #menu trabalhos disponiveis
        clickEspecifico(1,'up')
        clickEspecifico(2,'left')
    elif menu==menu_trab_especifico:
        #menu trabalho específico
        clickEspecifico(1,'f1')
        clickContinuo(3,'up')
        clickEspecifico(2,'left')
    elif menu==menu_ofe_diaria:
        #menu oferta diária
        clickEspecifico(1,'f1')
    elif menu==menu_inicial:
        #tela principal
        clickEspecifico(1,'f2')
        clickEspecifico(1,'num1')
        clickEspecifico(1,'num7')
    else:
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    erro=verificaErro(None)
    if erro==erroOutraConexao:
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
    return dicionarioPersonagem
    
def configuraLicenca(dicionarioTrabalho):
    if dicionarioTrabalho==None:
        return None
    return dicionarioTrabalho[CHAVE_LICENCA]

def abreCaixaCorreio():
    clickEspecifico(1,'f2')
    clickEspecifico(1,'1')
    clickEspecifico(1,'9')

def verificaCaixaCorreio():
    telaInteira=retornaAtualizacaoTela()
    frameTela=telaInteira[233:233+30,235:235+200]
    print(f'Verificando se possui correspondencia...')
    linhaSeparacao()
    if np.sum(frameTela==255)>0:
        return True
    return False

def retornaConteudoCorrespondencia(dicionarioPersonagem):
    telaInteira=retornaAtualizacaoTela()
    frameTela=telaInteira[231:231+50,168:168+343]
    textoCarta=reconheceTexto(frameTela)
    if textoCarta!=None:
        produto=verificaVendaProduto(textoCarta)
        if produto!=None:
            if produto:
                print(f'Produto vendido:')
                listaTextoCarta=textoCarta.split()
                quantidadeProduto=retornaQuantidadeProdutoVendido(listaTextoCarta)
                # nomeProduto=retornaNomeProdutoVendido(listaTextoCarta)
                frameTela=telaInteira[415:415+30,250:250+260]
                frameTelaTratado=retornaImagemBinarizada(frameTela)
                ouro=reconhece_digito(frameTelaTratado)
                ouro=re.sub('[^0-9]','',ouro)
                if ouro.isdigit():
                    ouro=int(ouro)
                dataAtual=str(datetime.date.today())
                listaTextoCarta=' '.join(listaTextoCarta)
                dicionarioVenda={CHAVE_NOME_PERSONAGEM:dicionarioPersonagem[CHAVE_NOME_PERSONAGEM],
                                 'nomeProduto':listaTextoCarta,
                                 'quantidadeProduto':quantidadeProduto,
                                 'valorProduto':ouro,
                                 'dataVenda':dataAtual}
                adicionaVenda(dicionarioPersonagem,dicionarioVenda)
                # print(dicionarioVenda)
                linhaSeparacao()
            else:
                print(f'Produto expirado:')
                removerPalavras=['a','oferta','de','expirou']
                # print(textoCarta)
                listaTextoCarta=textoCarta.split()
                result = [palavra for palavra in listaTextoCarta if palavra.lower() not in removerPalavras]
                # print(result)
                retorno = ' '.join(result)
                print(retorno)
                linhaSeparacao()
        else:
            print(f'Erro...')

def retornaQuantidadeProdutoVendido(listaTextoCarta):
    x=0
    for texto in listaTextoCarta:
        if 'un' in texto.lower():
            # print(f'un encontrado na posição: {x}, {listaTextoCarta[x]}')
            quantidadeProduto=re.sub('[^0-9]','',listaTextoCarta[x])
            if not quantidadeProduto.isdigit():
                quantidadeProduto=re.sub('[^0-9]','',listaTextoCarta[x-1])
                if quantidadeProduto.isdigit():
                    print(f'Digito encontrado em: {listaTextoCarta[x-1]}')
                else:
                    print(f'Não foi possível reconhecer a quantidade do produto.')
                    linhaSeparacao()
            # else:
                # print(f'Digito encontrado em: {listaTextoCarta[x]}')
            print(f'quantidadeProduto:{quantidadeProduto}')
        x+=1
    return int(quantidadeProduto)

def verificaVendaProduto(texto):
    if 'vendeu'in texto.lower():
        return True
    elif 'expirou'in texto.lower():
        return False
    return None

def recuperaCorrespondencia(dicionarioPersonagem):
    while verificaCaixaCorreio():
        clickEspecifico(1,'enter')
        conteudoCorrespondencia=retornaConteudoCorrespondencia(dicionarioPersonagem)
        clickEspecifico(1,'f2')
    else:
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1,2,35)
        linhaSeparacao()

def existePixelCorrespondencia():
    confirmacao=False
    tela=retornaAtualizacaoTela()
    frameTela=tela[665:690,644:675]
    contadorPixelCorrespondencia=np.sum(frameTela==(173,239,247))
    if contadorPixelCorrespondencia>50:
        print(f'Há correspondencia!')
        confirmacao=True
    else:
        print(f'Não há correspondencia!')
    linhaSeparacao()
    return confirmacao

def percorreFrameItemBolsa():
    # x=168-488=320
    # larguraFrameItem=64
    # y=187-alturaTela
    # alturaFrameItem=64
    x=168
    y=187
    larguraAlturaFrame=64
    telaInteira=retornaAtualizacaoTela()
    contadorItensPercorridos=1
    while True:
        frameNomeItemBolsa=telaInteira[588:588+30,172:172+337]
        frameNomeItemBolsa=retornaImagemBinarizada(frameNomeItemBolsa)
        nomeItemBolsaReconhecido=reconheceTexto(frameNomeItemBolsa)
        print(f'Item: {nomeItemBolsaReconhecido}')
        mostraImagem(0,frameNomeItemBolsa,None)
        if nomeItemBolsaReconhecido==None:
            break
        # frameItemBolsa=telaInteira[y:y+larguraAlturaFrame,x:x+larguraAlturaFrame]
        # frameItemBolsa=retorna_imagem_cinza(frameItemBolsa)
        # quantidadeItemBolsa=reconhece_digito(frameItemBolsa)
        # mostraImagem(0,frameItemBolsa,quantidadeItemBolsa)
        if contadorItensPercorridos%5==0:
            y+=larguraAlturaFrame
            x=168
        else:
            x+=larguraAlturaFrame
        if contadorItensPercorridos>=30:
            y=507
        clickEspecifico(1,'right')
        telaInteira=retornaAtualizacaoTela()
        contadorItensPercorridos+=1

def descobreFrames():
    tela_inteira=retornaAtualizacaoTela()
    alturaTela=tela_inteira.shape[0]
    larguraTela=tela_inteira.shape[1]

    centroAltura=alturaTela//2
    centroMetade=larguraTela//4

    frameMenuNoticias=[30,350]
    frameMenuNoticias=tela_inteira[centroAltura-190:centroAltura-190+frameMenuNoticias[0],centroMetade-(frameMenuNoticias[1]//2):centroMetade+(frameMenuNoticias[1]//2)]
    frameMenuVoltar=[30,100]
    frameMenuVoltar=tela_inteira[centroAltura+225:centroAltura+225+frameMenuVoltar[0],centroMetade-150:centroMetade-150+frameMenuVoltar[1]]
    frameMenuAvancar=[30,130]
    frameMenuAvancar=tela_inteira[centroAltura+225:centroAltura+225+frameMenuAvancar[0],centroMetade+30:centroMetade+30+frameMenuAvancar[1]]
    frameMenuProfissoes=[20,150]
    frameMenuProfissoes=tela_inteira[centroAltura-140:centroAltura-140+frameMenuProfissoes[0],centroMetade-(frameMenuProfissoes[1]//2):centroMetade+(frameMenuProfissoes[1]//2)]
    frameMenuParametros=[30,300]
    frameMenuParametros=tela_inteira[centroAltura-65:centroAltura-65+frameMenuParametros[0],centroMetade-(frameMenuParametros[1]//2):centroMetade+(frameMenuParametros[1]//2)]
    frameMenuProfissional=[30,120]
    frameMenuProfissional=tela_inteira[centroAltura+45:centroAltura+45+frameMenuProfissional[0],centroMetade-(frameMenuProfissional[1]//2):centroMetade+(frameMenuProfissional[1]//2)]
    frameMenuOferta=[30,150]
    frameMenuOferta=tela_inteira[centroAltura-115:centroAltura-115+frameMenuOferta[0],centroMetade-(frameMenuOferta[1]//2):centroMetade+(frameMenuOferta[1]//2)]
    frameMenuInteragir=[30,100]
    frameMenuInteragir=tela_inteira[centroAltura+25:centroAltura+25+frameMenuInteragir[0],centroMetade-(frameMenuInteragir[1]//2):centroMetade+(frameMenuInteragir[1]//2)]
    
    frame_menu_tratado=retornaImagemBinarizada(frameMenuOferta)
    print(reconheceTexto(frame_menu_tratado))
    mostraImagem(0,frameMenuOferta,None)
    # mostra_imagem(0,frameMenuProfissoes,None)
    # mostra_imagem(0,frameMenuVoltar,None)
    # mostra_imagem(0,frameMenuNoticias,None)
    # mostra_imagem(0,frameMenuAvancar,None)
# descobreFrames()

def retornaTextoSair():
    texto=None
    telaInteira=retornaAtualizacaoTela()
    frameTela=telaInteira[telaInteira.shape[0]-50:telaInteira.shape[0]-25,50:50+60]
    frameTelaTratado=retornaImagemBinarizada(frameTela)
    contadorPixelPreto=np.sum(frameTelaTratado==0)
    # print(f'Quantidade de pixels pretos: {contadorPixelPreto}')
    # mostraImagem(0,frameTelaTratado,None)
    if contadorPixelPreto>400 and contadorPixelPreto<430:
        texto=reconheceTexto(frameTelaTratado)
        if variavelExiste(texto):
            texto=limpaRuidoTexto(texto)
    return texto

def retorna_lista_pixel_minimap():
    lista_pixel=[]
    xMapa=568
    yMapa=179
    somaX=1
    somaY=0
    fundo=retorna_fundo_branco()
    telaInteira=retornaAtualizacaoTela()
    for x in range(444):
        lista_pixel.append(telaInteira[yMapa,xMapa])
        if (telaInteira[yMapa,xMapa]==(0,221,255)).all():
            fundo[yMapa-150,xMapa-500]=(0,221,255)
        else:
            fundo[yMapa-150,xMapa-500]=(0,0,0)
        if x>=110 and x<221:
            somaX=0
            somaY=1
        elif x>=221 and x<332:
            somaX=-1
            somaY=0
        elif x>=332:
            somaX=0
            somaY=-1
        xMapa=xMapa+somaX
        yMapa=yMapa+somaY
    mostraImagem(0,fundo,'Minimapa')
    return lista_pixel

def encontraMercador():
    # cor mercador:432
    telaInteira=retornaAtualizacaoTela()
    quantidadeLinhas=1
    contadorCorMercador=0
    for y in range(31,telaInteira.shape[0],24):
        print(f'Linhas: {quantidadeLinhas}')
        if y+46>telaInteira.shape[0]:
            continue
        for x in range(0,telaInteira.shape[1]//2,24):
            if x+46>telaInteira.shape[1]//2:
                quantidadeLinhas+=1
                continue
            frameTela=telaInteira[y:y+46,x:x+46]
            mostraImagem(300,frameTela,None)
            for yFrame in range(0,frameTela.shape[0]):
                for xFrame in range(0,frameTela.shape[1]):
                    if (frameTela[yFrame,xFrame]==(51,51,187)).all():
                        contadorCorMercador+=1
            if contadorCorMercador==104:
                print(f'Debug - Frame icone mercador encontrado!')
                linhaSeparacao()
                mostraImagem(0,frameTela,None)
                # return frameTela

def salva_imagem_envia_servidor():
    tela_inteira = retornaAtualizacaoTela()
    imagem_trabalho = tela_inteira[273:273+311,167:167+347]
    cv2.imwrite('imagem_trabalho.png', imagem_trabalho)

def salva_imagem():
    tela_inteira = retornaAtualizacaoTela()
    imagem_trabalho = tela_inteira[486:486+45,181:181+43]
    cv2.imwrite('imagem_produzir.png', imagem_trabalho)

def verifica_valor_numerico(valor):
    return valor.isdigit()

def verifica_valor_alfabetico(valor):
    return valor.isalpha()

def linhaSeparacao():
    print(f'____________________________________________________')

def entra_usuario():
    email = input(f'Email: ')
    senha = input(f'Senha: ')
    if autenticar_usuario(email,senha):
        return True
    return False
    
def deleta_item_lista():
    lista=['a','b','c']
    print(f'{lista}')
    item=int(input(f'Deletar: '))
    del lista[item]
    print(f'{lista}')

def funcao_teste(dicionarioUsuario):
    dicionarioTrabalho={CHAVE_LICENCA:None}
    dicionarioPersonagem={CHAVE_ID_USUARIO:dicionarioUsuario[CHAVE_ID_USUARIO],
                          CHAVE_ID_PERSONAGEM:dicionarioUsuario[CHAVE_ID_PERSONAGEM],
                          CHAVE_NOME_PERSONAGEM:'Nome teste',
                          CHAVE_LISTA_PROFISSAO_MODIFICADA:False}
    listaPersonagem=[dicionarioPersonagem[CHAVE_ID_PERSONAGEM]]
    while input(f'Continuar?')!='n':
        click_atalho_especifico('alt','tab')
        # texto_menu=retornaTextoMenuReconhecido(26,1,100)
        # verificaErro(dicionarioTrabalho)
        # dicionarioTrabalho[CHAVE_PROFISSAO]='armaduradetecido'
        # dicionarioTrabalho[CHAVE_LISTA_DESEJO]=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
        # dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=defineListaDicionarioPersonagem(dicionarioUsuario)
        # dicionarioPersonagem=defineListaDicionarioPersonagemAtivo(dicionarioPersonagem)
        # dicionarioPersonagemReconhecido=verificaNomePersonagemAtivoReconhecido(dicionarioPersonagem)
        # retornaTipoErro()
        # telaInteira=retornaAtualizacaoTela()
        # frameTela=telaInteira[263:263+46,284:284+46]
        # contadorCorMercador=0
        # for yFrame in range(0,frameTela.shape[0]):
        #     for xFrame in range(0,frameTela.shape[1]):
        #         if (frameTela[yFrame,xFrame]==(51,51,187)).all():
        #                 contadorCorMercador+=1
        # print(contadorCorMercador)
        # adicionaAtributoRecorrencia(dicionarioPersonagem)
        # mostra_imagem(0,frameTela,None)
        # encontraMercador()
        # print(texto_menu)
        # deleta_item_lista()
        # print(verificaCaixaCorreio())
        # dataAtual=datetime.date.today()
        # print(dataAtual.ctime())
        percorreFrameItemBolsa()
        # dicionarioPersonagens=retornaDicionarioPersonagens(dicionarioUsuario)
        # listaDicionarioPersonagensAtivos=retornaListaDicionarioPersonagensAtivos(dicionarioPersonagens)
        # print(f'Lista dicionarios personagem ativo: {listaDicionarioPersonagensAtivos}.')
        # linhaSeparacao()
        # dicionarioPrimeiroPersonagem=listaDicionarioPersonagensAtivos[0]
        # print(dicionarioPrimeiroPersonagem)
        # linhaSeparacao()
        # retornaConteudoCorrespondencia(dicionarioPersonagem)
        # click_atalho_especifico('win','up')
        # lista_personagem_ativo = consulta_lista_personagem(usuario_id)
        # busca_lista_personagem_ativo(lista_personagem_ativo)
        # while not loga_personagem('caah.rm15@gmail.com','aeioukel'):
        #     continue
        # verifica_producao_recursos('Licença de produção do aprendiz')
        # click_continuo(9,'up')
        # recupera_trabalho_concluido(dicionarioPersonagem)
        # while True:
        # atualiza_nova_tela()
        # click_continuo(8,'up')
        # confirma_nome_trabalho('Melhorar licença comum',1)
        #     menu=retorna_menu()
        #     if menu!=11:
        #         trata_menu(menu,dicionarioPersonagem)
        #     break
        # print('Fim')
        # lista_habilidade = retorna_lista_habilidade_verificada()
        # lista_ativos = consulta_lista_personagem(usuario_id)
        # print(lista_ativos)
        # modifica_quantidade_personagem_ativo()
        # while True:
        #     verifica_habilidade_central(lista_habilidade)
        # print(retorna_licenca_reconhecida())
        # print(verifica_licenca('principiante'))
        # linhaSeparacao()
        # valor=True
        # while input(f'Continuar?')=='s':
        #     if valor:
        #         uso={'uso':1}
        #         valor=False
        #     else:
        #         uso={'uso':0}
        #         valor=True
        #     mudaAtributoPersonagem(usuario_id,listaPersonagem,'espacoProducao',valor)
        # if verifica_menu_referencia():
        #     print('Achei!')
        # else:
        #     print('Não achei...')
        # retorna_tipo_erro()
        # dicionarioPersonagem=retorna_lista_profissao_verificada(dicionarioPersonagem)
        # atualiza_lista_profissao(dicionarioPersonagem)
            # retornaMenu()
        # verificaPixelCorrespondencia()
        # dicionarioPersonagem={CHAVE_ID_PERSONAGEM:personagem_id_global,CHAVE_ESPACO_PRODUCAO:True,CHAVE_UNICA_CONEXAO:True}
        # print(dicionarioPersonagem[CHAVE_UNICA_CONEXAO])
        # adicionar_profissao(personagem_id_global,'Teste')
        # trabalho = 'trabalhoid','Apêndice de jade ofuscada','profissaoteste','comum','Licença de produção do iniciante'
        # inicia_producao(trabalho,dicionarioPersonagem)
        # verifica_trabalho_comum(trabalho,'profissaoteste')
        # while inicia_busca_trabalho():
        #     continue
        # recuperaPresente()
        # print(retornaTextoSair())
        # entra_personagem_ativo('mrninguem')
        # inicia_busca_trabalho()
        # retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
        # dicionarioTrabalho=defineListaDicionariosTrabalhosPriorizados(dicionarioTrabalho)
        # confirmaNomeTrabalho(dicionarioTrabalho,1)
        click_atalho_especifico('alt','tab')
# entra_personagem_ativo('Raulssauro')
# recebeTodasRecompensas(menu)
# entraPersonagem(['tobraba','gunsa','totiste'])
# entra_personagem_ativo('tobraba')
# busca_lista_personagem_ativo_teste()
