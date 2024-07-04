import cv2
import numpy as np
from metodos.manipula_imagem import *
from metodos.manipula_teclado import *
from metodos.manipula_cliente import *
from metodos.Utilitarios import *
from metodos.lista_chaves import *
import metodos.lista_chaves as LC
from modelos.objetoTrabalho import Trabalho
import time
import datetime
import os.path
import re

xinicial=181
xfinal = 228
yinicial = 295
yfinal = 342
yinicial_nivel = 285
yfinal_nivel = 285 + 69

cont_voltas = 0
altura_frame = 70
porcentagem_vida = 25

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
erroConexaoInterrompida=13
erroSemMoedas=14
erroEmailSenhaIncorreta=15
erroTempoProducaoExpirou=16
erroReinoIndisponivel=17
erroAtualizaJogo=18
erroRestaurandoConexao=19
erroUsarObjetoParaProduzir=20
erroSemEspacosBolsa=21
erroSairWarspear = 22

lista_personagem_ativo=[]

tela = 'atualizacao_tela.png'

dicionarioPersonagemAtributos = {}

def atualiza_nova_tela():
    imagem = tiraScreenshot()
    salvaNovaTela(imagem)
    print(f'Atualizou a tela.')
    linhaSeparacao()

def atualizaListaProfissao():
    global dicionarioPersonagemAtributos
    print(f'Atualizando lista de profissões...')
    linhaSeparacao()
    listaProfissaoReconhecida = defineListaProfissaoReconhecida()
    if len(listaProfissaoReconhecida) == CHAVE_QUANTIDADE_PROFISSAO:
        verificaProfissao(listaProfissaoReconhecida)
        dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = False
        print(f'Processo de verificação concluído com sucesso!')
    else:
        print(f'Erro ao definir lista de profissões reconhecidas.')

def verificaEspacoProducao():
    global dicionarioPersonagemAtributos
    quantidadeEspacoProducao = retornaQuantidadeEspacosDeProducao()
    caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/.json'
    dados = {CHAVE_ESPACO_PRODUCAO: quantidadeEspacoProducao}
    if CHAVE_ESPACO_PRODUCAO in dicionarioPersonagemAtributos:
        if type(dicionarioPersonagemAtributos[CHAVE_ESPACO_PRODUCAO]) == bool:
            modificaAtributo(caminhoRequisicao, dados)
        else:
            if dicionarioPersonagemAtributos[CHAVE_ESPACO_PRODUCAO] != quantidadeEspacoProducao:
                modificaAtributo(caminhoRequisicao, dados)
    else:
        modificaAtributo(caminhoRequisicao, dados)
    dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO] = quantidadeEspacoProducao

def verificaProfissao(listaProfissaoReconhecida):
    global dicionarioPersonagemAtributos
    listaDicionariosProfissoes = dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]
    for posicao in range(len(listaProfissaoReconhecida)):
        if textoEhIgual(listaProfissaoReconhecida[posicao],listaDicionariosProfissoes[posicao][CHAVE_NOME]):
            continue
        else:
            posicaoDicionarioAux2 = retornaPosicaoDicionarioAux2(listaProfissaoReconhecida[posicao])
            dicionarioAux1 = listaDicionariosProfissoes[posicao]
            if posicaoDicionarioAux2 != -1:
                dicionarioAux2 = listaDicionariosProfissoes[posicaoDicionarioAux2]
                dados = {
                    CHAVE_NOME:dicionarioAux2[CHAVE_NOME],
                    CHAVE_EXPERIENCIA:dicionarioAux2[CHAVE_EXPERIENCIA],
                    CHAVE_PRIORIDADE:dicionarioAux2[CHAVE_PRIORIDADE]}
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioAux1[CHAVE_ID]}/.json'
                modificaAtributo(caminhoRequisicao,dados)
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicao][CHAVE_NOME] = dicionarioAux2[CHAVE_NOME]
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicao][CHAVE_EXPERIENCIA] = dicionarioAux2[CHAVE_EXPERIENCIA]
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicao][CHAVE_PRIORIDADE] = dicionarioAux2[CHAVE_PRIORIDADE]
                dados = {
                    CHAVE_NOME:dicionarioAux1[CHAVE_NOME],
                    CHAVE_EXPERIENCIA:dicionarioAux1[CHAVE_EXPERIENCIA],
                    CHAVE_PRIORIDADE:dicionarioAux1[CHAVE_PRIORIDADE]}
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioAux2[CHAVE_ID]}/.json'
                modificaAtributo(caminhoRequisicao,dados)
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicaoDicionarioAux2][CHAVE_NOME] = dicionarioAux1[CHAVE_NOME]
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicaoDicionarioAux2][CHAVE_EXPERIENCIA] = dicionarioAux1[CHAVE_EXPERIENCIA]
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicaoDicionarioAux2][CHAVE_PRIORIDADE] = dicionarioAux1[CHAVE_PRIORIDADE]
                verificaProfissao(listaProfissaoReconhecida)
                break

def retornaPosicaoDicionarioAux2(profissaoReconhecida):
    for posicao in range (len(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO])):
        if textoEhIgual(profissaoReconhecida, dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO][posicao][CHAVE_NOME]):
            return posicao
    return -1

def defineListaProfissaoReconhecida():
    yinicialProfissao=285
    listaProfissaoReconhecida=[]
    for x in range(CHAVE_QUANTIDADE_PROFISSAO):
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
            listaProfissaoReconhecida.append(profissaoReconhecida)
            yinicialProfissao+=70
        else:
            print(f'Processo interrompido!')
            break
    else:
        clickContinuo(10,'up')
        print(f'Processo de reconhecimento concluído!')
    return listaProfissaoReconhecida

def ehMaisQueQuartaVerificacao(x):
    return x>4

def ehQuartaVerificacao(x):
    return x==4

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
            experiencia = input(f'Experiência: ')
            print(f'Confirma novo trabalho:(S/N)?')
            confirmaTrabalho=input(f'Escolha: ')
            if confirmaTrabalho.replace(' ','').lower()=='s':
                dicionarioTrabalho={
                    CHAVE_NOME:nome,
                    CHAVE_PROFISSAO:profissao[CHAVE_NOME],
                    CHAVE_RARIDADE:raridade,
                    CHAVE_NIVEL:nivel,
                    CHAVE_EXPERIENCIA:int(experiencia)}
                # # print(f'{D}:dicionarioTrablho{dicionarioTrabalho}.')
                linhaSeparacao()
                cadastraNovoTrabalho(dicionarioTrabalho)
        else:
            print(f'Nome vazio!')
            linhaSeparacao()
        confirmacao=input(f'Cadastra novo trabalho:(S/N)?')

def detectaMovimento():
    detec = []
    print(f'Atualizou o background.')
    backgroud = retornaBackGround()
    referenciaAnterior1, referenciaAnterior2 = retornaReferencias()
    while True:
        if not verificaReferenciaTela(referenciaAnterior1, referenciaAnterior2):
            print(f'Atualizou o background.')
            backgroud = retornaBackGround()
        telaInteira = retornaAtualizacaoTela()
        alturaTela = telaInteira.shape[0]
        frameTela = telaInteira[0:alturaTela,0:674]
        frameTela = cv2.resize(frameTela,(0,0),fx=0.9,fy=0.9)
        frameTelaCinza = cv2.cvtColor(frameTela,cv2.COLOR_BGR2GRAY)
        frameTelaBorado = cv2.GaussianBlur(frameTelaCinza,(3,3),5)
        bgFrame = backgroud.apply(frameTelaBorado)
        frameTelaDilatado = cv2.dilate(bgFrame,np.ones((5,5)))
        nucleo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        dilatado = cv2.morphologyEx(frameTelaDilatado,cv2.MORPH_CLOSE,nucleo)

        contorno, imagem = cv2.findContours(dilatado, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for (i, c) in enumerate(contorno):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = (w >= 40) and (h >= 40)
            if not validar_contorno:
                continue
            cv2.rectangle(frameTela, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frameTela, centro, 4, (0, 0, 255), -1)

        referenciaAnterior1, referenciaAnterior2 = retornaReferencias()
        cv2.imshow('Teste',dilatado)
        cv2.imshow('Teste2',frameTela)
        print(centro)
        # clickMouseEsquerdo(1,centro[0],centro[1])
        frame_nome_objeto = frameTela[32:32+30,frameTela.shape[1]-164:frameTela.shape[1]]
        # nome_objeto_reconhecido=reconheceTexto(frame_nome_objeto)
        # print(f'Nome reconhecido: {nome_objeto_reconhecido}')
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.3)
    cv2.destroyAllWindows()

def mostraLista(listaDicionarios):
    x = 1
    for dicionario in listaDicionarios:
        print(f'{x} - {dicionario[CHAVE_NOME]}.')
        x += 1
    print(f'0 - Voltar\n')

def mostraListaDesejo(dicionarioUsuario):
    dicionarioUsuario = defineChaveListaDicionariosTrabalhosDesejados(dicionarioUsuario)
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DESEJO]):
        dicionarioUsuario[CHAVE_LISTA_DESEJO] = sorted(dicionarioUsuario[CHAVE_LISTA_DESEJO],key=lambda dicionario:(dicionario[CHAVE_PROFISSAO],dicionario[CHAVE_RARIDADE],dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
        print(f'{"Nível".ljust(5)}|{"Raridade".ljust(10)}|{"Profissão".ljust(22)}|{"Nome".ljust(45)}|{"Trabalho necessário"}')
        for trabalhoDesejado in dicionarioUsuario[CHAVE_LISTA_DESEJO]:
            if estadoTrabalhoEParaProduzir(trabalhoDesejado):
                trabalhoNecessario = 'Indefinido' if not CHAVE_TRABALHO_NECESSARIO in trabalhoDesejado else trabalhoDesejado[CHAVE_TRABALHO_NECESSARIO]
                print(f'{str(trabalhoDesejado[CHAVE_NIVEL]).ljust(5)}|{trabalhoDesejado[CHAVE_RARIDADE].ljust(10)}|{trabalhoDesejado[CHAVE_PROFISSAO].ljust(22)}|{trabalhoDesejado[CHAVE_NOME].ljust(45)}|{trabalhoNecessario}')
        linhaSeparacao()
    else:
        print(f'A lista está vazia.')
        linhaSeparacao()
    return dicionarioUsuario

def mostraListaDesejoComIndice(dicionarioUsuario):
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DESEJO]):
        dicionarioUsuario[CHAVE_LISTA_DESEJO] = sorted(dicionarioUsuario[CHAVE_LISTA_DESEJO],key=lambda dicionario:(dicionario[CHAVE_ESTADO],dicionario[CHAVE_PROFISSAO],dicionario[CHAVE_RARIDADE],str(dicionario[CHAVE_NIVEL]),dicionario[CHAVE_NOME]))
        print(f'{"Índice".ljust(6)}|{"Nível".ljust(5)}|{"Raridade".ljust(10)}|{"Profissão".ljust(22)}|{"Estado".ljust(11)}|{"Nome"}')
        indice = 1
        for trabalhoDesejado in dicionarioUsuario[CHAVE_LISTA_DESEJO]:
            estadoProducao = 'Aguardando' if trabalhoDesejado[CHAVE_ESTADO] == 0 else 'Produzindo' if trabalhoDesejado[CHAVE_ESTADO] == 1 else 'Pronto'
            print(f'{str(indice).ljust(6)}|{str(trabalhoDesejado[CHAVE_NIVEL]).ljust(5)}|{trabalhoDesejado[CHAVE_RARIDADE].ljust(10)}|{trabalhoDesejado[CHAVE_PROFISSAO].ljust(22)}|{estadoProducao.ljust(11)}|{trabalhoDesejado[CHAVE_NOME]}')
            indice += 1
        print(f'{"0".ljust(6)}|"Voltar"')
        linhaSeparacao()
    else:
        print(f'A lista está vazia.')
        linhaSeparacao()

def verifica_lista_inimigo(nome_reconhecido):
    lista_inimigos = ['Sombradapodridãofuriosa','Mineradorlouco','Lobocego','adecãoebuliente','Chamadasprofundezas','Párialouco','Harpialadra','Sombradapodridão','Goblinmestreminério','ChifraçoAncião']
    for indice in range(len(lista_inimigos)):
        if lista_inimigos[indice]==nome_reconhecido:
            print(f'Encontrou: {lista_inimigos[indice]}')
            return True
    return False

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

def retornaEstadoTrabalho():
    estadoTrabalho=CODIGO_PARA_PRODUZIR
    #icone do primeiro espaço de produç 181,295 228,342
    telaInteira=retornaAtualizacaoTela()
    frameTelaInteira=telaInteira[311:311+43, 233:486]
    texto=reconheceTexto(frameTelaInteira)
    if variavelExiste(texto):
        if textoEhIgual("pedidoconcluído",texto):
            print(f'Pedido concluído!')
            estadoTrabalho=CODIGO_CONCLUIDO
        elif texto1PertenceTexto2('adicionarnovo',texto):
            print(f'Nem um trabalho!')
            estadoTrabalho=CODIGO_PARA_PRODUZIR
        else:
            print(f'Em produção...')
            estadoTrabalho=CODIGO_PRODUZINDO
    else:
        print(f'Ocorreu algum erro ao verificar o espaço de produção!')
    linhaSeparacao()
    return estadoTrabalho

def verificaLicenca(dicionarioTrabalho, dicionarioPersonagem):
    confirmacao = False
    if variavelExiste(dicionarioTrabalho):
        print(f"Buscando: {dicionarioTrabalho[CHAVE_LICENCA]}")
        linhaSeparacao()
        textoReconhecido = retornaLicencaReconhecida()
        if variavelExiste(textoReconhecido) and variavelExiste(dicionarioTrabalho[CHAVE_LICENCA]):
            print(f'Licença reconhecida: {textoReconhecido}.')
            linhaSeparacao()
            if not texto1PertenceTexto2('licençasdeproduçao', textoReconhecido):
                primeiraBusca = True
                listaCiclo = []
                while not texto1PertenceTexto2(textoReconhecido, dicionarioTrabalho[CHAVE_LICENCA]):
                    clickEspecifico(1, "right")
                    listaCiclo.append(textoReconhecido)
                    textoReconhecido = retornaLicencaReconhecida()
                    if variavelExiste(textoReconhecido):
                        print(f'Licença reconhecida: {textoReconhecido}.')
                        linhaSeparacao()
                        if texto1PertenceTexto2('nenhumitem', textoReconhecido) or len(listaCiclo) > 10:
                            if textoEhIgual(dicionarioTrabalho[CHAVE_LICENCA], 'Licença de produção do iniciante')and primeiraBusca:
                                break
                            dicionarioTrabalho[CHAVE_LICENCA] = 'Licença de produção do iniciante'
                            print(f'Licença para trabalho agora é: {dicionarioTrabalho[CHAVE_LICENCA]}.')
                            linhaSeparacao()
                            listaCiclo = []
                    else:
                        print(f'Erro ao reconhecer licença!')
                        linhaSeparacao()
                        break
                    primeiraBusca = False
                else:#se encontrou a licença buscada
                    if primeiraBusca:
                        clickEspecifico(1, "f1")
                    else:
                        clickEspecifico(1, "f2")
                    confirmacao = True
            else:
                print(f'Sem licenças de produção...')
                clickEspecifico(1, 'f1')
                listaPersonagem = [dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
                modificaAtributoPersonagem(dicionarioPersonagem, listaPersonagem, CHAVE_ESTADO, False)
                linhaSeparacao()
        else:
            print(f'Erro ao reconhecer licença!')
            linhaSeparacao()
    return confirmacao, dicionarioTrabalho

def retornaLicencaReconhecida():
    licencaRetornada=None
    listaLicencas=['iniciante','principiante','aprendiz','mestre','nenhumitem','licençasdeproduçao']
    telaInteira=retornaAtualizacaoTela()
    frameTela=telaInteira[275:317,169:512]
    frameTelaCinza=retornaImagemCinza(frameTela)
    frameTelaEqualizado=retornaImagemEqualizada(frameTelaCinza)
    textoReconhecido=reconheceTexto(frameTelaEqualizado)
    # print(f'{D}:{textoReconhecido}.')
    # linhaSeparacao()
    # mostraImagem(0,frameTelaEqualizado,textoReconhecido)
    if variavelExiste(textoReconhecido):
        for licenca in listaLicencas:
            if texto1PertenceTexto2(licenca,textoReconhecido):
                return textoReconhecido
    return licencaRetornada
    
def verifica_ciclo(lista):
    if len(lista)>=4:
        if lista[0]==lista[-1]:
            return True
    return False

def confirmaNomeTrabalho(dicionarioTrabalho, tipoTrabalho):
    print(f'Confirmando nome do trabalho...')
    frameTelaTrabalhoEspecifico = retornaAtualizacaoTela()
    if  tipoTrabalho == 0:
        frameTelaTrabalhoEspecifico = retornaFrameTelaTrabalhoEspecifico()
    listaFrames = [[169, 280, 303, 33], [183, 195, 318, 31]]
    posicao = listaFrames[tipoTrabalho]
    frameNomeTrabalho = frameTelaTrabalhoEspecifico[posicao[1]:posicao[1] + posicao[3], posicao[0]:posicao[0] + posicao[2]]
    frameNomeTrabalhoTratado = retornaImagemCinza(frameNomeTrabalho)
    frameNomeTrabalhoTratado = retornaImagemBinarizada(frameNomeTrabalho)
    nomeTrabalhoReconhecido = reconheceTexto(frameNomeTrabalhoTratado)
    if variavelExiste(nomeTrabalhoReconhecido) and CHAVE_LISTA_DESEJO_PRIORIZADA in dicionarioTrabalho:
        for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
            if CHAVE_NOME_PRODUCAO in dicionarioTrabalhoDesejado:
                nomeTrabalhoDesejado = dicionarioTrabalhoDesejado[CHAVE_NOME].replace('-','')
                nomeProducaoTrabalhoDesejado = dicionarioTrabalhoDesejado[CHAVE_NOME_PRODUCAO].replace('-','')
                if len(dicionarioTrabalhoDesejado[CHAVE_NOME]) > 30:
                    nomeTrabalhoDesejado = nomeTrabalhoDesejado[0:30]
                if len(dicionarioTrabalhoDesejado[CHAVE_NOME_PRODUCAO]) > 30:
                    nomeProducaoTrabalhoDesejado = nomeProducaoTrabalhoDesejado[0:30]
                trabalhoDesejadoNaoEhProducaoRecursosENomeEhIgualAoReconhecidoOuNomeProducaoEhIgualAoReconhecido = (
                    not trabalhoEhProducaoRecursos(dicionarioTrabalhoDesejado)
                    and (textoEhIgual(nomeTrabalhoReconhecido, nomeTrabalhoDesejado)
                    or textoEhIgual(nomeTrabalhoReconhecido, nomeProducaoTrabalhoDesejado)))
                if trabalhoDesejadoNaoEhProducaoRecursosENomeEhIgualAoReconhecidoOuNomeProducaoEhIgualAoReconhecido:
                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoDesejado
                    print(f'Trabalho confirmado: {nomeTrabalhoReconhecido}!')
                    return dicionarioTrabalho
                else:
                    if texto1PertenceTexto2(nomeTrabalhoReconhecido[3:-2], nomeProducaoTrabalhoDesejado):
                        dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoDesejado
                        print(f'Trabalho confirmado: {nomeTrabalhoReconhecido}!')
                        return dicionarioTrabalho
        else:
            print(f'Trabalho negado: {nomeTrabalhoReconhecido}!')
    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = None
    return dicionarioTrabalho

def retornaFrameTelaTrabalhoEspecifico():
    clickEspecifico(1, 'down')
    clickEspecifico(1, 'enter')
    telaInteira = retornaAtualizacaoTela()
    clickEspecifico(1, 'f1')
    clickEspecifico(1, 'up')
    return telaInteira

def retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade):
    listaDicionariosTrabalhosDesejados = []
    listaDesejos = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    print(f'Buscando trabalho {raridade} na lista...')
    for trabalhoDesejado in listaDesejos:
        raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir = (
            textoEhIgual(trabalhoDesejado[CHAVE_RARIDADE], raridade)
            and textoEhIgual(trabalhoDesejado[CHAVE_PROFISSAO], dicionarioTrabalho[CHAVE_PROFISSAO])
            and trabalhoDesejado[CHAVE_ESTADO] == CODIGO_PARA_PRODUZIR)
        if raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir:
            for dicionarioTrabalhoDesejado in listaDicionariosTrabalhosDesejados:
                if textoEhIgual(dicionarioTrabalhoDesejado[CHAVE_NOME], trabalhoDesejado[CHAVE_NOME]):
                    break
            else:
                print(f'Trabalho {raridade} encontado: {trabalhoDesejado[CHAVE_NOME]}.')
                listaDicionariosTrabalhosDesejados.append(trabalhoDesejado)
    if tamanhoIgualZero(listaDicionariosTrabalhosDesejados):
        print(f'Nem um trabaho {raridade} na lista!')
        linhaSeparacao()
    else:
        for dicionarioTrabalhoDesejado in listaDicionariosTrabalhosDesejados:
            if not trabalhoEhProducaoRecursos(dicionarioTrabalhoDesejado):
                dicionarioTrabalhoDesejado[CHAVE_PRIORIDADE] = 1
            else:
                dicionarioTrabalhoDesejado[CHAVE_PRIORIDADE] = 2
        linhaSeparacao()
    return listaDicionariosTrabalhosDesejados

def retornaListaDicionariosTrabalhosBuscados(listaDicionariosTrabalhos,profissao,raridade):
    listaDicionariosTrabalhosBuscados=[]
    listaDicionariosTrabalhosBuscadosOrdenados=[]
    for dicionarioTrabalho in listaDicionariosTrabalhos:
        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO],profissao)and
            textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE],raridade)):
            listaDicionariosTrabalhosBuscados.append(dicionarioTrabalho)
    listaDicionariosTrabalhosBuscadosOrdenados=sorted(listaDicionariosTrabalhosBuscados,key=lambda dicionario:(dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
    return listaDicionariosTrabalhosBuscadosOrdenados

def defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho):
    print(f'Buscando trabalho {dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA][0][CHAVE_RARIDADE]}.')
    contadorParaBaixo = 0
    if not primeiraBusca(dicionarioTrabalho):
        contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO]
        clickEspecifico(contadorParaBaixo, 'down')
    while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
        erro = verificaErro(dicionarioTrabalho)
        if erroEncontrado(erro):
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
            break
        if primeiraBusca(dicionarioTrabalho):
            clicks = 3
            contadorParaBaixo = 3
            clickEspecifico(clicks, 'down')
            yinicialNome = (2 * 70) + 285
            nomeTrabalhoReconhecido = retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        elif contadorParaBaixo == 3:
            yinicialNome = (2 * 70) + 285
            nomeTrabalhoReconhecido = retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        elif contadorParaBaixo == 4:
            yinicialNome = (3 * 70) + 285
            nomeTrabalhoReconhecido = retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        elif contadorParaBaixo > 4:
            nomeTrabalhoReconhecido = retornaNomeTrabalhoReconhecido(530, 1)
        if variavelExiste(nomeTrabalhoReconhecido):
            print(f'Trabalho reconhecido: {nomeTrabalhoReconhecido}')
            for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
                print(f'Trabalho na lista: {dicionarioTrabalhoDesejado[CHAVE_NOME]}')
                if texto1PertenceTexto2(nomeTrabalhoReconhecido, dicionarioTrabalhoDesejado[CHAVE_NOME_PRODUCAO]):
                    clickEspecifico(1, 'enter')
                    dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoDesejado
                    contadorParaBaixo += 1
                    linhaSeparacao()
                    tipoTrabalho = 0
                    if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]):
                        tipoTrabalho = 1
                    dicionarioTrabalho = confirmaNomeTrabalho(dicionarioTrabalho, tipoTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                        break
                    else:
                        clickEspecifico(1, 'f1')
            else:
                linhaSeparacao()
                clickEspecifico(1, 'down')
                dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                contadorParaBaixo += 1
        else:
            if not primeiraBusca(dicionarioTrabalho) and dicionarioTrabalho[CHAVE_POSICAO] > 5:
                # dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                print(f'Trabalho {dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA][0][CHAVE_RARIDADE]} não reconhecido!')
                linhaSeparacao()
                break
            else:
                linhaSeparacao()
                clickEspecifico(1, 'down')
                dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                contadorParaBaixo += 1
    return dicionarioTrabalho

def vaiParaMenuTrabalhoEmProducao():
    clickEspecifico(1,'f1')
    clickContinuo(9,'up')
    clickEspecifico(1,'left')

def vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho):
    print(f'{D}: Voltando para o topo da lista!')
    clickContinuo(dicionarioTrabalho[CHAVE_POSICAO]+5,'up')
    linhaSeparacao()

