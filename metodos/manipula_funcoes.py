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

tela = 'atualizacao_tela.png'

def atualiza_nova_tela():
    imagem = tiraScreenshot()
    salvaNovaTela(imagem)
    print(f'Atualizou a tela.')
    linhaSeparacao()

def atualizaListaProfissao(dicionarioPersonagem):
    print(f'Atualizando lista de profissões...')
    linhaSeparacao()
    listaProfissaoReconhecida = defineListaProfissaoReconhecida()
    if len(listaProfissaoReconhecida) == CHAVE_QUANTIDADE_PROFISSAO:
        verificaProfissao(dicionarioPersonagem, listaProfissaoReconhecida)
        dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]=retornaListaDicionarioProfissao(dicionarioPersonagem)
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]=False
        print(f'Processo de verificação concluído com sucesso!')
    else:
        print(f'Erro ao definir lista de profissões reconhecidas.')
    linhaSeparacao()
    return dicionarioPersonagem

def verificaProfissao(dicionarioPersonagem, listaProfissaoReconhecida):
    listaDicionarioProfissao = dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]
    for posicao in range(len(listaProfissaoReconhecida)):
        if textoEhIgual(listaProfissaoReconhecida[posicao],listaDicionarioProfissao[posicao][CHAVE_NOME]):
            continue
        else:
            dicionarioAux1 = listaDicionarioProfissao[posicao]
            dicionarioAux2 = defineDicionarioAux2(listaDicionarioProfissao, listaProfissaoReconhecida[posicao])
            if not tamanhoIgualZero(dicionarioAux2):
                dados={CHAVE_NOME:dicionarioAux2[CHAVE_NOME],CHAVE_EXPERIENCIA:dicionarioAux2[CHAVE_EXPERIENCIA],CHAVE_PRIORIDADE:dicionarioAux2[CHAVE_PRIORIDADE]}
                caminhoRequisicao=f'Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioAux1[CHAVE_ID]}/.json'
                modificaAtributo(caminhoRequisicao,dados)
                dados={CHAVE_NOME:dicionarioAux1[CHAVE_NOME],CHAVE_EXPERIENCIA:dicionarioAux1[CHAVE_EXPERIENCIA],CHAVE_PRIORIDADE:dicionarioAux1[CHAVE_PRIORIDADE]}
                caminhoRequisicao=f'Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioAux2[CHAVE_ID]}/.json'
                modificaAtributo(caminhoRequisicao,dados)
                dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionarioProfissao(dicionarioPersonagem)
                verificaProfissao(dicionarioPersonagem, listaProfissaoReconhecida)
                break

def defineDicionarioAux2(listaDicionarioProfissao, profissaoReconhecida):
    dicionarioAux2={}
    for dicionarioProfissao in listaDicionarioProfissao:
        if textoEhIgual(profissaoReconhecida,dicionarioProfissao[CHAVE_NOME]):
            dicionarioAux2=dicionarioProfissao
            break
    return dicionarioAux2

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
    estadoTrabalho=para_produzir
    #icone do primeiro espaço de produç 181,295 228,342
    telaInteira=retornaAtualizacaoTela()
    frameTelaInteira=telaInteira[311:311+43, 233:486]
    texto=reconheceTexto(frameTelaInteira)
    if variavelExiste(texto):
        if textoEhIgual("trabalhoconcluído",texto):
            print(f'Trabalho concluído!')
            estadoTrabalho=concluido
        elif texto1PertenceTexto2('adicionarnovo',texto):
            print(f'Nem um trabalho!')
            estadoTrabalho=para_produzir
        else:
            print(f'Em produção...')
            estadoTrabalho=produzindo
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
                    primeiraBusca = False
                    clickEspecifico(1, "right")
                    listaCiclo.append(textoReconhecido)
                    textoReconhecido = retornaLicencaReconhecida()
                    if variavelExiste(textoReconhecido):
                        print(f'Licença reconhecida: {textoReconhecido}.')
                        linhaSeparacao()
                        if texto1PertenceTexto2('nenhumitem', textoReconhecido) or len(listaCiclo) > 10:
                            if textoEhIgual(dicionarioTrabalho[CHAVE_LICENCA], 'Licença de produção do iniciante'):
                                break
                            dicionarioTrabalho[CHAVE_LICENCA] = 'Licença de produção do iniciante'
                            print(f'Licença para trabalho agora é: {dicionarioTrabalho[CHAVE_LICENCA]}.')
                            linhaSeparacao()
                            listaCiclo = []
                    else:
                        print(f'Erro ao reconhecer licença!')
                        linhaSeparacao()
                        break
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
    frameNomeTrabalhoTratado=retornaImagemCinza(frameNomeTrabalho)
    frameNomeTrabalhoTratado=retornaImagemBinarizada(frameNomeTrabalho)
    nomeTrabalhoReconhecido=reconheceTexto(frameNomeTrabalhoTratado)
    # mostraImagem(0,frameNomeTrabalhoTratado,nomeTrabalhoReconhecido)
    if variavelExiste(nomeTrabalhoReconhecido):
        for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
            if texto1PertenceTexto2(nomeTrabalhoReconhecido[3:-1],dicionarioTrabalhoDesejado[CHAVE_NOME].replace('-','')):
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

def defineListaDicionarioTrabalhoComumMelhorado(dicionarioTrabalho):
    listaDicionariosTrabalhosComunsMelhoradosDesejados=[]
    print(f'Buscando trabalho comum na lista...')
    for trabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:#retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
        #se o trabalho na lista de desejo NÃO for da profissão verificada no momento, passa para o proximo trabalho na lista
        if raridadeTrabalhoEhComum(trabalhoDesejado)or raridadeTrabalhoEhMelhorado(trabalhoDesejado):
            print(f'Trabalho comum/melhorado encontado: {trabalhoDesejado[CHAVE_NOME]}.')
            linhaSeparacao()
            listaDicionariosTrabalhosComunsMelhoradosDesejados.append(trabalhoDesejado)
    if tamanhoIgualZero(listaDicionariosTrabalhosComunsMelhoradosDesejados):
        print(f'Nem um trabaho comum na lista!')
        linhaSeparacao()
    dicionarioTrabalho[CHAVE_LISTA_TRABALHO_COMUM_MELHORADO]=listaDicionariosTrabalhosComunsMelhoradosDesejados
    return dicionarioTrabalho

def retornaListaDicionariosTrabalhosBuscados(listaDicionariosTrabalhos,profissao,raridade):
    listaDicionariosTrabalhosBuscados=[]
    listaDicionariosTrabalhosBuscadosOrdenados=[]
    for dicionarioTrabalho in listaDicionariosTrabalhos:
        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO],profissao)and
            textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE],raridade)):
            listaDicionariosTrabalhosBuscados.append(dicionarioTrabalho)
    listaDicionariosTrabalhosBuscadosOrdenados=sorted(listaDicionariosTrabalhosBuscados,key=lambda dicionario:(dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
    return listaDicionariosTrabalhosBuscadosOrdenados

def defineDicionarioTrabalhoComum(dicionarioTrabalho):
    print(f'Buscando trabalho comum.')
    contadorParaBaixo = 0
    if not primeiraBusca(dicionarioTrabalho):
        contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]
        clickEspecifico(contadorParaBaixo, 'down')
    while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
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
            for dicionarioTrabalhoDesejado in dicionarioTrabalho[CHAVE_LISTA_TRABALHO_COMUM_MELHORADO]:
                print(f'Trabalho na lista: {dicionarioTrabalhoDesejado[CHAVE_NOME]}')
                if textoEhIgual(nomeTrabalhoReconhecido, dicionarioTrabalhoDesejado[CHAVE_NOME]):
                    clickEspecifico(1, 'enter')
                    dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM] = contadorParaBaixo
                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoDesejado
                    contadorParaBaixo += 1
                    linhaSeparacao()
                    break
            else:
                linhaSeparacao()
                clickEspecifico(1, 'down')
                dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM] = contadorParaBaixo
                contadorParaBaixo += 1
        else:
            if not primeiraBusca(dicionarioTrabalho):
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                vaiParaMenuTrabalhoEmProducao()
                print(f'Trabalho comum não reconhecido!')
                linhaSeparacao()
                break
            else:
                linhaSeparacao()
                clickEspecifico(1, 'down')
                dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM] = contadorParaBaixo
                contadorParaBaixo += 1
    return dicionarioTrabalho

def vaiParaMenuTrabalhoEmProducao():
    clickEspecifico(1,'f1')
    clickContinuo(9,'up')
    clickEspecifico(1,'left')

def requisitoRaridadecomumProfissaoEstadoproduzirSatisteito(dicionarioTrabalho, trabalhoListaDesejo):
    return raridadeTrabalhoEhComum(trabalhoListaDesejo)and profissaoEIgual(dicionarioTrabalho, trabalhoListaDesejo)and estadoTrabalhoEParaProduzir(trabalhoListaDesejo)

def estadoTrabalhoEParaProduzir(trabalhoListaDesejo):
    return trabalhoListaDesejo[CHAVE_ESTADO]==para_produzir

def profissaoEIgual(dicionarioTrabalho, trabalhoListaDesejo):
    return textoEhIgual(trabalhoListaDesejo[CHAVE_PROFISSAO],dicionarioTrabalho[CHAVE_PROFISSAO])

def raridadeTrabalhoEhComum(trabalhoListaDesejo):
    return textoEhIgual(trabalhoListaDesejo[CHAVE_RARIDADE],'comum')

def raridadeTrabalhoEhMelhorado(trabalhoListaDesejo):
    return textoEhIgual(trabalhoListaDesejo[CHAVE_RARIDADE],'melhorado')

def texto1PertenceTexto2(texto1,texto2):
    # print(f'{D}:{texto1} pertence a {texto2}?')
    return limpaRuidoTexto(texto1)in limpaRuidoTexto(texto2)

def textoEhIgual(texto1,texto2):
    # print(f'{D}:{limpaRuidoTexto(texto1)}.')
    # print(f'{D}:{limpaRuidoTexto(texto2)}.')
    return limpaRuidoTexto(texto1)==limpaRuidoTexto(texto2)

def variavelExiste(variavelVerificada):
    return variavelVerificada!=None

def primeiraBusca(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM]==-1

def limpaRuidoTexto(texto):
    return unidecode(texto).replace(' ','').replace('-','').lower()

def retiraDigitos(texto):
    listaDigitos=['0','1','2','3','4','5','6','7','8','9']
    for digito in listaDigitos:
        texto=texto.replace(digito,'')
    return texto

def trabalhoEhProducaoRecursos(dicionarioTrabalhoLista):
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
        'adquirirfuradordoprincipiante','produzindotecidodenso','extraçãodesubstânciaestável',
        'recebendofibradebronze','recebendoprata','recebendoinsígniadeestudante',
        'recebendofibradeplatina','recebendoâmbar','recebendodistintivodeaprendiz']
    for recurso in listaProducaoRecurso:
        if textoEhIgual(recurso,dicionarioTrabalhoLista[CHAVE_NOME]):
            confirmacao=True
            break
    # print(f'{D}: {dicionarioTrabalhoLista[CHAVE_NOME]} é recurso de produção? {confirmacao}.')
    # linhaSeparacao()
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
    # mostraImagem(0,frameTelaInteira,None)
    #teste trata frame trabalho comum
    frameNomeTrabalhoTratado=retornaImagemCinza(frameTelaInteira)
    frameNomeTrabalhoTratado=retornaImagemBinarizada(frameNomeTrabalhoTratado)
    contadorPixelPreto=np.sum(frameNomeTrabalhoTratado==0)
    # # print(f'{D}:Quantidade de pixels pretos: {contadorPixelPreto}')
    if contadorPixelPreto>0:
        nomeTrabalhoReconhecido=reconheceTexto(frameNomeTrabalhoTratado)
    # # print(f'{D}:Trabalho reconhecido {nomeTrabalhoReconhecido}.')
    return nomeTrabalhoReconhecido

def verificaErro(dicionarioTrabalho):
    dicionarioTrabalho=configuraLicenca(dicionarioTrabalho)
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
    if not erroEncontrado(erro):
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
    # # print(f'{D}:{textoErroEncontrado}')
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
                # # print(f'{D}:"{textoErro}" encontrado em "{textoErroEncontrado}".')
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