def vaiParaMenuProduzir():
    global dicionarioPersonagemAtributos
    erro = verificaErro(None)
    if not erroEncontrado(erro):
        menu = retornaMenu()
        if estaMenuInicial(menu):
            if existePixelCorrespondencia():
                vaiParaMenuCorrespondencia()
                recuperaCorrespondencia()
        while naoEstiverMenuProduzir(menu):
            trataMenu(menu)
            if not chaveConfirmacaoForVerdadeira(dicionarioPersonagemAtributos):
                break
            menu = retornaMenu()
        else:
            return True
    elif existeOutraConexao(erro):
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
    return False

def retornaNomeTrabalhoReconhecido(yinicialNome, identificador):
    time.sleep(1)
    altura = 34
    if identificador == 1:
        altura = 68
    telaInteira = retornaAtualizacaoTela()
    frameTelaInteira = telaInteira[yinicialNome:yinicialNome + altura, 233:478]
    frameNomeTrabalhoTratado = retornaImagemCinza(frameTelaInteira)
    frameNomeTrabalhoTratado = retornaImagemBinarizada(frameNomeTrabalhoTratado)
    if np.sum(frameNomeTrabalhoTratado == 0) > 0:
        return reconheceTexto(frameNomeTrabalhoTratado)
    return None

def verificaErro(dicionarioTrabalho):
    dicionarioTrabalho = configuraLicenca(dicionarioTrabalho)
    time.sleep(0.5)
    print(f'Verificando erro...')
    erro=retornaTipoErro()
    if erro==erroPrecisaLicenca or erro==erroFalhaConectar or erro==erroConexaoInterrompida or erro==erroManutencaoServidor or erro==erroReinoIndisponivel:
        clickEspecifico(2,"enter")
        if erro==erroPrecisaLicenca:
            verificaLicenca(None,None)
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
        clickEspecifico(2,'f1')
        clickContinuo(9,'up')
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
    elif (erro==erroReceberRecompensas or erro==erroAtualizaJogo or erro==erroUsarObjetoParaProduzir
          or erro == erroSairWarspear):
        clickEspecifico(1,'f2')
        if erro==erroReceberRecompensas:
            print(f'Recuperar presente.')
        elif erro==erroUsarObjetoParaProduzir:
            print(f'Usa objeto para produzir outro.')
        elif erro==erroSairWarspear:
            print(f'Sair do jogo.')
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
    dicionarioPersonagem[CHAVE_CONFIRMACAO] = False
    erro = verificaErro(None)
    if not erroEncontrado(erro):
        dicionarioPersonagem[CHAVE_CONFIRMACAO] = True
        clickEspecifico(1, 'up')
        clickEspecifico(1, 'enter')
    elif erro == erroOutraConexao:
        dicionarioPersonagem[CHAVE_UNICA_CONEXAO] = False
    return dicionarioPersonagem

def entraTrabalhoEncontrado(dicionarioTrabalho, trabalhoListaDesejo):
    posicao = dicionarioTrabalho[CHAVE_POSICAO]
    if posicao < 0:
        posicao = 0
    dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
    erro = verificaErro(trabalhoListaDesejo)
    print(f'Entra trabalho na posição: {posicao + 1}.')
    if erroEncontrado(erro):
        if erro == erroOutraConexao or erro == erroConectando or erro == erroRestaurandoConexao:
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
            if erro == erroOutraConexao:
                dicionarioTrabalho[CHAVE_UNICA_CONEXAO] = False
    clickContinuo(3, 'up')
    clickEspecifico(posicao + 1, 'down')
    clickEspecifico(1, 'enter')
    linhaSeparacao()
    return dicionarioTrabalho

#modificado 12/01
def retornaTipoErro():
    erro=0
    telaInteira=retornaAtualizacaoTela()
    frameErro=telaInteira[335:335+100,150:526]
    # mostraImagem(0, frameErro, None)
    textoErroEncontrado=reconheceTexto(frameErro)
    print(f'{D}:{textoErroEncontrado}')
    linhaSeparacao()
    if variavelExiste(textoErroEncontrado):
        textoErroEncontrado=limpaRuidoTexto(textoErroEncontrado)
        textoErroEncontrado=retiraDigitos(textoErroEncontrado)
        tipoErro = ['Você precisa de uma licença defabricação para iniciar este pedido',
            'Falha ao se conectar ao servidor',
            'Você precisa de mais recursos parainiciar este pedido',
            'Selecione um item para produzir',
            'Conectando',
            'Você precisa de mais experiência de produção para iniciar este pedido',
            'Você recebeu um novo presenteDessgja ir à Loja Milagrosa paraconferir',
            'Todos os espaços de fabricaçãoestão ocupados',
            'agorapormoedas',
            'Estamos fazendo de tudo paraconcluíla o mais rápido possível',
            'No momento esta conta está sendousada em outro dispositivo',
            'Gostanadecomprar',
            'Conexão perdida com o servidor',
            'Vocêprecisademaismoedas',
            'Nome de usuário ou senha inválida',
            'Pedido de produção expirado',
            'reinodejogoselecionado',
            'jogoestadesatualizada',
            'restaurandoconexão',
            'paraatarefadeprodução',
            'Bolsa chela Deseja liberar',
            'Desgeja sair do Warspear Online']
        for posicaoTipoErro in range(len(tipoErro)):
            textoErro=limpaRuidoTexto(tipoErro[posicaoTipoErro])
            if textoErro in textoErroEncontrado:
                print(f'{D}:"{textoErro}" encontrado em "{textoErroEncontrado}".')
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
        histograma_modelo = retornaHistograma(modelo)
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

def defineListaDicionariosProfissoesNecessarias():
    global dicionarioPersonagemAtributos
    print(f'Verificando profissões necessárias...')
    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA] = []
    posicao = 1
    for profissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        for trabalhoDesejado in dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO]:
            chaveProfissaoEhIgualEEstadoEhParaProduzir = (
                textoEhIgual(profissao[CHAVE_NOME],trabalhoDesejado[CHAVE_PROFISSAO]) 
                and estadoTrabalhoEParaProduzir(trabalhoDesejado))
            if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                dicionarioProfissao = {
                    CHAVE_ID:profissao[CHAVE_ID],
                    CHAVE_NOME:profissao[CHAVE_NOME],
                    CHAVE_PRIORIDADE:profissao[CHAVE_PRIORIDADE],
                    CHAVE_POSICAO:posicao}
                dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA].append(dicionarioProfissao)
                break
        posicao+=1
    else:
        dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA] = sorted(dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA],key=lambda dicionario:dicionario[CHAVE_PRIORIDADE],reverse=True)
        mostraProfissoesNecessarias(dicionarioPersonagemAtributos)

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

def entraPersonagemAtivo():
    global dicionarioPersonagemAtributos
    contadorPersonagem = 0
    menu = retornaMenu()
    if menu == MENU_JOGAR:
        print(f'Buscando personagem ativo...')
        clickEspecifico(1, 'enter')
        time.sleep(1)
        tentativas = 1
        erro = verificaErro(None)
        while erroEncontrado(erro):
            if erro == erroConectando:
                if tentativas > 10:
                    clickEspecifico(2, 'enter')
                    tentativas = 0
                tentativas += 1
            erro = verificaErro(None)
        else:
            clickEspecifico(1, 'f2')
            clickContinuo(10, 'left')   
            personagemReconhecido = retornaNomePersonagem(1)
            while variavelExiste(personagemReconhecido) and contadorPersonagem < 13:
                confirmaNomePersonagem(personagemReconhecido)
                if variavelExiste(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                    modificaAtributoUso(True)
                    clickEspecifico(1, 'f2')
                    time.sleep(1)
                    print(f'{D}: Personagem ({dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME]}) ESTÁ EM USO.')
                    linhaSeparacao()
                    tentativas = 1
                    erro = verificaErro(None)
                    while erroEncontrado(erro):
                        if erro == erroOutraConexao:
                            dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
                            contadorPersonagem = 14
                            break
                        elif erro == erroConectando:
                            if tentativas > 10:
                                clickEspecifico(2, 'enter')
                                tentativas = 0
                            tentativas += 1
                        erro = verificaErro(None)
                    else:
                        print(f'Login efetuado com sucesso!')
                        linhaSeparacao()
                        break
                else:
                    clickEspecifico(1, 'right')
                    personagemReconhecido = retornaNomePersonagem(1)
                contadorPersonagem += 1
            else:
                print(f'Personagem não encontrado!')
                linhaSeparacao()
                if retornaMenu() == MENU_ESCOLHA_PERSONAGEM:
                    clickEspecifico(1, 'f1')
    elif menu == MENU_INICIAL:
        deslogaPersonagem(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1][CHAVE_EMAIL])
    else:
        clickMouseEsquerdo(1,2,35)

def confirmaNomePersonagem(personagemReconhecido):
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = None
    for dicionarioPersonagemAtivo in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
        if textoEhIgual(personagemReconhecido, dicionarioPersonagemAtivo[CHAVE_NOME]):
            print(f'Personagem {personagemReconhecido} confirmado!')
            dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = dicionarioPersonagemAtivo
            break

def defineListaDicionarioPersonagemMesmoEmail(dicionarioPersonagemEmUso):
    listaDicionarioPersonagemMesmoEmail=[]
    for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        if textoEhIgual(dicionarioPersonagem[CHAVE_EMAIL],dicionarioPersonagemEmUso[CHAVE_EMAIL]):
            listaDicionarioPersonagemMesmoEmail.append(dicionarioPersonagem)
    return listaDicionarioPersonagemMesmoEmail

def modificaAtributoUso(valor):
    if valor:
        dicionarioPersonagemEmUso = dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]
    else:
        dicionarioPersonagemEmUso = dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1]
    listaPersonagemMesmoEmail = defineListaDicionarioPersonagemMesmoEmail(dicionarioPersonagemEmUso)
    if not tamanhoIgualZero(listaPersonagemMesmoEmail):
        for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            if dicionarioPersonagem[CHAVE_USO]:
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_ID]}/.json'
                dados = {CHAVE_USO:False}
                print(f'{D}: Atributo USO de {dicionarioPersonagem[CHAVE_NOME]} modificado para FALSO.')
                modificaAtributo(caminhoRequisicao, dados)
                dicionarioPersonagem[CHAVE_USO] = False
        for personagemEmUso in listaPersonagemMesmoEmail:
            if personagemEmUso[CHAVE_USO] != valor:
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{personagemEmUso[CHAVE_ID]}/.json'
                dados = {CHAVE_USO:valor}
                modificaAtributo(caminhoRequisicao, dados)
                print(f'{D}: Atributo USO de {personagemEmUso[CHAVE_NOME]} modificado para VERDADEIRO.')
        for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            if textoEhIgual(dicionarioPersonagem[CHAVE_EMAIL], personagemEmUso[CHAVE_EMAIL]):
                dicionarioPersonagem[CHAVE_USO] = True
        linhaSeparacao()
        
def preparaPersonagem(dicionarioUsuario):
    click_atalho_especifico('alt', 'tab')
    click_atalho_especifico('win', 'left')
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
        if not dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESTADO]:#se o personagem estiver inativo, troca o estado
            listaPersonagemId = [dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
            dicionarioUsuario = modificaAtributoPersonagem(dicionarioUsuario, listaPersonagemId, CHAVE_ESTADO, True)
        iniciaProcessoBusca(dicionarioUsuario)
    else:
        print(f'Erro ao configurar atributos do personagem!')
        linhaSeparacao()

def defineChaveListaDicionarioPersonagemAtivo():
    global dicionarioPersonagemAtributos
    print(f'Definindo lista de personagem ativo.')
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO] = []
    for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        chaveEstadoEhAtivo = (dicionarioPersonagem[CHAVE_ESTADO] or dicionarioPersonagem[CHAVE_ESTADO] == 1)
        if chaveEstadoEhAtivo:
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO].append(dicionarioPersonagem)
    linhaSeparacao()

def iniciaProcessoBusca(dicionarioUsuario):
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_ID_USUARIO] = dicionarioUsuario[CHAVE_ID_USUARIO]
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO] = []
    defineChaveListaDicionarioPersonagemAtivo()
    while True:
        if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = retornaListaDicionariosPersonagens(dicionarioUsuario)
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO] = []
            defineChaveListaDicionarioPersonagemAtivo()
        else:
            defineChaveDicionarioPersonagemEmUso()
            if variavelExiste(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                modificaAtributoUso(True)
                print(f'{D}: Personagem ({dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME]}) ESTÁ EM USO.')
                inicializaChavesPersonagem()
                print('Inicia busca...')
                linhaSeparacao()
                if vaiParaMenuProduzir():
                    while defineTrabalhoComumProfissaoPriorizada():
                        continue
                    listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
                    if not tamanhoIgualZero(listaDicionariosTrabalhosParaProduzirProduzindo):#verifica se a lista está vazia
                        dicionarioTrabalho = {
                            CHAVE_LISTA_DESEJO: listaDicionariosTrabalhosParaProduzirProduzindo,
                            CHAVE_DICIONARIO_TRABALHO_DESEJADO: None}
                        verificaProdutosRarosMaisVendidos()
                        iniciaBuscaTrabalho(dicionarioTrabalho)
                    else:
                        print(f'Lista de trabalhos desejados vazia.')
                        linhaSeparacao()
                        listaPersonagem = [dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
                        dicionarioPersonagemAtributos = modificaAtributoPersonagem(dicionarioPersonagemAtributos,listaPersonagem,CHAVE_ESTADO,False)
                if dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO]:
                    if haMaisQueUmPersonagemAtivo():
                        clickMouseEsquerdo(1, 2, 35)
                    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO])
                    retiraDicionarioPersonagemListaAtivo()
                else:
                    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO])
                    retiraDicionarioPersonagemListaAtivo()
            else:#se o nome reconhecido não estiver na lista de ativos
                if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]):
                    if configuraLoginPersonagem():
                        entraPersonagemAtivo()
                else:
                    if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1][CHAVE_EMAIL],dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][0][CHAVE_EMAIL]):
                        entraPersonagemAtivo()
                    elif configuraLoginPersonagem():
                        entraPersonagemAtivo()

def inicializaChavesPersonagem():
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO] = retornaListaDicionariosTrabalhos()
    dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = True
    dicionarioPersonagemAtributos[CHAVE_ESPACO_BOLSA] = True
    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = False
    dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS] = retornaListaDicionariosTrabalhosVendidos(dicionarioPersonagemAtributos)
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionariosProfissoes(dicionarioPersonagemAtributos)
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE] = retornaListaDicionariosTrabalhosEstoque(dicionarioPersonagemAtributos)
    dicionarioPersonagemAtributos = defineChaveListaDicionariosTrabalhosDesejados(dicionarioPersonagemAtributos)

def haMaisQueUmPersonagemAtivo():
    return not len(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO])==1
                    
def retornaTextoMenuReconhecido(x,y,largura):
    telaInteira = retornaAtualizacaoTela()
    # print(centroAltura,centroMetade)# 384 341
    alturaFrame = 30
    texto = None
    frameTela = telaInteira[y:y+alturaFrame,x:x+largura]
    # mostraImagem(0,frameTela,None)
    if y > 30:
        frameTela = retornaImagemCinza(frameTela)
        frameTela = retornaImagemEqualizada(frameTela)
        frameTela = retornaImagemBinarizada(frameTela)
        # mostraImagem(0,frameTela,None)
    contadorPixelPreto = np.sum(frameTela==0)
    # print(f'Quantidade de pixels pretos: {contadorPixelPreto}')
    if existePixelPretoSuficiente(contadorPixelPreto):
        texto = reconheceTexto(frameTela)
        if variavelExiste(texto):
            texto = limpaRuidoTexto(texto)
            # print(f'{D}:Texto reconhecimento de menus: {texto}.')
    print(f'{D}:{texto}')
    return texto

def existePixelPretoSuficiente(contadorPixelPreto):
    return contadorPixelPreto>250 and contadorPixelPreto<3000