def defineListaDicionariosProfissoesNecessarias(dicionarioPersonagem):
    print(f'Verificando profissões necessárias...')
    #cria lista vazia
    dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA] = []
    #abre o arquivo lista de profissoes
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionarioProfissao(dicionarioPersonagem)
    #abre o arquivo lista de desejos
    dicionarioPersonagem[CHAVE_LISTA_DESEJO] = retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
    #percorre todas as linha do aquivo profissoes
    posicao = 1
    for profissao in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        #percorre todas as linhas do aquivo lista de desejos
        for trabalhoDesejado in dicionarioPersonagem[CHAVE_LISTA_DESEJO]:
            if textoEhIgual(profissao[CHAVE_NOME],trabalhoDesejado[CHAVE_PROFISSAO]) and estadoTrabalhoEParaProduzir(trabalhoDesejado):
                #verifca se o indice já está na lista
                dicionarioProfissao = {
                    CHAVE_ID:profissao[CHAVE_ID],
                    CHAVE_NOME:profissao[CHAVE_NOME],
                    CHAVE_PRIORIDADE:profissao[CHAVE_PRIORIDADE],
                    CHAVE_POSICAO:posicao}
                dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA].append(dicionarioProfissao)
                break
        posicao+=1
    else:
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA] = sorted(dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_VERIFICADA],key=lambda dicionario:dicionario[CHAVE_PRIORIDADE],reverse=True)
        mostraProfissoesNecessarias(dicionarioPersonagem)
    return dicionarioPersonagem

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
    contadorPersonagem = 0
    menu = retornaMenu()
    if menu == menu_jogar:
        print(f'Buscando personagem ativo...')
        clickEspecifico(1,'enter')
        time.sleep(1)
        tentativas=1
        erro=verificaErro(None)
        while erroEncontrado(erro):
            if erro==erroConectando:
                if tentativas>10:
                    clickEspecifico(2,'enter')
                    tentativas = 0
                tentativas+=1
            erro=verificaErro(None)
        else:
            clickEspecifico(1,'f2')
            clickContinuo(10,'left')   
            personagemReconhecido=retornaNomePersonagem(1)
            # print(f'{D}:personagem reconhecido: {personagemReconhecido}.')
            dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=None
            while variavelExiste(personagemReconhecido) and contadorPersonagem<13:
                dicionarioPersonagem=confirmaNomePersonagem(personagemReconhecido,dicionarioPersonagem)
                if variavelExiste(dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                    modificaAtributoUso(dicionarioPersonagem,True)
                    clickEspecifico(1,'f2')
                    time.sleep(1)
                    tentativas=1
                    erro=verificaErro(None)
                    while erroEncontrado(erro):
                        if erro==erroOutraConexao:
                            dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
                            contadorPersonagem=14
                            break
                        elif erro==erroConectando:
                            if tentativas>10:
                                clickEspecifico(2,'enter')
                                tentativas = 0
                            tentativas+=1
                        erro=verificaErro(None)
                    else:
                        print(f'Login efetuado com sucesso!')
                        linhaSeparacao()
                        break
                else:
                    clickEspecifico(1,'right')
                    personagemReconhecido=retornaNomePersonagem(1)
                    # # print(f'{D}:personagem reconhecido: {personagemReconhecido}.')
                contadorPersonagem+=1
            else:
                print(f'Personagem não encontrado!')
                linhaSeparacao()
                if retornaMenu()==menu_escolha_p:
                    clickEspecifico(1,'f1')
    elif menu == menu_inicial:
        deslogaPersonagem(dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1][CHAVE_EMAIL], dicionarioPersonagem)
    else:
        clickMouseEsquerdo(1,2,35)
    return dicionarioPersonagem

def confirmaNomePersonagem(personagemReconhecido,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=None
    for dicionarioPersonagemAtivo in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
        # # print(f'{D}:{personagemReconhecido} e {dicionarioPersonagemAtivo[CHAVE_NOME]}.')
        if textoEhIgual(personagemReconhecido,dicionarioPersonagemAtivo[CHAVE_NOME]):
            print(f'Personagem {personagemReconhecido} confirmado!')
            linhaSeparacao()
            dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=dicionarioPersonagemAtivo
            break
    return dicionarioPersonagem

def defineListaDicionarioPersonagemMesmoEmail(dicionarioPersonagemAtributos, dicionarioPersonagemEmUso):
    listaDicionarioPersonagemMesmoEmail=[]
    for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        if textoEhIgual(dicionarioPersonagem[CHAVE_EMAIL],dicionarioPersonagemEmUso[CHAVE_EMAIL]):
            listaDicionarioPersonagemMesmoEmail.append(dicionarioPersonagem)
    return listaDicionarioPersonagemMesmoEmail

def modificaAtributoUso(dicionarioPersonagemAtributos,Chave):
    if Chave:
        dicionarioPersonagemEmUso = dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]
    else:
        dicionarioPersonagemEmUso = dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1]
    listaPersonagemMesmoEmail = defineListaDicionarioPersonagemMesmoEmail(dicionarioPersonagemAtributos, dicionarioPersonagemEmUso)
    if not tamanhoIgualZero(listaPersonagemMesmoEmail):
        for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            if personagem[CHAVE_USO]:
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{personagem[CHAVE_ID]}/.json'
                dados = {
                    CHAVE_USO:False}
                print(f'{D}: Atributo USO de {personagem[CHAVE_NOME]} modificado para FALSO.')
                modificaAtributo(caminhoRequisicao, dados)
                personagem[CHAVE_USO] = False
        for personagemEmUso in listaPersonagemMesmoEmail:
            if personagemEmUso[CHAVE_USO] != Chave:
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{personagemEmUso[CHAVE_ID]}/.json'
                dados = {
                    CHAVE_USO:Chave}
                modificaAtributo(caminhoRequisicao, dados)
                print(f'{D}: Atributo USO de {personagemEmUso[CHAVE_NOME]} modificado para VERDADEIRO.')
        for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            if textoEhIgual(personagem[CHAVE_EMAIL], personagemEmUso[CHAVE_EMAIL]):
                personagem[CHAVE_USO] = True
        linhaSeparacao()
    return dicionarioPersonagemAtributos
        
def preparaPersonagem(dicionarioUsuario):
    #lista_profissao_necessaria é uma matrix onde o indice 0=posição da profissão
    #e o indice 1=nome da profissão
    click_atalho_especifico('alt','tab')
    click_atalho_especifico('win','left')
    dicionarioDadosPersonagem=retornaDicionarioDadosPersonagem(dicionarioUsuario)
    if not tamanhoIgualZero(dicionarioDadosPersonagem):
        if not dicionarioDadosPersonagem[CHAVE_ESTADO]:#se o personagem estiver inativo, troca o estado
            listaPersonagemId=[dicionarioDadosPersonagem[CHAVE_ID]]
            modificaAtributoPersonagem(dicionarioUsuario,listaPersonagemId,CHAVE_ESTADO,True)
        iniciaProcessoBusca(dicionarioUsuario)
    else:
        print(f'Erro ao configurar atributos do personagem!')
        linhaSeparacao()

def defineListaDicionarioPersonagemAtivo(dicionarioPersonagem):
    print(f'Definindo lista de personagem ativo.')
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]=[]
    for personagem in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        if (personagem[CHAVE_ESTADO]or
            personagem[CHAVE_ESTADO]==1):
            dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO].append(personagem)
    # print(f'{D}:Lista de personagens ativos:')
    # for personagem in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
    #     # print(f'{D}:{personagem[CHAVE_NOME]}.')
    linhaSeparacao()
    return dicionarioPersonagem