def retornaMenu():
    print(f'Reconhecendo menu.')
    textoMenu = retornaTextoMenuReconhecido(26,1,150)
    if variavelExiste(textoMenu):
        if texto1PertenceTexto2('spearonline',textoMenu):
            textoMenu=retornaTextoMenuReconhecido(216,197,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Notícias',textoMenu):
                    print(f'Menu notícias...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_NOTICIAS
                elif texto1PertenceTexto2('Personagens',textoMenu):
                    print(f'Menu escolha de personagem...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_ESCOLHA_PERSONAGEM
                elif texto1PertenceTexto2('Produção',textoMenu):
                    textoMenu=retornaTextoMenuReconhecido(266,242,150)
                    if variavelExiste(textoMenu):
                        if texto1PertenceTexto2('Artesanatos',textoMenu):
                            textoMenu=retornaTextoMenuReconhecido(191,612,100)
                            if variavelExiste(textoMenu):
                                if texto1PertenceTexto2('fechar',textoMenu):
                                    print(f'Menu produzir...')
                                    linhaSeparacao()
                                    fim = time.time()
                                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                                    linhaSeparacao()
                                    return MENU_PRODUZIR
                                elif texto1PertenceTexto2('voltar',textoMenu):
                                    print(f'Menu trabalhos diponíveis...')
                                    linhaSeparacao()
                                    fim = time.time()
                                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                                    linhaSeparacao()
                                    return MENU_TRABALHOS_DISPONIVEIS
                        elif texto1PertenceTexto2('Pedidos ativos',textoMenu):
                            print(f'Menu trabalhos atuais...')
                            linhaSeparacao()
                            fim = time.time()
                            # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                            linhaSeparacao()
                            return MENU_TRABALHOS_ATUAIS
            textoMenu=retornaTextoSair()
            if variavelExiste(textoMenu):
                if textoEhIgual(textoMenu,'sair'):
                    print(f'Menu jogar...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_JOGAR
            if verificaMenuReferencia():
                print(f'Menu tela inicial...')
                linhaSeparacao()
                fim = time.time()
                # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                linhaSeparacao()
                return MENU_INICIAL
            textoMenu=retornaTextoMenuReconhecido(291,412,100)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('conquistas',textoMenu):
                    print(f'Menu personagem...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_PERSONAGEM
                elif texto1PertenceTexto2('interagir',textoMenu):
                    print(f'Menu principal...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_PRINCIPAL
            textoMenu=retornaTextoMenuReconhecido(191,319,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('parâmetros',textoMenu):
                    if texto1PertenceTexto2('requisitos',textoMenu):
                        print(f'Menu atributo do trabalho...')
                        linhaSeparacao()
                        fim = time.time()
                        # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                        linhaSeparacao()
                        return MENU_TRABALHOS_ATRIBUTOS
                    else:
                        print(f'Menu licenças...')
                        linhaSeparacao()
                        fim = time.time()
                        # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                        linhaSeparacao()
                        return MENU_LICENSAS
            textoMenu=retornaTextoMenuReconhecido(275,400,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensa',textoMenu):
                    print(f'Menu trabalho específico...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_TRABALHO_ESPECIFICO
            textoMenu=retornaTextoMenuReconhecido(266,269,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('ofertadiária',textoMenu):
                    print(f'Menu oferta diária...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_OFERTA_DIARIA
            textoMenu=retornaTextoMenuReconhecido(181,71,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Loja Milagrosa',textoMenu):
                    print(f'Menu loja milagrosa...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_LOJA_MILAGROSA
            textoMenu=retornaTextoMenuReconhecido(180,40,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensas diárias',textoMenu):
                    # # print(f'{D}:Menu recompensas diárias...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_RECOMPENSAS_DIARIAS
            textoMenu=retornaTextoMenuReconhecido(180,60,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensas diárias',textoMenu):
                    print(f'Menu recompensas diárias...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_RECOMPENSAS_DIARIAS
            textoMenu=retornaTextoMenuReconhecido(310,338,57)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('meu',textoMenu):
                    print(f'Menu meu perfil...')
                    linhaSeparacao()
                    fim=time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_MEU_PERFIL           
            textoMenu=retornaTextoMenuReconhecido(169,97,75)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Bolsa',textoMenu):
                    print(f'Menu bolsa...')
                    linhaSeparacao()
                    fim=time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return MENU_BOLSA
            clickMouseEsquerdo(1,35,35)
        else:
            click_atalho_especifico('win','left')
            click_atalho_especifico('win','left')
            linhaSeparacao()
    else:
        print(f'Menu não reconhecido...')
        linhaSeparacao()
    verificaErro(None)
    return MENU_DESCONHECIDO

def deslogaPersonagem(personagemEmail):
    menu = retornaMenu()
    while menu != MENU_JOGAR:
        if menu == MENU_INICIAL:
            encerra_secao()
            break
        elif menu == MENU_JOGAR:
            break
        else:
            clickMouseEsquerdo(1, 2, 35)
        menu = retornaMenu()
    if personagemEmail != None and dicionarioPersonagemAtributos != None:
        modificaAtributoUso(False)

def retiraDicionarioPersonagemListaAtivo():
    defineChaveListaDicionarioPersonagemAtivo()
    for dicionarioPersonagemRemovido in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]:#percorre lista de personagem retirado
        posicao=0
        for dicionarioPersonagemAtivo in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:#percorre lista de personagem ativo
            if textoEhIgual(dicionarioPersonagemAtivo[CHAVE_NOME],dicionarioPersonagemRemovido[CHAVE_NOME]):#compara nome na lista de ativo com nome na lista de retirado
                print(f'{dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][posicao][CHAVE_NOME]} foi retirado da lista de ativos!')
                linhaSeparacao()
                del dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][posicao]
                break
            else:
                posicao+=1

def defineChaveDicionarioPersonagemEmUso():
    nomePersonagemReconhecidoTratado = retornaNomePersonagem(0)
    if variavelExiste(nomePersonagemReconhecidoTratado):
        confirmaNomePersonagem(nomePersonagemReconhecidoTratado)
    elif nomePersonagemReconhecidoTratado == 'provisorioatecair':
        print(f'Nome personagem diferente!')
        linhaSeparacao()

def configuraLoginPersonagem():
    menu = retornaMenu()
    while menu != MENU_JOGAR:
        if menu == MENU_NOTICIAS or menu == MENU_ESCOLHA_PERSONAGEM:
            clickEspecifico(1, 'f1')
        elif menu != MENU_INICIAL:
            clickMouseEsquerdo(1, 2, 35)
        else:
            encerra_secao()
        linhaSeparacao()
        menu = retornaMenu()
    else:
        login = logaContaPersonagem()
    return login
    
def logaContaPersonagem():
    confirmacao=False
    email=dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][0][CHAVE_EMAIL]
    senha=dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][0][CHAVE_SENHA]
    print(f'Tentando logar conta personagem...')
    preencheCamposLogin(email,senha)
    tentativas=1
    erro=verificaErro(None)
    while erroEncontrado(erro):
        if erro==erroConectando or erro==erroRestaurandoConexao:
            if tentativas>10:
                clickEspecifico(1,'enter')
                tentativas = 0
            tentativas+=1
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

def retornaListaDicionariosTrabalhosParaProduzirProduzindo():
    listaDicionariosTrabalhosParaProduzirProduzindo = []
    for dicionarioTrabalhoDesejado in dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO]:
        if trabalhoEhParaProduzir(dicionarioTrabalhoDesejado) or trabalhoEhProduzindo(dicionarioTrabalhoDesejado):
            listaDicionariosTrabalhosParaProduzirProduzindo.append(dicionarioTrabalhoDesejado)
    return listaDicionariosTrabalhosParaProduzirProduzindo

def iniciaBuscaTrabalho(dicionarioTrabalho):
    global dicionarioPersonagemAtributos
    defineListaDicionariosProfissoesNecessarias()
    indiceProfissao = 0
    dicionarioTrabalho[CHAVE_POSICAO] = -1
    while indiceProfissao < len(dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA]):#percorre lista de profissao
        if vaiParaMenuProduzir():
            dicionarioProfissaoVerificada = dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA][indiceProfissao]
            if not chaveConfirmacaoForVerdadeira(dicionarioPersonagemAtributos) or not chaveUnicaConexaoForVerdadeira(dicionarioPersonagemAtributos):
                break
            elif not existeEspacoProducao():
                indiceProfissao += 1
                continue
            if listaProfissoesFoiModificada():
                atualizaListaProfissao()
                verificaEspacoProducao()
            entraProfissaoEspecifica(dicionarioProfissaoVerificada)
            print(f'Verificando profissão: {dicionarioProfissaoVerificada[CHAVE_NOME]}')
            linhaSeparacao()
            listaDeListaTrabalhos = []
            dicionarioTrabalho[CHAVE_PROFISSAO] = dicionarioProfissaoVerificada[CHAVE_NOME]
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
            listaDicionariosTrabalhosEspeciais = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_ESPECIAL)
            if not tamanhoIgualZero(listaDicionariosTrabalhosEspeciais):
                listaDicionariosTrabalhosEspeciais = sorted(listaDicionariosTrabalhosEspeciais,key=lambda dicionario:dicionario[CHAVE_NOME])
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosEspeciais)
            listaDicionariosTrabalhosRaros = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_RARO)
            if not tamanhoIgualZero(listaDicionariosTrabalhosRaros):
                listaDicionariosTrabalhosRaros = sorted(listaDicionariosTrabalhosRaros,key=lambda dicionario:(dicionario[CHAVE_PRIORIDADE], dicionario[CHAVE_NOME]))
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosRaros)
            listaDicionariosTrabalhosMelhorados = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_MELHORADO)
            if not tamanhoIgualZero(listaDicionariosTrabalhosMelhorados):
                listaDicionariosTrabalhosMelhorados = sorted(listaDicionariosTrabalhosMelhorados,key=lambda dicionario:dicionario[CHAVE_NOME])
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosMelhorados)
            listaDicionariosTrabalhosComuns = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_COMUM)
            if not tamanhoIgualZero(listaDicionariosTrabalhosComuns):
                listaDicionariosTrabalhosComuns = sorted(listaDicionariosTrabalhosComuns,key=lambda dicionario:(dicionario[CHAVE_PRIORIDADE], dicionario[CHAVE_NOME]))
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosComuns)
            indiceLista = 0
            while indiceLista < len(listaDeListaTrabalhos):
                listaVerificada = listaDeListaTrabalhos[indiceLista]
                dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA] = listaVerificada
                for dicionarioTrabalhoVerificado in listaVerificada:
                    if raridadeTrabalhoEhEspecial(dicionarioTrabalhoVerificado)or raridadeTrabalhoEhRaro(dicionarioTrabalhoVerificado):
                        print(f'Trabalho desejado: {dicionarioTrabalhoVerificado[CHAVE_NOME]}.')
                        posicaoAux = -1
                        if dicionarioTrabalho[CHAVE_POSICAO] != -1:
                            posicaoAux = dicionarioTrabalho[CHAVE_POSICAO]
                        dicionarioTrabalho[CHAVE_POSICAO] = 0
                        while naoFizerQuatroVerificacoes(dicionarioTrabalho)and not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                            nomeTrabalhoReconhecido = retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                            print(f'Trabalho {dicionarioTrabalhoVerificado[CHAVE_RARIDADE]} reconhecido: {nomeTrabalhoReconhecido}.')
                            if variavelExiste(nomeTrabalhoReconhecido):
                                if texto1PertenceTexto2(nomeTrabalhoReconhecido, dicionarioTrabalhoVerificado[CHAVE_NOME_PRODUCAO]):
                                    dicionarioTrabalho = entraTrabalhoEncontrado(dicionarioTrabalho, dicionarioTrabalhoVerificado)
                                    if chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                        dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoVerificado
                                        tipoTrabalho = 0
                                        if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]):
                                            tipoTrabalho = 1
                                        dicionarioTrabalho = confirmaNomeTrabalho(dicionarioTrabalho, tipoTrabalho)
                                        if not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                            clickEspecifico(1,'f1')
                                            clickContinuo(dicionarioTrabalho[CHAVE_POSICAO]+1,'up')
                                    else:
                                        break
                            else:
                                dicionarioTrabalho[CHAVE_POSICAO] = 4
                            dicionarioTrabalho = incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                        dicionarioTrabalho[CHAVE_POSICAO] = posicaoAux
                        linhaSeparacao()
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                            break
                    elif raridadeTrabalhoEhMelhorado(dicionarioTrabalhoVerificado)or raridadeTrabalhoEhComum(dicionarioTrabalhoVerificado):
                        dicionarioTrabalho = defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = dicionarioTrabalho[CHAVE_CONFIRMACAO]
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                            break
                        elif indiceLista + 1 >= len(listaDeListaTrabalhos):
                            vaiParaMenuTrabalhoEmProducao()
                        else:
                            vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                        break
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                    break
                else:
                    indiceLista += 1
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
            if chaveConfirmacaoForVerdadeira(dicionarioPersonagemAtributos):# CHAVE que indica que nem um erro foi detectado
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):# Começa processo de produção do trabalho
                    dicionarioTrabalho = iniciaProcessoDeProducao(dicionarioTrabalho)
                    linhaSeparacao()
                else:
                    saiProfissaoVerificada(dicionarioTrabalho)
                    indiceProfissao += 1
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
                if chaveUnicaConexaoForVerdadeira(dicionarioPersonagemAtributos):
                    if chaveEspacoBolsaForVerdadeira(dicionarioPersonagemAtributos):
                        if retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                            nomeTrabalhoConcluido = reconheceRecuperaTrabalhoConcluido()
                            if variavelExiste(nomeTrabalhoConcluido):
                                dicionarioTrabalhoConcluido = retornaDicionarioTrabalhoConcluido(nomeTrabalhoConcluido)
                                if not tamanhoIgualZero(dicionarioTrabalhoConcluido):
                                    dicionarioTrabalhoConcluido = modificaTrabalhoConcluidoListaProduzirProduzindo(dicionarioTrabalhoConcluido)
                                    modificaExperienciaProfissao(dicionarioTrabalhoConcluido)
                                    atualizaEstoquePersonagem(dicionarioTrabalhoConcluido)
                                    verificaProducaoTrabalhoRaro(dicionarioTrabalhoConcluido)
                                else:
                                    print(f'{D}: Dicionário trabalho concluido não reconhecido.')
                                    linhaSeparacao()
                            else:
                                print(f'{D}: Dicionário trabalho concluido não reconhecido.')
                                linhaSeparacao()
                        elif not existeEspacoProducao():
                            break
                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = None
                    clickContinuo(3,'up')
                    clickEspecifico(1,'left')
                    linhaSeparacao()
                    time.sleep(1.5)
        else:
            break
    else:
        if listaProfissoesFoiModificada():
            atualizaListaProfissao()
            verificaEspacoProducao()
        print(f'Fim da lista de profissões...')
        linhaSeparacao()

def saiProfissaoVerificada(dicionarioProfissao):
    print(f'Nem um trabalho disponível está na lista de desejos.')
    clickEspecifico(1,'f1')
    clickContinuo(dicionarioProfissao[CHAVE_POSICAO] + 10,'up')
    clickEspecifico(1,'left')
    time.sleep(1)
    linhaSeparacao()

def defineTrabalhoComumProfissaoPriorizada():
    confirmacao = True
    global dicionarioPersonagemAtributos
    print(f'Verifica profissão priorizada!')
    dicionarioProfissaoPrioridade = retornaDicionarioProfissaoPrioridade()
    if not tamanhoIgualZero(dicionarioProfissaoPrioridade):
        nivelProfissao, xpMinimo, xpMaximo = retornaNivelXpMinimoMaximo(dicionarioProfissaoPrioridade)
        xpNecessario = xpMaximo - xpMinimo
        xpRestante = xpNecessario - (dicionarioProfissaoPrioridade[CHAVE_EXPERIENCIA] - xpMinimo)
        nivelTrabalhoProducao = retornaNivelTrabalhoProducao(nivelProfissao)
        if nivelTrabalhoProducao != 1 and nivelTrabalhoProducao != 8:
            listaDicionarioTrabalhoComum = retornaListaDicionarioTrabalhoComumNivelEspecifico(dicionarioProfissaoPrioridade, nivelTrabalhoProducao)
            if not tamanhoIgualZero(listaDicionarioTrabalhoComum):
                listaDicionarioTrabalhoComum = defineQuantidadeTrabalhoEstoque(listaDicionarioTrabalhoComum)
                listaDicionarioTrabalhoComum, quantidadeTrabalhoProduzirProduzindo = defineSomaQuantidadeTrabalhoEstoqueProduzirProduzindo(listaDicionarioTrabalhoComum)
                somatorioXpProduzindo = retornaSomatorioXpTrabalhoProduzindo(dicionarioProfissaoPrioridade)
                xpSuficienteParaEvoluir = xpNecessario - somatorioXpProduzindo >= 0
                if xpSuficienteParaEvoluir:
                    quantidadeTrabalhoProduzir = CODIGO_TRABALHO_MAXIMO - quantidadeTrabalhoProduzirProduzindo
                    if quantidadeTrabalhoProduzindoMenorQueOPermitido(quantidadeTrabalhoProduzir):
                        listaDicionariosRecursos = defineListaDicionarioRecursos(listaDicionarioTrabalhoComum[0])
                        listaDicionariosRecursos = multiplicaQuantidadeDeRecursosPorQuantidadeDisponiveis(quantidadeTrabalhoProduzir, listaDicionariosRecursos)
                        exitemRecursosSuficientes, listaDicionariosRecursos = existemRecursosSuficientesEmEstoque(listaDicionariosRecursos)
                        if exitemRecursosSuficientes:
                            listaDicionarioTrabalhoComum = sorted(listaDicionarioTrabalhoComum,key=lambda dicionario:dicionario[CHAVE_QUANTIDADE])
                            print(f'{D}: Existem recursos suficientes para produzir: {listaDicionarioTrabalhoComum[0][CHAVE_NOME]} - nível: {nivelTrabalhoProducao}.')
                            for dicionarioTrabalhoComum in listaDicionarioTrabalhoComum:
                                for atributo in dicionarioTrabalhoComum:
                                    print(f'{D}: {atributo} - {dicionarioTrabalhoComum[atributo]}.')
                                linhaSeparacao()
                            dicionarioTrabalho = {
                                CHAVE_NOME:listaDicionarioTrabalhoComum[0][CHAVE_NOME],
                                CHAVE_NOME_PRODUCAO:listaDicionarioTrabalhoComum[0][CHAVE_NOME_PRODUCAO],
                                CHAVE_NIVEL:listaDicionarioTrabalhoComum[0][CHAVE_NIVEL],
                                CHAVE_PROFISSAO:listaDicionarioTrabalhoComum[0][CHAVE_PROFISSAO],
                                CHAVE_EXPERIENCIA:listaDicionarioTrabalhoComum[0][CHAVE_EXPERIENCIA],
                                CHAVE_RARIDADE:listaDicionarioTrabalhoComum[0][CHAVE_RARIDADE],
                                LC.CHAVE_RECORRENCIA:False,
                                CHAVE_ESTADO:CODIGO_PARA_PRODUZIR,
                                CHAVE_LICENCA:CHAVE_LICENCA_INICIANTE}
                            if trabalhoEhProducaoRecursos(dicionarioTrabalho):
                                dicionarioTrabalho[LC.CHAVE_RECORRENCIA] = True
                            dicionarioTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalho)
                            dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalho)
                        else:
                            dicionarioTrabalhoGrandeProducaoRecursos = retornaDicionarioTrabalhoGrandeProducaoRecursos(listaDicionarioTrabalhoComum[0])
                            if not tamanhoIgualZero(dicionarioTrabalhoGrandeProducaoRecursos):
                                if not verificaTrabalhoProducaoRecursosListaParaProduzirProduzindo(dicionarioTrabalhoGrandeProducaoRecursos):
                                    dicionarioTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalhoGrandeProducaoRecursos)
                                    dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalho)
                                if nivelProfissao < 9:
                                    produzRecursoFaltante(listaDicionariosRecursos)
                                    print(f'{D}: Existem unidades suficientes sendo produzidas de todos recursos necessários.')
                                    linhaSeparacao()
                                confirmacao = False
                            else:
                                confirmacao = False
                                print(f'{D}: Dicionário trabalho produção de recuros não encontrado.')
                                linhaSeparacao()
                    else:
                        confirmacao = False
                        print(f'{D}: Quantidade de trabalhos na fila para produzir ou produzindo execede o máximo permitido.')
                else:
                    confirmacao = False
                    print(f'{D}: Experiência trabalhos para produzir e produzindo é suficiente para evoluir nível da profissão.')    
            else:
                confirmacao = False
                print(f'{D}: Lista dicionário trabalho comum profissão: {dicionarioProfissaoPrioridade[CHAVE_NOME]}, nível: {nivelTrabalhoProducao}, está vazia!')
        else:
            listaDicionariosTrabalhosProducaoRecursos = []
            xpRecurso = 3
            if nivelTrabalhoProducao == 8:
                xpRecurso = 130
            for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
                condicoes = (
                    dicionarioTrabalho[CHAVE_NIVEL] == nivelTrabalhoProducao
                    and textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioProfissaoPrioridade[CHAVE_NOME])
                    and dicionarioTrabalho[CHAVE_EXPERIENCIA] == xpRecurso)
                if condicoes:
                    listaDicionariosTrabalhosProducaoRecursos.append(dicionarioTrabalho)
            if not tamanhoIgualZero(listaDicionariosTrabalhosProducaoRecursos):
                print(f'{D}: Dicionário trabalho para produção de recursos:')
                quantidadeTrabalhos = xpRestante / listaDicionariosTrabalhosProducaoRecursos[0][CHAVE_EXPERIENCIA]
                listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
                for dicionarioTrabalhoParaProduzirProduzindo in listaDicionariosTrabalhosParaProduzirProduzindo:
                    for dicionarioTrabalhoGrandeProducaoRecursos in listaDicionariosTrabalhosProducaoRecursos:
                        dicionarioTrabalhoGrandeProducaoRecursos[LC.CHAVE_RECORRENCIA] = False
                        dicionarioTrabalhoGrandeProducaoRecursos[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                        dicionarioTrabalhoGrandeProducaoRecursos[CHAVE_LICENCA] = CHAVE_LICENCA_APRENDIZ
                        if textoEhIgual(dicionarioTrabalhoParaProduzirProduzindo[CHAVE_NOME], dicionarioTrabalhoGrandeProducaoRecursos[CHAVE_NOME]):
                            quantidadeTrabalhos -= 1
                for dicionatrioTrabalho in listaDicionariosTrabalhosProducaoRecursos:
                    for atributo in dicionatrioTrabalho:
                        print(f'{D}: {atributo} - {dicionatrioTrabalho[atributo]}')
                    linhaSeparacao()
                if nivelProfissao == 1:
                    listaDicionariosTrabalhosProducaoRecursos[0][LC.CHAVE_RECORRENCIA] = False
                    listaDicionariosTrabalhosProducaoRecursos[0][CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                    listaDicionariosTrabalhosProducaoRecursos[0][CHAVE_LICENCA] = CHAVE_LICENCA_APRENDIZ
                    x = 0
                    while x < quantidadeTrabalhos:
                        dicionarioTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, listaDicionariosTrabalhosProducaoRecursos[0])
                        dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalho)
                        x += 1
                elif nivelProfissao == 8:
                    maximoTralhosProduzirProduzindo = 3
                    for dicionarioRecurso in listaDicionariosTrabalhosProducaoRecursos:
                        for dicionarioTrabalhoProduzirProduzindo in listaDicionariosTrabalhosParaProduzirProduzindo:
                            if textoEhIgual(dicionarioRecurso[CHAVE_NOME], dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME]):
                                maximoTralhosProduzirProduzindo -= 1
                    if maximoTralhosProduzirProduzindo > 0:
                        for dicionarioTrabalhoRecurso in listaDicionariosTrabalhosProducaoRecursos:
                            dicionarioTrabalhoRecurso[CHAVE_TIPO] = retornaChaveTipoRecurso(dicionarioTrabalhoRecurso)
                        listaDicionariosTrabalhosProducaoRecursos = sorted(listaDicionariosTrabalhosProducaoRecursos, key = lambda dicionario:dicionario[CHAVE_TIPO], reverse=True)
                        for dicionarioRecurso in listaDicionariosTrabalhosProducaoRecursos:
                            for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
                                if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_ID_TRABALHO], dicionarioRecurso[CHAVE_ID]):
                                    dicionarioRecurso[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]
                                    break
                            else:
                                dicionarioRecurso[CHAVE_QUANTIDADE] = 0
                        for dicionarioRecurso in listaDicionariosTrabalhosProducaoRecursos:
                            for dicionarioTrabalhoProduzirProduzindo in listaDicionariosTrabalhosParaProduzirProduzindo:
                                if textoEhIgual(dicionarioRecurso[CHAVE_NOME], dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME]):
                                    quantidadeSendoProduzida = 2
                                    if textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_LICENCA], CHAVE_LICENCA_APRENDIZ):
                                        quantidadeSendoProduzida = 4
                                    dicionarioRecurso[CHAVE_QUANTIDADE] += quantidadeSendoProduzida
                        for dicionarioRecurso in listaDicionariosTrabalhosProducaoRecursos:
                            print(f'{D}: {dicionarioRecurso[CHAVE_NOME]} - tipo ({dicionarioRecurso[CHAVE_TIPO]}) - quantidade ({dicionarioRecurso[CHAVE_QUANTIDADE]}).')
                        if listaDicionariosTrabalhosProducaoRecursos[1][CHAVE_QUANTIDADE] - listaDicionariosTrabalhosProducaoRecursos[0][CHAVE_QUANTIDADE] >= 0:
                            dicionarioNovoTrabalho = retornaDicionarioNovoTrabalhoProducao(listaDicionariosTrabalhosProducaoRecursos[0])
                            dicionarioNovoTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioNovoTrabalho)
                            dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioNovoTrabalho)
                        elif (listaDicionariosTrabalhosProducaoRecursos[1][CHAVE_QUANTIDADE] - listaDicionariosTrabalhosProducaoRecursos[0][CHAVE_QUANTIDADE] < 0
                            and listaDicionariosTrabalhosProducaoRecursos[2][CHAVE_QUANTIDADE] - listaDicionariosTrabalhosProducaoRecursos[1][CHAVE_QUANTIDADE] >= 0):
                            dicionarioNovoTrabalho = retornaDicionarioNovoTrabalhoProducao(listaDicionariosTrabalhosProducaoRecursos[1])
                            dicionarioNovoTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioNovoTrabalho)
                            dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioNovoTrabalho)
                        else:
                            dicionarioNovoTrabalho = retornaDicionarioNovoTrabalhoProducao(listaDicionariosTrabalhosProducaoRecursos[2])
                            dicionarioNovoTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioNovoTrabalho)
                            dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioNovoTrabalho)
                    else:
                        confirmacao = False
                        print(f'{D}: O máximo de trabalhos para produzir/produzindo foi atingido!')
                        linhaSeparacao()
            else:
                confirmacao = False
                print(f'{D}: Dicionário vazio!')
                linhaSeparacao()
    else:
        confirmacao = False
        print(f'{D}: Dicionário profissão priorizada vazio!')
    return confirmacao

def retornaDicionarioNovoTrabalhoProducao(dicionarioTrabalho):
    return {
        CHAVE_NOME:dicionarioTrabalho[CHAVE_NOME],
        CHAVE_ESTADO:dicionarioTrabalho[CHAVE_ESTADO],
        CHAVE_EXPERIENCIA:dicionarioTrabalho[CHAVE_EXPERIENCIA],
        CHAVE_NIVEL:dicionarioTrabalho[CHAVE_NIVEL],
        CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
        CHAVE_RARIDADE:dicionarioTrabalho[CHAVE_RARIDADE],
        LC.CHAVE_RECORRENCIA:False,
        CHAVE_LICENCA:CHAVE_LICENCA_APRENDIZ,
        CHAVE_TRABALHO_NECESSARIO:dicionarioTrabalho[CHAVE_TRABALHO_NECESSARIO],
        CHAVE_NOME_PRODUCAO:dicionarioTrabalho[CHAVE_NOME_PRODUCAO]}

def retornaDicionarioTrabalhoEstoque(listaDicionariosTrabalhosEstoque, nomeTrabalhoRecurso):
    for dicionarioTrabalhoEstoque in listaDicionariosTrabalhosEstoque:
        if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], nomeTrabalhoRecurso):
            return dicionarioTrabalhoEstoque
    return {}

def multiplicaQuantidadeDeRecursosPorQuantidadeDisponiveis(quantidadeTrabalhoProduzir, listaDicionariosRecursos):
    for dicionarioRecurso in listaDicionariosRecursos:
        dicionarioRecurso[CHAVE_QUANTIDADE] = dicionarioRecurso[CHAVE_QUANTIDADE] * quantidadeTrabalhoProduzir
    return listaDicionariosRecursos

def produzRecursoFaltante(listaDicionariosRecursos):
    global dicionarioPersonagemAtributos
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]):
        for dicionarioRecurso in listaDicionariosRecursos:
            if dicionarioRecurso[CHAVE_QUANTIDADE] > 0:
                while True:
                    print(f'{D}: Faltam {dicionarioRecurso[CHAVE_QUANTIDADE]} de {dicionarioRecurso[CHAVE_NOME]}.')
                    linhaSeparacao()
                    quantidadeRecursoProduzirProduzindo = retornaQuantidadeRecursoProduzirProduzindo(dicionarioRecurso)
                    if dicionarioRecurso[CHAVE_QUANTIDADE] - quantidadeRecursoProduzirProduzindo > 0:
                            dicionarioTrabalho = defineDicionarioRecursoNecessario(dicionarioRecurso)
                            if not tamanhoIgualZero(dicionarioTrabalho):
                                dicionarioTrabalho = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalho)
                                dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalho)
                    else:
                        print(f'{D}: Existem unidades suficientes sendo produzidas de {dicionarioRecurso[CHAVE_NOME]}.')
                        linhaSeparacao()
                        listaDicionariosRecursos = atualizaQuantidadeRecursoLista(listaDicionariosRecursos, dicionarioRecurso)
                        break
    else:
        print(f'Erro ao definir lista de trabalhos!')
        linhaSeparacao()