def iniciaProcessoBusca(dicionarioUsuario):
    dicionarioPersonagemAtributos = {CHAVE_ID_USUARIO:dicionarioUsuario[CHAVE_ID_USUARIO]}
    dicionarioPersonagemAtributos = defineListaDicionarioPersonagem(dicionarioUsuario)
    dicionarioPersonagemAtributos = defineListaDicionarioPersonagemAtivo(dicionarioPersonagemAtributos)
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO] = []
    while True:
        if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
            dicionarioPersonagemAtributos = defineListaDicionarioPersonagem(dicionarioUsuario)
            linhaSeparacao()
            dicionarioPersonagemAtributos = defineListaDicionarioPersonagemAtivo(dicionarioPersonagemAtributos)
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO] = []
        else:#se houver pelo menos um personagem ativo
            dicionarioPersonagemAtributos = defineDicionarioPersonagemEmUso(dicionarioPersonagemAtributos)
            if variavelExiste(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                modificaAtributoUso(dicionarioPersonagemAtributos, True)
                dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = True
                dicionarioPersonagemAtributos[CHAVE_ESPACO_BOLSA] = True
                dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = False
                print('Inicia busca...')
                linhaSeparacao()
                dicionarioPersonagemAtributos = iniciaBuscaTrabalho(dicionarioPersonagemAtributos)
                if dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO]:
                    if haMaisQueUmPersonagemAtivo(dicionarioPersonagemAtributos):
                        clickMouseEsquerdo(1, 2, 35)
                    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO])
                    dicionarioPersonagemAtributos = retiraDicionarioPersonagemListaAtivo(dicionarioPersonagemAtributos)
                else:
                    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO])
                    dicionarioPersonagemAtributos = retiraDicionarioPersonagemListaAtivo(dicionarioPersonagemAtributos)
            else:#se o nome reconhecido não estiver na lista de ativos
                if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]):
                    if configuraLoginPersonagem(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
                        dicionarioPersonagemAtributos = entraPersonagemAtivo(dicionarioPersonagemAtributos)
                else:
                    if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1][CHAVE_EMAIL],dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][0][CHAVE_EMAIL]):
                        dicionarioPersonagemAtributos = entraPersonagemAtivo(dicionarioPersonagemAtributos)
                    elif configuraLoginPersonagem(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
                        dicionarioPersonagemAtributos = entraPersonagemAtivo(dicionarioPersonagemAtributos)

def haMaisQueUmPersonagemAtivo(dicionarioPersonagemAtributos):
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
    # print(f'{D}:{texto}')
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
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_noticias
                elif texto1PertenceTexto2('seleçãodepersonagem',textoMenu):
                    print(f'Menu escolha de personagem...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
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
                                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                                    linhaSeparacao()
                                    return menu_produzir
                                elif texto1PertenceTexto2('voltar',textoMenu):
                                    print(f'Menu trabalhos diponíveis...')
                                    linhaSeparacao()
                                    fim = time.time()
                                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                                    linhaSeparacao()
                                    return menu_trab_disponiveis
                        elif texto1PertenceTexto2('trabalhosatuais',textoMenu):
                            print(f'Menu trabalhos atuais...')
                            linhaSeparacao()
                            fim = time.time()
                            # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                            linhaSeparacao()
                            return menu_trab_atuais
            textoMenu=retornaTextoSair()
            if variavelExiste(textoMenu):
                if textoEhIgual(textoMenu,'sair'):
                    print(f'Menu jogar...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_jogar
            if verificaMenuReferencia():
                print(f'Menu tela inicial...')
                linhaSeparacao()
                fim = time.time()
                # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                linhaSeparacao()
                return menu_inicial
            textoMenu=retornaTextoMenuReconhecido(291,409,100)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('conquistas',textoMenu):
                    print(f'Menu personagem...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_personagem
                elif texto1PertenceTexto2('interagir',textoMenu):
                    print(f'Menu principal...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_principal
            textoMenu=retornaTextoMenuReconhecido(191,319,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('parâmetros',textoMenu):
                    if texto1PertenceTexto2('requisitos',textoMenu):
                        print(f'Menu atributo do trabalho...')
                        linhaSeparacao()
                        fim = time.time()
                        # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                        linhaSeparacao()
                        return menu_trab_atributos
                    else:
                        print(f'Menu licenças...')
                        linhaSeparacao()
                        fim = time.time()
                        # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                        linhaSeparacao()
                        return menu_licencas
            textoMenu=retornaTextoMenuReconhecido(281,429,120)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('profissional',textoMenu):
                    print(f'Menu trabalho específico...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_trab_especifico
            textoMenu=retornaTextoMenuReconhecido(266,269,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('ofertadiária',textoMenu):
                    print(f'Menu oferta diária...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_ofe_diaria
            textoMenu=retornaTextoMenuReconhecido(181,71,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('lojamilagrosa',textoMenu):
                    print(f'Menu loja milagrosa...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_loja_milagrosa
            textoMenu=retornaTextoMenuReconhecido(180,40,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('recompensasdiarias',textoMenu):
                    # # print(f'{D}:Menu recompensas diárias...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_rec_diarias
            textoMenu=retornaTextoMenuReconhecido(180,60,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('recompensasdiarias',textoMenu):
                    print(f'Menu recompensas diárias...')
                    linhaSeparacao()
                    fim = time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_rec_diarias
            textoMenu=retornaTextoMenuReconhecido(310,338,57)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('meu',textoMenu):
                    print(f'Menu meu perfil...')
                    linhaSeparacao()
                    fim=time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_meu_perfil
            
            textoMenu=retornaTextoMenuReconhecido(169,97,75)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('bolsa',textoMenu):
                    print(f'Menu bolsa...')
                    linhaSeparacao()
                    fim=time.time()
                    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_bolsa

    print(f'Menu não reconhecido...')
    linhaSeparacao()
    fim = time.time()
    # # print(f'{D}:Tempo de reconhece_texto: {fim - inicio}')
    linhaSeparacao()
    click_atalho_especifico('win','left')
    click_atalho_especifico('win','left')
    clickMouseEsquerdo(1,35,35)
    verificaErro(None)
    return menu_desconhecido

def deslogaPersonagem(personagemEmail, dicionarioPersonagemAtributos):
    menu = retornaMenu()
    while menu != menu_jogar:
        if menu == menu_inicial:
            encerra_secao()
            break
        elif menu == menu_jogar:
            break
        else:
            clickMouseEsquerdo(1, 2, 35)
        menu = retornaMenu()
    if personagemEmail != None and dicionarioPersonagemAtributos != None:
        modificaAtributoUso(dicionarioPersonagemAtributos, False)

def retiraDicionarioPersonagemListaAtivo(dicionarioPersonagemAtributos):
    dicionarioPersonagemAtributos=defineListaDicionarioPersonagem(dicionarioPersonagemAtributos)
    linhaSeparacao()
    dicionarioPersonagemAtributos=defineListaDicionarioPersonagemAtivo(dicionarioPersonagemAtributos)
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
    # print(f'{D}:Lista de personagem ativo após retirarverificado:')
    # for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
        # print(f'{D}:{personagem[CHAVE_NOME]}.')
    # linhaSeparacao()
    return dicionarioPersonagemAtributos

def defineDicionarioPersonagemEmUso(dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=None
    nomePersonagemReconhecidoTratado=retornaNomePersonagem(0)
    # # print(f'{D}:Nome personagem na posição 0:{nomePersonagemReconhecidoTratado}')
    if variavelExiste(nomePersonagemReconhecidoTratado):
        for dicionarioPersonagemVerificado in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
            if textoEhIgual(nomePersonagemReconhecidoTratado,dicionarioPersonagemVerificado[CHAVE_NOME]):
                print(f'Personagem {nomePersonagemReconhecidoTratado} confirmado!')
                linhaSeparacao()
                dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=dicionarioPersonagemVerificado
    elif nomePersonagemReconhecidoTratado=='provisorioatecair':
        print(f'Nome personagem diferente!')
        linhaSeparacao()
    # print(f'{D}:Personagem ativo reconhecido: {dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]}.')
    # linhaSeparacao()
    return dicionarioPersonagem

def configuraLoginPersonagem(listaDicionarioPersonagensAtivos):
    menu = retornaMenu()
    while menu != menu_jogar:
        if menu == menu_noticias or menu == menu_escolha_p:
            clickEspecifico(1, 'f1')
        elif menu != menu_inicial:
            clickMouseEsquerdo(1, 2, 35)
        else:
            encerra_secao()
        linhaSeparacao()
        menu = retornaMenu()
    else:
        login = logaContaPersonagem(listaDicionarioPersonagensAtivos)
    return login
    
def logaContaPersonagem(listaDicionarioPersonagensAtivos):
    confirmacao=False
    email=listaDicionarioPersonagensAtivos[0][CHAVE_EMAIL]
    senha=listaDicionarioPersonagensAtivos[0][CHAVE_SENHA]
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

def defineListaDicionariosTrabalhosPriorizados(dicionarioTrabalho):
    listaDicionariosTrabalhosDesejadosPriorizados=[]
    for dicionarioTrabalhoLista in dicionarioTrabalho[CHAVE_LISTA_DESEJO]:
        if (estadoTrabalhoEParaProduzir(dicionarioTrabalhoLista)and
            textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO],dicionarioTrabalhoLista[CHAVE_PROFISSAO])):
            if textoEhIgual(dicionarioTrabalhoLista[CHAVE_RARIDADE],'especial'):
                dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=1
            elif textoEhIgual(dicionarioTrabalhoLista[CHAVE_RARIDADE],'raro'):
                if trabalhoEhProducaoRecursos(dicionarioTrabalhoLista):
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=3
                else:
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=2
            else:
                if trabalhoEhProducaoRecursos(dicionarioTrabalhoLista):
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=5
                else:
                    dicionarioTrabalhoLista[CHAVE_PRIORIDADE]=4
            if not tamanhoIgualZero(listaDicionariosTrabalhosDesejadosPriorizados):
                for trabalhoPriorizado in listaDicionariosTrabalhosDesejadosPriorizados:
                    if textoEhIgual(dicionarioTrabalhoLista[CHAVE_NOME],trabalhoPriorizado[CHAVE_NOME]):
                        break
                else:
                    listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
            else:         
                listaDicionariosTrabalhosDesejadosPriorizados.append(dicionarioTrabalhoLista)
    else:
        listaDicionariosTrabalhosDesejadosPriorizadosOrdenada=sorted(listaDicionariosTrabalhosDesejadosPriorizados,key=lambda dicionario:(dicionario[CHAVE_PRIORIDADE],dicionario[CHAVE_NOME]))
        # print(f'{D}: Lista de trabalhos priorizados ordenados:')
        # for trabalho in listaDicionariosTrabalhosDesejadosPriorizadosOrdenada:
        #     for atributo in trabalho:
        #         print(f'{D}:{atributo} = {trabalho[atributo]}')
    dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]=listaDicionariosTrabalhosDesejadosPriorizadosOrdenada
    return dicionarioTrabalho

def retornaListaDicionariosTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos):
    listaDicionariosTrabalhosParaProduzirProduzindo=[]
    listaDicionariosTrabalhosDesejados = retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagemAtributos)
    for dicionarioTrabalhoDesejado in listaDicionariosTrabalhosDesejados:
        if textoEhIgual(dicionarioTrabalhoDesejado[CHAVE_PROFISSAO], 'mantos'): 
            caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalhoDesejado[CHAVE_ID]}/.json'
            dados = {CHAVE_PROFISSAO:'Capotes'}
            modificaAtributo(caminhoRequisicao, dados)
            dicionarioTrabalhoDesejado[CHAVE_PROFISSAO] = 'Capotes'
            print(f'{D}: Profissão de {dicionarioTrabalhoDesejado[CHAVE_NOME]} alterada para Capotes.')
            linhaSeparacao()
        if trabalhoEhParaProduzir(dicionarioTrabalhoDesejado) or trabalhoEhProduzindo(dicionarioTrabalhoDesejado):
            listaDicionariosTrabalhosParaProduzirProduzindo.append(dicionarioTrabalhoDesejado)
    # print(f'{D}: Lista de todos os trabalhos desejados:')
    # for dicionarioTrabalho in listaDicionariosTrabalhosParaProduzirProduzindo:
    #     for atributo in dicionarioTrabalho:
    #         print(f'{D}: {atributo} = {dicionarioTrabalho[atributo]}.')
    #     linhaSeparacao()
    # linhaSeparacao()
    return listaDicionariosTrabalhosParaProduzirProduzindo

def trabalhoEhParaProduzir(dicionarioTrabalhoDesejado):
    return dicionarioTrabalhoDesejado[CHAVE_ESTADO]==para_produzir

def trabalhoEhProduzindo(dicionarioTrabalhoDesejado):
    return dicionarioTrabalhoDesejado[CHAVE_ESTADO]==produzindo

def iniciaBuscaTrabalho(dicionarioPersonagemAtributos):
    erro = verificaErro(None)
    if not erroEncontrado(erro):
        menu = retornaMenu()
        if estaMenuInicial(menu):
            if existePixelCorrespondencia():
                vaiParaMenuCorrespondencia()
                recuperaCorrespondencia(dicionarioPersonagemAtributos)
        while naoEstiverMenuProduzir(menu):
            dicionarioPersonagemAtributos = trataMenu(menu,dicionarioPersonagemAtributos)
            if not chaveConfirmacaoForVerdadeira(dicionarioPersonagemAtributos):
                return dicionarioPersonagemAtributos
            menu = retornaMenu()
        else:
            while defineTrabalhoComumProfissaoPriorizada(dicionarioPersonagemAtributos):
                continue
            listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos)
            dicionarioTrabalho = {
                CHAVE_LISTA_DESEJO:listaDicionariosTrabalhosParaProduzirProduzindo,
                CHAVE_DICIONARIO_TRABALHO_DESEJADO:None}
            if not tamanhoIgualZero(listaDicionariosTrabalhosParaProduzirProduzindo):#verifica se a lista está vazia
                dicionarioPersonagemAtributos = defineListaDicionariosProfissoesNecessarias(dicionarioPersonagemAtributos)
                for profissaoVerificada in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA]:#percorre lista de profissao
                    if not chaveUnicaConexaoForVerdadeira(dicionarioPersonagemAtributos) or not chaveEspacoProducaoForVerdadeira(dicionarioPersonagemAtributos):
                        continue
                    if listaProfissoesFoiModificada(dicionarioPersonagemAtributos):
                        dicionarioPersonagemAtributos = atualizaListaProfissao(dicionarioPersonagemAtributos)
                    print(f'Verificando profissão: {profissaoVerificada[CHAVE_NOME]}')
                    linhaSeparacao()
                    dicionarioTrabalho[CHAVE_PROFISSAO] = profissaoVerificada[CHAVE_NOME]
                    dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_COMUM] = -1
                    dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
                    while chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                        entraProfissaoEspecifica(profissaoVerificada[CHAVE_POSICAO])
                        dicionarioTrabalho = defineListaDicionariosTrabalhosPriorizados(dicionarioTrabalho)
                        if not tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]):
                            dicionarioTrabalho = defineListaDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                            if primeiroTrabalhoDaListaEhRaroOuEspecial(dicionarioTrabalho):
                                dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL] = 0
                                for trabalhoPriorizado in dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA]:
                                    if textoEhIgual(trabalhoPriorizado[CHAVE_RARIDADE],'raro') or textoEhIgual(trabalhoPriorizado[CHAVE_RARIDADE],'especial'):
                                        print(f'Trabalho desejado: {trabalhoPriorizado[CHAVE_NOME]}.')
                                        while naoFizerQuatroVerificacoes(dicionarioTrabalho)and not variavelExiste(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]):
                                            nomeTrabalhoReconhecido = reconheceTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                                            print(f'Trabalho raro/especial reconhecido: {nomeTrabalhoReconhecido}.')
                                            if variavelExiste(nomeTrabalhoReconhecido):
                                                if texto1PertenceTexto2(nomeTrabalhoReconhecido,trabalhoPriorizado[CHAVE_NOME]):
                                                    dicionarioTrabalho = entraTrabalhoEncontrado(dicionarioTrabalho,trabalhoPriorizado)
                                                    if chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                                        dicionarioTrabalho = confirmaNomeTrabalho(dicionarioTrabalho,1)
                                                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                                            dicionarioTrabalho,dicionarioPersonagemAtributos = iniciaProducao(dicionarioTrabalho,dicionarioPersonagemAtributos)
                                                            break
                                                        else:    
                                                            clickEspecifico(1,'f1')
                                                            clickContinuo(dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]+1,'up')
                                                    else:
                                                        break
                                            else:
                                                dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL] = 4
                                            incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                                        dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL] = 0
                                        linhaSeparacao()
                                        if not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                            break
                                else:
                                    if not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                        if tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_TRABALHO_COMUM_MELHORADO]):
                                            saiProfissaoVerificada(dicionarioTrabalho)
                                        else:
                                            dicionarioTrabalho,dicionarioPersonagemAtributos = buscaTrabalhoComumMelhorado(dicionarioTrabalho,dicionarioPersonagemAtributos)
                                            if not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                                break
                            else:
                                dicionarioTrabalho,dicionarioPersonagemAtributos = buscaTrabalhoComumMelhorado(dicionarioTrabalho,dicionarioPersonagemAtributos)
                                if not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                    break
                        else:
                            saiProfissaoVerificada(dicionarioTrabalho)
                        if chaveUnicaConexaoForVerdadeira(dicionarioPersonagemAtributos):
                            if chaveEspacoBolsaForVerdadeira(dicionarioPersonagemAtributos):
                                if retornaEstadoTrabalho() == concluido:
                                    dicionarioPersonagemAtributos,dicionarioTrabalhoConcluido = verificaTrabalhoConcluido(dicionarioPersonagemAtributos)
                                    if not tamanhoIgualZero(dicionarioTrabalhoConcluido):
                                        modificaExperienciaProfissao(dicionarioPersonagemAtributos, dicionarioTrabalhoConcluido)
                                        atualizaEstoquePersonagem(dicionarioPersonagemAtributos,dicionarioTrabalhoConcluido)
                                elif not chaveEspacoProducaoForVerdadeira(dicionarioPersonagemAtributos):
                                    break
                            dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = None
                            clickContinuo(3,'up')
                            clickEspecifico(1,'left')
                            linhaSeparacao()
                            time.sleep(1.5)
                else:
                    if listaProfissoesFoiModificada(dicionarioPersonagemAtributos):
                        dicionarioPersonagemAtributos = atualizaListaProfissao(dicionarioPersonagemAtributos)
                    print(f'Fim da lista de profissões...')
                    linhaSeparacao()
            else:
                print(f'Lista de trabalhos desejados vazia.')
                linhaSeparacao()
                listaPersonagem = [dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
                modificaAtributoPersonagem(dicionarioPersonagemAtributos,listaPersonagem,CHAVE_ESTADO,False)

    elif existeOutraConexao(erro):
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
    return dicionarioPersonagemAtributos

def primeiroTrabalhoDaListaEhRaroOuEspecial(dicionarioTrabalho):
    return (not primeiroTrabalhoDaListaEhComum(dicionarioTrabalho) or
            not primeiroTrabalhoDaListaEhMelhorado(dicionarioTrabalho))

def primeiroTrabalhoDaListaEhMelhorado(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA][0][CHAVE_RARIDADE],'melhorado')

def primeiroTrabalhoDaListaEhComum(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA][0][CHAVE_RARIDADE],'comum')