def defineDicionarioRecursoNecessario(dicionarioRecurso):
    for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
        nomeRecursoProduzido = retornaNomeRecursoTrabalhoProducao(dicionarioTrabalho[CHAVE_NOME])
        if variavelExiste(nomeRecursoProduzido) and textoEhIgual(nomeRecursoProduzido, dicionarioRecurso[CHAVE_NOME]):
            dicionarioTrabalho[CHAVE_LICENCA] = CHAVE_LICENCA_APRENDIZ
            dicionarioTrabalho[LC.CHAVE_RECORRENCIA] = False
            dicionarioTrabalho[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
            print(f'{D}: Dicionario trabalho recurso faltante:')
            linhaSeparacao()
            for atributo in dicionarioTrabalho:
                print(f'{D}: {atributo} = {dicionarioTrabalho[atributo]}.')
            linhaSeparacao()
            break
    else:
        dicionarioTrabalho = {}
        print(f'Erro ao definir dicionário de recurso necessário!')
        linhaSeparacao()
    return dicionarioTrabalho

def atualizaQuantidadeRecursoLista(listaDicionariosRecursos, dicionarioRecurso):
    if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT:
        for dicionarioRecurso1 in listaDicionariosRecursos:
            if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCT:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = 0
            elif dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] - (dicionarioRecurso[CHAVE_QUANTIDADE] * 4) - (dicionarioRecurso[CHAVE_QUANTIDADE] * 3)
    elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
        for dicionarioRecurso1 in listaDicionariosRecursos:
            if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCS:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = 0
            elif dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] - (dicionarioRecurso[CHAVE_QUANTIDADE] * 3.5) - (dicionarioRecurso[CHAVE_QUANTIDADE] * 2)
    elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
        for dicionarioRecurso1 in listaDicionariosRecursos:
            if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] - (dicionarioRecurso[CHAVE_QUANTIDADE] * 3)
    elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
        for dicionarioRecurso1 in listaDicionariosRecursos:
            if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] - (dicionarioRecurso[CHAVE_QUANTIDADE] * 3)
    elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS:
        for dicionarioRecurso1 in listaDicionariosRecursos:
            if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] - (dicionarioRecurso[CHAVE_QUANTIDADE] * 2)
    return listaDicionariosRecursos

def retornaQuantidadeRecursoProduzirProduzindo(dicionarioRecurso):
    listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    quantidadeRecursoProduzirProduzindo = 0
    for dicionarioTrabalhoProduzirProduzindo in listaDicionarioTrabalhoProduzirProduzindo:
        nomeRecursoProduzido = retornaNomeRecursoTrabalhoProducao(dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME])
        if variavelExiste(nomeRecursoProduzido):
            if textoEhIgual(nomeRecursoProduzido, dicionarioRecurso[CHAVE_NOME]):
                if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS or dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
                    dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = 1
                elif (dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCP or
                    dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP or
                    dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS or
                    dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT):
                    dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = 2
                if textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_LICENCA], 'licença de produção do aprendiz'):
                    dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] * 2                                        
                quantidadeRecursoProduzirProduzindo += dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE]
        else:
            nivelProducao = 0
            if dicionarioTrabalhoProduzirProduzindo[CHAVE_NIVEL] == 3:
                nivelProducao = 1
            elif dicionarioTrabalhoProduzirProduzindo[CHAVE_NIVEL] == 10:
                nivelProducao = 8
            if (dicionarioTrabalhoProduzirProduzindo[CHAVE_ESTADO] == 1 and
                textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_PROFISSAO], dicionarioRecurso[CHAVE_PROFISSAO])and
                textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_RARIDADE],CHAVE_RARIDADE_RARO)and
                trabalhoEhProducaoRecursos(dicionarioTrabalhoProduzirProduzindo)and
                nivelProducao == dicionarioRecurso[CHAVE_NIVEL]):
                    if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
                        dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = 2
                    elif (dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS or dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT):
                        dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = 3
                    elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCP or dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
                        dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = 4
                    elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
                        dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = 5
                    if textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_LICENCA], 'licença de produção do aprendiz'):
                        dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] = dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE] * 2                                        
                    quantidadeRecursoProduzirProduzindo += dicionarioTrabalhoProduzirProduzindo[CHAVE_QUANTIDADE]
    print(f'{D}: Existem {quantidadeRecursoProduzirProduzindo} unidades sendo produzidas de {dicionarioRecurso[CHAVE_NOME]}.')
    linhaSeparacao()
    return quantidadeRecursoProduzirProduzindo

def existemRecursosSuficientesEmEstoque(listaDicionariosRecursos):
    confirmacao = True
    for dicionarioRecurso in listaDicionariosRecursos:
        quantidadeRecursoFaltante = dicionarioRecurso[CHAVE_QUANTIDADE]
        dicionarioTrabalhoEstoque = retornaDicionarioTrabalhoEspecificoEstoque(dicionarioRecurso[CHAVE_NOME])
        if not tamanhoIgualZero(dicionarioTrabalhoEstoque):
            quantidadeRecursoFaltante -= dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]
        if quantidadeRecursoFaltante > 0: #se falta pelo menos um recurso
            if quantidadeRecursoFaltante != dicionarioRecurso[CHAVE_QUANTIDADE]:
                quantidadeRecurso = (dicionarioRecurso[CHAVE_QUANTIDADE] - quantidadeRecursoFaltante)
                if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT:
                    for recurso in listaDicionariosRecursos:
                        if recurso[CHAVE_TIPO] == CHAVE_RCT:
                            recurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
                        elif recurso[CHAVE_TIPO] == CHAVE_RCP:
                            recurso[CHAVE_QUANTIDADE] = recurso[CHAVE_QUANTIDADE] - (quantidadeRecurso * 7)
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
                    for recurso in listaDicionariosRecursos:
                        if recurso[CHAVE_TIPO] == CHAVE_RCS:
                            recurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
                        elif recurso[CHAVE_TIPO] == CHAVE_RCP:
                            recurso[CHAVE_QUANTIDADE] = recurso[CHAVE_QUANTIDADE] - (quantidadeRecurso * 5.5)
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
                    for recurso in listaDicionariosRecursos:
                        if recurso[CHAVE_TIPO] == CHAVE_RCP:
                            recurso[CHAVE_QUANTIDADE] = recurso[CHAVE_QUANTIDADE] - (quantidadeRecurso * 3)
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
                    for recurso in listaDicionariosRecursos:
                        if recurso[CHAVE_TIPO] == CHAVE_RCP:
                            recurso[CHAVE_QUANTIDADE] = recurso[CHAVE_QUANTIDADE] - (quantidadeRecurso * 1.5)
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS:
                    for recurso in listaDicionariosRecursos:
                        if recurso[CHAVE_TIPO] == CHAVE_RCP:
                            recurso[CHAVE_QUANTIDADE] = recurso[CHAVE_QUANTIDADE] - quantidadeRecurso
                dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
            confirmacao = False
        elif quantidadeRecursoFaltante <= 0: #se não faltam recursos
            if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT:
                for recurso in listaDicionariosRecursos:
                    if recurso[CHAVE_TIPO] == CHAVE_RCT:
                        recurso[CHAVE_QUANTIDADE] = 0
                    elif recurso[CHAVE_TIPO] == CHAVE_RCP:
                        recurso[CHAVE_QUANTIDADE] = recurso[CHAVE_QUANTIDADE] - (dicionarioRecurso[CHAVE_QUANTIDADE] * 7)
            elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
                for recurso in listaDicionariosRecursos:
                    if recurso[CHAVE_TIPO] == CHAVE_RCS:
                        recurso[CHAVE_QUANTIDADE] = 0
                    elif recurso[CHAVE_TIPO] == CHAVE_RCP:
                        recurso[CHAVE_QUANTIDADE] -= (dicionarioRecurso[CHAVE_QUANTIDADE] * 5.5)
            elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
                for recurso in listaDicionariosRecursos:
                    if recurso[CHAVE_TIPO] == CHAVE_RCP:
                        recurso[CHAVE_QUANTIDADE] -= (dicionarioRecurso[CHAVE_QUANTIDADE] * 3)
            elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
                for recurso in listaDicionariosRecursos:
                    if recurso[CHAVE_TIPO] == CHAVE_RCP:
                        recurso[CHAVE_QUANTIDADE] -= (dicionarioRecurso[CHAVE_QUANTIDADE] * 3)
            elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS:
                for recurso in listaDicionariosRecursos:
                    if recurso[CHAVE_TIPO] == CHAVE_RCP:
                        recurso[CHAVE_QUANTIDADE] -= (dicionarioRecurso[CHAVE_QUANTIDADE] * 2)
            dicionarioRecurso[CHAVE_QUANTIDADE] = 0
    else:
        listaDicionariosRecursos = sorted(listaDicionariosRecursos, key = lambda dicionario:dicionario[CHAVE_TIPO])
        print(f'{D}: Lista dicionários recursos depois de subtrair estoque:')
        linhaSeparacao()
        for dicionariosRecursos in listaDicionariosRecursos:
            for atributo in dicionariosRecursos:
                print(f'{D}: {atributo} = {dicionariosRecursos[atributo]}.')
            linhaSeparacao()
        linhaSeparacao()
    return confirmacao, listaDicionariosRecursos 

def retornaDicionarioTrabalhoEspecificoEstoque(nomeTrabalho):
    for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
        if textoEhIgual(nomeTrabalho, dicionarioTrabalhoEstoque[CHAVE_NOME]):
            return dicionarioTrabalhoEstoque
    else:
        print(f'{D}: Recurso: {nomeTrabalho} não encontrado no estoque.')
        linhaSeparacao()
    return {}

def quantidadeTrabalhoProduzindoMenorQueOPermitido(quantidadeTrabalhoProduzir):
    return quantidadeTrabalhoProduzir > 0

def defineListaDicionarioRecursos(dicionarioProdutoParaProduzir):
    print(f'Definindo lista de dicionários de recursos.')
    listaDicionariosRecursos = []
    dicionarioProdutoParaProduzir = defineQuantidadeRecursos(dicionarioProdutoParaProduzir)
    chaveProfissao = limpaRuidoTexto(dicionarioProdutoParaProduzir[CHAVE_PROFISSAO])
    nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 1)
    if dicionarioProdutoParaProduzir[CHAVE_NIVEL] <= 14:
        DRCT = {
            CHAVE_NOME:nomeRecursoTerciario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:5,
            CHAVE_TIPO:CHAVE_RCT,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RCT]}
        DRCS = {
            CHAVE_NOME:nomeRecursoSecundario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:4,
            CHAVE_TIPO:CHAVE_RCS,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RCS]}
        DRCP = {
            CHAVE_NOME:nomeRecursoPrimario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:3,
            CHAVE_TIPO:CHAVE_RCP,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RCP]}
        listaDicionariosRecursos.append(DRCT)
        listaDicionariosRecursos.append(DRCS)
        listaDicionariosRecursos.append(DRCP)
    else:
        DRCT = {
            CHAVE_NOME:nomeRecursoTerciario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:5,
            CHAVE_TIPO:CHAVE_RCT,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RCT]}
        DRCS = {
            CHAVE_NOME:nomeRecursoSecundario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:4,
            CHAVE_TIPO:CHAVE_RCS,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RCS]}
        DRCP = {
            CHAVE_NOME:nomeRecursoPrimario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:3,
            CHAVE_TIPO:CHAVE_RCP,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RCP]}
        nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 8)
        DRAT = {
            CHAVE_NOME:nomeRecursoTerciario,
            CHAVE_NIVEL:8,
            CHAVE_EXPERIENCIA:130,
            CHAVE_TIPO:CHAVE_RAT,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RAT]}
        DRAS = {
            CHAVE_NOME:nomeRecursoSecundario,
            CHAVE_NIVEL:8,
            CHAVE_EXPERIENCIA:130,
            CHAVE_TIPO:CHAVE_RAS,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RAS]}
        DRAP = {
            CHAVE_NOME:nomeRecursoPrimario,
            CHAVE_NIVEL:8,
            CHAVE_EXPERIENCIA:130,
            CHAVE_TIPO:CHAVE_RAP,
            CHAVE_PROFISSAO:dicionarioProdutoParaProduzir[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioProdutoParaProduzir[CHAVE_RAP]}
        listaDicionariosRecursos.append(DRAT)
        listaDicionariosRecursos.append(DRAS)
        listaDicionariosRecursos.append(DRAP)
        listaDicionariosRecursos.append(DRCT)
        listaDicionariosRecursos.append(DRCS)
        listaDicionariosRecursos.append(DRCP)
    print(f'{D}: Lista de dicionários recursos:')
    for dicionarioRecurso in listaDicionariosRecursos:
        for atributo in dicionarioRecurso:
            print(f'{D}: {atributo} = {dicionarioRecurso[atributo]}.')
        linhaSeparacao()
    linhaSeparacao()
    return listaDicionariosRecursos

def retornaChaveTipoRecurso(dicionarioRecurso):
    listaDicionarioProfissaoRecursos = retornaListaDicionarioProfissaoRecursos(dicionarioRecurso[CHAVE_NIVEL])
    chaveProfissao = limpaRuidoTexto(dicionarioRecurso[CHAVE_PROFISSAO])
    for dicionarioProfissaoRecursos in listaDicionarioProfissaoRecursos:
        if chaveProfissao in dicionarioProfissaoRecursos:
            for x in range(len(dicionarioProfissaoRecursos[chaveProfissao])):
                if textoEhIgual(dicionarioProfissaoRecursos[chaveProfissao][x],dicionarioRecurso[CHAVE_NOME]):
                    if x == 0 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        return CHAVE_RCP
                    elif x == 0 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        return CHAVE_RAP
                    elif x == 1 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        return CHAVE_RCS
                    elif x == 1 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        return CHAVE_RAS
                    elif x == 2 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        return CHAVE_RCT
                    elif x == 2 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        return CHAVE_RAT
                    break
    return None

def defineNomeRecursos(dicionarioTrabalho):
    chaveProfissao = limpaRuidoTexto(dicionarioTrabalho[CHAVE_PROFISSAO])
    if dicionarioTrabalho[CHAVE_NIVEL] <= 14:
        nivelRecurso = 1
    else:
        nivelRecurso = 8
    nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, nivelRecurso)
    dicionarioTrabalho[CHAVE_NOME_PRIMARIO] = nomeRecursoPrimario
    dicionarioTrabalho[CHAVE_NOME_SECUNDARIO] = nomeRecursoSecundario
    dicionarioTrabalho[CHAVE_NOME_TERCIARIO] = nomeRecursoTerciario
    print(f'{D}: Dicionário trabalho:')
    for atributo in dicionarioTrabalho:
        print(f'{D}: {atributo} = {dicionarioTrabalho[atributo]}.')
    linhaSeparacao()
    return dicionarioTrabalho

def retornaListaDicionarioProfissaoRecursos(nivelProduzTrabalhoComum):
    listaDicionarioProfissaoRecursos = []
    if nivelProduzTrabalhoComum == 1:
        listaDicionarioProfissaoRecursos=[
                {'braceletes':['Fibra de Bronze','Prata','Pin de Estudante']},
                {'capotes':['Furador do aprendiz','Tecido delicado','Substância instável']},
                {'amuletos':['Pinça do aprendiz','Jade bruta','Energia inicial']},
                {'aneis':['Molde do aprendiz','Pepita de cobre','Pedra de sombras']},
                {'armadurapesada':['Marretão do aprendiz','Placas de cobre','Anéis de bronze']},
                {'armaduraleve':['Faca do aprendiz','Escamas da serpente','Couro resistente']},
                {'armaduradetecido':['Tesoura do aprendiz','Fio grosseiro','Tecido de linho']},
                {'armacorpoacorpo':['Lascas','Minério de cobre','Mó do aprendiz']},
                {'armadelongoalcance':['Esfera do aprendiz','Varinha de madeira','Cabeça do cajado de jade']}]
    elif nivelProduzTrabalhoComum == 8:    
        listaDicionarioProfissaoRecursos=[
                {'braceletes':['Fibra de Platina','Âmbarito','Pino do Aprendiz']},
                {'capotes':['Furador do principiante','Tecido espesso','Substância estável']},
                {'amuletos':['Pinça do principiante','Ônix extraordinária','Éter inicial']},
                {'aneis':['Molde do principiante','Pepita de prata','Pedra da luz']},
                {'armadurapesada':['Marretão do principiante','Placas de ferro','Anéis de aço']},
                {'armaduraleve':['Faca do principiante','Escamas do lagarto','Couro grosso']},
                {'armaduradetecido':['Tesoura do principiante','Fio grosso','Tecido de cetim']},
                {'armacorpoacorpo':['Lascas de quartzo','Minério de ferro','Mó do principiante']},
                {'armadelongoalcance':['Esfera do neófito','Varinha de aço','Cabeça do cajado de ônix']}]
    return listaDicionarioProfissaoRecursos

def retornaNomesRecursos(chaveProfissao, nivelRecurso):
    nomeRecursoPrimario = None
    nomeRecursoSecundario = None
    nomeRecursoTerciario = None
    listaDicionarioProfissao = retornaListaDicionarioProfissaoRecursos(nivelRecurso)
    if not tamanhoIgualZero(listaDicionarioProfissao):
        for dicionarioProfissao in listaDicionarioProfissao:
            if chaveProfissao in dicionarioProfissao:
                nomeRecursoPrimario = dicionarioProfissao[chaveProfissao][0]
                nomeRecursoSecundario = dicionarioProfissao[chaveProfissao][1]
                nomeRecursoTerciario = dicionarioProfissao[chaveProfissao][2]
                break
    return nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario

def retornaNomeRecursoTrabalhoProducao(nomeTrabalhoProducao):
    nomeRecurso = None
    listaNomeRecursos = [
        ['criar esfera do aprendiz','Esfera do aprendiz'],['produzindo a varinha de madeira','Varinha de madeira'],['produzindo cabeça do cajado de jade','Cabeça do cajado de jade'],
        ['produzindo cabeça de cajado de ônix','Cabeça do cajado de ônix'],['criar esfera do neófito','Esfera do neófito'],['produzindo a varinha de aço','Varinha de aço'],
        ['extracao de lascas','Lascas'],['manipulacao de lascas','Minerio de cobre'],['fazer mo do aprendiz','Mo do aprendiz'],
        ['preparando lascas de quartzo','Lascas de quartzo'],['manipulacao de minerio de cobre','Minério de ferro'],['fazer mo do princiante','Mo do principiante'],
        ['adquirir tesoura do aprendiz','Tesoura do aprendiz'],['produzindo fio resistente','Fio grosseiro'],['fazendo tecido de linho','Tecido de linho'],
        ['fazendo tecido de cetim','Tecido de cetim'],['comprar tesoura do principiante','Tesoura do principiante'],['produzindo fio grosso','Fio grosso'],
        ['adquirir faca do aprendiz','Faca do aprendiz'],['recebendo escamas da serpente','Escamas da serpente'],['Concluindo couro resistente','Couro resistente'],
        ['adquirir faca do principiante','Faca do principiante'],['recebendo escamas do lagarto','Escamas do lagarto'],['curtindo couro grosso','Couro grosso'],
        ['adquirir marretão do aprendiz','Marretão do aprendiz'],['forjando placas de cobre','Placas de cobre'],['fazendo placas de bronze','Anéis de bronze'],
        ['adquirir marretão do principiante','Marretão do principiante'],['forjando placas de ferro','Placas de ferro'],['fazendo anéis de aço','Anéis de aço'],
        ['adquirir molde do aprendiz','Molde do aprendiz'],['extração de pepitas de cobre','Pepita de cobre'],['recebendo gema das sombras','Pedra de sombras'],
        ['adquirir molde do principiante','Molde do principiante'],['extração de pepitas de prata','Pepitas de prata'],['recebendo gema da luz','Pedra da luz'],
        ['adquirir pinça do aprendiz','Pinça do aprendiz'],['extração de jade bruta','Jade bruta'],['recebendo energia inicial','Energia inicial'],
        ['adquirir pinças do principiante','Pinça do principiante'],['extração de ônix extraordinária','Ônix extraordinária'],['recebendo éter inicial','Éter inicial'],
        ['adquirir furador do aprendiz','Furador do aprendiz'],['produzindo tecido delicado','Tecido delicado'],['extração de substância instável','Substância instável'],
        ['adquirir furador do principiante','Furador do principiante'],['produzindo tecido denso','Tecido espesso'],['extração de substância estável','Substância estável'],
        ['Recebendo fibra de bronze','Fibra de Bronze'],['recebendo prata','Prata'],['recebendo insígnia de estudante','Pin de Estudante'],
        ['recebendo fibra de platina','Fibra de Platina'],['recebendo âmbar','Âmbarito'],['recebendo distintivo de aprendiz','Pino do Aprendiz']]
    for recurso in listaNomeRecursos:
        if textoEhIgual(recurso[0], nomeTrabalhoProducao):
            nomeRecurso = recurso[1]
            break
    return nomeRecurso

def defineQuantidadeRecursos(dicionarioTrabalho):
    print(f'Define quantidade de recursos.')
    nivelProduzTrabalhoComum = dicionarioTrabalho[CHAVE_NIVEL]
    recursoTerciario = 0
    if textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE):
        recursoTerciario = 1
    if nivelProduzTrabalhoComum <= 14:
        if nivelProduzTrabalhoComum == 10:
            recursoTerciario += 2
        elif nivelProduzTrabalhoComum == 12:
            recursoTerciario += 4
        elif nivelProduzTrabalhoComum == 14:
            recursoTerciario += 6
        dicionarioTrabalho[CHAVE_RCT] = recursoTerciario
        dicionarioTrabalho[CHAVE_RCS] = recursoTerciario + 1
        dicionarioTrabalho[CHAVE_RCP] = (recursoTerciario + 2) + (dicionarioTrabalho[CHAVE_RCS] * 2) + (dicionarioTrabalho[CHAVE_RCT] * 3)
    else:
        if nivelProduzTrabalhoComum == 16:
            recursoTerciario += 2
        elif nivelProduzTrabalhoComum == 18:
            recursoTerciario += 4
        elif nivelProduzTrabalhoComum == 20:
            recursoTerciario += 6
        elif nivelProduzTrabalhoComum == 22:
            recursoTerciario += 8
        elif nivelProduzTrabalhoComum == 24:
            recursoTerciario += 10
        elif nivelProduzTrabalhoComum == 26:
            recursoTerciario += 12
        elif nivelProduzTrabalhoComum == 28:
            recursoTerciario += 14
        elif nivelProduzTrabalhoComum == 30:
            recursoTerciario += 16
        elif nivelProduzTrabalhoComum == 32:
            recursoTerciario += 18
        dicionarioTrabalho[CHAVE_RAT] = recursoTerciario
        dicionarioTrabalho[CHAVE_RAS] = recursoTerciario + 1
        dicionarioTrabalho[CHAVE_RAP] = recursoTerciario + 2

        dicionarioTrabalho[CHAVE_RCT] = dicionarioTrabalho[CHAVE_RAT]
        dicionarioTrabalho[CHAVE_RCS] = dicionarioTrabalho[CHAVE_RAS]
        dicionarioTrabalho[CHAVE_RCP] = (dicionarioTrabalho[CHAVE_RAP] * 3) + (dicionarioTrabalho[CHAVE_RAS] * 5.5) + (dicionarioTrabalho[CHAVE_RAT] * 7) 
    for atributo in dicionarioTrabalho:
        print(f'{D}: {atributo} - {dicionarioTrabalho[atributo]}.')
    linhaSeparacao()
    return dicionarioTrabalho

def retornaSomatorioXpTrabalhoProduzindo(dicionarioProfissaoPrioridade):
    somaXpProduzirProduzindo = 0
    listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    for dicionarioTrabalhoProduzirProduzindo in listaDicionarioTrabalhoProduzirProduzindo:
        if (textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_PROFISSAO],dicionarioProfissaoPrioridade[CHAVE_NOME])
            and dicionarioTrabalhoProduzirProduzindo[CHAVE_ESTADO] == CODIGO_PRODUZINDO):
            somaXpProduzirProduzindo += dicionarioTrabalhoProduzirProduzindo[CHAVE_EXPERIENCIA]
    return somaXpProduzirProduzindo