def saiProfissaoVerificada(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
    print(f'Nem um trabalho disponível está na lista de desejos.')
    clickContinuo(4,'up')
    clickEspecifico(1,'left')
    time.sleep(1)
    linhaSeparacao()

def buscaTrabalhoComumMelhorado(dicionarioTrabalho,dicionarioPersonagem):
    dicionarioTrabalho = defineDicionarioTrabalhoComum(dicionarioTrabalho)
    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
        dicionarioTrabalho, dicionarioPersonagem = iniciaProducao(dicionarioTrabalho,dicionarioPersonagem)
        linhaSeparacao()
    return dicionarioTrabalho,dicionarioPersonagem

def defineTrabalhoComumProfissaoPriorizada(dicionarioPersonagemAtributos):
    confirmacao = True
    print(f'Verifica profissão priorizada!')
    dicionarioProfissaoPrioridade = retornaDicionarioProfissaoPrioridade(dicionarioPersonagemAtributos)
    if not tamanhoIgualZero(dicionarioProfissaoPrioridade):
        nivelProfissao, xpMinimo, xpMaximo = retornaNivelXpMinimoMaximo(dicionarioProfissaoPrioridade)
        xpNecessario = xpMaximo - xpMinimo
        xpRestante = xpNecessario - (dicionarioProfissaoPrioridade[CHAVE_EXPERIENCIA] - xpMinimo)
        nivelProduzTrabalhoComum = retornaNivelProduzTrabalhoComum(nivelProfissao)
        listaDicionarioTrabalhoComum = retornaListaDicionarioTrabalhoComumNivelEspecifico(dicionarioProfissaoPrioridade, nivelProduzTrabalhoComum)
        if not tamanhoIgualZero(listaDicionarioTrabalhoComum):
            listaDicionarioTrabalhoComum = defineQuantidadeTrabalhoEstoque(dicionarioPersonagemAtributos,listaDicionarioTrabalhoComum)
            listaDicionarioTrabalhoComum, quantidadeTrabalhoProduzirProduzindo = defineSomaQuantidadeTrabalhoEstoqueProduzirProduzindo(dicionarioPersonagemAtributos,listaDicionarioTrabalhoComum)
            somaXpProduzirProduzindo = retornaSomaXpTrabalhoProducao(dicionarioPersonagemAtributos,dicionarioProfissaoPrioridade)
            if xpSuficienteParaEvoluir(xpRestante, somaXpProduzirProduzindo):
                quantidadeTrabalhoProduzir = CHAVE_TRABALHO_MAXIMO - quantidadeTrabalhoProduzirProduzindo
                if quantidadeTrabalhoProduzindoMenorQueOPermitido(quantidadeTrabalhoProduzir):
                    listaDicionariosRecursos = defineListaDicionarioRecursos(listaDicionarioTrabalhoComum[0])
                    for dicionarioRecurso in listaDicionariosRecursos:
                        dicionarioRecurso[CHAVE_QUANTIDADE] = dicionarioRecurso[CHAVE_QUANTIDADE] * quantidadeTrabalhoProduzir
                    exitemRecursosSuficientes, listaDicionariosRecursos = existemRecursosSuficientesEmEstoque(listaDicionariosRecursos, dicionarioPersonagemAtributos)
                    if exitemRecursosSuficientes:
                        print(f'{D}: Existem recursos suficientes para produzir: {listaDicionarioTrabalhoComum[0][CHAVE_NOME]} - nível: {nivelProduzTrabalhoComum}.')
                        listaDicionarioTrabalhoComum = sorted(listaDicionarioTrabalhoComum,key=lambda dicionario:dicionario[CHAVE_QUANTIDADE])
                        dicionarioTrabalho = {
                            CHAVE_NOME:listaDicionarioTrabalhoComum[0][CHAVE_NOME],
                            CHAVE_NIVEL:listaDicionarioTrabalhoComum[0][CHAVE_NIVEL],
                            CHAVE_PROFISSAO:listaDicionarioTrabalhoComum[0][CHAVE_PROFISSAO],
                            CHAVE_EXPERIENCIA:listaDicionarioTrabalhoComum[0][CHAVE_EXPERIENCIA],
                            CHAVE_RARIDADE:listaDicionarioTrabalhoComum[0][CHAVE_RARIDADE],
                            CHAVE_RECORRENCIA:False,
                            CHAVE_ESTADO:0,
                            CHAVE_LICENCA:'Licença de produção do iniciante'
                            }
                        adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalho)
                    else:
                        produzRecursoFaltante(dicionarioPersonagemAtributos, listaDicionariosRecursos)
                        confirmacao = False
                        print(f'{D}: Existem unidades suficientes sendo produzidas de todos recursos necessários.')
                        linhaSeparacao()
                else:
                    confirmacao = False
                    print(f'{D}:Quantidade de trabalhos na fila para produzir ou produzindo execede o máximo permitido.')
            else:
                confirmacao = False
                print(f'{D}:Experiência trabalhos para produzir e produzindo é suficiente para evoluir nível da profissão.')    
        else:
            confirmacao = False
            print(f'{D}:Lista dicionário trabalho comum profissão: {dicionarioProfissaoPrioridade[CHAVE_NOME]}, nível: {nivelProduzTrabalhoComum} está vazia!')
    else:
        confirmacao = False
        print(f'{D}:Dicionário profissão priorizada vazio!')
    return confirmacao

def produzRecursoFaltante(dicionarioPersonagemAtributos, listaDicionariosRecursos):
    listaDicionarioTrabalhos = retornaListaDicionariosTrabalhos()
    if not tamanhoIgualZero(listaDicionarioTrabalhos):
        for dicionarioRecurso in listaDicionariosRecursos:
            if dicionarioRecurso[CHAVE_QUANTIDADE] > 0:
                while True:
                    print(f'{D}: Faltam {dicionarioRecurso[CHAVE_QUANTIDADE]} de {dicionarioRecurso[CHAVE_NOME]}.')
                    linhaSeparacao()
                    quantidadeRecursoProduzirProduzindo = retornaQuantidadeRecursoProduzirProduzindo(dicionarioPersonagemAtributos, dicionarioRecurso)
                    if dicionarioRecurso[CHAVE_QUANTIDADE] - quantidadeRecursoProduzirProduzindo > 0:
                            dicionarioTrabalho = defineDicionarioRecursoNecessario(dicionarioRecurso, listaDicionarioTrabalhos)
                            if not tamanhoIgualZero(dicionarioTrabalho):
                                adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalho)
                    else:
                        print(f'{D}: Existem unidades suficientes sendo produzidas de {dicionarioRecurso[CHAVE_NOME]}.')
                        linhaSeparacao()
                        listaDicionariosRecursos = atualizaQuantidadeRecursoLista(listaDicionariosRecursos, dicionarioRecurso)
                        break
    else:
        print(f'Erro ao definir lista de trabalhos!')
        linhaSeparacao()

def defineDicionarioRecursoNecessario(dicionarioRecurso, listaDicionarioTrabalhos):
    for dicionarioTrabalho in listaDicionarioTrabalhos:
        nomeRecursoProduzido = retornaNomeRecursoTrabalhoProducao(dicionarioTrabalho[CHAVE_NOME])
        if variavelExiste(nomeRecursoProduzido):
            if textoEhIgual(nomeRecursoProduzido, dicionarioRecurso[CHAVE_NOME]):
                dicionarioTrabalho[CHAVE_LICENCA] = 'Licença de produção do aprendiz'
                dicionarioTrabalho[CHAVE_RECORRENCIA] = False
                dicionarioTrabalho[CHAVE_ESTADO] = 0
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

def retornaQuantidadeRecursoProduzirProduzindo(dicionarioPersonagemAtributos, dicionarioRecurso):
    listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos)
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
                textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_RARIDADE],'raro')and
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

def existemRecursosSuficientesEmEstoque(listaDicionariosRecursos, dicionarioPersonagemAtributos):
    confirmacao = True
    listaDicionarioTrabalhoEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioPersonagemAtributos)
    chaveProfissao = limpaRuidoTexto(listaDicionariosRecursos[0][CHAVE_PROFISSAO])
    nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 1)
    for dicionarioRecurso in listaDicionariosRecursos:
        for dicionarioTrabalhoEstoque in listaDicionarioTrabalhoEstoque:
            if textoEhIgual(dicionarioRecurso[CHAVE_NOME],dicionarioTrabalhoEstoque[CHAVE_NOME]):
                quantidadeRecursoFaltante = dicionarioRecurso[CHAVE_QUANTIDADE] - dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]
                break
        else:
            quantidadeRecursoFaltante = dicionarioRecurso[CHAVE_QUANTIDADE]
            print(f'{D}: Recurso: {dicionarioRecurso[CHAVE_NOME]} não encontrado no estoque.')
            linhaSeparacao()
        if quantidadeRecursoFaltante > 0:
            confirmacao = False
        if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT:
            if quantidadeRecursoFaltante > 0:
                DR13 = {
                    CHAVE_NOME:nomeRecursoTerciario,
                    CHAVE_NIVEL:1,
                    CHAVE_EXPERIENCIA:5,
                    CHAVE_TIPO:CHAVE_RCT,
                    CHAVE_PROFISSAO:dicionarioRecurso[CHAVE_PROFISSAO],
                    CHAVE_QUANTIDADE:quantidadeRecursoFaltante}
                listaDicionariosRecursos.append(DR13)
                DR11 = {
                    CHAVE_NOME:nomeRecursoPrimario,
                    CHAVE_NIVEL:1,
                    CHAVE_EXPERIENCIA:3,
                    CHAVE_TIPO:CHAVE_RCP,
                    CHAVE_PROFISSAO:dicionarioRecurso[CHAVE_PROFISSAO],
                    CHAVE_QUANTIDADE:(quantidadeRecursoFaltante * 4) + (quantidadeRecursoFaltante * 3)}
                listaDicionariosRecursos.append(DR11)
            else:
                quantidadeRecursoFaltante = 0
            dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
        elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
            if quantidadeRecursoFaltante > 0:
                DR12 = {
                    CHAVE_NOME:nomeRecursoSecundario,
                    CHAVE_NIVEL:1,
                    CHAVE_EXPERIENCIA:4,
                    CHAVE_TIPO:CHAVE_RCS,
                    CHAVE_PROFISSAO:dicionarioRecurso[CHAVE_PROFISSAO],
                    CHAVE_QUANTIDADE:quantidadeRecursoFaltante}
                listaDicionariosRecursos.append(DR12)
                quantidadeR11 = (quantidadeRecursoFaltante * 3.5) + (quantidadeRecursoFaltante * 2)
                for dicionarioRecurso1 in listaDicionariosRecursos:
                    if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                        dicionarioRecurso1[CHAVE_QUANTIDADE] += quantidadeR11
                        break
                else:
                    DR11 = {
                        CHAVE_NOME:nomeRecursoPrimario,
                        CHAVE_NIVEL:1,
                        CHAVE_EXPERIENCIA:3,
                        CHAVE_TIPO:CHAVE_RCP,
                        CHAVE_PROFISSAO:dicionarioRecurso[CHAVE_PROFISSAO],
                        CHAVE_QUANTIDADE:quantidadeR11}
                    listaDicionariosRecursos.append(DR11)
            else:
                quantidadeRecursoFaltante = 0
            dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
        elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
            if quantidadeRecursoFaltante > 0:
                for dicionarioRecurso1 in listaDicionariosRecursos:
                    if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                        dicionarioRecurso1[CHAVE_QUANTIDADE] += (quantidadeRecursoFaltante * 3)
                        break
                else:
                    DR11 = {
                        CHAVE_NOME:nomeRecursoPrimario,
                        CHAVE_NIVEL:1,
                        CHAVE_EXPERIENCIA:3,
                        CHAVE_TIPO:CHAVE_RCP,
                        CHAVE_PROFISSAO:dicionarioRecurso[CHAVE_PROFISSAO],
                        CHAVE_QUANTIDADE:quantidadeRecursoFaltante * 3}
                    listaDicionariosRecursos.append(DR11)
            else:
                quantidadeRecursoFaltante = 0
            dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
        elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
            if quantidadeRecursoFaltante <= 0:
                quantidadeRecursoFaltante = 0
            quantidadeR11 = quantidadeRecursoFaltante * 3
            for dicionarioRecurso1 in listaDicionariosRecursos:
                if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                    dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] + quantidadeR11
                    break
            dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
        elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS:
            if quantidadeRecursoFaltante <= 0:
                quantidadeRecursoFaltante = 0
            quantidadeR11 = quantidadeRecursoFaltante * 2
            for dicionarioRecurso1 in listaDicionariosRecursos:
                if dicionarioRecurso1[CHAVE_TIPO] == CHAVE_RCP:
                    dicionarioRecurso1[CHAVE_QUANTIDADE] = dicionarioRecurso1[CHAVE_QUANTIDADE] + quantidadeR11
                    break
            dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
        elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCP:
            if quantidadeRecursoFaltante <= 0:
                quantidadeRecursoFaltante = 0
            dicionarioRecurso[CHAVE_QUANTIDADE] = quantidadeRecursoFaltante
        listaDicionariosRecursos = sorted(listaDicionariosRecursos,key=lambda dicionario:dicionario[CHAVE_TIPO])
    else:
        print(f'{D}: Lista dicionários recursos depois de subtrair estoque:')
        linhaSeparacao()
        for dicionariosRecursos in listaDicionariosRecursos:
            for atributo in dicionariosRecursos:
                print(f'{D}: {atributo} = {dicionariosRecursos[atributo]}.')
            linhaSeparacao()
        linhaSeparacao()
    return confirmacao, listaDicionariosRecursos 