def defineSomaQuantidadeTrabalhoEstoqueProduzirProduzindo(listaDicionarioTrabalhoComum):
    quantidadeTrabalhoProduzirProduzindo = 0
    listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    for dicionarioTrabalhoProduzirProduzindo in listaDicionarioTrabalhoProduzirProduzindo:
        for dicionarioTrabalhoComum in listaDicionarioTrabalhoComum:
            if textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME],dicionarioTrabalhoComum[CHAVE_NOME]):
                dicionarioTrabalhoComum[CHAVE_QUANTIDADE] += 1
                quantidadeTrabalhoProduzirProduzindo += 1
    return listaDicionarioTrabalhoComum, quantidadeTrabalhoProduzirProduzindo

def defineQuantidadeTrabalhoEstoque(listaDicionarioTrabalhoComum):
    for dicionarioTrabalhoComum in listaDicionarioTrabalhoComum:
        for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
            if textoEhIgual(dicionarioTrabalhoComum[CHAVE_ID], dicionarioTrabalhoEstoque[CHAVE_ID_TRABALHO]):
                print(f'{D}: {dicionarioTrabalhoEstoque[CHAVE_ID_TRABALHO]}.')
                dicionarioTrabalhoComum[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]
                break
        else:
            dicionarioTrabalhoComum[CHAVE_QUANTIDADE] = 0
    return listaDicionarioTrabalhoComum

def retornaListaDicionarioTrabalhoComumNivelEspecifico(dicionarioProfissaoPrioridade, nivelProduzTrabalhoComum):
    listaDicionarioTrabalhoComum = []
    for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioProfissaoPrioridade[CHAVE_NOME])
            and dicionarioTrabalho[CHAVE_NIVEL] == nivelProduzTrabalhoComum
            and textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_COMUM)):
            for atributo in dicionarioTrabalho:
                print(f'{D}: {atributo} - {dicionarioTrabalho[atributo]}.')
            linhaSeparacao()
            listaDicionarioTrabalhoComum.append(dicionarioTrabalho)
    return listaDicionarioTrabalhoComum

def retornaNivelTrabalhoProducao(nivelProfissao):
    if nivelProfissao == 1:
        nivelTrabalhoProducao = 1
    elif nivelProfissao == 8:
        nivelTrabalhoProducao = 8
    elif nivelProfissao >= 2 and nivelProfissao < 4:
        nivelTrabalhoProducao = 10
    elif nivelProfissao >= 4 and nivelProfissao < 6:
        nivelTrabalhoProducao = 12
    elif nivelProfissao >= 6 and nivelProfissao < 8:
        nivelTrabalhoProducao = 14
    elif nivelProfissao >= 9 and nivelProfissao < 11:
        nivelTrabalhoProducao = 16
    elif nivelProfissao >= 11 and nivelProfissao < 13:
        nivelTrabalhoProducao = 18
    elif nivelProfissao >= 13 and nivelProfissao < 15:
        nivelTrabalhoProducao = 20
    elif nivelProfissao >= 15 and nivelProfissao < 17:
        nivelTrabalhoProducao = 22
    elif nivelProfissao >= 17 and nivelProfissao < 19:
        nivelTrabalhoProducao = 24
    elif nivelProfissao >= 19 and nivelProfissao < 21:
        nivelTrabalhoProducao = 26
    elif nivelProfissao >= 21 and nivelProfissao < 23:
        nivelTrabalhoProducao = 28
    elif nivelProfissao >= 23 and nivelProfissao < 25:
        nivelTrabalhoProducao = 30
    elif nivelProfissao >= 25 and nivelProfissao < 27:
        nivelTrabalhoProducao = 32
    return nivelTrabalhoProducao

def retornaNivelXpMinimoMaximo(dicionarioProfissaoPrioridade):
    listaXPMaximo = [
        20, 200, 540, 1250, 2550, 4700, 7990, 12770
        ,19440, 28440, 40270, 55450, 74570, 98250, 127180, 156110
        ,185040, 215000, 245000, 300000, 375000, 470000, 585000, 706825
        ,830000, 1050000]
    xpAtual = dicionarioProfissaoPrioridade[CHAVE_EXPERIENCIA]
    nivelProfissao = 1
    xpMinimo = 0
    xpMaximo = 0
    for posicao in range(0,len(listaXPMaximo)):
        if listaXPMaximo[posicao] == 20:
            if xpAtual < listaXPMaximo[posicao]:
                xpMinimo = 0
                xpMaximo = listaXPMaximo[posicao]
                break
        else:
            if xpAtual < listaXPMaximo[posicao] and xpAtual >= listaXPMaximo[posicao-1]:
                nivelProfissao = posicao + 1
                xpMinimo = listaXPMaximo[posicao-1]
                xpMaximo = listaXPMaximo[posicao]
                break
    return nivelProfissao, xpMinimo, xpMaximo

def retornaDicionarioProfissaoPrioridade():
    dicionarioProfissaoPrioridade = {}
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]):
        for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
            if dicionarioProfissao[CHAVE_PRIORIDADE]:
                return dicionarioProfissao
        else:
            print(f'{D}:Nenhuma profissão priorizada!')
    else:
        print(f'{D}:Lista profissões vazia!')
    linhaSeparacao()
    return dicionarioProfissaoPrioridade

def retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho):
    time.sleep(1)
    return retornaNomeTrabalhoReconhecido((dicionarioTrabalho[CHAVE_POSICAO]*72)+289, 0)

def existeEspacoProducao():
    espacoProducao = dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]
    listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    for dicionarioTrabalho in listaDicionariosTrabalhosParaProduzirProduzindo:
        if dicionarioTrabalho[CHAVE_ESTADO] == CODIGO_PRODUZINDO:
            espacoProducao -= 1
            if espacoProducao <= 0:
                print(f'{D}: {espacoProducao} espaços de produção - FALSO.')
                return False
    print(f'{D}: {espacoProducao} espaços de produção - VERDADEIRO.')
    return True

def incrementaChavePosicaoTrabalho(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_POSICAO] += 1
    return dicionarioTrabalho

def chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
    # # print(f'{D}:CHAVE_DICIONARIO_TRABALHO_DESEJADO: {dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]}.')
    return dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]!=None

def naoFizerQuatroVerificacoes(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO] < 4

def chaveEspacoBolsaForVerdadeira(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_ESPACO_BOLSA]

def existeOutraConexao(erro):
    return erro==erroOutraConexao

def listaProfissoesFoiModificada():
    return dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA]

def tamanhoIgualZero(lista):
    return len(lista)==0

def chaveUnicaConexaoForVerdadeira(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_UNICA_CONEXAO]

def chaveConfirmacaoForVerdadeira(dicionario):
    return dicionario[CHAVE_CONFIRMACAO]

def naoEstiverMenuProduzir(menu):
    return menu!=MENU_PRODUZIR

def erroEncontrado(erro):
    return erro != 0

def retornaInputConfirmacao():
    confirmacao = input(f'S/N: ')
    linhaSeparacao()
    while (not ehValorAlfabetico(confirmacao)or
           not texto1PertenceTexto2(confirmacao, 'ns')or
            not len(confirmacao) == 1):
        print(f'Valor inválido!')
        confirmacao = input(f'S/N: ')
        linhaSeparacao()
    else:
        if textoEhIgual(confirmacao, 's'):
            return True
        elif textoEhIgual(confirmacao, 'n'):
            return False

def vaiParaMenuCorrespondencia():
    clickEspecifico(1,'f2')
    clickEspecifico(1,'1')
    clickEspecifico(1,'9')

def estaMenuInicial(menu):
    return menu==MENU_INICIAL

def modificaTrabalhoConcluidoListaProduzirProduzindo(dicionarioTrabalhoConcluido):
    global dicionarioPersonagemAtributos
    if trabalhoEhProducaoRecursos(dicionarioTrabalhoConcluido):
        dicionarioTrabalhoConcluido[LC.CHAVE_RECORRENCIA] = True
    if dicionarioTrabalhoConcluido[LC.CHAVE_RECORRENCIA]:
        print(f'Trabalho recorrente.')
        excluiTrabalhoListaDesejos(dicionarioPersonagemAtributos, dicionarioTrabalhoConcluido)
        for posicao in range(len(dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO])):
            if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO][posicao][CHAVE_ID], dicionarioTrabalhoConcluido[CHAVE_ID]):
                del dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO][posicao]
                break
    else:
        print(f'Trabalho sem recorrencia.')
        caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalhoConcluido[CHAVE_ID]}/.json'
        dados = {
            CHAVE_ESTADO:2,
            CHAVE_EXPERIENCIA:dicionarioTrabalhoConcluido[CHAVE_EXPERIENCIA],
            CHAVE_ID:dicionarioTrabalhoConcluido[CHAVE_ID],
            CHAVE_ID_TRABALHO:dicionarioTrabalhoConcluido[CHAVE_ID_TRABALHO],
            CHAVE_NIVEL:dicionarioTrabalhoConcluido[CHAVE_NIVEL],
            CHAVE_NOME:dicionarioTrabalhoConcluido[CHAVE_NOME],
            CHAVE_PROFISSAO:dicionarioTrabalhoConcluido[CHAVE_PROFISSAO],
            CHAVE_RARIDADE:dicionarioTrabalhoConcluido[CHAVE_RARIDADE],
            LC.CHAVE_RECORRENCIA:dicionarioTrabalhoConcluido[LC.CHAVE_RECORRENCIA],
            LC.CHAVE_LICENCA:dicionarioTrabalhoConcluido[LC.CHAVE_LICENCA]}
        print(f'{D}: Trabalho ({dicionarioTrabalhoConcluido[CHAVE_NOME]}) modificado para concluído.')
        modificaAtributo(caminhoRequisicao, dados)
        for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO]:
            if textoEhIgual(dicionarioTrabalho[CHAVE_ID], dicionarioTrabalhoConcluido[CHAVE_ID]):
                dicionarioTrabalho[CHAVE_ESTADO] = 2
                CHAVE_RECORRENCIA:dicionarioTrabalhoConcluido[CHAVE_RECORRENCIA]
                CHAVE_LICENCA:dicionarioTrabalhoConcluido[CHAVE_LICENCA]
                break
        else:
            dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dados)
    linhaSeparacao()
    return dicionarioTrabalhoConcluido

def retornaListaDicionarioTrabalhoProduzido(dicionarioTrabalhoConcluido):
    listaDicionarioTrabalhoProduzido = []
    dicionarioTrabalhoEstoque = {}
    if trabalhoEhProducaoRecursos(dicionarioTrabalhoConcluido):
        if trabalhoEhProducaoLicenca(dicionarioTrabalhoConcluido):
            dicionarioTrabalhoEstoque = {
                CHAVE_NIVEL:0,
                CHAVE_NOME:CHAVE_LICENCA_APRENDIZ,
                CHAVE_QUANTIDADE:2,
                CHAVE_PROFISSAO:None,
                CHAVE_RARIDADE:'Recurso',
                CHAVE_ID_TRABALHO:dicionarioTrabalhoConcluido[CHAVE_ID_TRABALHO]
            }
        else:
            if trabalhoEhMelhoriaEssenciaComum(dicionarioTrabalhoConcluido):
                dicionarioTrabalhoEstoque = {
                    CHAVE_NIVEL:0,
                    CHAVE_NOME:'Essência composta',
                    CHAVE_QUANTIDADE:5,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Recurso'
                }
            elif trabalhoEhMelhoriaEssenciaComposta(dicionarioTrabalhoConcluido):
                dicionarioTrabalhoEstoque = {
                    CHAVE_NIVEL:0,
                    CHAVE_NOME:'Essência de energia',
                    CHAVE_QUANTIDADE:1,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Recurso'
                }
            elif trabalhoEhMelhoriaSubstanciaComum(dicionarioTrabalhoConcluido):
                dicionarioTrabalhoEstoque = {
                    CHAVE_NIVEL:0,
                    CHAVE_NOME:'Substância composta',
                    CHAVE_QUANTIDADE:5,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Recurso'
                }
            elif trabalhoEhMelhoriaSubstanciaComposta(dicionarioTrabalhoConcluido):
                dicionarioTrabalhoEstoque = {
                    CHAVE_NIVEL:0,
                    CHAVE_NOME:'Substância energética',
                    CHAVE_QUANTIDADE:1,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Recurso'
                }
            elif trabalhoEhMelhoriaCatalisadorComum(dicionarioTrabalhoConcluido):
                dicionarioTrabalhoEstoque = {
                    CHAVE_NIVEL:0,
                    CHAVE_NOME:'Catalisador amplificado',
                    CHAVE_QUANTIDADE:5,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Recurso'
                }
            elif trabalhoEhMelhoriaCatalisadorComposto(dicionarioTrabalhoConcluido):
                dicionarioTrabalhoEstoque = {
                    CHAVE_NIVEL:0,
                    CHAVE_NOME:'Catalisador de energia',
                    CHAVE_QUANTIDADE:1,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Recurso'
                }
            if not tamanhoIgualZero(dicionarioTrabalhoEstoque):
                if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA], CHAVE_LICENCA_APRENDIZ):
                    dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] * 2
        if not tamanhoIgualZero(dicionarioTrabalhoEstoque):
            listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)
        if trabalhoEhColecaoRecursosComuns(dicionarioTrabalhoConcluido) or trabalhoEhColecaoRecursosAvancados(dicionarioTrabalhoConcluido):
                nivelColecao = 1
                if trabalhoEhColecaoRecursosAvancados(dicionarioTrabalhoConcluido):
                    nivelColecao = 8
                listaDicionariosTrabalhos = retornaListaDicionariosTrabalhos()
                for dicionarioTrabalho in listaDicionariosTrabalhos:
                    condicoes = (
                        textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioTrabalhoConcluido[CHAVE_PROFISSAO])
                        and dicionarioTrabalho[CHAVE_NIVEL] == nivelColecao
                        and textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_COMUM))
                    if condicoes:
                        dicionarioTrabalhoEstoque = {
                            CHAVE_NIVEL:dicionarioTrabalho[CHAVE_NIVEL],
                            CHAVE_NOME:dicionarioTrabalho[CHAVE_NOME],
                            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
                            CHAVE_RARIDADE:dicionarioTrabalho[CHAVE_RARIDADE],
                            CHAVE_ID_TRABALHO:dicionarioTrabalho[CHAVE_ID]}
                        listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)
                for dicionarioTrabalhoProduzido in listaDicionarioTrabalhoProduzido:
                    tipoRecurso = retornaChaveTipoRecurso(dicionarioTrabalhoProduzido)
                    if variavelExiste(tipoRecurso):
                        if tipoRecurso == CHAVE_RCT:
                            dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE] = 2
                        if tipoRecurso == CHAVE_RAT or tipoRecurso == CHAVE_RCS:
                            dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE] = 3
                        elif tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RCP:
                            dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE] = 4
                        elif tipoRecurso == CHAVE_RAP:
                            dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE] = 5
                        if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA], CHAVE_LICENCA_APRENDIZ):
                            dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE] = dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE] * 2
                    else:
                        print(f'{D}: Tipo de recurso não encontrado!')
                        linhaSeparacao()
        if tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
                dicionarioTrabalhoEstoque[CHAVE_NIVEL] = dicionarioTrabalhoConcluido[CHAVE_NIVEL]
                dicionarioTrabalhoEstoque[CHAVE_NOME] = dicionarioTrabalhoConcluido[CHAVE_NOME]
                dicionarioTrabalhoEstoque[CHAVE_PROFISSAO] = dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                dicionarioTrabalhoEstoque[CHAVE_RARIDADE] = dicionarioTrabalhoConcluido[CHAVE_RARIDADE]
                dicionarioTrabalhoEstoque[CHAVE_ID_TRABALHO] = dicionarioTrabalhoConcluido[CHAVE_ID_TRABALHO]
                tipoRecurso = retornaChaveTipoRecurso(dicionarioTrabalhoEstoque)
                if variavelExiste(tipoRecurso):
                    if tipoRecurso == CHAVE_RCS or tipoRecurso == CHAVE_RCT:
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = 1
                    elif tipoRecurso == CHAVE_RCP or tipoRecurso == CHAVE_RAP or tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RAT:
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = 2
                    if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA], CHAVE_LICENCA_APRENDIZ):
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] * 2
                    listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)
                else:
                    print(f'{D}: Tipo de recurso não encontrado!')
                    linhaSeparacao()
    else:
        dicionarioTrabalhoEstoque = {
            CHAVE_NIVEL:dicionarioTrabalhoConcluido[CHAVE_NIVEL],
            CHAVE_NOME:dicionarioTrabalhoConcluido[CHAVE_NOME],
            CHAVE_QUANTIDADE:1,
            CHAVE_PROFISSAO:dicionarioTrabalhoConcluido[CHAVE_PROFISSAO],
            CHAVE_RARIDADE:dicionarioTrabalhoConcluido[CHAVE_RARIDADE],
            CHAVE_ID_TRABALHO:dicionarioTrabalhoConcluido[CHAVE_ID_TRABALHO]
        }
        listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)
    print(f'{D}: Lista de dicionários trabalhos concluídos:')
    for dicionarioTrabalhoConcluido in listaDicionarioTrabalhoProduzido:
        for atributo in dicionarioTrabalhoConcluido:
            print(f'{D}: {atributo} - {dicionarioTrabalhoConcluido[atributo]}.')
        linhaSeparacao()
    linhaSeparacao()
    return listaDicionarioTrabalhoProduzido

def modificaExperienciaProfissao(dicionarioTrabalho):
    defineListaDicionariosProfissoesNecessarias()
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        condicoes = (
           textoEhIgual(dicionarioProfissao[CHAVE_NOME],dicionarioTrabalho[CHAVE_PROFISSAO])
           and trabalhoPossuiAtributoExperiencia(dicionarioTrabalho))
        if condicoes:
            caminhoRequisicao = (f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioProfissao[CHAVE_ID]}/.json')
            experiencia = dicionarioProfissao[CHAVE_EXPERIENCIA]+dicionarioTrabalho[CHAVE_EXPERIENCIA]
            if experiencia > 830000:
                experiencia = 830000
            dados = {CHAVE_EXPERIENCIA:experiencia}
            modificaAtributo(caminhoRequisicao,dados)
            dicionarioProfissao[CHAVE_EXPERIENCIA] = experiencia
            print(f'Experiência de {dicionarioProfissao[CHAVE_NOME]} atualizada para {experiencia}.')
            break
    linhaSeparacao()

def trabalhoPossuiAtributoExperiencia(dicionarioTrabalho):
    return CHAVE_EXPERIENCIA in dicionarioTrabalho

def reconheceRecuperaTrabalhoConcluido():
    global dicionarioPersonagemAtributos
    telaInteira = retornaAtualizacaoTela()
    frameNomeTrabalho = telaInteira[285:285+37, 233:486]
    frameNomeTrabalhoBinarizado = retornaImagemBinarizada(frameNomeTrabalho)
    erro = verificaErro(None)
    if not erroEncontrado(erro):
        nomeTrabalhoConcluido = reconheceTexto(frameNomeTrabalhoBinarizado)
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'f2')
        print(f'{D}: Trabalho concluido reconhecido: {nomeTrabalhoConcluido}.')
        if variavelExiste(nomeTrabalhoConcluido):
            erro = verificaErro(None)
            if not erroEncontrado(erro):
                if not dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA]:
                    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = True
                clickContinuo(3, 'up')
                linhaSeparacao()
                return nomeTrabalhoConcluido
            else:
                dicionarioPersonagemAtributos[CHAVE_ESPACO_BOLSA] = False
                clickContinuo(1, 'up')
                clickEspecifico(1, 'left')
    return None

def retornaDicionarioTrabalhoConcluido(nomeTrabalhoConcluido):
    listaPossiveisDicionariosTrabalhos = retornaListaPossiveisDicionariosTrabalhoRecuperado(nomeTrabalhoConcluido)
    if not tamanhoIgualZero(listaPossiveisDicionariosTrabalhos):
        listaDicionariosTrabalhosProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
        for possivelDicionarioTrabalho in listaPossiveisDicionariosTrabalhos:
            for dicionarioTrabalhoProduzirProduzindo in listaDicionariosTrabalhosProduzirProduzindo:
                condicoes = (
                    trabalhoEhProduzindo(dicionarioTrabalhoProduzirProduzindo)
                    and textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME], possivelDicionarioTrabalho[CHAVE_NOME]))
                if condicoes:
                    dicionarioTrabalhoProduzirProduzindo[CHAVE_ID_TRABALHO] = possivelDicionarioTrabalho[CHAVE_ID]
                    dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME_PRODUCAO] = possivelDicionarioTrabalho[CHAVE_NOME_PRODUCAO]
                    return dicionarioTrabalhoProduzirProduzindo
        else:
            print(f'{D}: Trabalho concluído ({listaPossiveisDicionariosTrabalhos[0][CHAVE_NOME]}) não encontrado na lista produzindo...')
            linhaSeparacao()
            return listaPossiveisDicionariosTrabalhos[0]
    return {}

def retornaListaPossiveisDicionariosTrabalhoRecuperado(nomeTrabalhoConcluido):
    listaPossiveisDicionariosTrabalhos = []
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]):
        for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], dicionarioTrabalho[CHAVE_NOME_PRODUCAO]):
                dicionarioTrabalhoConcluido = dicionarioTrabalho
                dicionarioTrabalhoConcluido[CHAVE_ID_TRABALHO] = dicionarioTrabalho[CHAVE_ID]
                dicionarioTrabalhoConcluido[CHAVE_LICENCA] = CHAVE_LICENCA_INICIANTE
                dicionarioTrabalhoConcluido[CHAVE_ESTADO] = CODIGO_CONCLUIDO
                dicionarioTrabalhoConcluido[LC.CHAVE_RECORRENCIA] = False
                listaPossiveisDicionariosTrabalhos.append(dicionarioTrabalho)
    else:
        print(f'{D}: Erro ao definir lista de trabalhos.')
        linhaSeparacao()
    return listaPossiveisDicionariosTrabalhos

def menuLicencasReconhecido(menu):
    return menu==MENU_LICENSAS

def removeTrabalhoEstoque(dicionarioTrabalhoProduzindo):
    caminhoEstoque = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/'
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]):
        if textoEhIgual(dicionarioTrabalhoProduzindo[CHAVE_RARIDADE], CHAVE_RARIDADE_COMUM):
            if trabalhoEhProducaoRecursos(dicionarioTrabalhoProduzindo):
                print(f'{D}: Trabalho é recurso de produção!')
                print(f'{D}: Nome recurso produzido: {dicionarioTrabalhoProduzindo[CHAVE_NOME]}')
                linhaSeparacao()
                dicionarioRecurso = {
                    CHAVE_NOME:dicionarioTrabalhoProduzindo[CHAVE_NOME],
                    CHAVE_PROFISSAO:dicionarioTrabalhoProduzindo[CHAVE_PROFISSAO],
                    CHAVE_NIVEL:dicionarioTrabalhoProduzindo[CHAVE_NIVEL]
                }
                dicionarioRecurso[CHAVE_TIPO] = retornaChaveTipoRecurso(dicionarioRecurso)
                print(f'{D}: Dicionário recurso reconhecido:')
                for atributo in dicionarioRecurso:
                    print(f'{D}: {atributo} - {dicionarioRecurso[atributo]}')
                linhaSeparacao()
                chaveProfissao = limpaRuidoTexto(dicionarioRecurso[CHAVE_PROFISSAO])
                nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 1)
                listaNomeRecursoBuscado = []
                if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 2])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 3])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 6])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 7])
                    listaNomeRecursoBuscado.append([nomeRecursoSecundario, 2])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 8])
                    listaNomeRecursoBuscado.append([nomeRecursoTerciario, 2])
                for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
                    for recursoBuscado in listaNomeRecursoBuscado:
                        if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], recursoBuscado[0]):
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - recursoBuscado[1]
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            dados = {CHAVE_QUANTIDADE:novaQuantidade}
                            caminhoRequisicao = f'{caminhoEstoque}{dicionarioTrabalhoEstoque[CHAVE_ID]}/.json'
                            print(f'{D}: Quantidade de {dicionarioTrabalhoEstoque[CHAVE_NOME]} atualizada de {dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]} para {novaQuantidade}.')
                            modificaAtributo(caminhoRequisicao, dados)
                            dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = novaQuantidade
                    if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], dicionarioTrabalhoProduzindo[CHAVE_LICENCA]):
                        novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - 1
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                        caminhoRequisicao = f'{caminhoEstoque}{dicionarioTrabalhoEstoque[CHAVE_ID]}/.json'
                        print(f'{D}: Quantidade de {dicionarioTrabalhoEstoque[CHAVE_NOME]} atualizada de {dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]} para {novaQuantidade}.')
                        modificaAtributo(caminhoRequisicao, dados)
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = novaQuantidade
            else:
                dicionarioTrabalhoProduzindo = defineQuantidadeRecursos(dicionarioTrabalhoProduzindo)
                dicionarioTrabalhoProduzindo = defineNomeRecursos(dicionarioTrabalhoProduzindo)
                for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
                    caminhoRequisicao = f'{caminhoEstoque}{dicionarioTrabalhoEstoque[CHAVE_ID]}/.json'
                    dados = {}
                    if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], dicionarioTrabalhoProduzindo[CHAVE_NOME_PRIMARIO]):
                        if dicionarioTrabalhoProduzindo[CHAVE_NIVEL] > 14:
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalhoProduzindo[CHAVE_RAP]
                        else:
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalhoProduzindo[CHAVE_RCP]
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                    elif textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], dicionarioTrabalhoProduzindo[CHAVE_NOME_SECUNDARIO]):
                        if dicionarioTrabalhoProduzindo[CHAVE_NIVEL] > 14:
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalhoProduzindo[CHAVE_RAS]
                        else:
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalhoProduzindo[CHAVE_RCS]
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                    elif textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], dicionarioTrabalhoProduzindo[CHAVE_NOME_TERCIARIO]):
                        if dicionarioTrabalhoProduzindo[CHAVE_NIVEL] > 14:
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalhoProduzindo[CHAVE_RAT]
                        else:
                            novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalhoProduzindo[CHAVE_RCT]
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                    elif textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], dicionarioTrabalhoProduzindo[CHAVE_LICENCA]):
                        novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - 1
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                    if not tamanhoIgualZero(dados):
                        print(f'{D}:Quantidade de {dicionarioTrabalhoEstoque[CHAVE_NOME]} atualizada para {novaQuantidade}.')
                        modificaAtributo(caminhoRequisicao, dados)
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = dados[CHAVE_QUANTIDADE]
        elif textoEhIgual(dicionarioTrabalhoProduzindo[CHAVE_RARIDADE], CHAVE_RARIDADE_MELHORADO) or textoEhIgual(dicionarioTrabalhoProduzindo[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO):
            if not trabalhoEhProducaoRecursos(dicionarioTrabalhoProduzindo):
                if CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalhoProduzindo:
                    listaTrabalhosNecessarios = dicionarioTrabalhoProduzindo[CHAVE_TRABALHO_NECESSARIO].split(',')
                    for trabalhoNecessario in listaTrabalhosNecessarios:
                        for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
                            if textoEhIgual(trabalhoNecessario, dicionarioTrabalhoEstoque[CHAVE_NOME]):
                                novaQuantidade = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] - 1
                                if novaQuantidade < 0:
                                    novaQuantidade = 0
                                caminhoRequisicao = f'{caminhoEstoque}{dicionarioTrabalhoEstoque[CHAVE_ID]}/.json'
                                dados = {CHAVE_QUANTIDADE:novaQuantidade}
                                print(f'{D}:Quantidade de {dicionarioTrabalhoEstoque[CHAVE_NOME]} atualizada para {novaQuantidade}.')
                                modificaAtributo(caminhoRequisicao,dados)
                                dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = novaQuantidade
                                break
    else:
        print(f'Lista de estoque está vazia!')
        linhaSeparacao()

def defineCloneDicionarioTrabalhoDesejado(dicionarioTrabalhoDesejado):
    cloneDicionarioTrabalho = {
        CHAVE_ID:None,
        CHAVE_NOME:dicionarioTrabalhoDesejado[CHAVE_NOME],
        CHAVE_NOME_PRODUCAO:dicionarioTrabalhoDesejado[CHAVE_NOME_PRODUCAO],
        CHAVE_ESTADO:CODIGO_PRODUZINDO,
        CHAVE_EXPERIENCIA:dicionarioTrabalhoDesejado[CHAVE_EXPERIENCIA],
        CHAVE_NIVEL:dicionarioTrabalhoDesejado[CHAVE_NIVEL],
        CHAVE_PROFISSAO:dicionarioTrabalhoDesejado[CHAVE_PROFISSAO],
        CHAVE_RARIDADE:dicionarioTrabalhoDesejado[CHAVE_RARIDADE],
        LC.CHAVE_RECORRENCIA:dicionarioTrabalhoDesejado[LC.CHAVE_RECORRENCIA],
        CHAVE_LICENCA:dicionarioTrabalhoDesejado[CHAVE_LICENCA]}
    return cloneDicionarioTrabalho

def trabalhoERecorrente(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][LC.CHAVE_RECORRENCIA]

def menuTrabalhosAtuaisReconhecido(menu):
    return menu==MENU_TRABALHOS_ATUAIS

def erroNaoHaRecursosSuficientes(erro):
    return erro == erroSemRecursos

def menuEscolhaEquipamentoReconhecido(menu):
    return menu==MENU_ESCOLHA_EQUIPAMENTO

def menuTrabalhoEspecificoReconhecido(menu):
    return menu==MENU_TRABALHO_ESPECIFICO

def naoReconheceMenu(menu):
    return menu==MENU_DESCONHECIDO

def iniciaProcessoDeProducao(dicionarioTrabalho):
    global dicionarioPersonagemAtributos
    primeiraBusca = True
    dicionarioTrabalhoDesejado = dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]
    while True:
        menu = retornaMenu()
        if menuTrabalhosAtuaisReconhecido(menu):
            if not tamanhoIgualZero(dicionarioTrabalhoDesejado):
                if trabalhoERecorrente(dicionarioTrabalho):
                    clonaDicionarioTrabalhoDesejado(dicionarioTrabalho, dicionarioTrabalhoDesejado)
                elif not trabalhoERecorrente(dicionarioTrabalho):
                    modificaEstadoDicionarioTrabalhoDesejado(dicionarioTrabalhoDesejado)
                removeTrabalhoEstoque(dicionarioTrabalhoDesejado)
                clickContinuo(12,'up')
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
                break
            else:
                print(f'{D}: Dicionário trabalho desejado está vazio!')
                linhaSeparacao()
                break
        elif menuTrabalhoEspecificoReconhecido(menu):
            if primeiraBusca:
                print(f'{D}: Entra menu licença.')
                linhaSeparacao()
                clickEspecifico(1, 'up')
                clickEspecifico(1, 'enter')
            else:
                print(f'{D}: Clica f2.')
                linhaSeparacao()
                clickEspecifico(1, 'f2')
        elif menuLicencasReconhecido(menu):
            print(f"Buscando: {dicionarioTrabalhoDesejado[CHAVE_LICENCA]}")
            linhaSeparacao()
            textoReconhecido = retornaLicencaReconhecida()
            if variavelExiste(textoReconhecido):
                print(f'Licença reconhecida: {textoReconhecido}.')
                linhaSeparacao()
                if not texto1PertenceTexto2('licençasdeproduçao', textoReconhecido):
                    primeiraBusca = True
                    listaCiclo = []
                    while not texto1PertenceTexto2(textoReconhecido, dicionarioTrabalhoDesejado[CHAVE_LICENCA]):
                        listaCiclo.append(textoReconhecido)
                        clickEspecifico(1, "right")
                        textoReconhecido = retornaLicencaReconhecida()
                        if variavelExiste(textoReconhecido):
                            print(f'Licença reconhecida: {textoReconhecido}.')
                            linhaSeparacao()
                            if textoEhIgual(textoReconhecido, 'nenhumitem'):
                                if textoEhIgual(dicionarioTrabalhoDesejado[CHAVE_LICENCA], 'licença de produção do iniciante'):
                                    if not textoEhIgual(listaCiclo[-1], 'nenhumitem'):
                                        print(f'Sem licenças de produção...')
                                        listaPersonagem = [dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
                                        dicionarioPersonagemAtributos = modificaAtributoPersonagem(dicionarioPersonagemAtributos, listaPersonagem, CHAVE_ESTADO, False)
                                        clickEspecifico(3, 'f1')
                                        clickContinuo(10, 'up')
                                        clickEspecifico(1, 'left')
                                        linhaSeparacao()
                                        break
                                else:
                                    print(f'{dicionarioTrabalhoDesejado[CHAVE_LICENCA]} não encontrado!')
                                    print(f'Licença buscada agora é Licença de produção do iniciante!')
                                    dicionarioTrabalhoDesejado[CHAVE_LICENCA] = 'Licença de produção do iniciante'
                                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoDesejado
                                    linhaSeparacao()
                            else:
                                if len(listaCiclo) > 10:
                                    print(f'{dicionarioTrabalhoDesejado[CHAVE_LICENCA]} não encontrado!')
                                    print(f'Licença buscada agora é Licença de produção do iniciante!')
                                    dicionarioTrabalhoDesejado[CHAVE_LICENCA] = 'Licença de produção do iniciante'
                                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoDesejado
                                    linhaSeparacao()
                        else:
                            erro = verificaErro(None)
                            if erro == erroOutraConexao:
                                dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
                            print(f'Erro ao reconhecer licença!')
                            linhaSeparacao()
                            break
                        primeiraBusca = False
                    else:
                        if primeiraBusca:
                            clickEspecifico(1, "f1")
                        else:
                            clickEspecifico(1, "f2")
                else:
                    print(f'Sem licenças de produção...')
                    listaPersonagem = [dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
                    dicionarioPersonagemAtributos = modificaAtributoPersonagem(dicionarioPersonagemAtributos, listaPersonagem, CHAVE_ESTADO, False)
                    clickEspecifico(3, 'f1')
                    clickContinuo(10, 'up')
                    clickEspecifico(1, 'left')
                    linhaSeparacao()
                    break
            else:
                print(f'Erro ao reconhecer licença!')
                linhaSeparacao()
                break
        elif menuEscolhaEquipamentoReconhecido(menu) or menuAtributosEquipamentoReconhecido(menu):
            print(f'{D}: Clica f2.')
            linhaSeparacao()
            clickEspecifico(1, 'f2')
        else:
            break
        print(f'Tratando possíveis erros...')
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
        tentativas = 1
        erro = verificaErro(dicionarioTrabalhoDesejado)
        while erroEncontrado(erro):
            if erroNaoHaRecursosSuficientes(erro):
                excluiTrabalhoListaDesejos(dicionarioPersonagemAtributos, dicionarioTrabalhoDesejado)
                for posicao in range(len(dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO])):
                    if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO][posicao][CHAVE_ID], dicionarioTrabalhoDesejado[CHAVE_ID]):
                        del dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO][posicao]
                        break
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
            elif erroNaoHaEspacosDeProducao(erro) or erroHaOutraConexao(erro) or erroEstaConectando(erro) or erroReconectando(erro):
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                if erroHaOutraConexao(erro):
                    dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
                elif erroEstaConectando(erro):
                    if tentativas > 10:
                        clickEspecifico(1, 'enter')
                        tentativas = 0
                    tentativas+=1
            erro = verificaErro(dicionarioTrabalhoDesejado)
        linhaSeparacao()
        if not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
            break
        primeiraBusca = False
    return dicionarioTrabalho

def modificaEstadoDicionarioTrabalhoDesejado(dicionarioTrabalhoDesejado):
    print(f'Recorrencia está desligada.')
    caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalhoDesejado[CHAVE_ID]}/.json'
    dados = {
        CHAVE_ESTADO:CODIGO_PRODUZINDO,
        CHAVE_EXPERIENCIA:dicionarioTrabalhoDesejado[CHAVE_EXPERIENCIA]}
    modificaAtributo(caminhoRequisicao, dados)
    for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO]:
        if textoEhIgual(dicionarioTrabalho[CHAVE_ID], dicionarioTrabalhoDesejado[CHAVE_ID]):
            dicionarioTrabalho[CHAVE_ESTADO] = CODIGO_PRODUZINDO
            break
    linhaSeparacao()

def clonaDicionarioTrabalhoDesejado(dicionarioTrabalho, dicionarioTrabalhoDesejado):
    global dicionarioPersonagemAtributos
    print(f'Recorrencia está ligada.')
    cloneDicionarioTrabalhoDesejado = defineCloneDicionarioTrabalhoDesejado(dicionarioTrabalhoDesejado)
    cloneDicionarioTrabalhoDesejado = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, cloneDicionarioTrabalhoDesejado)
    dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(cloneDicionarioTrabalhoDesejado)
    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = cloneDicionarioTrabalhoDesejado
    linhaSeparacao()

def menuAtributosEquipamentoReconhecido(menu):
    return menu == MENU_TRABALHOS_ATRIBUTOS

def erroReconectando(erro):
    return erro == erroRestaurandoConexao

def erroEstaConectando(erro):
    return erro == erroConectando

def erroHaOutraConexao(erro):
    return erro == erroOutraConexao

def erroNaoHaEspacosDeProducao(erro):
    return erro == erroSemEspacosProducao

def retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado):
    if tamanhoIgualZero(listaPersonagemPresenteRecuperado):
        print(f'Limpou a lista...')
        linhaSeparacao()
        listaPersonagemPresenteRecuperado = []
    nomePersonagemReconhecido = retornaNomePersonagem(0)
    if variavelExiste(nomePersonagemReconhecido):
        print(f'{nomePersonagemReconhecido} foi adicionado a lista!')
        linhaSeparacao()
        listaPersonagemPresenteRecuperado.append(nomePersonagemReconhecido)
    else:#ocorreu algum erro
        print(f'Erro ao reconhecer nome...')
        linhaSeparacao()
    return listaPersonagemPresenteRecuperado

def retornaListaDicionariosTrabalhosRarosVendidos():
    print(f'Definindo lista dicionários produtos raros vendidos...')
    listaDicionariosTrabalhosRarosVendidos = []
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]):
        for dicionarioProdutoVendido in dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS]:
            for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
                condicoes = (
                    textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO)
                    and texto1PertenceTexto2(dicionarioTrabalho[CHAVE_NOME], dicionarioProdutoVendido['nomeProduto'])
                    and textoEhIgual(dicionarioProdutoVendido['nomePersonagem'], dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID])
                    and not trabalhoEhProducaoRecursos(dicionarioTrabalho))
                if condicoes:
                    dicionarioTrabalhoRaroVendido = {
                        CHAVE_ID:dicionarioTrabalho[CHAVE_ID],
                        CHAVE_NOME:dicionarioTrabalho[CHAVE_NOME],
                        CHAVE_NOME_PRODUCAO:dicionarioTrabalho[CHAVE_NOME_PRODUCAO],
                        CHAVE_NIVEL:dicionarioTrabalho[CHAVE_NIVEL],
                        CHAVE_RARIDADE:dicionarioTrabalho[CHAVE_RARIDADE],
                        CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
                        CHAVE_QUANTIDADE:dicionarioProdutoVendido['quantidadeProduto'],
                        CHAVE_EXPERIENCIA:dicionarioTrabalho[CHAVE_EXPERIENCIA]}
                    if CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalho:
                        dicionarioTrabalhoRaroVendido[CHAVE_TRABALHO_NECESSARIO] = dicionarioTrabalho[CHAVE_TRABALHO_NECESSARIO]
                    listaDicionariosTrabalhosRarosVendidos.append(dicionarioTrabalhoRaroVendido)
                    break
    linhaSeparacao()
    listaDicionariosTrabalhosRarosVendidosOrdenados = sorted(listaDicionariosTrabalhosRarosVendidos, key = lambda dicionario: (dicionario[CHAVE_PROFISSAO], dicionario[CHAVE_NIVEL], dicionario[CHAVE_NOME]))
    return listaDicionariosTrabalhosRarosVendidosOrdenados

def retornaListaDicionariosTrabalhosRarosVendidosOrdenada(listaDicionariosProdutosRarosVendidos):
    print(f'Definindo lista dicionários produtos raros vendidos ordenada...')
    listaDicionariosProdutosRarosVendidosOrdenada = []
    for dicionariosProdutosRarosVendidos in listaDicionariosProdutosRarosVendidos:
        if tamanhoIgualZero(listaDicionariosProdutosRarosVendidosOrdenada):
            listaDicionariosProdutosRarosVendidosOrdenada.append(dicionariosProdutosRarosVendidos)
        else:
            for dicionariosProdutosRarosVendidosOrdenada in listaDicionariosProdutosRarosVendidosOrdenada:
                if textoEhIgual(dicionariosProdutosRarosVendidosOrdenada[CHAVE_NOME], dicionariosProdutosRarosVendidos[CHAVE_NOME]):
                    dicionariosProdutosRarosVendidosOrdenada[CHAVE_QUANTIDADE] += 1
                    break
            else:
                listaDicionariosProdutosRarosVendidosOrdenada.append(dicionariosProdutosRarosVendidos)
    listaDicionariosProdutosRarosVendidosOrdenada = sorted(listaDicionariosProdutosRarosVendidosOrdenada, key = lambda dicionario: (dicionario[CHAVE_QUANTIDADE], dicionario[CHAVE_NIVEL], dicionario[CHAVE_NOME]), reverse = True)
    for dicionarioTrabalhoRaroVendido in listaDicionariosProdutosRarosVendidosOrdenada:
        for atributo in dicionarioTrabalhoRaroVendido:
            print(f'{D}: {atributo} - {dicionarioTrabalhoRaroVendido[atributo]}.')
        linhaSeparacao()
    return listaDicionariosProdutosRarosVendidosOrdenada

def retornaQuantidadeTrabalhoNoEstoque(nomeTrabalhoRaroVendido):
    for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
        if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], nomeTrabalhoRaroVendido):
            return dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]
    return 0

def retornaQuantidadeTrabalhoListaProduzirProduzindo(nomeTrabalhoRaroVendido):
    listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    quantidadeTrabalhoParaProduzirOuProduzindo = 0
    for dicionarioTrabalhoParaProduzirProduzindo in listaDicionariosTrabalhosParaProduzirProduzindo:
        if textoEhIgual(dicionarioTrabalhoParaProduzirProduzindo[CHAVE_NOME], nomeTrabalhoRaroVendido):
            quantidadeTrabalhoParaProduzirOuProduzindo += 1
    return quantidadeTrabalhoParaProduzirOuProduzindo

def retornaDicinarioTrabalhoNecessario(trabalhoNecessario):
    for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
        if textoEhIgual(dicionarioTrabalho[CHAVE_NOME], trabalhoNecessario):
            return dicionarioTrabalho
    print(F'Diconário trabalho necessário ({trabalhoNecessario}) não encontrado!')
    linhaSeparacao()
    return None

def produzProdutoMaisVendido(listaDicionariosProdutosRarosVendidos):
    listaDicionariosProdutosRarosVendidosOrdenada = retornaListaDicionariosTrabalhosRarosVendidosOrdenada(listaDicionariosProdutosRarosVendidos)
    verificacoes = 0
    for dicionarioProdutoRaroVendido in listaDicionariosProdutosRarosVendidosOrdenada:
        print(f'{D}: {verificacoes+1} verificações.')
        linhaSeparacao()
        if verificacoes >= 4:
            break
        verificacoes = verificaTrabalhoRaroNecessario(verificacoes, dicionarioProdutoRaroVendido)
    print(f'{D}: Fim do processo de verificação de produto mais vendido...')

def verificaTrabalhoRaroNecessario(verificacoes, dicionarioProdutoRaroVendido):
    global dicionarioPersonagemAtributos
    print(f'{D}: Verificando quantidade de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) no estoque...')
    quantidadeTrabalhoRaroNoEstoque = retornaQuantidadeTrabalhoNoEstoque(dicionarioProdutoRaroVendido[CHAVE_NOME])
    quantidadeTrabalhoRaroNecessario = CODIGO_QUANTIDADE_MINIMA_TRABALHO_RARO_EM_ESTOQUE - quantidadeTrabalhoRaroNoEstoque
    if quantidadeTrabalhoRaroNecessario > 0:
        print(f'{D}: Quantidade de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) no estoque é ({quantidadeTrabalhoRaroNoEstoque}).')
        print(f'{D}: Verificando se ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) já está sendo produzido...')
        quantidadeTrabalhoRaroProduzirOuProduzindo = retornaQuantidadeTrabalhoListaProduzirProduzindo(dicionarioProdutoRaroVendido[CHAVE_NOME])
        quantidadeTrabalhoRaroNecessario = quantidadeTrabalhoRaroNecessario - quantidadeTrabalhoRaroProduzirOuProduzindo
        if quantidadeTrabalhoRaroNecessario > 0:
            print(f'{D}: Existem {quantidadeTrabalhoRaroProduzirOuProduzindo} unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) na lista para produzir/produzindo.')
            linhaSeparacao()
            print(f'{D}: Atributos do trabalho raro mais vendido:')
            for atributo in dicionarioProdutoRaroVendido:
                print(f'{D}: {atributo} - {dicionarioProdutoRaroVendido[atributo]}.')
            linhaSeparacao()
            if CHAVE_TRABALHO_NECESSARIO in dicionarioProdutoRaroVendido:
                listaTrabalhosMelhoradosNecessarios = dicionarioProdutoRaroVendido[CHAVE_TRABALHO_NECESSARIO].split(',')
                if not tamanhoIgualZero(listaTrabalhosMelhoradosNecessarios):
                    print(f'{D}: Lista de trabalhos MELHORADOS necessários: ({listaTrabalhosMelhoradosNecessarios}).')
                    if len(listaTrabalhosMelhoradosNecessarios) == 1:
                        dicionarioProfissao = retornaDicionarioProfissaoTrabalho(dicionarioProdutoRaroVendido)
                        _, _, xpMaximo = retornaNivelXpMinimoMaximo(dicionarioProfissao)
                        licencaProducaoIdeal = CHAVE_LICENCA_PRINCIPIANTE
                        if xpMaximo >= 830000:
                            licencaProducaoIdeal = CHAVE_LICENCA_INICIANTE
                        nomeTrabalhoMelhoradoNecessario = listaTrabalhosMelhoradosNecessarios[0]
                        print(f'{D}: Verificando quantidade de ({nomeTrabalhoMelhoradoNecessario}) no estoque...')
                        quantidadeTrabalhoMelhoradoNecessarioNoEstoque = retornaQuantidadeTrabalhoNoEstoque(nomeTrabalhoMelhoradoNecessario)
                        print(f'{D}: Quantidade de ({nomeTrabalhoMelhoradoNecessario}) no estoque é ({quantidadeTrabalhoMelhoradoNecessarioNoEstoque}).')
                        if quantidadeTrabalhoMelhoradoNecessarioNoEstoque >= quantidadeTrabalhoRaroNecessario:
                            if quantidadeTrabalhoMelhoradoNecessarioNoEstoque > 0:
                                print(f'{D}: Adicionando ({quantidadeTrabalhoRaroNecessario}) unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) a lista para produzir/produzindo...')
                                dicionarioProdutoRaroVendido[LC.CHAVE_RECORRENCIA] = False
                                dicionarioProdutoRaroVendido[CHAVE_LICENCA] = licencaProducaoIdeal
                                dicionarioProdutoRaroVendido[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                                for x in range(quantidadeTrabalhoRaroNecessario):
                                    dicionarioProdutoRaroVendido = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioProdutoRaroVendido)
                                    dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioProdutoRaroVendido)
                                linhaSeparacao()
                        elif quantidadeTrabalhoMelhoradoNecessarioNoEstoque < quantidadeTrabalhoRaroNecessario and quantidadeTrabalhoMelhoradoNecessarioNoEstoque >= 0:
                            print(f'{D}: Adicionando ({quantidadeTrabalhoMelhoradoNecessarioNoEstoque}) unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) a lista para produzir/produzindo...')
                            dicionarioProdutoRaroVendido[LC.CHAVE_RECORRENCIA] = False
                            dicionarioProdutoRaroVendido[CHAVE_LICENCA] = licencaProducaoIdeal
                            dicionarioProdutoRaroVendido[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                            for x in range(quantidadeTrabalhoMelhoradoNecessarioNoEstoque):
                                dicionarioProdutoRaroVendido = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioProdutoRaroVendido)
                                dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioProdutoRaroVendido)
                            linhaSeparacao()
                            quantidadeTrabalhoMelhoradoNecessarioFaltante = quantidadeTrabalhoRaroNecessario - quantidadeTrabalhoMelhoradoNecessarioNoEstoque
                            quantidadeTrabalhoMelhoradoNecessarioNaListaProduzirProduzindo = retornaQuantidadeTrabalhoListaProduzirProduzindo(nomeTrabalhoMelhoradoNecessario)
                            quantidadeTrabalhoMelhoradoNecessarioFaltante = quantidadeTrabalhoMelhoradoNecessarioFaltante - quantidadeTrabalhoMelhoradoNecessarioNaListaProduzirProduzindo
                            print(f'{D}: Verificando se ({nomeTrabalhoMelhoradoNecessario}) já está sendo produzido...')
                            print(f'{D}: Existem ({quantidadeTrabalhoMelhoradoNecessarioNaListaProduzirProduzindo}) unidades de ({nomeTrabalhoMelhoradoNecessario}) na lista para produzir/produzindo.')
                            if quantidadeTrabalhoMelhoradoNecessarioFaltante <= 0:
                                print(f'{D}: Passando para o próximo trabalho...')
                                linhaSeparacao()
                            else:
                                verificacoes += 1
                                verificaTrabalhoMelhoradoNecessario(licencaProducaoIdeal, nomeTrabalhoMelhoradoNecessario, quantidadeTrabalhoMelhoradoNecessarioFaltante)
                    elif len(listaTrabalhosMelhoradosNecessarios) == 2:
                        print(f'{D}: Falta desenvolver...')
                        print(f'{D}: Passando para o próximo trabalho...')
                        linhaSeparacao()
                else:
                    print(f'{D}: Lista de trabalhos raros necessários do trabalho ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) está vazia.')
                    print(f'{D}: Passando para o próximo trabalho...')
                    linhaSeparacao()
            else:
                print(f'{D}: Trabalho ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) não possui CHAVE_TRABALHO_NECESSARIO.')
                print(f'{D}: Passando para o próximo trabalho...')
                linhaSeparacao()
        else:
            print(f'{D}: Existem ({quantidadeTrabalhoRaroProduzirOuProduzindo}) unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) sendo produzidos!')
            print(f'{D}: Passando para o próximo trabalho...')
            linhaSeparacao()       
    else:
        print(f'{D}: Existem ({quantidadeTrabalhoRaroNoEstoque}) unidades do produto mais vendido ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) no estoque.')
        print(f'{D}: Passando para o próximo trabalho...')
        linhaSeparacao()
    return verificacoes