def quantidadeTrabalhoProduzindoMenorQueOPermitido(quantidadeTrabalhoProduzir):
    return quantidadeTrabalhoProduzir > 0

def xpSuficienteParaEvoluir(xpNecessario, somaXpProduzirProduzindo):
    return xpNecessario - somaXpProduzirProduzindo >= 0

def defineListaDicionarioRecursos(dicionarioTrabalho):
    print(f'Definindo lista de dicionários de recursos.')
    listaDicionariosRecursos = []
    dicionarioTrabalho = defineQuantidadeRecursos(dicionarioTrabalho)
    chaveProfissao = limpaRuidoTexto(dicionarioTrabalho[CHAVE_PROFISSAO])
    nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 1)
    if dicionarioTrabalho[CHAVE_NIVEL] <= 14:
        DRCT = {
            CHAVE_NOME:nomeRecursoTerciario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:5,
            CHAVE_TIPO:CHAVE_RCT,
            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioTrabalho[CHAVE_QUANTIDADE_TERCIARIO]}
        DRCS = {
            CHAVE_NOME:nomeRecursoSecundario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:4,
            CHAVE_TIPO:CHAVE_RCS,
            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioTrabalho[CHAVE_QUANTIDADE_SECUNDARIO]}
        DRCP = {
            CHAVE_NOME:nomeRecursoPrimario,
            CHAVE_NIVEL:1,
            CHAVE_EXPERIENCIA:3,
            CHAVE_TIPO:CHAVE_RCP,
            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioTrabalho[CHAVE_QUANTIDADE_PRIMARIO]}
        DRCP[CHAVE_QUANTIDADE] += (DRCT[CHAVE_QUANTIDADE]*3)+(DRCS[CHAVE_QUANTIDADE]*2)
        listaDicionariosRecursos.append(DRCT)
        listaDicionariosRecursos.append(DRCS)
        listaDicionariosRecursos.append(DRCP)
    else:
        nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 8)
        DRAT = {
            CHAVE_NOME:nomeRecursoTerciario,
            CHAVE_NIVEL:8,
            CHAVE_EXPERIENCIA:130,
            CHAVE_TIPO:CHAVE_RAT,
            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioTrabalho[CHAVE_QUANTIDADE_TERCIARIO]}
        DRAS = {
            CHAVE_NOME:nomeRecursoSecundario,
            CHAVE_NIVEL:8,
            CHAVE_EXPERIENCIA:130,
            CHAVE_TIPO:CHAVE_RAS,
            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioTrabalho[CHAVE_QUANTIDADE_SECUNDARIO]}
        DRAP = {
            CHAVE_NOME:nomeRecursoPrimario,
            CHAVE_NIVEL:8,
            CHAVE_EXPERIENCIA:130,
            CHAVE_TIPO:CHAVE_RAP,
            CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
            CHAVE_QUANTIDADE:dicionarioTrabalho[CHAVE_QUANTIDADE_PRIMARIO]}
        listaDicionariosRecursos.append(DRAT)
        listaDicionariosRecursos.append(DRAS)
        listaDicionariosRecursos.append(DRAP)
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
                        tipoRecurso = CHAVE_RCP
                    elif x == 0 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        tipoRecurso = CHAVE_RAP
                    elif x == 1 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        tipoRecurso = CHAVE_RCS
                    elif x == 1 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        tipoRecurso = CHAVE_RAS
                    elif x == 2 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        tipoRecurso = CHAVE_RCT
                    elif x == 2 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        tipoRecurso = CHAVE_RAT
                    break
    return tipoRecurso

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
        ['criar esfera do aprendiz','esfera do aprendiz'],['produzindo a varinha de madeira','varinha de madeira'],['produzindo cabeça do cajado de jade','cabeça do cajado de jade'],
        ['produzindo cabeça de cajado de ônix','cabeça do cajado de ônix'],['criar esfera do neófito','esfera do neófito'],['produzindo a varinha de aço','varinha de aço'],
        ['extracao de lascas','lascas'],['manipulacao de lascas','minerio de cobre'],['fazer mo do aprendiz','mo do aprendiz'],
        ['preparando lascas de quartzo','lascas de quartzo'],['manipulacao de minerio de cobre','minerio de ferro'],['fazer mo do princiante','mo do principiante'],
        ['adquirir tesoura do aprendiz','tesoura do aprendiz'],['produzindo fio resistente','fio grosseiro'],['fazendo tecido de linho','tecido de linho'],
        ['fazendo tecido de cetim','tecido de cetim'],['comprar tesoura do principiante','tesoura do principiante'],['produzindo fio grosso','fio grosso'],
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
        if textoEhIgual(recurso[0],nomeTrabalhoProducao):
            nomeRecurso = recurso[1]
            break
    return nomeRecurso

def defineQuantidadeRecursos(dicionarioTrabalho):
    print(f'Define quantidade de recursos primário, segundário e terciário.')
    nivelProduzTrabalhoComum = dicionarioTrabalho[CHAVE_NIVEL]
    recursoTerciario = 0
    if nivelProduzTrabalhoComum == 10:
        recursoTerciario = 2
    elif nivelProduzTrabalhoComum == 12:
        recursoTerciario = 4
    elif nivelProduzTrabalhoComum == 14:
        recursoTerciario = 6
    elif nivelProduzTrabalhoComum == 16:
        recursoTerciario = 2
    elif nivelProduzTrabalhoComum == 18:
        recursoTerciario = 4
    elif nivelProduzTrabalhoComum == 20:
        recursoTerciario = 6
    elif nivelProduzTrabalhoComum == 22:
        recursoTerciario = 8
    elif nivelProduzTrabalhoComum == 24:
        recursoTerciario = 10
    elif nivelProduzTrabalhoComum == 26:
        recursoTerciario = 12
    elif nivelProduzTrabalhoComum == 28:
        recursoTerciario = 14
    elif nivelProduzTrabalhoComum == 30:
        recursoTerciario = 16
    elif nivelProduzTrabalhoComum == 32:
        recursoTerciario = 18
    dicionarioTrabalho[CHAVE_QUANTIDADE_TERCIARIO] = recursoTerciario
    dicionarioTrabalho[CHAVE_QUANTIDADE_SECUNDARIO] = recursoTerciario + 1
    dicionarioTrabalho[CHAVE_QUANTIDADE_PRIMARIO] = recursoTerciario + 2
    for atributo in dicionarioTrabalho:
        print(f'{D}: {atributo} - {dicionarioTrabalho[atributo]}.')
    linhaSeparacao()
    return dicionarioTrabalho

def retornaSomaXpTrabalhoProducao(dicionarioPersonagemAtributos,dicionarioProfissaoPrioridade):
    somaXpProduzirProduzindo = 0
    listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos)
    for dicionarioTrabalhoProduzirProduzindo in listaDicionarioTrabalhoProduzirProduzindo:
        if textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_PROFISSAO],dicionarioProfissaoPrioridade[CHAVE_NOME]):
            somaXpProduzirProduzindo += dicionarioTrabalhoProduzirProduzindo[CHAVE_EXPERIENCIA]
    return somaXpProduzirProduzindo

def defineSomaQuantidadeTrabalhoEstoqueProduzirProduzindo(dicionarioPersonagemAtributos,listaDicionarioTrabalhoComum):
    quantidadeTrabalhoProduzirProduzindo = 0
    listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos)
    for dicionarioTrabalhoProduzirProduzindo in listaDicionarioTrabalhoProduzirProduzindo:
        for dicionarioTrabalhoComum in listaDicionarioTrabalhoComum:
            if textoEhIgual(dicionarioTrabalhoProduzirProduzindo[CHAVE_NOME],dicionarioTrabalhoComum[CHAVE_NOME]):
                dicionarioTrabalhoComum[CHAVE_QUANTIDADE] += 1
                quantidadeTrabalhoProduzirProduzindo += 1
    return listaDicionarioTrabalhoComum, quantidadeTrabalhoProduzirProduzindo

def defineQuantidadeTrabalhoEstoque(dicionarioPersonagemAtributos,listaDicionarioTrabalhoComum):
    listaDicionarioTrabalhoEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioPersonagemAtributos)
    for dicionarioTrabalhoComum in listaDicionarioTrabalhoComum:
        for dicionarioTrabalhoEstoque in listaDicionarioTrabalhoEstoque:
            if textoEhIgual(dicionarioTrabalhoComum[CHAVE_NOME], dicionarioTrabalhoEstoque[CHAVE_NOME]):
                dicionarioTrabalhoComum[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE]
                break
        else:
            dicionarioTrabalhoComum[CHAVE_QUANTIDADE] = 0
    return listaDicionarioTrabalhoComum

def retornaListaDicionarioTrabalhoComumNivelEspecifico(dicionarioProfissaoPrioridade, nivelProduzTrabalhoComum):
    listaDicionarioTrabalhoComum = []
    listaDicionarioTrabalhos = retornaListaDicionariosTrabalhos()
    for dicionarioTrabalho in listaDicionarioTrabalhos:
        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO],dicionarioProfissaoPrioridade[CHAVE_NOME])and
            dicionarioTrabalho[CHAVE_NIVEL]==nivelProduzTrabalhoComum and
            textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE],'Comum')):
            listaDicionarioTrabalhoComum.append(dicionarioTrabalho)
    return listaDicionarioTrabalhoComum

def retornaNivelProduzTrabalhoComum(nivelProfissao):
    if nivelProfissao == 1:
        nivelProduzTrabalhoComum = 1
    elif nivelProfissao == 8:
        nivelProduzTrabalhoComum = 8
    elif nivelProfissao >= 2 and nivelProfissao < 4:
        nivelProduzTrabalhoComum = 10
    elif nivelProfissao >= 4 and nivelProfissao < 6:
        nivelProduzTrabalhoComum = 12
    elif nivelProfissao >= 6 and nivelProfissao < 8:
        nivelProduzTrabalhoComum = 14
    elif nivelProfissao >= 9 and nivelProfissao < 11:
        nivelProduzTrabalhoComum = 16
    elif nivelProfissao >= 11 and nivelProfissao < 13:
        nivelProduzTrabalhoComum = 18
    elif nivelProfissao >= 13 and nivelProfissao < 15:
        nivelProduzTrabalhoComum = 20
    elif nivelProfissao >= 15 and nivelProfissao < 17:
        nivelProduzTrabalhoComum = 22
    elif nivelProfissao >= 17 and nivelProfissao < 19:
        nivelProduzTrabalhoComum = 24
    elif nivelProfissao >= 19 and nivelProfissao < 21:
        nivelProduzTrabalhoComum = 26
    elif nivelProfissao >= 21 and nivelProfissao < 23:
        nivelProduzTrabalhoComum = 28
    elif nivelProfissao >= 23 and nivelProfissao < 25:
        nivelProduzTrabalhoComum = 30
    elif nivelProfissao >= 25 and nivelProfissao < 27:
        nivelProduzTrabalhoComum = 32
    return nivelProduzTrabalhoComum

def retornaNivelXpMinimoMaximo(dicionarioProfissaoPrioridade):
    listaXPMaximo = [20,200,540,1250,2550,4700,7990,12770,19440,28440,40270,55450,74570,98250,127180,156110,185040,215000,245000,300000,375000,470000,585000,720000,875000,1050000]
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
    return nivelProfissao,xpMinimo,xpMaximo

def retornaDicionarioProfissaoPrioridade(dicionarioPersonagemAtributos):
    dicionarioProfissaoPrioridade = {}
    listaDicionarioProfissao = retornaListaDicionarioProfissao(dicionarioPersonagemAtributos)
    if not tamanhoIgualZero(listaDicionarioProfissao):
        for dicionarioProfissao in listaDicionarioProfissao:
            if dicionarioProfissao[CHAVE_PRIORIDADE]:
                dicionarioProfissaoPrioridade = dicionarioProfissao
                print(f'{D}: Dicionário profissão priorizada:')
                for chaveAtributo in dicionarioProfissaoPrioridade:
                    print(f'{D}:{chaveAtributo}:{dicionarioProfissao[chaveAtributo]}.')
                break
            elif dicionarioProfissao[CHAVE_NOME] == 'capotes':
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioProfissao[CHAVE_ID]}/.json'
                dados = {
                    CHAVE_NOME:'Capotes'
                }
                modificaAtributo(caminhoRequisicao, dados)
        else:
            print(f'{D}:Nenhuma profissão priorizada!')
    else:
        print(f'{D}:Lista profissões vazia!')
    linhaSeparacao()
    return dicionarioProfissaoPrioridade

def reconheceTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho):
    yinicialNome = (dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]*70)+285
    return retornaNomeTrabalhoReconhecido(yinicialNome,0)

def chaveEspacoProducaoForVerdadeira(dicionarioPersonagemAtributos):
    # # print(f'{D}:CHAVE_ESPACO_PRODUCAO={dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]}.')
    return dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]