def verificaTrabalhoMelhoradoNecessario(licencaProducaoIdeal, nomeTrabalhoMelhoradoNecessario, quantidadeTrabalhoMelhoradoNecessarioFaltante):
    global dicionarioPersonagemAtributos
    dicionarioTrabalhoMelhoradoNecessario = retornaDicinarioTrabalhoNecessario(nomeTrabalhoMelhoradoNecessario)
    if variavelExiste(dicionarioTrabalhoMelhoradoNecessario) and CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalhoMelhoradoNecessario:
        listaTrabalhosComunsNecessarios = dicionarioTrabalhoMelhoradoNecessario[CHAVE_TRABALHO_NECESSARIO].split(',')
        if not tamanhoIgualZero(listaTrabalhosComunsNecessarios):
            if len(listaTrabalhosComunsNecessarios) == 1:
                nomeTrabalhoComumNecessario = listaTrabalhosComunsNecessarios[0]
                print(f'{D}: Verificando quantidade de ({nomeTrabalhoComumNecessario}) no estoque...')
                quantidadeTrabalhoComumNecessarioNoEstoque = retornaQuantidadeTrabalhoNoEstoque(nomeTrabalhoComumNecessario)
                print(f'{D}: Quantidade de ({nomeTrabalhoComumNecessario}) no estoque é ({quantidadeTrabalhoComumNecessarioNoEstoque}).')
                if quantidadeTrabalhoComumNecessarioNoEstoque >= quantidadeTrabalhoMelhoradoNecessarioFaltante:
                    if quantidadeTrabalhoComumNecessarioNoEstoque > 0:
                        print(f'{D}: Adicionando ({quantidadeTrabalhoMelhoradoNecessarioFaltante}) unidades de ({dicionarioTrabalhoMelhoradoNecessario[CHAVE_NOME]}) a lista para produzir/produzindo...')
                        dicionarioTrabalhoMelhoradoNecessario[LC.CHAVE_RECORRENCIA] = False
                        dicionarioTrabalhoMelhoradoNecessario[CHAVE_LICENCA] = licencaProducaoIdeal
                        dicionarioTrabalhoMelhoradoNecessario[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                        for x in range(quantidadeTrabalhoMelhoradoNecessarioFaltante):
                            dicionarioTrabalhoMelhoradoNecessario = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalhoMelhoradoNecessario)
                            dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalhoMelhoradoNecessario)
                        linhaSeparacao()
                elif quantidadeTrabalhoComumNecessarioNoEstoque < quantidadeTrabalhoMelhoradoNecessarioFaltante and quantidadeTrabalhoComumNecessarioNoEstoque >= 0:
                    print(f'{D}: Adicionando ({quantidadeTrabalhoComumNecessarioNoEstoque}) unidades de ({dicionarioTrabalhoMelhoradoNecessario[CHAVE_NOME]}) a lista para produzir/produzindo...')
                    dicionarioTrabalhoMelhoradoNecessario[LC.CHAVE_RECORRENCIA] = False
                    dicionarioTrabalhoMelhoradoNecessario[CHAVE_LICENCA] = licencaProducaoIdeal
                    dicionarioTrabalhoMelhoradoNecessario[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                    for x in range(quantidadeTrabalhoComumNecessarioNoEstoque):
                        dicionarioTrabalhoMelhoradoNecessario = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalhoMelhoradoNecessario)
                        dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalhoMelhoradoNecessario)
                    linhaSeparacao()
                    quantidadeTrabalhoComumNecessarioNaListaProduzirProduzindo = retornaQuantidadeTrabalhoListaProduzirProduzindo(nomeTrabalhoComumNecessario)
                    quantidadeTrabalhoComumNecessarioFaltante = quantidadeTrabalhoMelhoradoNecessarioFaltante - quantidadeTrabalhoComumNecessarioNaListaProduzirProduzindo
                    print(f'{D}: Verificando se ({nomeTrabalhoComumNecessario}) já está sendo produzido...')
                    print(f'{D}: Existem ({quantidadeTrabalhoComumNecessarioNaListaProduzirProduzindo}) unidades de ({nomeTrabalhoComumNecessario}) na lista para produzir/produzindo.')
                    if quantidadeTrabalhoComumNecessarioFaltante <= 0:
                        print(f'{D}: Passando para o próximo trabalho...')
                        linhaSeparacao()
                    else:
                        verificaTrabalhoComumNecessario(nomeTrabalhoComumNecessario, quantidadeTrabalhoComumNecessarioFaltante)
        else:
            print(f'{D}: Lista de trabalhos comuns necessários do trabalho ({dicionarioTrabalhoMelhoradoNecessario[CHAVE_NOME]}) está vazia.')
            print(f'{D}: Passando para o próximo trabalho...')
            linhaSeparacao()
    else:
        print(f'{D}: Trabalho ({dicionarioTrabalhoMelhoradoNecessario[CHAVE_NOME]}) não possui CHAVE_TRABALHO_NECESSARIO.')
        print(f'{D}: Passando para o próximo trabalho...')
        linhaSeparacao()

def verificaTrabalhoComumNecessario(nomeTrabalhoComumNecessario, quantidadeTrabalhoComumNecessarioFaltante):
    dicionarioTrabalhoComumNecessario = retornaDicinarioTrabalhoNecessario(nomeTrabalhoComumNecessario)
    if variavelExiste(dicionarioTrabalhoComumNecessario):
        listaDicionariosRecursos = defineListaDicionarioRecursos(dicionarioTrabalhoComumNecessario)
        for dicionarioRecurso in listaDicionariosRecursos:
            dicionarioRecurso[CHAVE_QUANTIDADE] = dicionarioRecurso[CHAVE_QUANTIDADE] * quantidadeTrabalhoComumNecessarioFaltante
        existemRecursosSuficientes, _ = existemRecursosSuficientesEmEstoque(listaDicionariosRecursos)
        if existemRecursosSuficientes:
            dicionarioTrabalhoComumNecessario[LC.CHAVE_RECORRENCIA] = False
            dicionarioTrabalhoComumNecessario[CHAVE_LICENCA] = CHAVE_LICENCA_INICIANTE
            dicionarioTrabalhoComumNecessario[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
            linhaSeparacao()
            print(f'{D}: Atributos do trabalho comum:')
            for atributo in dicionarioTrabalhoComumNecessario:
                print(f'{D}: {atributo} - {dicionarioTrabalhoComumNecessario[atributo]}.')
            for x in range(quantidadeTrabalhoComumNecessarioFaltante):
                dicionarioTrabalhoComumNecessario = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalhoComumNecessario)
                dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalhoComumNecessario)
            print(f'{D}: Passando para o próximo trabalho...')
            linhaSeparacao()
        else:
            dicionarioTrabalhoProducaoRecursos = retornaDicionarioTrabalhoGrandeProducaoRecursos(dicionarioTrabalhoComumNecessario)
            if not tamanhoIgualZero(dicionarioTrabalhoProducaoRecursos):
                if not verificaTrabalhoProducaoRecursosListaParaProduzirProduzindo(dicionarioTrabalhoProducaoRecursos):
                    dicionarioTrabalhoComumNecessario = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalhoProducaoRecursos)
                    dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalhoComumNecessario)
                else:
                    print(f'{D}: Dicionário trabalho produção de recursos está na lista para produzir/produzindo!')
                    print(f'{D}: Passando para o próximo trabalho...')
                    linhaSeparacao()
            else:
                print(f'{D}: Dicionário trabalho produção de recursos não encontrado!')
                linhaSeparacao()
    else:
        print(f'{D}: Dicionário trabalho comum ({nomeTrabalhoComumNecessario}) não encontrado!')
        print(f'{D}: Passando para o próximo trabalho...')
        linhaSeparacao()

def retornaDicionarioProfissaoTrabalho(dicionarioProdutoRaroVendido):
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if textoEhIgual(dicionarioProfissao[CHAVE_NOME], dicionarioProdutoRaroVendido[CHAVE_PROFISSAO]):
            return dicionarioProfissao
    return {}

def verificaTrabalhoProducaoRecursosListaParaProduzirProduzindo(dicionarioTrabalhoProducaoRecursos):
    listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    for dicionarioTrabalhoParaProduzirProduzindo in listaDicionariosTrabalhosParaProduzirProduzindo:
        condicoes = (textoEhIgual(dicionarioTrabalhoParaProduzirProduzindo[CHAVE_NOME], dicionarioTrabalhoProducaoRecursos[CHAVE_NOME])
            and dicionarioTrabalhoParaProduzirProduzindo[CHAVE_ESTADO] == CODIGO_PARA_PRODUZIR
            and textoEhIgual(dicionarioTrabalhoParaProduzirProduzindo[CHAVE_PROFISSAO], dicionarioTrabalhoProducaoRecursos[CHAVE_PROFISSAO]))
        if condicoes:
            return True
    print(f'Dicionário trabalho produção de recursos ({dicionarioTrabalhoProducaoRecursos[CHAVE_NOME]}, {dicionarioTrabalhoProducaoRecursos[CHAVE_PROFISSAO]}) não encontrado na lista produzir/produzindo!') 
    linhaSeparacao() 
    return False


def retornaDicionarioTrabalhoGrandeProducaoRecursos(dicionarioTrabalhoComumNecessario):
    nivelTrabalhoProducaoRecursos = 3
    if dicionarioTrabalhoComumNecessario[CHAVE_NIVEL] >= 16:
        nivelTrabalhoProducaoRecursos = 10
    for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
        condicoes = (
            dicionarioTrabalho[CHAVE_NIVEL] == nivelTrabalhoProducaoRecursos
            and textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO)
            and trabalhoEhProducaoRecursos(dicionarioTrabalho)
            and textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioTrabalhoComumNecessario[CHAVE_PROFISSAO]))
        if condicoes:
            dicionarioTrabalho[CHAVE_LICENCA] = CHAVE_LICENCA_APRENDIZ
            dicionarioTrabalho[LC.CHAVE_RECORRENCIA] = True
            dicionarioTrabalho[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
            print(f'{D}: Dicionário trabalho produção de recursos:')
            for atributo in dicionarioTrabalho:
                print(f'{D}: {atributo} - {dicionarioTrabalho[atributo]}')
            linhaSeparacao()
            return dicionarioTrabalho
    return {}

def recebeTodasRecompensas(menu):
    listaPersonagemPresenteRecuperado = retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado=[])
    while True:
        reconheceMenuRecompensa(menu)
        if existePixelCorrespondencia():
            vaiParaMenuCorrespondencia()
            recuperaCorrespondencia()
        print(f'Lista: {listaPersonagemPresenteRecuperado}.')
        linhaSeparacao()
        deslogaPersonagem(None)
        if entraPersonagem(listaPersonagemPresenteRecuperado):
            listaPersonagemPresenteRecuperado = retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado)
        else:
            print(f'Todos os personagens foram verificados!')
            linhaSeparacao()
            break
        menu = retornaMenu()

def recuperaPresente():
    evento = 0
    print(f'Buscando recompensa diária...')
    while evento < 2:
        time.sleep(2)
        print(f'Buscando referência "PEGAR"...')
        telaInteira = retornaAtualizacaoTela()
        frameTela = telaInteira[0:telaInteira.shape[0],330:488]
        imagem = retornaImagemCinza(frameTela)
        imagem = cv2.GaussianBlur(imagem,(1,1),0)
        imagem = cv2.Canny(imagem,150,180)
        kernel = np.ones((2,2),np.uint8)
        imagem = retornaImagemDitalata(imagem,kernel,1)
        imagem = retornaImagemErodida(imagem,kernel,1)
        contornos,h1 = cv2.findContours(imagem,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area = cv2.contourArea(cnt)
            if area > 4500 and area < 5700:
                x, y, l, a = cv2.boundingRect(cnt)
                print(f'Area:{area}, x:{x}, y:{y}.')
                cv2.rectangle(frameTela,(x,y),(x+l,y+a),(0,255,0),2)
                frameTratado = frameTela[y:y+a,x:x+l]
                centroX = 330+x+(l/2)
                centroY = y+(a/2)
                print(f'Referência encontrada!')
                clickMouseEsquerdo(1,centroX,centroY)
                posicionaMouseEsquerdo(telaInteira.shape[1]//2,telaInteira.shape[0]//2)
                if verificaErro(None) != 0:
                    evento=2
                    break
                clickEspecifico(1,'f2')
                break
        print(f'Próxima busca.')
        clickContinuo(8,'up')
        clickEspecifico(1,'left')
        linhaSeparacao()
        # mostraImagem(0,frameTela,None)
        evento += 1
    clickEspecifico(2,'f1')

def existemPixelsSuficientes(contadorPixelPreto):
    return contadorPixelPreto>7000 and contadorPixelPreto<11000.

def reconheceMenuRecompensa(menu):
    print(f'Entrou em recuperaPresente.')
    linhaSeparacao()
    if menu == MENU_LOJA_MILAGROSA:
        clickEspecifico(1,'down')
        clickEspecifico(1,'enter')
        recuperaPresente()
    elif menu == MENU_RECOMPENSAS_DIARIAS:
        recuperaPresente()
    else:
        print(f'Recompensa diária já recebida!')
        linhaSeparacao()

def retornaNomePersonagem(posicao):
    print(f'Verificando nome personagem...')
    posicaoNome = [[2,33,169,27], [190,351,177,30]]
    telaInteira = retornaAtualizacaoTela()
    frameNomePersonagem = telaInteira[posicaoNome[posicao][1]:posicaoNome[posicao][1]+posicaoNome[posicao][3], posicaoNome[posicao][0]:posicaoNome[posicao][0]+posicaoNome[posicao][2]]
    frameNomePersonagemTratado = retornaImagemCinza(frameNomePersonagem)
    frameNomePersonagemTratado = retornaImagemEqualizada(frameNomePersonagemTratado)
    frameNomePersonagemTratado = retornaImagemBinarizada(frameNomePersonagemTratado)
    contadorPixelPreto = np.sum(frameNomePersonagemTratado == 0)
    # # print(f'{D}:{contadorPixelPreto}')
    # mostraImagem(0,frameNomePersonagemTratado,None)
    if contadorPixelPreto > 50:
        nomePersonagemReconhecido = reconheceTexto(frameNomePersonagemTratado)
        if variavelExiste(nomePersonagemReconhecido):
            nome = limpaRuidoTexto(nomePersonagemReconhecido)
            print(f'{D}: Personagem reconhecido: {nome}.')
            return nome
        elif contadorPixelPreto > 50:
            return 'provisorioatecair'
    return None

def entraPersonagem(listaPersonagemPresenteRecuperado):
    confirmacao = False
    print(f'Buscando próximo personagem...')
    clickEspecifico(1, 'enter')
    time.sleep(1)
    tentativas = 1
    erro = verificaErro(None)
    while erroEncontrado(erro):
        if erro == erroConectando:
            if tentativas > 10:
                clickEspecifico(2, 'enter')
                tentativas = 0
            tentativas += 1
        erro = verificaErro(None)
    else:
        clickEspecifico(1, 'f2')
        if len(listaPersonagemPresenteRecuperado) == 1:
            clickContinuo(8, 'left')
        else:
            clickEspecifico(1, 'right')
        nomePersonagem = retornaNomePersonagem(1)               
        while True:
            nomePersonagemPresenteado = None
            for nomeLista in listaPersonagemPresenteRecuperado:
                if nomePersonagem == nomeLista and nomePersonagem != None:
                    nomePersonagemPresenteado = nomeLista
                    break
            if nomePersonagemPresenteado != None:
                clickEspecifico(1, 'right')
                nomePersonagem = retornaNomePersonagem(1)
            if nomePersonagem == None:
                print(f'Fim da lista de personagens!')
                linhaSeparacao()
                clickEspecifico(1, 'f1')
                break
            else:
                clickEspecifico(1, 'f2')
                time.sleep(1)
                tentativas = 1
                erro = verificaErro(None)
                while erroEncontrado(erro):
                    if erro == erroReceberRecompensas:
                        break
                    elif erro == erroConectando:
                        if tentativas > 10:
                            clickEspecifico(2, 'enter')
                            tentativas = 0
                        tentativas += 1
                    time.sleep(1.5)
                    erro = verificaErro(None)
                confirmacao = True
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

def retornaAtualizacaoTela():
    screenshot = tiraScreenshot()
    return retornaImagemColorida(screenshot)

def trataMenu(menu):
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
    if menu==MENU_DESCONHECIDO:
        pass
    elif menu==MENU_TRABALHOS_ATUAIS:
        estadoTrabalho = retornaEstadoTrabalho()
        if estadoTrabalho == CODIGO_CONCLUIDO:
            nomeTrabalhoConcluido = reconheceRecuperaTrabalhoConcluido()
            if variavelExiste(nomeTrabalhoConcluido):
                dicionarioTrabalhoConcluido = retornaDicionarioTrabalhoConcluido(nomeTrabalhoConcluido)
                if not tamanhoIgualZero(dicionarioTrabalhoConcluido):
                    dicionarioTrabalhoConcluido = modificaTrabalhoConcluidoListaProduzirProduzindo(dicionarioTrabalhoConcluido)
                    modificaExperienciaProfissao(dicionarioTrabalhoConcluido)
                    atualizaEstoquePersonagem(dicionarioTrabalhoConcluido)
                    verificaProducaoTrabalhoRaro(dicionarioTrabalhoConcluido)
                else:
                    print(f'{D}: Dicionário trabalho concluido não reconhecido.')
                    linhaSeparacao()
            else:
                print(f'{D}: Nome trabalho concluído não reconhecido.')
                linhaSeparacao()
        elif estadoTrabalho == CODIGO_PRODUZINDO:
            # lista_profissao.clear()
            if not existeEspacoProducao():
                print(f'Todos os espaços de produção ocupados.')
                linhaSeparacao()
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
            else:
                clickContinuo(3,'up')
                clickEspecifico(1,'left')
        elif estadoTrabalho==0:
            clickContinuo(3,'up')
            clickEspecifico(1,'left')
    elif menu==MENU_RECOMPENSAS_DIARIAS or menu==MENU_LOJA_MILAGROSA:
        recebeTodasRecompensas(menu)
        for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            if not dicionarioPersonagem[CHAVE_ESTADO]:
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_ID]}/.json'
                dados = {CHAVE_ESTADO:True}
                modificaAtributo(caminhoRequisicao,dados)
                dicionarioPersonagem[CHAVE_ESTADO] = True
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO]=False
    elif menu==MENU_PRINCIPAL:
        clickEspecifico(1,'num1')
        clickEspecifico(1,'num7')
    elif menu==MENU_PERSONAGEM:
        clickEspecifico(1,'num7')
    elif menu==MENU_TRABALHOS_DISPONIVEIS:
        clickEspecifico(1,'up')
        clickEspecifico(2,'left')
    elif menu==MENU_TRABALHO_ESPECIFICO:
        clickEspecifico(1,'f1')
        clickContinuo(3,'up')
        clickEspecifico(2,'left')
    elif menu==MENU_OFERTA_DIARIA:
        clickEspecifico(1,'f1')
    elif menu==MENU_INICIAL:
        clickEspecifico(1,'f2')
        clickEspecifico(1,'num1')
        clickEspecifico(1,'num7')
    else:
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
    erro = verificaErro(None)
    if erro == erroOutraConexao:
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False

def verificaProducaoTrabalhoRaro(dicionarioTrabalhoConcluido):
    global dicionarioPersonagemAtributos
    dicionarioTrabalhoRaro = {}
    dicionarioProfissao = retornaDicionarioProfissaoTrabalho(dicionarioTrabalhoConcluido)
    _, _, xpMaximo = retornaNivelXpMinimoMaximo(dicionarioProfissao)
    licencaProducaoIdeal = CHAVE_LICENCA_PRINCIPIANTE
    if xpMaximo >= 830000:
        licencaProducaoIdeal = CHAVE_LICENCA_INICIANTE
    if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_RARIDADE], CHAVE_RARIDADE_MELHORADO):
        print(f'{D}: Trabalhos MELHORADO. Profissão {dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]}. Nível {dicionarioTrabalhoConcluido[CHAVE_NIVEL]}.')
        for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
            condicoes = (
                textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioTrabalhoConcluido[CHAVE_PROFISSAO])
                and textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO)
                and dicionarioTrabalho[CHAVE_NIVEL] == dicionarioTrabalhoConcluido[CHAVE_NIVEL])
            if condicoes:    
                if CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalho:
                    if textoEhIgual(dicionarioTrabalho[CHAVE_TRABALHO_NECESSARIO], dicionarioTrabalhoConcluido[CHAVE_NOME]):
                        dicionarioTrabalho[CHAVE_LICENCA] = licencaProducaoIdeal
                        dicionarioTrabalho[LC.CHAVE_RECORRENCIA] = False
                        dicionarioTrabalho[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
                        dicionarioTrabalho[CHAVE_EXPERIENCIA] = dicionarioTrabalho[CHAVE_EXPERIENCIA] * 1.5
                        for atributo in dicionarioTrabalho:
                            print(f'{D}: {atributo} - {dicionarioTrabalho[atributo]}.')
                        linhaSeparacao()
                        dicionarioTrabalhoRaro = dicionarioTrabalho
                        break
                else:
                    print(f'{D}: Trabalho não possue CHAVE:{CHAVE_TRABALHO_NECESSARIO}.')
    if not tamanhoIgualZero(dicionarioTrabalhoRaro):
        dicionarioTrabalhoRaro = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalhoRaro)
        dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioTrabalhoRaro)

def atualizaEstoquePersonagem(dicionarioTrabalhoProduzido):
    global dicionarioPersonagemAtributos
    listaDicionarioTrabalhoProduzido = retornaListaDicionarioTrabalhoProduzido(dicionarioTrabalhoProduzido)
    if not tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
        if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]):
            for dicionarioTrabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
                listaDicionarioTrabalhoProduzido, trabalhoEstoque = modificaQuantidadeTrabalhoEstoque(listaDicionarioTrabalhoProduzido, dicionarioTrabalhoEstoque)
                dicionarioTrabalhoEstoque = trabalhoEstoque
            else:
                if not tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
                    for trabalhoProduzido in listaDicionarioTrabalhoProduzido:
                        trabalhoProduzido = adicionaTrabalhoEstoque(dicionarioPersonagemAtributos, trabalhoProduzido)
                        dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE].append(trabalhoProduzido)
        else:
            for trabalhoProduzido in listaDicionarioTrabalhoProduzido:
                trabalhoProduzido = adicionaTrabalhoEstoque(dicionarioPersonagemAtributos, trabalhoProduzido)
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE].append(trabalhoProduzido)

def modificaQuantidadeTrabalhoEstoque(listaDicionarioTrabalhoProduzido, trabalhoEstoque):
    for dicionarioTrabalhoProduzido in listaDicionarioTrabalhoProduzido:
        if textoEhIgual(dicionarioTrabalhoProduzido[CHAVE_NOME], trabalhoEstoque[CHAVE_NOME]):
            novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] + dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE]
            caminhoRequisicao = (f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json')
            dados = {CHAVE_QUANTIDADE:novaQuantidade}
            modificaAtributo(caminhoRequisicao, dados)
            print(f'{trabalhoEstoque[CHAVE_NOME]} - Quantidade: {novaQuantidade}.')
            trabalhoEstoque[CHAVE_QUANTIDADE] = novaQuantidade
            linhaSeparacao()
            for indice in range(len(listaDicionarioTrabalhoProduzido)):
                if listaDicionarioTrabalhoProduzido[indice][CHAVE_NOME] == trabalhoEstoque[CHAVE_NOME]:
                    del listaDicionarioTrabalhoProduzido[indice]
                    break
            if tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
                break
    return listaDicionarioTrabalhoProduzido, trabalhoEstoque
    
def configuraLicenca(dicionarioTrabalho):
    if dicionarioTrabalho==None:
        return None
    return dicionarioTrabalho

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

def retornaConteudoCorrespondencia():
    telaInteira = retornaAtualizacaoTela()
    frameTela = telaInteira[231:231+50,168:168+343]
    textoCarta = reconheceTexto(frameTela)
    dicionarioVenda = {}
    if variavelExiste(textoCarta):
        produto = verificaVendaProduto(textoCarta)
        if variavelExiste(produto):
            if produto:
                print(f'Produto vendido:')
                listaTextoCarta = textoCarta.split()
                quantidadeProduto = retornaQuantidadeProdutoVendido(listaTextoCarta)
                frameTela = telaInteira[490:490+30,410:410+100]
                frameTelaTratado = retornaImagemCinza(frameTela)
                frameTelaTratado = retornaImagemBinarizada(frameTelaTratado)
                ouro = reconhece_digito(frameTelaTratado)
                ouro = re.sub('[^0-9]','',ouro)
                if ouro.isdigit():
                    ouro = int(ouro)
                else:
                    ouro = 0
                dataAtual = str(datetime.date.today())
                listaTextoCarta = ' '.join(listaTextoCarta)
                chaveIdTrabalho = ''
                for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHO]:
                    if texto1PertenceTexto2(dicionarioTrabalho[CHAVE_NOME], listaTextoCarta):
                        chaveIdTrabalho = dicionarioTrabalho[CHAVE_ID]
                        break
                dicionarioVenda = {
                    CHAVE_NOME_PERSONAGEM:dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID],
                    CHAVE_ID_TRABALHO:chaveIdTrabalho,
                    'nomeProduto':listaTextoCarta,
                    'quantidadeProduto':quantidadeProduto,
                    'valorProduto':int(ouro),
                    'dataVenda':dataAtual}
                adicionaVenda(dicionarioPersonagemAtributos, dicionarioVenda)
                for atributo in dicionarioVenda:
                    print(f'{D}: {atributo} - {dicionarioVenda[atributo]}')
                linhaSeparacao()
        else:
            print(f'Erro...')
    return dicionarioVenda

def retornaQuantidadeProdutoVendido(listaTextoCarta):
    x=0
    quantidadeProduto=0
    for texto in listaTextoCarta:
        if texto1PertenceTexto2('x',texto):
            quantidadeProduto=re.sub('[^0-9]','',listaTextoCarta[x])
            if not quantidadeProduto.isdigit():
                quantidadeProduto=re.sub('[^0-9]','',listaTextoCarta[x-1])
                if not quantidadeProduto.isdigit():
                    print(f'Não foi possível reconhecer a quantidade do produto.')
                    linhaSeparacao()
            print(f'quantidadeProduto:{quantidadeProduto}')
        x+=1
    return int(quantidadeProduto)

def verificaVendaProduto(texto):
    if texto1PertenceTexto2('Lote vendido', texto):
        return True
    elif texto1PertenceTexto2('Expirou', texto):
        return False
    return None

def recuperaCorrespondencia():
    verificaTrabalhoRaroVendido = False
    while verificaCaixaCorreio():
        clickEspecifico(1, 'enter')
        dicionarioVenda = retornaConteudoCorrespondencia()
        if not tamanhoIgualZero(dicionarioVenda):
            verificaTrabalhoRaroVendido = True
            atualizaQuantidadeTrabalhoEstoque(dicionarioVenda)
        clickEspecifico(1,'f2')
    else:
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1, 2, 35)
        linhaSeparacao()
    return verificaTrabalhoRaroVendido

def atualizaQuantidadeTrabalhoEstoque(dicionarioVenda):
    for trabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_ESTOQUE]:
        if texto1PertenceTexto2(trabalhoEstoque[CHAVE_ID_TRABALHO], dicionarioVenda[CHAVE_ID_TRABALHO]):
            quantidadeVendida = dicionarioVenda['quantidadeProduto']
            if quantidadeVendida == 0:
                quantidadeVendida = 1
            novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] - quantidadeVendida
            if novaQuantidade < 0:
                novaQuantidade = 0
            caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
            dados = {CHAVE_QUANTIDADE:novaQuantidade}
            modificaAtributo(caminhoRequisicao, dados)
            trabalhoEstoque[CHAVE_QUANTIDADE] = novaQuantidade
            print(f'{D}: Quantidade do trabalho ({trabalhoEstoque[CHAVE_NOME]}) atualizada para {novaQuantidade}.')
            break
    else:
        nomeProduto = dicionarioVenda["nomeProduto"]
        print(f'{D}: Trabalho ({nomeProduto}) não encontrado no estoque.')
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
    x=168
    y=187
    larguraAlturaFrame=64
    telaInteira=retornaAtualizacaoTela()
    contadorItensPercorridos=1
    while contadorItensPercorridos<20:
        # 617
        frameNomeItemBolsa=telaInteira[580:623,180:500]
        frameNomeItemBolsaCinza=retornaImagemCinza(frameNomeItemBolsa)
        frameNomeItemBolsaEqualizada=retornaImagemEqualizada(frameNomeItemBolsaCinza)
        frameNomeItemBolsaBinarizada=retornaImagemBinarizada(frameNomeItemBolsaEqualizada)
        nomeItemBolsaReconhecido=reconheceTexto(frameNomeItemBolsaBinarizada)
        print(f'Item: {nomeItemBolsaReconhecido}')
        mostraImagem(2000,frameNomeItemBolsaBinarizada,nomeItemBolsaReconhecido)
        if nomeItemBolsaReconhecido==None:
            break
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
    
    frame_menu_tratado=retornaImagemCinza(frameMenuOferta)
    frame_menu_tratado=retornaImagemBinarizada(frame_menu_tratado)
    print(reconheceTexto(frame_menu_tratado))
    mostraImagem(0,frameMenuOferta,None)
    # mostra_imagem(0,frameMenuProfissoes,None)
    # mostra_imagem(0,frameMenuVoltar,None)
    # mostra_imagem(0,frameMenuNoticias,None)
    # mostra_imagem(0,frameMenuAvancar,None)
# descobreFrames()

def retornaTextoSair():
    texto = None
    telaInteira = retornaAtualizacaoTela()
    frameTela = telaInteira[telaInteira.shape[0]-50:telaInteira.shape[0]-15,50:50+60]
    frameTelaTratado = retornaImagemCinza(frameTela)
    frameTelaTratado = retornaImagemBinarizada(frameTelaTratado)
    contadorPixelPreto = np.sum(frameTelaTratado==0)
    # print(f'{D}:Quantidade de pixels pretos: {contadorPixelPreto}')
    # mostraImagem(0, frameTelaTratado, None)
    if contadorPixelPreto > 100 and contadorPixelPreto < 400:
        texto = reconheceTexto(frameTelaTratado)
        if variavelExiste(texto):
            texto = limpaRuidoTexto(texto)
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

def defineProfissaoEscolhida(dicionarioUsuario):
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]):  
        mostraLista(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO])
        opcaoProfissao=input('Profissão escolhida: ')
        linhaSeparacao()
        while not opcaoProfissao.isdigit() or int(opcaoProfissao)<0 or int(opcaoProfissao)>len(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]):
            print(f'Opção inválida! Selecione uma das opções.')
            opcaoProfissao=input(f'Sua escolha: ')
            linhaSeparacao()
        else:
            opcaoProfissao=int(opcaoProfissao)
            if opcaoProfissao==0:
                dicionarioUsuario[CHAVE_PROFISSAO]={}
            else:
                x=1
                for profissao in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
                    if x==opcaoProfissao:
                        dicionarioUsuario[CHAVE_PROFISSAO]=profissao
                        break
                    x+=1
    return dicionarioUsuario

def defineTrabalho(dicionarioUsuario):
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_TRABALHO]):
        listaDicionariosTrabalhosBuscados=retornaListaDicionariosTrabalhosBuscados(dicionarioUsuario[CHAVE_LISTA_TRABALHO],dicionarioUsuario[CHAVE_PROFISSAO][CHAVE_NOME],CHAVE_RARIDADE_MELHORADO)
        if not tamanhoIgualZero(listaDicionariosTrabalhosBuscados):
            x=1
            for dicionario in listaDicionariosTrabalhosBuscados:
                print(f'{x} - {dicionario[CHAVE_NIVEL]}:{dicionario[CHAVE_NOME]}.')
                x+=1
            print(f'0 - Voltar.')
            opcaoTrabalho=input(f'Trabalho escolhido: ')
            linhaSeparacao()
            while not opcaoTrabalho.isdigit() or int(opcaoTrabalho)<0 or int(opcaoTrabalho)>len(listaDicionariosTrabalhosBuscados):
                print(f'Opção inválida! Selecione uma das opções.')
                opcaoTrabalho=input(f'Sua escolha: ')
                linhaSeparacao()
            else:
                opcaoTrabalho=int(opcaoTrabalho)
                if opcaoTrabalho==0:
                    dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO]={}
                else:
                    x=1
                    for trabalho in listaDicionariosTrabalhosBuscados:
                        if x==opcaoTrabalho:
                            dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO]=trabalho
                            break
                        x+=1
    return dicionarioUsuario

def defineTrabalhoNecessario(dicionarioUsuario):
    x=1
    listaDicionarioTrabalho=[]
    for trabalho in dicionarioUsuario[CHAVE_LISTA_TRABALHO]:
        if raridadeTrabalhoEhComum(trabalho) and trabalho[CHAVE_NIVEL]==dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_NIVEL]and trabalho[CHAVE_PROFISSAO]==dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_PROFISSAO]:
            print(f'{x} - {trabalho[CHAVE_NIVEL]}:{trabalho[CHAVE_NOME]}.')
            x+=1
            listaDicionarioTrabalho.append(trabalho)
    print(f'0 - Voltar.')
    opcaoTrabalho=input(f'Trabalho escolhido: ')
    linhaSeparacao()
    while not opcaoTrabalho.isdigit() or int(opcaoTrabalho)<0 or int(opcaoTrabalho)>len(listaDicionarioTrabalho):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoTrabalho=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoTrabalho=int(opcaoTrabalho)
        if opcaoTrabalho==0:
            dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO]={}
        else:
            y=1
            for trabalho in listaDicionarioTrabalho:
                if y==opcaoTrabalho:
                    dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO]=trabalho
                    break
                y+=1
    return dicionarioUsuario

def defineAtributoTrabalhoNecessario(dicionarioUsuario):
    dicionarioUsuario=defineProfissaoEscolhida(dicionarioUsuario)
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_PROFISSAO]):
        while True:
            dicionarioUsuario=defineTrabalho(dicionarioUsuario)
            if tamanhoIgualZero(dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO]):
                break
            else:
                dicionarioUsuario=defineTrabalhoNecessario(dicionarioUsuario)
                if tamanhoIgualZero(dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO]):
                    break
                else:
                    # for chave in dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO]:
                    #     print(f'{chave}:{dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO][chave]}.')
                    adicionaAtributoTrabalhoNecessario(dicionarioUsuario)
                # modificaRaridadeTrabalho(dicionarioTrabalho,raridade=CHAVE_RARIDADE_MELHORADO)
    linhaSeparacao()

def mostraListaTrabalhoSemExperiencia(dicionarioUsuario):
    x=1
    listaDicionarioTrabalhoSemXp=[]
    for trabalho in dicionarioUsuario[CHAVE_LISTA_TRABALHO]:
        if textoEhIgual(trabalho[CHAVE_RARIDADE],CHAVE_RARIDADE_COMUM)and trabalho[CHAVE_NIVEL]==1:
            # if trabalhoEProducaoRecursos(trabalho):
            listaDicionarioTrabalhoSemXp.append(trabalho)
    listaDicionarioTrabalhoSemXp=sorted(listaDicionarioTrabalhoSemXp,key=lambda dicionario:(dicionario[CHAVE_PROFISSAO],dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
    for trabalho in listaDicionarioTrabalhoSemXp:
        print(f'{x} - {trabalho[CHAVE_PROFISSAO]}:{trabalho[CHAVE_NOME]}:{trabalho[CHAVE_EXPERIENCIA]}')
        x+=1
    print(f'0 - Voltar')
    opcao=int(input(f'Opção:'))
    trabalhoEscolhido=listaDicionarioTrabalhoSemXp[opcao-1]
    experiencia=int(input(f'XP:'))
    caminhoRequisicao=f'Lista_trabalhos/{trabalhoEscolhido[CHAVE_ID]}/.json'
    dados={CHAVE_EXPERIENCIA:experiencia}
    modificaAtributo(caminhoRequisicao,dados)
    return

def defineAtributoExperienciaTrabalho(dicionarioUsuario):
    raridade=input(f'Raridade: ')
    nivel=int(input(f'Nível: '))
    experiencia=int(input(f'Experiência: '))
    for trabalho in dicionarioUsuario[CHAVE_LISTA_TRABALHO]:
        if textoEhIgual(trabalho[CHAVE_RARIDADE],raridade)and trabalho[CHAVE_NIVEL]==(nivel):
            caminhoRequisicao=f'Lista_trabalhos/{trabalho[CHAVE_ID]}/.json'
            dados={CHAVE_EXPERIENCIA:experiencia}
            modificaAtributo(caminhoRequisicao,dados)
            print(f'ID: {trabalho[CHAVE_ID]}')
            print(f'NOME: {trabalho[CHAVE_NOME]}')
            linhaSeparacao()
    linhaSeparacao()

def definePrioridadeProfissao(dicionarioUsuario):
    if not tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]):
        mostraLista(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO])
        opcaoProfissao = input('Profissão escolhida: ')
        linhaSeparacao()
        while opcaoInvalida(opcaoProfissao,len(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO])):
            print(f'Opção inválida! Selecione uma das opções.')
            opcaoProfissao=input(f'Sua escolha: ')
            linhaSeparacao()
        else:
            opcaoProfissao = int(opcaoProfissao)
            if opcaoProfissao == 0:
                return None
            else:
                dicionarioProfissao=retornaDicionarioProfissaoEscolhida(dicionarioUsuario, opcaoProfissao)
                caminhoRequisicao = f'Usuarios/{dicionarioUsuario[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioProfissao[CHAVE_ID]}/.json'
                if dicionarioProfissao[CHAVE_PRIORIDADE]:
                    print(f'Prioridade inativa!')
                    dados = {CHAVE_PRIORIDADE:False}
                else:
                    print(f'Prioridade ativa!')
                    dados = {CHAVE_PRIORIDADE:True}
                    for dicionarioProfissaoPriorizada in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
                        if dicionarioProfissaoPriorizada[CHAVE_PRIORIDADE]:
                            caminhoRequisicaoProfissaoPriorizada = f'Usuarios/{dicionarioUsuario[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioProfissaoPriorizada[CHAVE_ID]}/.json'
                            dadosProfissaoPriorizada = {CHAVE_PRIORIDADE:False}
                            modificaAtributo(caminhoRequisicaoProfissaoPriorizada,dadosProfissaoPriorizada)
                            break
                modificaAtributo(caminhoRequisicao,dados)
    else:
        print(f'Lista profissão vazia!')
    linhaSeparacao()

def retornaQuantidadeEspacosDeProducao():
    print(f'Define quantidade de espaços de produção...')
    quantidadeEspacosProducao = 2
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        nivel, _ , _= retornaNivelXpMinimoMaximo(dicionarioProfissao)
        dicionarioProfissao[CHAVE_NIVEL] = nivel
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if dicionarioProfissao[CHAVE_NIVEL] >= 5:
            quantidadeEspacosProducao += 1
            break
    listaNiveis = [10, 15, 20, 25]
    for nivel in listaNiveis:
        quantidadeEspacosProducao = retornaContadorEspacosProducao(quantidadeEspacosProducao, nivel)
    print(f'{D}: Espaços de produção disponíveis: {quantidadeEspacosProducao}.')
    linhaSeparacao()
    return quantidadeEspacosProducao

def retornaContadorEspacosProducao(contadorEspacosProducao, nivel):
    contadorNivel = 0
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if dicionarioProfissao[CHAVE_NIVEL] >= nivel:
            contadorNivel += 1
    else:
        print(f'{D}: Contador de profissões nível {nivel} ou superior: {contadorNivel}.')
        if contadorNivel > 0 and contadorNivel < 3:
            contadorEspacosProducao += 1
        elif contadorNivel >= 3:
            contadorEspacosProducao += 2
    return contadorEspacosProducao

def verificaProdutosRarosMaisVendidos():
    listaDicionariosProdutosRarosVendidos = retornaListaDicionariosTrabalhosRarosVendidos()
    if not tamanhoIgualZero(listaDicionariosProdutosRarosVendidos):
        produzProdutoMaisVendido(listaDicionariosProdutosRarosVendidos)
    else:
        print(f'{D}: Lista de trabalhos raros vendidos está vazia!')
        linhaSeparacao()

def adicionaAtributoTrabalhoId(dicionarioUsuario, dicionarioPersonagemAtributos, listaDicionarioTrabalhoEstoque):
    total = len(listaDicionarioTrabalhoEstoque)
    contador = 0
    for dicionarioTrabalhoEstoque in listaDicionarioTrabalhoEstoque:
        contador += 1
        for trabalho in dicionarioUsuario[CHAVE_LISTA_TRABALHO]:
            if textoEhIgual(trabalho[CHAVE_NOME], dicionarioTrabalhoEstoque[CHAVE_NOME]):
                if not CHAVE_ID_TRABALHO in trabalho:
                    caminhoRequisicao = f'Usuarios/{dicionarioUsuario[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{dicionarioTrabalhoEstoque[CHAVE_ID]}.json'
                    dados = {CHAVE_ID_TRABALHO:trabalho[CHAVE_ID]}
                    modificaAtributo(caminhoRequisicao, dados)
                break
        porcentagem = (contador / total) * 100
        print("\n" * os.get_terminal_size().lines)
        print(f'{D}: {porcentagem:,.2f}% concluído...')

def retornaDicionarioProfissaoEscolhida(dicionarioUsuario, opcaoProfissao):
    x=1
    for dicionarioProfissao in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if x==opcaoProfissao:
            break
        x+=1
    return dicionarioProfissao

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
    global dicionarioPersonagemAtributos
    profissaoVerificada = {
        CHAVE_NOME: 'Armadura de tecido'
    }
    trabalhoDesejado={
        CHAVE_ID:'-Ni8Nu1ul0uTMioGLH--',
        CHAVE_NOME:'Luvas do Senhor das profundezas',
        CHAVE_NOME:'Luvas do Senhor das profundezas',
        CHAVE_EXPERIENCIA:795,
        CHAVE_NIVEL:20,
        CHAVE_RARIDADE:'Melhorado',
        CHAVE_PROFISSAO:'Armadura de tecido'
        }
    trabalhoComumDesejado={
        CHAVE_ID:None,
        CHAVE_NOME:'Grande coleção de recursos avançados',
        CHAVE_EXPERIENCIA:90,
        CHAVE_NIVEL:5,
        CHAVE_RARIDADE:CHAVE_RARIDADE_RARO,
        CHAVE_PROFISSAO:'Braceletes',
        LC.CHAVE_RECORRENCIA:False,
        CHAVE_LICENCA:'Licença de produção do principiante',
        CHAVE_ESTADO:0
    }

    dicionarioTrabalhoConcluido = {
        CHAVE_ID:'ntTurggucHAkiTNJD6Fc9uFJM1zF',
        CHAVE_ID_TRABALHO:'',
        CHAVE_NOME:'Clâmide da chama celestial',
        CHAVE_NOME_PRODUCAO:'Melhorar capa do céu Azure',
        CHAVE_EXPERIENCIA:530,
        CHAVE_NIVEL:20,
        CHAVE_RARIDADE:'Melhorado',
        CHAVE_PROFISSAO:'Capotes',
        LC.CHAVE_RECORRENCIA:False,
        CHAVE_LICENCA:'Licença de produção do iniciante',
        CHAVE_ESTADO:2
        }

    dicionarioTrabalho={
        CHAVE_CONFIRMACAO:True,
        CHAVE_POSICAO:0,
        CHAVE_PROFISSAO:'Armadura de tecido',
        CHAVE_DICIONARIO_TRABALHO_DESEJADO:trabalhoDesejado,
        }
    dicionarioPersonagemAtributos = {
        CHAVE_ID_USUARIO:dicionarioUsuario[CHAVE_ID_USUARIO],
        CHAVE_DICIONARIO_PERSONAGEM_EM_USO:dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]
        }
    dicionarioVenda = {
        CHAVE_NOME_PERSONAGEM:dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID],
        'nomeProduto':'Produto vendido teste',
        'quantidadeProduto':1,
        'valorProduto':5000,
        'dataVenda':'00-00-00'
        }
    
    listaPersonagem=[dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
    inicializaChavesPersonagem()
    dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA] = dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO]
    while retornaInputConfirmacao():
        confirmaNomeTrabalho(dicionarioTrabalho, 0)
        pass