def incrementaChavePosicaoTrabalho(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_POSICAO_TRABALHO_RARO_ESPECIAL]+=1

def chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
    # # print(f'{D}:CHAVE_DICIONARIO_TRABALHO_DESEJADO: {dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]}.')
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

def chaveConfirmacaoForVerdadeira(dicionario):
    return dicionario[CHAVE_CONFIRMACAO]

def naoEstiverMenuProduzir(menu):
    return menu!=menu_produzir

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
    return menu==menu_inicial

def verificaTrabalhoConcluido(dicionarioPersonagemAtributos):
    dicionarioPersonagemAtributos,dicionarioTrabalhoConcluido=defineDicionarioTrabalhoConcluido(dicionarioPersonagemAtributos)
    if not tamanhoIgualZero(dicionarioTrabalhoConcluido):
        if dicionarioTrabalhoConcluido[CHAVE_RECORRENCIA]:
            print(f'Trabalho recorrente.')
            excluiTrabalho(dicionarioPersonagemAtributos,dicionarioTrabalhoConcluido)
        else:
            print(f'Trabalho sem recorrencia.')
            caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalhoConcluido[CHAVE_ID]}/.json'
            dados = {
                CHAVE_ESTADO:2,
                CHAVE_EXPERIENCIA:dicionarioTrabalhoConcluido[CHAVE_EXPERIENCIA],
                CHAVE_ID:dicionarioTrabalhoConcluido[CHAVE_ID],
                CHAVE_NIVEL:dicionarioTrabalhoConcluido[CHAVE_NIVEL],
                CHAVE_NOME:dicionarioTrabalhoConcluido[CHAVE_NOME],
                CHAVE_PROFISSAO:dicionarioTrabalhoConcluido[CHAVE_PROFISSAO],
                CHAVE_RARIDADE:dicionarioTrabalhoConcluido[CHAVE_RARIDADE],
                CHAVE_RECORRENCIA:dicionarioTrabalhoConcluido[CHAVE_RECORRENCIA],
                CHAVE_LICENCA:dicionarioTrabalhoConcluido[CHAVE_LICENCA]}
            modificaAtributo(caminhoRequisicao,dados)
        linhaSeparacao()
        if not dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]:
            dicionarioPersonagemAtributos=defineChaveEspacoProducaoVerdadeiro(dicionarioPersonagemAtributos)
    return dicionarioPersonagemAtributos,dicionarioTrabalhoConcluido

def defineChaveEspacoProducaoVerdadeiro(dicionarioPersonagem):
    listaPersonagem=[dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
    modificaAtributoPersonagem(dicionarioPersonagem,listaPersonagem,CHAVE_ESPACO_PRODUCAO,True)
    dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]=True
    return dicionarioPersonagem

def retornaListaDicionarioTrabalhoProduzido(dicionarioTrabalhoConcluido):
    listaDicionarioTrabalhoProduzido = []
    dicionarioTrabalhoEstoque = {}
    if trabalhoEhProducaoRecursos(dicionarioTrabalhoConcluido):
        if trabalhoEhProducaoLicenca(dicionarioTrabalhoConcluido):
            dicionarioTrabalhoEstoque = {
                CHAVE_NIVEL:0,
                CHAVE_NOME:'Licença de produção do aprendiz',
                CHAVE_QUANTIDADE:2,
                CHAVE_PROFISSAO:None,
                CHAVE_RARIDADE:'Recurso'
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
                if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA], 'licençadeproduçãodoaprendiz'):
                    dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] * 2
        if not tamanhoIgualZero(dicionarioTrabalhoEstoque):
            listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)
        if trabalhoEhColecaoRecursosComuns(dicionarioTrabalhoConcluido):
                DPC = {
                    CHAVE_NOME:None,
                    CHAVE_NIVEL:1,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Comum',
                    CHAVE_QUANTIDADE:4}
                DSC = {
                    CHAVE_NOME:None,
                    CHAVE_NIVEL:1,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Comum',
                    CHAVE_QUANTIDADE:3}
                DTC = {
                    CHAVE_NOME:None,
                    CHAVE_NIVEL:1,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Comum',
                    CHAVE_QUANTIDADE:2}
                chaveProfissao = limpaRuidoTexto(dicionarioTrabalhoConcluido[CHAVE_PROFISSAO])
                nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario= retornaNomesRecursos(chaveProfissao, 1)
                DPC[CHAVE_NOME] = nomeRecursoPrimario
                DSC[CHAVE_NOME] = nomeRecursoSecundario
                DTC[CHAVE_NOME] = nomeRecursoTerciario
                DPC[CHAVE_PROFISSAO] = dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                DSC[CHAVE_PROFISSAO] = dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                DTC[CHAVE_PROFISSAO] = dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA],'licençadeproduçãodoaprendiz'):
                    DPC[CHAVE_QUANTIDADE]=DPC[CHAVE_QUANTIDADE]*2
                    DSC[CHAVE_QUANTIDADE]=DSC[CHAVE_QUANTIDADE]*2
                    DTC[CHAVE_QUANTIDADE]=DTC[CHAVE_QUANTIDADE]*2
                listaDicionarioTrabalhoProduzido=[DPC,DSC,DTC]
        if trabalhoEhColecaoRecursosAvancados(dicionarioTrabalhoConcluido):
                DPA={
                    CHAVE_NOME:None,
                    CHAVE_NIVEL:8,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Avançado',
                    CHAVE_QUANTIDADE:5}
                DSA={
                    CHAVE_NOME:None,
                    CHAVE_NIVEL:8,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Avançado',
                    CHAVE_QUANTIDADE:4}
                DTA={
                    CHAVE_NOME:None,
                    CHAVE_NIVEL:8,
                    CHAVE_PROFISSAO:None,
                    CHAVE_RARIDADE:'Avançado',
                    CHAVE_QUANTIDADE:3}
                chaveProfissao = limpaRuidoTexto(dicionarioTrabalhoConcluido[CHAVE_PROFISSAO])
                nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 8)
                DPA[CHAVE_NOME] = nomeRecursoPrimario
                DSA[CHAVE_NOME] = nomeRecursoSecundario
                DTA[CHAVE_NOME] = nomeRecursoTerciario
                DPA[CHAVE_PROFISSAO]=dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                DSA[CHAVE_PROFISSAO]=dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                DTA[CHAVE_PROFISSAO]=dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA],'licençadeproduçãodoaprendiz'):
                    DPA[CHAVE_QUANTIDADE]=DPA[CHAVE_QUANTIDADE]*2
                    DSA[CHAVE_QUANTIDADE]=DSA[CHAVE_QUANTIDADE]*2
                    DTA[CHAVE_QUANTIDADE]=DTA[CHAVE_QUANTIDADE]*2
                listaDicionarioTrabalhoProduzido=[DPA,DSA,DTA]
        if tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
            nomeRecurso = retornaNomeRecursoTrabalhoProducao(dicionarioTrabalhoConcluido[CHAVE_NOME])
            if variavelExiste(nomeRecurso):
                dicionarioTrabalhoEstoque[CHAVE_NIVEL] = dicionarioTrabalhoConcluido[CHAVE_NIVEL]
                dicionarioTrabalhoEstoque[CHAVE_NOME] = nomeRecurso
                dicionarioTrabalhoEstoque[CHAVE_PROFISSAO] = dicionarioTrabalhoConcluido[CHAVE_PROFISSAO]
                dicionarioTrabalhoEstoque[CHAVE_RARIDADE] = dicionarioTrabalhoConcluido[CHAVE_RARIDADE]
                tipoRecurso = retornaChaveTipoRecurso(dicionarioTrabalhoEstoque)
                if variavelExiste(tipoRecurso):
                    if tipoRecurso == CHAVE_RCS or tipoRecurso == CHAVE_RCT:
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = 1
                    elif tipoRecurso == CHAVE_RCP or tipoRecurso == CHAVE_RAP or tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RAT:
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = 2
                    if textoEhIgual(dicionarioTrabalhoConcluido[CHAVE_LICENCA],'licençadeproduçãodoaprendiz'):
                        dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] = dicionarioTrabalhoEstoque[CHAVE_QUANTIDADE] * 2
                    listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)
                else:
                    print(f'{D}: Tipo de recurso não encontrado!')
                    linhaSeparacao()
            else:
                print(f'Erro ao definir nome da produção de recurso de {dicionarioTrabalhoConcluido[CHAVE_NOME]}.')
                linhaSeparacao()
    else:
        dicionarioTrabalhoEstoque = {
            CHAVE_NIVEL:dicionarioTrabalhoConcluido[CHAVE_NIVEL],
            CHAVE_NOME:dicionarioTrabalhoConcluido[CHAVE_NOME],
            CHAVE_QUANTIDADE:1,
            CHAVE_PROFISSAO:dicionarioTrabalhoConcluido[CHAVE_PROFISSAO],
            CHAVE_RARIDADE:dicionarioTrabalhoConcluido[CHAVE_RARIDADE]
        }
        listaDicionarioTrabalhoProduzido.append(dicionarioTrabalhoEstoque)

    print(f'{D}: Lista de dicionários trabalhos concluídos:')
    for dicionarioTrabalhoConcluido in listaDicionarioTrabalhoProduzido:
        for atributo in dicionarioTrabalhoConcluido:
            print(f'{D}: {atributo} = {dicionarioTrabalhoConcluido[atributo]}.')
        linhaSeparacao()
    linhaSeparacao()
    return listaDicionarioTrabalhoProduzido

def trabalhoEhColecaoRecursosAvancados(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'grandecoleçãoderecursosavançados')or
            textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'coletaemmassaderecursosavançados'))

def trabalhoEhColecaoRecursosComuns(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'grandecoleçãoderecursoscomuns')

def trabalhoEhMelhoriaCatalisadorComposto(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadocatalizadoramplificado'))

def trabalhoEhMelhoriaCatalisadorComum(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadocatalizadorcomum'))

def trabalhoEhMelhoriaSubstanciaComposta(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadasubstânciacomposta'))

def trabalhoEhMelhoriaSubstanciaComum(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadasubstânciacomum'))

def trabalhoEhMelhoriaEssenciaComposta(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadaessênciacomposta'))

def trabalhoEhMelhoriaEssenciaComum(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadaessênciacomum'))

def trabalhoEhProducaoLicenca(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhorarlicençacomum')or
            textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'licençadeproduçãodoaprendiz'))

def modificaExperienciaProfissao(dicionarioPersonagem, dicionarioTrabalho):
    dicionarioPersonagem = defineListaDicionariosProfissoesNecessarias(dicionarioPersonagem)
    for profissao in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if textoEhIgual(profissao[CHAVE_NOME],dicionarioTrabalho[CHAVE_PROFISSAO]):
            if trabalhoPossuiAtributoExperiencia(dicionarioTrabalho):
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{profissao[CHAVE_ID]}/.json'
                experiencia = profissao[CHAVE_EXPERIENCIA]+dicionarioTrabalho[CHAVE_EXPERIENCIA]
                dados = {CHAVE_EXPERIENCIA:experiencia}
                modificaAtributo(caminhoRequisicao,dados)
                print(f'Experiência de {profissao[CHAVE_NOME]} atualizada para {experiencia}.')
                dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionarioProfissao(dicionarioPersonagem)
                break
            else:
                print(f'Trabalho concluido não possui atributo "experiência".')
    linhaSeparacao()

def trabalhoPossuiAtributoExperiencia(dicionarioTrabalho):
    return CHAVE_EXPERIENCIA in dicionarioTrabalho

def defineDicionarioTrabalhoConcluido(dicionarioPersonagem):
    dicionarioTrabalhoConcluido = {}
    telaInteira = retornaAtualizacaoTela()
    frameNomeTrabalho = telaInteira[285:285+37, 233:486]
    erro = verificaErro(None)
    if not erroEncontrado(erro):
        nomeTrabalhoConcluido = reconheceTexto(frameNomeTrabalho)
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'f2')
        # # print(f'{D}:Trabalho concluido reconhecido: {nomeTrabalhoConcluido}.')
        if variavelExiste(nomeTrabalhoConcluido):
            erro = verificaErro(None)
            if not erroEncontrado(erro):
                if not dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]:
                    dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA] = True
                listaDicionarioTrabalhoDesejado = retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
                if not tamanhoIgualZero(listaDicionarioTrabalhoDesejado):
                    dicionarioTrabalhoConcluido = retornaDicionarioTrabalhoRecuperado(nomeTrabalhoConcluido,listaDicionarioTrabalhoDesejado,produzindo)
                if tamanhoIgualZero(dicionarioTrabalhoConcluido):
                    listaDicionariosTrabalhos = retornaListaDicionariosTrabalhos()
                    if not tamanhoIgualZero(listaDicionariosTrabalhos):
                        for dicionarioTrabalho in listaDicionariosTrabalhos:
                            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], dicionarioTrabalho[CHAVE_NOME]):
                                dicionarioTrabalhoConcluido = dicionarioTrabalho
                                dicionarioTrabalhoConcluido[CHAVE_LICENCA] = 'Licença de produção do principiante'
                                dicionarioTrabalhoConcluido[CHAVE_ESTADO] = concluido
                                dicionarioTrabalhoConcluido[CHAVE_RECORRENCIA] = False
                                break
                clickContinuo(3, 'up')
                linhaSeparacao()
            else:
                dicionarioPersonagem[CHAVE_ESPACO_BOLSA] = False
                clickContinuo(1, 'up')
                clickEspecifico(1, 'left')
    return dicionarioPersonagem, dicionarioTrabalhoConcluido

def retornaDicionarioTrabalhoRecuperado(nomeTrabalhoConcluido, listaDicionarioTrabalho, estado):
    dicionarioTrabalho = {}
    for trabalho in listaDicionarioTrabalho:
        if (texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho[CHAVE_NOME]) and
            trabalho[CHAVE_ESTADO] == estado):
            print(f'{trabalho[CHAVE_NOME]} recuperado.')
            dicionarioTrabalho = trabalho
            break
    else:
        print(f'{D}: Dicionário trabalho concluído não encontrado na lista de trabalhos em produção.')
    linhaSeparacao()
    return dicionarioTrabalho

def trataErros(dicionarioTrabalho,dicionarioPersonagem):
    print(f'Tratando possíveis erros...')
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
    tentativas = 1
    erro=verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
    while erroEncontrado(erro):
        if erro==erroSemRecursos:
            excluiTrabalho(dicionarioPersonagem,dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
            dicionarioTrabalho[CHAVE_LISTA_DESEJO]=retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
            if tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_DESEJO]):
                dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        elif erro==erroSemEspacosProducao or erro==erroOutraConexao or erro==erroConectando or erro==erroRestaurandoConexao:
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
            dicionarioTrabalho[CHAVE_CONFIRMACAO]=False
            if erro==erroSemEspacosProducao:
                listaPersonagem=[dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
                modificaAtributoPersonagem(dicionarioPersonagem,listaPersonagem,CHAVE_ESPACO_PRODUCAO,False)
                linhaSeparacao()
                dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]=False
            elif erro==erroOutraConexao:
                dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
            elif erro == erroConectando:
                if tentativas>10:
                    clickEspecifico(1,'enter')
                    tentativas = 0
                tentativas+=1
        erro=verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
    linhaSeparacao()
    return dicionarioTrabalho,dicionarioPersonagem

def trataMenus(dicionarioTrabalho,dicionarioPersonagemAtributos):
    print(f'Tratando possíveis menus...')
    dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
    while True:
        menu = retornaMenu()
        if naoReconheceMenu(menu):
            continue
        elif menuTrabalhoEspecificoReconhecido(menu):
            clickEspecifico(1,'f2')
            if naoHaRecursosSuficientes(dicionarioTrabalho):
                excluiTrabalho(dicionarioPersonagemAtributos,dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
                break
        elif menuEscolhaEquipamentoReconhecido(menu):
            clickEspecifico(1,'f2')
            time.sleep(1)
            verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
        elif menuTrabalhosAtuais(menu):
            if trabalhoERecorrente(dicionarioTrabalho):
                print(f'Recorrencia está ligada.')
                cloneDicionarioTrabalho = defineCloneDicionarioTrabalho(dicionarioTrabalho)
                dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos,cloneDicionarioTrabalho)
                linhaSeparacao()
            elif not trabalhoERecorrente(dicionarioTrabalho):
                print(f'Recorrencia está desligada.')
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_ID]}/.json'
                dados = {CHAVE_ESTADO:1,
                         CHAVE_EXPERIENCIA:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_EXPERIENCIA]}
                modificaAtributo(caminhoRequisicao,dados)
                linhaSeparacao()
            removeTrabalhoEstoque(dicionarioPersonagemAtributos, dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
            clickContinuo(12,'up')
            dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
            break
        elif menuLicencas(menu):
            clickEspecifico(2,'f2')
        else:
            break
    return dicionarioPersonagemAtributos

def menuLicencas(menu):
    return menu==menu_licencas

def removeTrabalhoEstoque(dicionarioPersonagemAtributos, dicionarioTrabalho):
    listaTrabalhoEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioPersonagemAtributos)
    if not tamanhoIgualZero(listaTrabalhoEstoque):
        if textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], 'Comum'):
            if trabalhoEhProducaoRecursos(dicionarioTrabalho):
                print(f'{D}: Trabalho é recurso de produção!')
                nomeRecurso = retornaNomeRecursoTrabalhoProducao(dicionarioTrabalho[CHAVE_NOME])
                print(f'{D}: Nome recurso produzido: {nomeRecurso}')
                linhaSeparacao()
                dicionarioRecurso = {
                    CHAVE_NOME:nomeRecurso,
                    CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
                    CHAVE_NIVEL:dicionarioTrabalho[CHAVE_NIVEL]
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
                for trabalhoEstoque in listaTrabalhoEstoque:
                    for recursoBuscado in listaNomeRecursoBuscado:
                        if textoEhIgual(trabalhoEstoque[CHAVE_NOME], recursoBuscado[0]):
                            novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] - recursoBuscado[1]
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
                            dados = {CHAVE_QUANTIDADE:novaQuantidade}
                            print(f'{D}: Quantidade de {trabalhoEstoque[CHAVE_NOME]} atualizada de {trabalhoEstoque[CHAVE_QUANTIDADE]} para {novaQuantidade}.')
                            modificaAtributo(caminhoRequisicao, dados)
            else:
                dicionarioTrabalho = defineQuantidadeRecursos(dicionarioTrabalho)
                dicionarioTrabalho = defineNomeRecursos(dicionarioTrabalho)
                for trabalhoEstoque in listaTrabalhoEstoque:
                    if textoEhIgual(trabalhoEstoque[CHAVE_NOME], dicionarioTrabalho[CHAVE_NOME_PRIMARIO]):
                        novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalho[CHAVE_QUANTIDADE_PRIMARIO]
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                        print(f'{D}: Quantidade de {trabalhoEstoque[CHAVE_NOME]} atualizada de {trabalhoEstoque[CHAVE_QUANTIDADE]} para {novaQuantidade}.')
                        modificaAtributo(caminhoRequisicao,dados)
                    elif textoEhIgual(trabalhoEstoque[CHAVE_NOME], dicionarioTrabalho[CHAVE_NOME_SECUNDARIO]):
                        novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalho[CHAVE_QUANTIDADE_SECUNDARIO]
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                        print(f'{D}:Quantidade de {trabalhoEstoque[CHAVE_NOME]} atualizada para {novaQuantidade}.')
                        modificaAtributo(caminhoRequisicao,dados)
                    elif textoEhIgual(trabalhoEstoque[CHAVE_NOME], dicionarioTrabalho[CHAVE_NOME_TERCIARIO]):
                        novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] - dicionarioTrabalho[CHAVE_QUANTIDADE_TERCIARIO]
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
                        dados = {CHAVE_QUANTIDADE:novaQuantidade}
                        print(f'{D}:Quantidade de {trabalhoEstoque[CHAVE_NOME]} atualizada para {novaQuantidade}.')
                        modificaAtributo(caminhoRequisicao,dados)
        elif textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE],'Melhorado'):
            pass
    else:
        print(f'Lista de estoque está vazia!')
        linhaSeparacao()
    return dicionarioPersonagemAtributos

def defineCloneDicionarioTrabalho(dicionarioTrabalho):
    cloneDicionarioTrabalho={
        CHAVE_ID:None,
        CHAVE_NOME:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_NOME],
        CHAVE_ESTADO:1,
        CHAVE_EXPERIENCIA:dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_EXPERIENCIA],
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

def iniciaProducao(dicionarioTrabalho, dicionarioPersonagem):
    dicionarioPersonagem = entraLicenca(dicionarioPersonagem)
    if chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
        confirmacao,dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = verificaLicenca(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO],dicionarioPersonagem)
        if confirmacao:#verifica tipo de licença de produção
            clickEspecifico(1,'f2')#click que definitivamente começa a produção
            dicionarioTrabalho, dicionarioPersonagem = trataErros(dicionarioTrabalho,dicionarioPersonagem)
            linhaSeparacao()
            if chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
                dicionarioPersonagem = trataMenus(dicionarioTrabalho,dicionarioPersonagem)
                if chaveConfirmacaoForVerdadeira(dicionarioPersonagem):
                    erro = verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
                    tentativas = 1
                    while erroEncontrado(erro):
                        if erro == erroConectando:
                            if tentativas > 10:
                                clickEspecifico(1, 'enter')
                            tentativas += 1
                        erro = verificaErro(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO])
                    dicionarioTrabalho[CHAVE_LISTA_DESEJO] = retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
                    if tamanhoIgualZero(dicionarioTrabalho[CHAVE_LISTA_DESEJO]):
                        dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                    print(f'Atualizou a CHAVE_LISTA_DESEJO.')
                    linhaSeparacao()
        else:
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
            print(f'Erro ao busca licença...')
            linhaSeparacao()
    else:
        print(f'Erro ao entrar na licença...')
        linhaSeparacao()
    return dicionarioTrabalho, dicionarioPersonagem

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

def retornaListaDicionariosTrabalhosRarosVendidos(listaDicionariosProdutosVendidos, dicionarioPersonagemAtributos):
    listaDicionariosTrabalhosRarosVendidos = []
    listaDicionariosTrabalhos = retornaListaDicionariosTrabalhos()
    if not tamanhoIgualZero(listaDicionariosTrabalhos):
        for dicionarioProdutoVendido in listaDicionariosProdutosVendidos:
            for dicionarioTrabalho in listaDicionariosTrabalhos:
                if textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], 'raro'):
                    if texto1PertenceTexto2(dicionarioTrabalho[CHAVE_NOME], dicionarioProdutoVendido['nomeProduto']):
                        if textoEhIgual(dicionarioProdutoVendido['nomePersonagem'], dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME]):
                            if not trabalhoEhProducaoRecursos(dicionarioTrabalho):
                                dicionarioTrabalho = {
                                    CHAVE_ID:dicionarioTrabalho[CHAVE_ID],
                                    CHAVE_NOME:dicionarioTrabalho[CHAVE_NOME],
                                    CHAVE_NIVEL:dicionarioTrabalho[CHAVE_NIVEL],
                                    CHAVE_RARIDADE:dicionarioTrabalho[CHAVE_RARIDADE],
                                    CHAVE_PROFISSAO:dicionarioTrabalho[CHAVE_PROFISSAO],
                                    CHAVE_QUANTIDADE:dicionarioProdutoVendido['quantidadeProduto'],
                                    CHAVE_EXPERIENCIA:dicionarioTrabalho[CHAVE_EXPERIENCIA]}
                                listaDicionariosTrabalhosRarosVendidos.append(dicionarioTrabalho)
                                break
    linhaSeparacao()
    for dicionarioTrabalhoRaroVendido in listaDicionariosTrabalhosRarosVendidos:
        for atributo in dicionarioTrabalhoRaroVendido:
            print(f'{D}: {atributo} - {dicionarioTrabalhoRaroVendido[atributo]}.')
        linhaSeparacao()
    return listaDicionariosTrabalhosRarosVendidos

def recebeTodasRecompensas(menu,dicionarioPersonagemAtributos):
    listaPersonagemPresenteRecuperado = retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado=[])
    while True:
        reconheceMenuRecompensa(menu)
        if existePixelCorrespondencia():
            vaiParaMenuCorrespondencia()
            recuperaCorrespondencia(dicionarioPersonagemAtributos)
        print(f'Lista: {listaPersonagemPresenteRecuperado}.')
        linhaSeparacao()
        deslogaPersonagem(None,None)
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
                clickMouseEsquerdo(1,centroX,centroY)
                posicionaMouseEsquerdo(telaInteira.shape[1]//2,telaInteira.shape[0]//2)
                if verificaErro(None) != 0:
                    evento=2
                    break
                clickEspecifico(1,'f2')
                break
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
    if menu == menu_loja_milagrosa:
        clickEspecifico(1,'down')
        clickEspecifico(1,'enter')
        recuperaPresente()
    elif menu == menu_rec_diarias:
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
    frameNomePersonagemTratado=retornaImagemCinza(frameNomePersonagem)
    frameNomePersonagemTratado=retornaImagemEqualizada(frameNomePersonagemTratado)
    frameNomePersonagemTratado=retornaImagemBinarizada(frameNomePersonagemTratado)
    contadorPixelPreto=np.sum(frameNomePersonagemTratado==0)
    # # print(f'{D}:{contadorPixelPreto}')
    # mostraImagem(0,frameNomePersonagemTratado,None)
    if contadorPixelPreto>50:
        nomePersonagemReconhecido=reconheceTexto(frameNomePersonagemTratado)
        # # print(f'{D}:{nomePersonagemReconhecido}.')
        if variavelExiste(nomePersonagemReconhecido):
            nome=limpaRuidoTexto(nomePersonagemReconhecido)
            print(f'{D}:Personagem reconhecido: {nome}')
            # linhaSeparacao()
        elif contadorPixelPreto>50:
            nome='provisorioatecair'
    return nome

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

def trataMenu(menu,dicionarioPersonagemAtributos):
    dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO]=True
    if menu==menu_desconhecido:
        pass
    elif menu==menu_trab_atuais:
        estado_trabalho=retornaEstadoTrabalho()
        if estado_trabalho==concluido:
            dicionarioPersonagemAtributos, dicionarioTrabalhoConcluido = verificaTrabalhoConcluido(dicionarioPersonagemAtributos)
            if not tamanhoIgualZero(dicionarioTrabalhoConcluido):
                modificaExperienciaProfissao(dicionarioPersonagemAtributos, dicionarioTrabalhoConcluido)
                atualizaEstoquePersonagem(dicionarioPersonagemAtributos, dicionarioTrabalhoConcluido)
        elif estado_trabalho==produzindo:
            # lista_profissao.clear()
            if not dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]:
                print(f'Todos os espaços de produção ocupados.')
                linhaSeparacao()
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO]=False
            else:
                clickContinuo(3,'up')
                clickEspecifico(1,'left')
        elif estado_trabalho==0:
            clickContinuo(3,'up')
            clickEspecifico(1,'left')
    elif menu==menu_rec_diarias or menu==menu_loja_milagrosa:
        recebeTodasRecompensas(menu,dicionarioPersonagemAtributos)
        for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            if not dicionarioPersonagem[CHAVE_ESTADO]:
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_ID]}/.json'
                dados = {CHAVE_ESTADO:True}
                modificaAtributo(caminhoRequisicao,dados)
        dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]=False
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO]=False
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
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO]=False
    erro=verificaErro(None)
    if erro==erroOutraConexao:
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO]=False
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO]=False
    return dicionarioPersonagemAtributos

def atualizaEstoquePersonagem(dicionarioPersonagem, dicionarioTrabalhoProduzido):
    listaDicionarioTrabalhoProduzido = retornaListaDicionarioTrabalhoProduzido(dicionarioTrabalhoProduzido)
    if not tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
        listaDicionarioTrabalhoEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioPersonagem)
        if not tamanhoIgualZero(listaDicionarioTrabalhoEstoque):
            for trabalhoEstoque in listaDicionarioTrabalhoEstoque:
                listaDicionarioTrabalhoProduzido = modificaQuantidadeTrabalhoEstoque(listaDicionarioTrabalhoProduzido, dicionarioPersonagem, trabalhoEstoque)
            else:
                if not tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
                    for trabalhoProduzido in listaDicionarioTrabalhoProduzido:
                        adicionaTrabalhoEstoque(dicionarioPersonagem, trabalhoProduzido)
        else:
            for trabalhoProduzido in listaDicionarioTrabalhoProduzido:
                adicionaTrabalhoEstoque(dicionarioPersonagem, trabalhoProduzido)

def modificaQuantidadeTrabalhoEstoque(listaDicionarioTrabalhoProduzido, dicionarioPersonagem, trabalhoEstoque):
    for dicionarioTrabalhoProduzido in listaDicionarioTrabalhoProduzido:
        if textoEhIgual(dicionarioTrabalhoProduzido[CHAVE_NOME], trabalhoEstoque[CHAVE_NOME]):
            novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] + dicionarioTrabalhoProduzido[CHAVE_QUANTIDADE]
            caminhoRequisicao = f'Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
            dados = {CHAVE_QUANTIDADE:novaQuantidade}
            modificaAtributo(caminhoRequisicao, dados)
            print(f'{trabalhoEstoque[CHAVE_NOME]} - Quantidade: {novaQuantidade}.')
            linhaSeparacao()
            for indice in range(len(listaDicionarioTrabalhoProduzido)):
                if listaDicionarioTrabalhoProduzido[indice][CHAVE_NOME] == trabalhoEstoque[CHAVE_NOME]:
                    del listaDicionarioTrabalhoProduzido[indice]
                    break
            if tamanhoIgualZero(listaDicionarioTrabalhoProduzido):
                break
    return listaDicionarioTrabalhoProduzido
    
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

def retornaConteudoCorrespondencia(dicionarioPersonagemAtributos):
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
                # nomeProduto=retornaNomeProdutoVendido(listaTextoCarta)
                frameTela = telaInteira[415:415+30,250:250+260]
                frameTelaTratado = retornaImagemCinza(frameTela)
                frameTelaTratado = retornaImagemBinarizada(frameTelaTratado)
                ouro = reconhece_digito(frameTelaTratado)
                ouro = re.sub('[^0-9]','',ouro)
                if ouro.isdigit():
                    ouro = int(ouro)
                dataAtual = str(datetime.date.today())
                listaTextoCarta = ' '.join(listaTextoCarta)
                dicionarioVenda = {CHAVE_NOME_PERSONAGEM:dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME],
                                 'nomeProduto':listaTextoCarta,
                                 'quantidadeProduto':quantidadeProduto,
                                 'valorProduto':ouro,
                                 'dataVenda':dataAtual}
                adicionaVenda(dicionarioPersonagemAtributos, dicionarioVenda)
                # print(dicionarioVenda)
                linhaSeparacao()
            else:
                print(f'Produto expirado:')
                removerPalavras = ['a','oferta','de','expirou']
                # print(textoCarta)
                listaTextoCarta = textoCarta.split()
                result = [palavra for palavra in listaTextoCarta if palavra.lower() not in removerPalavras]
                # print(result)
                retorno = ' '.join(result)
                print(retorno)
                linhaSeparacao()
        else:
            print(f'Erro...')
    return dicionarioVenda

def retornaQuantidadeProdutoVendido(listaTextoCarta):
    x=0
    quantidadeProduto=0
    for texto in listaTextoCarta:
        if texto1PertenceTexto2('un',texto):
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
    if 'vendeu'in texto.lower():
        return True
    elif 'expirou'in texto.lower():
        return False
    return None

def recuperaCorrespondencia(dicionarioPersonagemAtributos):
    while verificaCaixaCorreio():
        clickEspecifico(1, 'enter')
        dicionarioVenda = retornaConteudoCorrespondencia(dicionarioPersonagemAtributos)
        atualizaQuantidadeTrabalhoEstoque(dicionarioPersonagemAtributos, dicionarioVenda)
        clickEspecifico(1,'f2')
    else:
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1, 2, 35)
        linhaSeparacao()

def atualizaQuantidadeTrabalhoEstoque(dicionarioPersonagemAtributos, dicionarioVenda):
    if not tamanhoIgualZero(dicionarioVenda):
        listaDicionarioTrabalhoEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioPersonagemAtributos)
        for trabalhoEstoque in listaDicionarioTrabalhoEstoque:
            if (texto1PertenceTexto2(trabalhoEstoque[CHAVE_NOME], dicionarioVenda['nomeProduto']) and
                    textoEhIgual(dicionarioVenda['nomePersonagem'], dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME])):
                novaQuantidade = trabalhoEstoque[CHAVE_QUANTIDADE] - 1
                caminhoRequisicao = f'Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{trabalhoEstoque[CHAVE_ID]}/.json'
                dados = {CHAVE_QUANTIDADE:novaQuantidade}
                modificaAtributo(caminhoRequisicao, dados)
                print(f'{D}: Quantidade de {trabalhoEstoque[CHAVE_NOME]} atualizada para {novaQuantidade}.')
                break
        else:
            print(f'{D}: Trabalho vendido não encontrado no estoque.')
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
    texto=None
    telaInteira=retornaAtualizacaoTela()
    frameTela=telaInteira[telaInteira.shape[0]-50:telaInteira.shape[0]-25,50:50+60]
    frameTelaTratado=retornaImagemCinza(frameTela)
    frameTelaTratado=retornaImagemBinarizada(frameTelaTratado)
    contadorPixelPreto=np.sum(frameTelaTratado==0)
    # print(f'{D}:Quantidade de pixels pretos: {contadorPixelPreto}')
    # mostraImagem(0,frameTelaTratado,None)
    if contadorPixelPreto>100 and contadorPixelPreto<400:
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

def implementaNovaProfissao(dicionarioPersonagem):
    novaProfissao={CHAVE_NOME:'Braceletes'}
    print(f'Implementando profissao: {novaProfissao[CHAVE_NOME]}.')
    dicionarioPersonagem=defineListaDicionarioPersonagem(dicionarioPersonagem)
    for personagem in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=personagem
        dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]=retornaListaDicionarioProfissao(dicionarioPersonagem)
        for profissao in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
            if textoEhIgual(profissao[CHAVE_NOME],'Braceletes'):
                break
        else:
            adicionaNovaProfissao(dicionarioPersonagem,novaProfissao)
    else:
        print(f'Processo de verificação concluído com sucesso!!')
    linhaSeparacao()

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
        listaDicionariosTrabalhosBuscados=retornaListaDicionariosTrabalhosBuscados(dicionarioUsuario[CHAVE_LISTA_TRABALHO],dicionarioUsuario[CHAVE_PROFISSAO][CHAVE_NOME],'melhorado')
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
                # modificaRaridadeTrabalho(dicionarioTrabalho,raridade='Melhorado')
    linhaSeparacao()

def mostraListaTrabalhoSemExperiencia(dicionarioUsuario):
    x=1
    listaDicionarioTrabalhoSemXp=[]
    for trabalho in dicionarioUsuario[CHAVE_LISTA_TRABALHO]:
        if textoEhIgual(trabalho[CHAVE_RARIDADE],'comum')and trabalho[CHAVE_NIVEL]==1:
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
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionarioProfissao(dicionarioUsuario)
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

def adicionaAtributoIdProfissao(dicionarioPersonagem):
    for personagem in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=personagem
        listaDicionarioProfissao=retornaListaDicionarioProfissao(dicionarioPersonagem)
        linhaSeparacao()

def retornaDicionarioProfissaoEscolhida(dicionarioUsuario, opcaoProfissao):
    x=1
    for dicionarioProfissao in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if x==opcaoProfissao:
            break
        x+=1
    return dicionarioProfissao

def opcaoInvalida(opcaoLista, tamanhoMenu):
    return not ehValorNumerico(opcaoLista) or int(opcaoLista) < 0 or int(opcaoLista) > tamanhoMenu

def ehValorNumerico(valor):
    return valor.isdigit()

def ehValorAlfabetico(valor):
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
    trabalhoDesejado={
        CHAVE_ID:'-Ni8Nu1ul0uTMioGLH--',
        CHAVE_NOME:'recebendo âmbar',
        CHAVE_EXPERIENCIA:130,
        CHAVE_NIVEL:8,
        CHAVE_RARIDADE:'comum',
        CHAVE_PROFISSAO:'Braceletes'
        }
    trabalhoComumDesejado={
        CHAVE_ID:None,
        CHAVE_NOME:'Grande coleção de recursos avançados',
        CHAVE_EXPERIENCIA:90,
        CHAVE_NIVEL:5,
        CHAVE_RARIDADE:'raro',
        CHAVE_PROFISSAO:'Braceletes',
        CHAVE_RECORRENCIA:False,
        CHAVE_LICENCA:'Licença de produção do aprendiz',
        CHAVE_ESTADO:0
    }

    dicionarioTrabalhoConcluido = {
        CHAVE_ID:None,
        CHAVE_NOME:'Recebendo Distintivo de Aprendiz',
        CHAVE_EXPERIENCIA:130,
        CHAVE_NIVEL:8,
        CHAVE_RARIDADE:'Avançado',
        CHAVE_PROFISSAO:'Braceletes',
        CHAVE_RECORRENCIA:False,
        CHAVE_LICENCA:'Licença de produção do principiante',
        CHAVE_ESTADO:0
        }

    dicionarioTrabalho={
        CHAVE_CONFIRMACAO:True,
        CHAVE_POSICAO_TRABALHO_COMUM:-1,
        CHAVE_PROFISSAO:'Armadura de tecido',
        CHAVE_LISTA_TRABALHO_COMUM_MELHORADO:[trabalhoComumDesejado],
        CHAVE_DICIONARIO_TRABALHO_DESEJADO:None
        }
    dicionarioPersonagemAtributos = {
        CHAVE_ID_USUARIO:dicionarioUsuario[CHAVE_ID_USUARIO],
        CHAVE_DICIONARIO_PERSONAGEM_EM_USO:dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO],
        CHAVE_LISTA_PROFISSAO_MODIFICADA:False}
    dicionarioVenda = {
        CHAVE_NOME_PERSONAGEM:dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME],
        'nomeProduto':'Vendeu Faixa das llusões Cativantes1 un por 5999 de ouro',
        'quantidadeProduto':1,
        'valorProduto':5000,
        'dataVenda':'00-00-00'
        }
    listaPersonagem=[dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]=retornaListaDicionarioProfissao(dicionarioUsuario)
    while retornaInputConfirmacao():
        dicionarioPersonagemAtributos = defineListaDicionarioPersonagem(dicionarioUsuario)
        dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionarioProfissao(dicionarioUsuario)
        listaDicionarioTrabalhoProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos)
        dicionarioTrabalho[CHAVE_LISTA_DESEJO] = listaDicionarioTrabalhoProduzirProduzindo
        dicionarioUsuario[CHAVE_LISTA_TRABALHO] = retornaListaDicionariosTrabalhos()
        dicionarioTrabalho = defineListaDicionariosTrabalhosPriorizados(dicionarioTrabalho)
        dicionarioTrabalho = defineListaDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)

        removeTrabalhoEstoque(dicionarioPersonagemAtributos, trabalhoDesejado)