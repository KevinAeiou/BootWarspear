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

lista_personagem_ativo=[]

id=0
nome=1
profissao=2
nivel=3
licenca=4
raridade=5
recorrencia=6
estado=7

para_produzir=0
produzindo=1
concluido=2

CHAVE_ID_PERSONAGEM='idPersonagem'
CHAVE_ESPACO_PRODUCAO='espacoProducao'
CHAVE_ESPACO_BOLSA='espacoBolsa'
CHAVE_UNICA_CONEXAO='unicaConexao'
CHAVE_LISTA_DESEJO='listaDesejo'
CHAVE_LISTA_PROFISSAO='listaProfissao'
CHAVE_CONFIRMACAO='confirmacao'
CHAVE_TRABALHO_CONCLUIDO='trabalhoConcluido'
CHAVE_LISTA_PROFISSAO_MODIFICADA='listaProfissoesAtualizada'

usuario_id = 'eEDku1Rvy7f7vbwJiVW7YMsgkIF2'
tela = 'atualizacao_tela.png'

def atualiza_nova_tela():
    imagem = manipula_teclado.tira_screenshot()
    manipula_imagem.salva_nova_tela(imagem)
    print(f'Atualizou a tela.')
    linhaSeparacao()

def adiciona_trabalho(personagem_id,trabalho,licenca):
    manipula_cliente.adiciona_trabalho(personagem_id,trabalho,licenca,0)
    linhaSeparacao()

def profissaoExiste(profissaoReconhecida,listaProfissao):
    confirmacao=False
    for profissao in listaProfissao:
        if profissao[nome]in profissaoReconhecida:
            confirmacao=True
            break
    return confirmacao
#modificado16/01
def atualiza_lista_profissao(dicionarioPersonagem):
    #285,355
    yinicial_profissao=285
    listaProfissaoAtual=dicionarioPersonagem[CHAVE_LISTA_PROFISSAO]
    #altura frame: 35 pixel
    #altura entre os frames: 70 pixel
    print(f'Atualizando lista de profissões...')
    linhaSeparacao()
    for x in range(len(listaProfissaoAtual)):
        if x==4:
            manipula_teclado.click_especifico(5,'down')
            #yinicial_profissao recebe valor fixo=529
            yinicial_profissao = 529
        elif x>4:
            manipula_teclado.click_especifico(1,'down')
            yinicial_profissao=529
        tela_inteira=retorna_atualizacao_tela()
        frame_nome_profissao=tela_inteira[yinicial_profissao:yinicial_profissao+35,233:456]
        #reconhece a profissao do frame
        profissaoReconhecida=manipula_imagem.reconhece_texto(frame_nome_profissao)
        if profissaoReconhecida!=None:
            profissaoReconhecida=unidecode(profissaoReconhecida)
            if profissaoExiste(profissaoReconhecida,listaProfissaoAtual):
                if listaProfissaoAtual[x][nome]!=profissaoReconhecida:
                    manipula_cliente.modificarProfissao(dicionarioPersonagem[CHAVE_ID_PERSONAGEM],listaProfissaoAtual[x][id],profissaoReconhecida)
                yinicial_profissao+=70
            else:
                print(f'Profissão não existe!')
                break
        else:
            print(f'Processo interrompido!')
            break
    else:
        print(f'Processo concluído!')
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]=False
    linhaSeparacao()
    manipula_teclado.click_continuo(8,'up')
    return dicionarioPersonagem

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
    linhaSeparacao()
    while not nivel_trabalho.isdigit() or int(nivel_trabalho)<0 or int(nivel_trabalho)>32:
        print(f'Opção inválida! Selecione uma das opções.')
        nivel_trabalho = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        nivel_trabalho = int(nivel_trabalho)
        if nivel_trabalho==0:
            print(f'Voltar...')
            linhaSeparacao()
            return
        while True:
            tela_inteira = retorna_atualizacao_tela()
            frame_nome_trabalho = tela_inteira[280:280+33,169:169+303]#frame nome trabalho menu especifico
            # frame_nome_trabalho = tela_inteira[273:273+311,167:167+347]
            nome_trabalho_reconhecido = manipula_imagem.reconhece_texto(frame_nome_trabalho)
            confirma_cadastro = input(f'Cadastrar {nome_trabalho_reconhecido}? Sim ou não(S/N): ')
            linhaSeparacao()
            while not confirma_cadastro.isalpha() or (str(confirma_cadastro).lower().replace('\n','')!='s' and str(confirma_cadastro).lower().replace('\n','')!='n'):
                print(f'Opção inválida! Cadastrar {nome_trabalho_reconhecido}?')
                confirma_cadastro = input(f'Sim ou não(S/N): ')
                linhaSeparacao()
            else:
                confirma_cadastro = str(confirma_cadastro).lower().replace('\n','')
                if confirma_cadastro == 's':
                    atributos_trabalho=[nome_trabalho_reconhecido,tipo_raridade_trabalho,nivel_trabalho,nome_profissao]
                    manipula_cliente.cadastrar_trabalho(atributos_trabalho)
                    #manipula_arquivo.inclui_linha(linha,tipo_raridade_trabalho)
                    print(f'{nome_trabalho_reconhecido} foi cadastrado!')
                    linhaSeparacao()
                novo_cadastro = str(input(f'Deseja cadastrar novo trabalho? Sim ou não(S/N): '))
                linhaSeparacao()
                while not novo_cadastro.isalpha() or (str(novo_cadastro).lower().replace('\n','')!='s' and str(novo_cadastro).lower().replace('\n','')!='n'):
                    print(f'Opção inválida! Cadastrar novo trabalho?')
                    novo_cadastro = input(f'Sim ou não(S/N): ')
                    linhaSeparacao()
                else:
                    novo_cadastro = str(novo_cadastro).lower().replace('\n','')
                    if novo_cadastro == 'n':
                        print(f'Voltar.')
                        linhaSeparacao()
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
        linhaSeparacao()
        lista = 0
    return lista

def mostra_lista_desejo(tipo_lista):
    lista_desejo = manipula_cliente.consutar_lista(tipo_lista)
    tamanho_lista = len(lista_desejo)
    if tamanho_lista>0:
        for x in range(tamanho_lista):
            print(f'{lista_desejo[x][1]}')
        linhaSeparacao()
    else:
        print(f'A lista está vazia.')
        linhaSeparacao()
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
        linhaSeparacao()
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
    confirmacao=False
    posicao_menu=[[703,627],[712,1312]]
    tela_inteira=retorna_atualizacao_tela()
    for posicao in posicao_menu:
        frame_tela=tela_inteira[posicao[0]:posicao[0]+53,posicao[1]:posicao[1]+53]
        contadorPixelPreto=np.sum(frame_tela==(85,204,255))
        if contadorPixelPreto==1720:
            confirmacao=True
            break
    return confirmacao

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
def retornaEstadoTrabalho():
    estado_espaco=0
    #icone do primeiro espaço de produç 181,295 228,342
    tela_inteira = retorna_atualizacao_tela()
    frame_trabalho_concluido = tela_inteira[311:311+43, 233:486]
    texto=manipula_imagem.reconhece_texto(frame_trabalho_concluido)
    if texto!=None:
        texto=texto.replace(' ','').lower()
        if "trabalhoconcluído"==texto:
            print(f'Trabalho concluído!')
            estado_espaco=2
        elif 'adicionarnovo' in texto:
            print(f'Nem um trabalho!')
            estado_espaco=0
        else:
            print(f'Em produção...')
            estado_espaco=1
    else:
        print(f'Ocorreu algum erro ao verificar o espaço de produção!')
    linhaSeparacao()
    return estado_espaco
#modificado 10/01
def verifica_licenca(licenca_trabalho):
    confirmacao=False
    print(f"Buscando: {licenca_trabalho}")
    linhaSeparacao()
    licenca_reconhecida=retorna_licenca_reconhecida()
    if licenca_reconhecida!=None and licenca_trabalho!=None:
        licenca_trabalho=licenca_trabalho.replace(' ','').lower()
        print(f'Licença reconhecida: {licenca_reconhecida}.')
        linhaSeparacao()
        if 'licençasdeproduçaomaspode' not in licenca_reconhecida:
            primeira_busca=True
            lista_ciclo=[]
            while not licenca_reconhecida in licenca_trabalho:
                primeira_busca=False
                manipula_teclado.click_especifico(1,"right")
                lista_ciclo.append(licenca_reconhecida)
                licenca_reconhecida=retorna_licenca_reconhecida()
                if licenca_reconhecida!=None:
                    print(f'Licença reconhecida: {licenca_reconhecida}.')
                    linhaSeparacao()
                    print(f'Licença reconhecida: {licenca_reconhecida}.')
                    if verifica_ciclo(lista_ciclo)or licenca_reconhecida in 'nenhumitem':
                        licenca_trabalho='licençadeproduçãodoiniciante'
                        print(f'Licença para trabalho agora é: {licenca_trabalho}.')
                else:
                    print(f'Erro ao reconhecer licença!')
                    linhaSeparacao()
                    break
            else:#se encontrou a licença buscada
                if primeira_busca:
                    manipula_teclado.click_especifico(1,"f1")
                else:
                    manipula_teclado.click_especifico(1,"f2")
                confirmacao=True
    else:
        print(f'Erro ao reconhecer licença!')
        linhaSeparacao()
    return confirmacao

def retorna_licenca_reconhecida():
    licencaRetornada=None
    lista_licencas=['iniciante','principiante','aprendiz','mestre','nenhumitem','licençasdeproduçaomaspode']
    tela_inteira=retorna_atualizacao_tela()
    frame_tela=tela_inteira[275:317,169:512]
    frame_tela_equalizado=manipula_imagem.retorna_imagem_equalizada(frame_tela)
    licenca_reconhecida=manipula_imagem.reconhece_texto(frame_tela_equalizado)
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

def retorna_producao_recursos(nome_trabalho):
    #Grande coleção de rec
    lista_producao_recursos=([
        'Grande coleção de recursos comuns','de recursos avançados',
        'Melhoria da substância comum','Melhoria do catalisador comum','Melhoria da essência comum',
        'Melhoria da substância composta','Melhoria do catalisador amplificado','Melhoria da essência composta',
        'Melhorar licença comum','Licença de produção do aprendiz'])
    for trabalho in lista_producao_recursos:
        if  trabalho.replace(' ','').lower() in nome_trabalho.replace(' ','').lower():
            return True
    return False

def confirma_nome_trabalho(nome_trabalho_lista,tipo_trabalho):
    print(f'Confirmando nome do trabalho...')
    x=0
    y=1
    largura=2
    altura=3
    lista_frames=[[169,280,303,33],[169,195,343,31]]
    posicao=lista_frames[tipo_trabalho]
    imagem_inteira=retorna_atualizacao_tela()#tira novo print da tela
    frame_nome_trabalho=imagem_inteira[posicao[y]:posicao[y]+posicao[altura],posicao[x]:posicao[x]+posicao[largura]]
    frame_nome_trabalho_tratado=manipula_imagem.transforma_caracteres_preto(frame_nome_trabalho)
    nome_trabalho=manipula_imagem.reconhece_texto(frame_nome_trabalho_tratado)
    # manipula_imagem.mostra_imagem(0,frame_nome_trabalho_tratado,nome_trabalho)
    if nome_trabalho!=None:
        nome_trabalho_tratado=nome_trabalho.replace(' ','')[1:-1].lower()
        if  nome_trabalho_tratado in nome_trabalho_lista.replace(' ','').lower():
            print(f'Trabalho confirmado: {nome_trabalho}!')
            linhaSeparacao()
            return True
    print(f'Trabalho negado: {nome_trabalho}!')
    linhaSeparacao()
    return False
#modificado 16/01
def verifica_posicoes_trabalhos(profissao_verificada,dicionarioPersonagem):
    yinicial_nome=285
    posicao_trabalho_reconhecido=0
    posicao_trabalho=-1
    trabalho_lista=None
    #xinicial=233, xfinal=478, yinicial=285, yfinal=324 altura=70
    #sempre faz três verificações
    time.sleep(2)
    if not retorna_trabalho_comum(dicionarioPersonagem[CHAVE_LISTA_DESEJO],profissao_verificada):
        while posicao_trabalho_reconhecido<4 and trabalho_lista==None:
            nome_trabalho_reconhecido=retorna_nome_trabalho_reconhecido(yinicial_nome,0)
            if nome_trabalho_reconhecido!=None and trabalho_lista==None:
                print(f'Nome do trabalho disponível: {nome_trabalho_reconhecido}')
                #enquanto não comparar toda lista
                for trabalho_lista_desejo in dicionarioPersonagem[CHAVE_LISTA_DESEJO]:
                    #retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
                    nome_trabalho = trabalho_lista_desejo[nome]
                    profissao_trabalho = trabalho_lista_desejo[profissao]
                    #se o trabalho na lista de desejo NÃO for da profissão verificada no momento, passa para o proximo trabalho na lista
                    if profissao_verificada==profissao_trabalho:
                        print(f'Nome do trabalho na lista: {nome_trabalho}')
                        if nome_trabalho_reconhecido.replace(' ','').lower() in nome_trabalho.replace(' ','').lower():
                            linhaSeparacao()
                            print(f'{nome_trabalho} reconhecido...')
                            linhaSeparacao()
                            posicao_trabalho=posicao_trabalho_reconhecido
                            trabalho_lista=trabalho_lista_desejo
                            break
                else:
                    linhaSeparacao()
            else:
                posicao_trabalho_reconhecido=3
            yinicial_nome = yinicial_nome+70
            posicao_trabalho_reconhecido+=1
        else:
            if posicao_trabalho_reconhecido==4:
                trabalho_lista=''
                print(f'Nem um trabalho disponível está na lista de desejos.')
                manipula_teclado.click_continuo(4,'up')
                manipula_teclado.click_especifico(1,'left')
                linhaSeparacao()
    return posicao_trabalho,trabalho_lista

def retorna_trabalho_comum(conteudo_lista_desejo,profissao_verificada):
    trabalho_comum=False
    print(f'Buscando trabalho comum na lista...')
    for trabalho_lista_desejo in conteudo_lista_desejo:#retorna o nome do trabalho na lista de desejo na posição tamanho_lista_desejo-1
        nome_trabalho = trabalho_lista_desejo[nome]
        profissao_trabalho = trabalho_lista_desejo[profissao]
        raridade_trabalho = trabalho_lista_desejo[raridade]
        #se o trabalho na lista de desejo NÃO for da profissão verificada no momento, passa para o proximo trabalho na lista
        if profissao_verificada==profissao_trabalho and raridade_trabalho=='Comum':
            print(f'Trabalho comum encontado: {nome_trabalho}.')
            linhaSeparacao()
            trabalho_comum=True
    if not trabalho_comum:
        print(f'Nem um trabaho comum na lista!')
        linhaSeparacao()
    return trabalho_comum

def verifica_trabalho_comum(profissao_verificada):
    trabalho=None
    manipula_teclado.click_especifico(5,'down')
    global contador_paracima
    contador_paracima=5
    conteudo_lista_desejo=manipula_cliente.consulta_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id_global}/Lista_desejo')
    while trabalho==None:#51 capas, 100 acorpoacorpo,
        nome_trabalho_reconhecido = retorna_nome_trabalho_reconhecido(530,1)
        if nome_trabalho_reconhecido!=None:
            print(f'Trabalho reconhecido: {nome_trabalho_reconhecido}')
            for trabalho_lista in conteudo_lista_desejo:
                nome_trabalho=trabalho_lista[nome]
                profissao_trabalho=trabalho_lista[profissao]
                raridade_trabalho=trabalho_lista[raridade]
                estadoTrabalho=trabalho_lista[estado]
                if raridade_trabalho=='Comum' and profissao_trabalho==profissao_verificada and estadoTrabalho==para_produzir:
                    print(f'Trabalho na lista: {nome_trabalho}')
                    if nome_trabalho_reconhecido.replace(' ','').lower()==nome_trabalho.replace(' ','').replace('-','').lower():
                        linhaSeparacao()
                        manipula_teclado.click_especifico(1,'enter')
                        contador_paracima+=1
                        trabalho=trabalho_lista
                        break
            else:
                linhaSeparacao()
                manipula_teclado.click_especifico(1,'down')
                contador_paracima+=1
        else:
            manipula_teclado.click_especifico(1,'f1')
            manipula_teclado.click_continuo(9,'up')
            manipula_teclado.click_especifico(1,'left')
            print(f'Trabalho comum não reconhecido!')
            linhaSeparacao()
            break
        # print(f'Teste de contador: {contador_paracima}')
    return trabalho

def retorna_nome_trabalho_reconhecido(yinicial_nome,identificador):
    #recorta frame para reconhecimento de texto
    if identificador==0:
        altura=39
    elif identificador==1:
        altura=68
    #tira novo print da tela
    imagem_inteira=retorna_atualizacao_tela()
    frame_nome_trabalho=imagem_inteira[yinicial_nome:yinicial_nome+altura,233:478]
    #teste trata frame trabalho comum
    frame_nome_trabalho_tratado=manipula_imagem.transforma_branco_preto(frame_nome_trabalho)
    nomeTrabalhoReconhecido=manipula_imagem.reconhece_texto(frame_nome_trabalho_tratado)
    if nomeTrabalhoReconhecido!=None:
        nomeTrabalhoReconhecido=nomeTrabalhoReconhecido.replace(' ','').lower()
    else:
        print(f'Ocorreu algum erro ao reconhecer nome do trabalho!')
        linhaSeparacao()
    return nomeTrabalhoReconhecido

def sai_trabalho_encontrado(x,tipo_trabalho):
    clicks=[2,1]
    manipula_teclado.click_especifico(clicks[tipo_trabalho],'f1')
    manipula_teclado.click_continuo(x+1,'up')
    manipula_teclado.click_especifico(2,'left')

def verifica_erro(trabalho):
    licenca=configura_licenca(trabalho)
    print(f'Verificando erro...')
    erro = retorna_tipo_erro()
# erroPrecisaLicenca=1
# erroFalhaConectar=2
# erroSemRecursos=3
# erroPrecisaEscolherItem=4
# erroConectando=5
# erroSemExperiencia=6
# erroReceberRecompensas=7
# erroSemEspacosProducao=8
# erroConcluirTrabalho=9
# erroManutencaoServidor=10
# erroOutraConeccao=11
# erroSemEspacosBolsa=12
# erroConeccaoInterrompida=13
# erroSemMoedas=14
# erroEmailSenhaIncorreta=15
# erroTempoProducaoExpirou=16
# erroReinoIndisponivel=17
# erroAtualizaJogo=18
    if erro==erroPrecisaLicenca or erro==erroFalhaConectar or erro==erroConexaoInterrompida or erro==erroManutencaoServidor or erro==erroReinoIndisponivel:
        manipula_teclado.click_especifico(2,"enter")
        if erro==erroPrecisaLicenca:
            verifica_licenca(licenca)
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
        manipula_teclado.click_especifico(1,'enter')
        print(f'Voltando para a tela inicial.')
        linhaSeparacao()
    elif erro==erroSemRecursos or erro==erroTempoProducaoExpirou or erro==erroSemExperiencia or erro==erroSemEspacosProducao:
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_continuo(contador_paracima,'up')
        if erro==erroSemRecursos:
            print(f'Retirrando trabalho da lista.')
        elif erro==erroSemExperiencia:
            manipula_teclado.click_especifico(1,'left')
            print(f'Voltando para o menu profissões.')
        elif erro==erroSemEspacosProducao:
            print(f'Sem espaços livres para produção....')
        elif erro==erroTempoProducaoExpirou:
            print(f'O trabalho não está disponível.')
        linhaSeparacao()
    elif erro==erroPrecisaEscolherItem:
        print(f'Escolhendo item.')
        linhaSeparacao()
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(2,'f2')
        manipula_teclado.click_continuo(9,'up')
    elif erro==erroConectando:
        print(f'Conectando...')
        linhaSeparacao()
        time.sleep(1)
    elif erro==erroReceberRecompensas or erro==erroAtualizaJogo:
        manipula_teclado.click_especifico(1,'f2')
        if erro==erroReceberRecompensas:
            print(f'Recuperar presente.')
        elif erro==erroAtualizaJogo:
            print(f'Atualizando jogo...')
            manipula_teclado.click_especifico(1,'f1')
            exit()
        linhaSeparacao()
    elif erro==erroConcluirTrabalho:
        print(f'Trabalho não está concluido!')
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_continuo(8,'up')
        linhaSeparacao()
    elif erro==erroSemEspacosBolsa:
        manipula_teclado.click_especifico(1,'f1')
        print(f'Ignorando trabalho concluído!')
        linhaSeparacao()
    elif erro==erroSemMoedas:
        manipula_teclado.click_especifico(1,'f1')
        linhaSeparacao()
    elif erro==erroEmailSenhaIncorreta:
        manipula_teclado.click_especifico(1,'enter')
        manipula_teclado.click_especifico(1,'f1')
        print(f'Login ou senha incorreta...')
        linhaSeparacao()
    else:
        print(f'Nem um erro encontrado!')
        linhaSeparacao()
    return erro

def entra_licenca(dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    erro=verifica_erro(None)
    if erro==0:
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
        manipula_teclado.click_especifico(1,'up')
        manipula_teclado.click_especifico(1,'enter')
    elif erro==erroOutraConexao:
        dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
    return dicionarioPersonagem

def entra_trabalho_encontrado(x):
    if verifica_erro(None)!=0:
        return False
    manipula_teclado.click_continuo(3,'up')
    manipula_teclado.click_especifico(x+1,'down')
    manipula_teclado.click_especifico(1,'enter')
    return True

#modificado 12/01
def retorna_tipo_erro():
    erro=0
    tela_inteira=retorna_atualizacao_tela()
    frame_erro=tela_inteira[335:335+100,150:526]
    erro_encontrado=manipula_imagem.reconhece_texto(frame_erro)
    print(erro_encontrado)
    if erro_encontrado!=None:
        tipo_erro_trabalho=['precisoumalicençadeproduçãoparainiciarotrabalho','Nãofoipossívelseconectaraoservidor',
                            'Vocênãotemosrecursosnecessáriasparaessetrabalho','Vocêprecisaescolherumitemparainiciarumtrabalhodeprodução',
                            'Conectando','precisomaisexperiênciaprofissionalparainiciarotrabalho','GostariadeiràLojaMilagrosaparaveralistadepresentes',
                            'Vocênãotemespaçoslivresparaotrabalho','agorapormoedas','Oservidorestáemmanutenção',
                            'Foidetectadaoutraconexãousandoseuperfil','Gostanadecomprar','conexãocomoservidorfoiinterrompida',
                            'Vocêprecisademaismoedas','Loginousenhaincorreta','otempodevidada',
                            'reinodejogoselecionado','jogoestadesatualizada']
        for tamanho_tipo_erro in range(len(tipo_erro_trabalho)):
            if tipo_erro_trabalho[tamanho_tipo_erro].lower() in erro_encontrado.replace(' ','').lower():
                erro=tamanho_tipo_erro+1
    return erro

def retorna_nome_inimigo(tela_inteira):
    altura_tela = tela_inteira.shape[0]
    frame_tela = tela_inteira[0:altura_tela,0:674]
    frame_nome_objeto = frame_tela[32:32+30,frame_tela.shape[1]-164:frame_tela.shape[1]]
    frame_nome_objeto_tratado = manipula_imagem.trata_frame_nome_inimigo(frame_nome_objeto)
    nomeInimigo=manipula_imagem.reconhece_texto(frame_nome_objeto_tratado)
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

def verifica_nome_personagem(nome_personagem,posicao):
    confirmacao=False
    nome_personagem_reconhecido_tratado=retornaNomePersonagem(posicao)
    if nome_personagem_reconhecido_tratado!=None:
        if nome_personagem_reconhecido_tratado.replace(' ','').lower()in nome_personagem.replace(' ','').lower():
            print(f'Personagem {nome_personagem_reconhecido_tratado} confirmado!')
            linhaSeparacao()
            confirmacao=True
    else:
        print(f'Nome personagem diferente!')
        linhaSeparacao()
    return confirmacao

def retorna_lista_profissao_verificada(dicionarioPersonagem):
    print(f'Verificando profissões necessárias...')
    #cria lista vazia
    lista_profissao_verificada=[]
    #abre o arquivo lista de profissoes
    conteudo_lista_profissoes=manipula_cliente.consutar_lista(f'{usuario_id}/Lista_personagem/{dicionarioPersonagem[CHAVE_ID_PERSONAGEM]}/Lista_profissoes')
    #abre o arquivo lista de desejos
    conteudo_lista_desejo=manipula_cliente.consulta_lista_desejo(f'{usuario_id}/Lista_personagem/{dicionarioPersonagem[CHAVE_ID_PERSONAGEM]}/Lista_desejo')
    #percorre todas as linha do aquivo profissoes
    for linhaProfissao in range(len(conteudo_lista_profissoes)):
        profissao=conteudo_lista_profissoes[linhaProfissao]
        #percorre todas as linhas do aquivo lista de desejos
        for linhaDesejo in range(len(conteudo_lista_desejo)):
            atributos=conteudo_lista_desejo[linhaDesejo]
            nome_profissao_desejo=atributos[2]
            if(profissao[nome].lower()==nome_profissao_desejo.lower()):
                #verifca se o indice já está na lista
                lista_profissao_verificada.append([profissao[id],profissao[nome],linhaProfissao+1])
                break
    else:
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO]=lista_profissao_verificada
        mostra_profissoes_necessarias(lista_profissao_verificada)
    return dicionarioPersonagem

def mostra_profissoes_necessarias(lista_profissao_verificada):
    for profissao in lista_profissao_verificada:
        print(f'Profissão necessária: {profissao[nome]}')
    linhaSeparacao()

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

def entra_personagem_ativo(listaPersonagem):
    personagem=None
    contadorPersonagem=0
    print(f'Buscando personagem ativo...')
    ativaAtributoUso(listaPersonagem)
    manipula_teclado.click_especifico(1,'enter')
    time.sleep(1)
    while verifica_erro(None)!=0:
        continue
    else:
        manipula_teclado.click_especifico(1,'f2')
        manipula_teclado.click_continuo(8,'left')   
        personagemReconhecido=retornaNomePersonagem(1)
        while personagemReconhecido!=None and contadorPersonagem<13:
            if confirmaNomePersonagem(personagemReconhecido,listaPersonagem):
                manipula_teclado.click_especifico(1,'f2')
                time.sleep(1)
                erro=verifica_erro(None)
                while erro!=0:
                    if erro==11:
                        personagem=personagemReconhecido
                        personagemReconhecido=None
                        break
                    erro=verifica_erro(None)
                else:
                    print(f'Login efetuado com sucesso!')
                    linhaSeparacao()
                    break
            else:
                manipula_teclado.click_especifico(1,'right')
                personagemReconhecido=retornaNomePersonagem(1)
            contadorPersonagem+=1
        else:
            print(f'Personagem não encontrado!')
            linhaSeparacao()
            manipula_teclado.click_especifico(1,'f1')
    return personagem

def confirmaNomePersonagem(personagemReconhecido,listaPersonagem):
    confirmacao=False
    for personagem in listaPersonagem:
        print(f'{personagemReconhecido} e {personagem[nome]}.')
        if personagemReconhecido.replace(' ','').lower() in personagem[nome].replace(' ','').lower():
            print(f'Personagem {personagemReconhecido} confirmado!')
            linhaSeparacao()
            confirmacao=True
    return confirmacao

def ativaAtributoUso(primeiroPersonagem):
    listaPersonagemId=manipula_cliente.retornaListaPersonagemId(usuario_id,primeiroPersonagem[0][2])
    manipula_cliente.mudaAtributoPersonagem(usuario_id,listaPersonagemId,'uso',1)

def retorna_medidas_modelos():
    lista_modelos = [1,2,5,9]
    lista_medidas = []
    print(f'Reconhecendo medidas dos tipos de menus.')
    linhaSeparacao()
    for x in range(len(lista_modelos)):
        nome_modelo = f'modelos/modelo_menu_{lista_modelos[x]}.png'
        modelo = manipula_imagem.abre_imagem(nome_modelo)
        lista_medidas.append(modelo.shape[:2])
    return lista_medidas
#modificado 16/01
def prepara_personagem(id_personagem):
    global personagem_id_global
    #lista_profissao_necessaria é uma matrix onde o indice 0=posição da profissão
    #e o indice 1=nome da profissão
    manipula_teclado.click_atalho_especifico('alt','tab')
    manipula_teclado.click_atalho_especifico('win','left')
    personagem_id_global=id_personagem
    atributosPersonagem=configura_atributos()
    if len(atributosPersonagem)!=0:
        if atributosPersonagem[4]!=1:#se o personagem estiver inativo, troca o estado
            listaPersonagemId=[personagem_id_global]
            manipula_cliente.mudaAtributoPersonagem(usuario_id,listaPersonagemId,'estado',1)
        busca_lista_personagem_ativo()
    else:
        print(f'Erro ao configurar atributos do personagem!')
        linhaSeparacao()

def busca_lista_personagem_ativo():
    global personagem_id_global
    lista_personagem_retirado=[]
    lista_personagem_ativo=manipula_cliente.consulta_lista_personagem(usuario_id)
    lista_personagem=lista_personagem_ativo
    email=2
    senha=3
    while True:
        if verifica_lista_vazia(lista_personagem):
            lista_personagem_retirado=[]
            lista_personagem_ativo=manipula_cliente.consulta_lista_personagem(usuario_id)
            lista_personagem=lista_personagem_ativo
            print(f'Lista de personagens ativos atualizada...')
            linhaSeparacao()
        else:#se houver pelo menos um personagem ativo
            personagem=verifica_nome_reconhecido_na_lista(lista_personagem)
            if personagem!=None:
                personagem_id_global=personagem[id]
                dicionarioPersonagem={CHAVE_ID_PERSONAGEM:personagem_id_global,
                                      CHAVE_UNICA_CONEXAO:True,
                                      CHAVE_ESPACO_BOLSA:True,
                                      CHAVE_LISTA_PROFISSAO_MODIFICADA:False}
                dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=personagem[4]
                print('Inicia busca...')
                linhaSeparacao()
                dicionarioPersonagem=inicia_busca_trabalho(dicionarioPersonagem)
                if dicionarioPersonagem[CHAVE_UNICA_CONEXAO]:
                    if verifica_erro(None)!=0 or len(lista_personagem_ativo)==1:
                        lista_personagem_ativo=manipula_cliente.consulta_lista_personagem(usuario_id)
                        lista_personagem=lista_personagem_ativo
                        print(f'Lista de personagens ativos atualizada...')
                        linhaSeparacao()
                        continue
                    else:
                        manipula_teclado.click_mouse_esquerdo(1,2,35)
                        deslogaPersonagem(personagem[email])
                        lista_personagem_retirado,lista_personagem=remove_personagem_lista(lista_personagem_retirado,personagem)
                else:
                    lista_personagem_retirado,lista_personagem=remove_personagem_lista(lista_personagem_retirado,personagem)
                    continue
            else:#se o nome reconhecido não estiver na lista de ativos
                if len(lista_personagem_retirado)!=0 and lista_personagem_retirado[-1][email]==lista_personagem[0][email]:
                    nome=entra_personagem_ativo(lista_personagem)
                elif configura_login_personagem(lista_personagem[0][email],lista_personagem[0][senha]):
                    nome=entra_personagem_ativo(lista_personagem)
                    if nome!=None:
                        lista_personagem_retirado,lista_personagem=remove_personagem_lista(lista_personagem_retirado,nome)

def retorna_texto_menu_reconhecido(x,y,largura):
    tela_inteira=retorna_atualizacao_tela()
    centroAltura=tela_inteira.shape[0]//2
    centroMetade=tela_inteira.shape[1]//4
    # print(centroAltura)
    alturaFrame=30
    texto=None
    frame_menu=tela_inteira[centroAltura+y:centroAltura+y+alturaFrame,centroMetade+x:centroMetade+x+largura]
    frame_menu_tratado=manipula_imagem.transforma_caracteres_preto(frame_menu)
    # manipula_imagem.mostra_imagem(0,frame_menu_tratado,None)
    # print(f'Quantidade de pixels pretos: {np.sum(frame_menu_tratado==0)}')
    contadorPixelPreto=np.sum(frame_menu_tratado==0)
    if contadorPixelPreto>1000 and contadorPixelPreto<3010:
        texto=manipula_imagem.reconhece_texto(frame_menu_tratado)
        if texto!=None:
            texto=texto.lower().replace(' ','')
            print(f'Texto reconhecimento de menus: {texto}.')
    return texto

def retorna_menu():
    # 1050,1077,3006,1035,1251,1092,1215,1854,1863,1617,1377,2637,1344,
    # 1947,2721
    inicio = time.time()
    print(f'Reconhecendo menu.')
    texto_menu=retorna_texto_menu_reconhecido(-125,-190,350)
    if texto_menu!=None:
        if ('notícias'in texto_menu):
            print(f'Menu notícias...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_noticias
        elif ('seleçãodepersonagem'in texto_menu):
            print(f'Menu escolha de personagem...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_escolha_p
        elif ('produzir'in texto_menu):
            texto_menu=retorna_texto_menu_reconhecido(-75,-140,150)
            if texto_menu!=None:
                if ('profissões'in texto_menu):
                    texto_menu=retorna_texto_menu_reconhecido(-150,225,100)
                    if texto_menu!=None:
                        if('fechar'in texto_menu):
                            print(f'Menu produzir...')
                            linhaSeparacao()
                            fim = time.time()
                            print(f'Tempo de reconhece_texto: {fim - inicio}')
                            linhaSeparacao()
                            return menu_produzir
                        elif ('voltar' in texto_menu):
                            print(f'Menu trabalhos diponíveis...')
                            linhaSeparacao()
                            fim = time.time()
                            print(f'Tempo de reconhece_texto: {fim - inicio}')
                            linhaSeparacao()
                            return menu_trab_disponiveis
                elif ('trabalhosatuais'in texto_menu):
                    print(f'Menu trabalhos atuais...')
                    linhaSeparacao()
                    fim = time.time()
                    print(f'Tempo de reconhece_texto: {fim - inicio}')
                    linhaSeparacao()
                    return menu_trab_atuais
    texto_menu=retorna_texto_sair()
    if texto_menu!=None:
        if texto_menu.lower()=='sair':
            print(f'Menu jogar...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_jogar
    if verifica_menu_referencia():
        print(f'Menu tela inicial...')
        linhaSeparacao()
        fim = time.time()
        print(f'Tempo de reconhece_texto: {fim - inicio}')
        linhaSeparacao()
        return menu_inicial
    texto_menu=retorna_texto_menu_reconhecido(-50,25,100)
    if texto_menu!=None:
        if ('conquistas'in texto_menu):
            print(f'Menu personagem...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_personagem
        elif ('interagir'in texto_menu):
            print(f'Menu principal...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_principal
    texto_menu=retorna_texto_menu_reconhecido(-150,-65,300)
    if texto_menu!=None:
        if('parâmetros'in texto_menu):
            if('requisitos'in texto_menu):
                print(f'Menu atributo do trabalho...')
                linhaSeparacao()
                fim = time.time()
                print(f'Tempo de reconhece_texto: {fim - inicio}')
                linhaSeparacao()
                return menu_trab_atributos
            else:
                print(f'Menu licenças...')
                linhaSeparacao()
                fim = time.time()
                print(f'Tempo de reconhece_texto: {fim - inicio}')
                linhaSeparacao()
                return menu_licencas
    texto_menu=retorna_texto_menu_reconhecido(-60,45,120)
    if texto_menu!=None:
        if('profissional'in texto_menu):
            print(f'Menu trabalho específico...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_trab_especifico
    texto_menu=retorna_texto_menu_reconhecido(-75,-115,150)
    if texto_menu!=None:
        if ('ofertadiária'in texto_menu):
            print(f'Menu oferta diária...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_ofe_diaria
    texto_menu=retorna_texto_menu_reconhecido(-161,-314,300)
    if texto_menu!=None:
        if 'lojamilagrosa'in texto_menu:
            print(f'Menu loja milagrosa...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_loja_milagrosa
    texto_menu=retorna_texto_menu_reconhecido(-161,-344,300)
    if texto_menu!=None:
        if('recompensasdiárias'in texto_menu):
            print(f'Menu recompensas diárias...')
            linhaSeparacao()
            fim = time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_rec_diarias
    texto_menu=retorna_texto_menu_reconhecido(-31,-46,57)
    if texto_menu!=None:
        if 'meuperfil'in texto_menu:
            print(f'Menu meu perfil...')
            linhaSeparacao()
            fim=time.time()
            print(f'Tempo de reconhece_texto: {fim - inicio}')
            linhaSeparacao()
            return menu_meu_perfil

    print(f'Menu não reconhecido...')
    linhaSeparacao()
    fim = time.time()
    print(f'Tempo de reconhece_texto: {fim - inicio}')
    linhaSeparacao()
    manipula_teclado.click_atalho_especifico('win','left')
    manipula_teclado.click_atalho_especifico('win','left')
    verifica_erro(None)
    return menu_desconhecido

def deslogaPersonagem(email):
    menu=retorna_menu()
    while menu!=menu_jogar:
        if menu==menu_inicial:
            manipula_teclado.encerra_secao()
            break
        elif menu==menu_jogar:
            break
        else:
            manipula_teclado.click_mouse_esquerdo(1,2,35)
        menu=retorna_menu()
    if email!=None:
        listaPersonagemId=manipula_cliente.retornaListaPersonagemId(usuario_id,email)
        manipula_cliente.mudaAtributoPersonagem(usuario_id,listaPersonagemId,'uso',0)

def remove_personagem_lista(lista_personagem_retirado,personagem):
    personagem_retirado=personagem[nome]
    lista_personagem_retirado.append(personagem)
    print(f'{personagem_retirado} adicionado a lista de retirados.')
    linhaSeparacao()
    lista_personagem=manipula_cliente.consulta_lista_personagem(usuario_id)
    nova_lista_personagem_ativo=lista_personagem
    print(f'Lista de personagens ativos atualizada!')
    linhaSeparacao()
    for personagem_retirado in lista_personagem_retirado:#percorre lista de personagem retirado
        posicao=0
        for personagem_lista in lista_personagem:#percorre lista de personagem ativo
            if personagem_lista[nome] in personagem_retirado[nome]:#compara nome na lista de ativo com nome na lista de retirado
                print(f'{nova_lista_personagem_ativo[posicao][nome]} foi retirado da lista de ativos!')
                linhaSeparacao()
                del nova_lista_personagem_ativo[posicao]
                posicao-=1
            else:
                posicao+=1
    return lista_personagem_retirado,nova_lista_personagem_ativo

def verifica_lista_vazia(lista_personagem_ativo):
    if len(lista_personagem_ativo)==0:
        print(f'Lista vazia. Buscando nova lista no servidor.')
        linhaSeparacao()
        return True
    return False

def verifica_nome_reconhecido_na_lista(lista_personagem_ativo):
    confirmacao=None
    print(f'Verificando nome personagem...')
    nome_personagem_reconhecido_tratado=retornaNomePersonagem(0)
    if nome_personagem_reconhecido_tratado!=None:
        for personagem_lista in lista_personagem_ativo:
            if nome_personagem_reconhecido_tratado.replace(' ','').lower()in personagem_lista[nome].replace(' ','').lower():
                print(f'Personagem {nome_personagem_reconhecido_tratado} confirmado!')
                linhaSeparacao()
                confirmacao=personagem_lista
    else:
        print(f'Nome personagem diferente!')
        linhaSeparacao()
    return confirmacao

def configura_login_personagem(email, senha):
    login=False
    menu=retorna_menu()
    while menu!=menu_jogar:
        if menu==menu_noticias or menu==menu_escolha_p:
            manipula_teclado.click_especifico(1,'f1')
        elif menu!=menu_inicial:
            manipula_teclado.click_mouse_esquerdo(1,2,35)
        else:
            manipula_teclado.encerra_secao()
        linhaSeparacao()
        menu=retorna_menu()
    else:
        login=loga_personagem(email,senha)
    return login

def configura_atributos():
    return manipula_cliente.consulta_dados_personagem(usuario_id,personagem_id_global)
    
def loga_personagem(email, senha):
    confirmacao=False
    print(f'Tentando logar conta personagem...')
    manipula_teclado.entra_secao(email,senha)
    if verifica_erro(None)!=0:
        print('Erro ao tentar logar...')
    else:
        print(f'Login efetuado com sucesso!')
        confirmacao=True
    linhaSeparacao()
    return confirmacao

def inicia_busca_trabalho(dicionarioPersonagem):
    conteudo_lista_desejo=manipula_cliente.consulta_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id_global}/Lista_desejo')
    dicionarioPersonagem[CHAVE_LISTA_DESEJO]=conteudo_lista_desejo
    if len(conteudo_lista_desejo)>0:#verifica se a lista está vazia
        dicionarioPersonagem=retorna_lista_profissao_verificada(dicionarioPersonagem)
        for profissao_necessaria in dicionarioPersonagem[CHAVE_LISTA_PROFISSAO]:#percorre lista de profissao
            if not dicionarioPersonagem[CHAVE_UNICA_CONEXAO]:
                continue
            erro=verifica_erro(None)
            if erro==0:
                menu=retorna_menu()
                while menu!=menu_produzir:
                    dicionarioPersonagem=trata_menu(menu,dicionarioPersonagem)
                    if not dicionarioPersonagem[CHAVE_CONFIRMACAO]:
                        return dicionarioPersonagem
                    menu=retorna_menu()
                else:
                    if dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]:
                        atualiza_lista_profissao(dicionarioPersonagem)
                    nome_profissao=profissao_necessaria[nome]
                    print(f'Verificando profissão: {nome_profissao}')
                    linhaSeparacao()
                    while True:
                        manipula_teclado.retorna_menu_profissao_especifica(profissao_necessaria[2])
                        posicao_trabalho,trabalho_lista_desejo=verifica_posicoes_trabalhos(nome_profissao,dicionarioPersonagem)
                        dicionarioPersonagem=inicia_processo(posicao_trabalho,trabalho_lista_desejo,nome_profissao,dicionarioPersonagem)
                        if not dicionarioPersonagem[CHAVE_CONFIRMACAO]:#só quebra o laço quando retornar falso
                            break
                    if dicionarioPersonagem[CHAVE_UNICA_CONEXAO]:
                        if dicionarioPersonagem[CHAVE_ESPACO_BOLSA]:
                            if retornaEstadoTrabalho()==concluido:
                                dicionarioPersonagem=verificaTrabalhoConcluido(dicionarioPersonagem)
                        manipula_teclado.click_especifico(1,'left')
            elif erro==erroOutraConexao:
                dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
            else:
                print(f'Erro ao percorrer lista de profissões...')
                linhaSeparacao()
                break
        else:
            print(f'Fim da lista de profissões...')
            linhaSeparacao()
    else:
        print(f'Lista de trabalhos desejados vazia.')
        print(f'Voltando.')
        linhaSeparacao()
    return dicionarioPersonagem

def inicia_processo(posicao_trabalho,trabalho_lista_desejo,profissao_verificada,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    if posicao_trabalho!=-1 and trabalho_lista_desejo!=None:#inicia processo busca por trabalho raro/especial
        if entra_trabalho_encontrado(posicao_trabalho):
            if confirma_nome_trabalho(trabalho_lista_desejo[nome],1):#confirma o nome do trabalho
                dicionarioPersonagem=inicia_producao(trabalho_lista_desejo,dicionarioPersonagem)
                manipula_teclado.click_especifico(1,'left')
            else:    
                sai_trabalho_encontrado(posicao_trabalho,1)
        else:
            print(f'Erro ao entrar no trabalho encontrado...')
            linhaSeparacao()
    elif posicao_trabalho==-1 and trabalho_lista_desejo==None:#inicia processo busca por trabalho comum
        trabalho_comum_reconhecido=verifica_trabalho_comum(profissao_verificada)
        if trabalho_comum_reconhecido!=None:
            dicionarioPersonagem=inicia_producao(trabalho_comum_reconhecido,dicionarioPersonagem)
            manipula_teclado.click_especifico(1,'left')
        else:
            print(f'Erro ao buscar trabalho comum!')
            linhaSeparacao()
    return dicionarioPersonagem

def verificaTrabalhoConcluido(dicionarioPersonagem):
    dicionarioPersonagem=recupera_trabalho_concluido(dicionarioPersonagem)
    if dicionarioPersonagem[CHAVE_TRABALHO_CONCLUIDO]!=False:
        listaPersonagem=[dicionarioPersonagem[CHAVE_ID_PERSONAGEM]]
        dicionarioPersonagem[CHAVE_LISTA_PROFISSAO_MODIFICADA]=True
        manipula_cliente.muda_estado_trabalho(usuario_id,
                                              dicionarioPersonagem[CHAVE_ID_PERSONAGEM],
                                              dicionarioPersonagem[CHAVE_TRABALHO_CONCLUIDO],
                                              2)
        if not dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]:
            manipula_cliente.mudaAtributoPersonagem(usuario_id,listaPersonagem,'espacoProducao',True)
            dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=True
    return dicionarioPersonagem

def recupera_trabalho_concluido(dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_TRABALHO_CONCLUIDO]=False
    tela_inteira=retorna_atualizacao_tela()
    frame_nome_trabalho=tela_inteira[285:285+37, 233:486]
    if verifica_erro(None)==0:
        nome_trabalho_concluido=manipula_imagem.reconhece_texto(frame_nome_trabalho)
        manipula_teclado.click_especifico(1,'down')
        manipula_teclado.click_especifico(1,'f2')
        if nome_trabalho_concluido!=None:
            if verifica_erro(None)==0:
                trabalho_concluido=['',nome_trabalho_concluido,'',0,'','',0,0]
                print(f'{trabalho_concluido[nome]} recuperado.')
                manipula_teclado.click_especifico(1,'up')
                linhaSeparacao()
                dicionarioPersonagem[CHAVE_TRABALHO_CONCLUIDO]=trabalho_concluido[1:-1]
            else:
                dicionarioPersonagem[CHAVE_ESPACO_BOLSA]=False
                manipula_teclado.click_especifico(1,'up')
                manipula_teclado.click_especifico(1,'left')
    return dicionarioPersonagem

def trataErros(trabalho,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
    erro=verifica_erro(trabalho)
    while erro!=0:
        if erro==erroSemRecursos:
            caminho_trabalho=f'{personagem_id_global}/Lista_desejo/{trabalho[id]}'
            excluir_trabalho(caminho_trabalho)  
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        elif erro==erroSemEspacosProducao:#sem espaços de produção livres
            listaPersonagem=[dicionarioPersonagem[CHAVE_ID_PERSONAGEM]]
            manipula_cliente.mudaAtributoPersonagem(usuario_id,listaPersonagem,'espacoProducao',False)
            dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=False
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        elif erro==erroOutraConexao:
            dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        erro=verifica_erro(trabalho)
    return dicionarioPersonagem

def trataMenus(trabalho,dicionarioPersonagem):
    dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    while True:
        menu=retorna_menu()
        if menu==menu_desconhecido:
            continue
        elif menu==menu_trab_especifico:#trabalho especifico
            manipula_teclado.click_especifico(1,'f2')
            if verifica_erro(trabalho)==erroSemRecursos:
                caminho_trabalho=f'{personagem_id_global}/Lista_desejo/{trabalho[id]}'
                excluir_trabalho(caminho_trabalho)
                break
        elif menu==menu_esc_equipamento:#menu escolha equipamento
            manipula_teclado.click_especifico(1,'f2')
            time.sleep(1)
            verifica_erro(trabalho)
        elif menu==menu_trab_atuais:#trabalhos atuais
            clone_trabalho=trabalho
            if trabalho[recorrencia]==1:
                print(f'Recorrencia está ligada.')
                linhaSeparacao()
                clone_trabalho=manipula_cliente.adiciona_trabalho(personagem_id_global,trabalho,trabalho[licenca],1)
            elif trabalho[recorrencia]==0:
                print(f'Recorrencia está desligada.')
                linhaSeparacao()
                manipula_cliente.muda_estado_trabalho(usuario_id,personagem_id_global,clone_trabalho,1)
            manipula_teclado.click_continuo(9,'up')
            dicionarioPersonagem[CHAVE_CONFIRMACAO]=True
            break
        else:
            break
    return dicionarioPersonagem

def inicia_producao(trabalho,dicionarioPersonagem):
    dicionarioPersonagem=entra_licenca(dicionarioPersonagem)
    if dicionarioPersonagem[CHAVE_CONFIRMACAO]:
        if verifica_licenca(trabalho[licenca]):#verifica tipo de licença de produção
            manipula_teclado.click_especifico(1,'f2')#click que definitivamente começa a produção
            dicionarioPersonagem=trataErros(trabalho,dicionarioPersonagem)
            if dicionarioPersonagem[CHAVE_CONFIRMACAO]:
                dicionarioPersonagem=trataMenus(trabalho,dicionarioPersonagem)
                if dicionarioPersonagem[CHAVE_CONFIRMACAO]:
                    while verifica_erro(trabalho)!=0:
                        continue
                    dicionarioPersonagem[CHAVE_LISTA_DESEJO]=conteudo_lista_desejo=manipula_cliente.consulta_lista_desejo(f'{usuario_id}/Lista_personagem/{personagem_id_global}/Lista_desejo')
        else:
            print(f'Erro ao busca licença...')
            linhaSeparacao()
    else:
        print(f'Erro ao entrar na licença...')
        linhaSeparacao()
    return dicionarioPersonagem
    
def verifica_producao_recursos(nome_trabalho_lista_desejo):
    producao_recurso=True
    if not retorna_producao_recursos(nome_trabalho_lista_desejo):
        print(f'Trabalho de produção de equipamentos...')
        linhaSeparacao()
        producao_recurso=False
    else:
        print(f'Trabalho de produção de recursos...')
        linhaSeparacao()
    return producao_recurso

def retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado):
    if listaPersonagemPresenteRecuperado==None:
        print(f'Limpou a lista...')
        linhaSeparacao()
        listaPersonagemPresenteRecuperado=[]
    nomePersonagemReconhecido=retornaNomePersonagem(0)
    if nomePersonagemReconhecido!=None:
        print(f'{nomePersonagemReconhecido} foi adicionado a lista!')
        linhaSeparacao()
        listaPersonagemPresenteRecuperado.append(nomePersonagemReconhecido)
    else:#ocorreu algum erro
        print(f'Erro ao reconhecer nome...')
        linhaSeparacao()
    return listaPersonagemPresenteRecuperado

def recebeTodasRecompensas(menu):
    listaPersonagemPresenteRecuperado=retornaListaPersonagemRecompensaRecebida(None)
    while True:
        reconheceMenuRecompensa(menu)
        print(f'Lista: {listaPersonagemPresenteRecuperado}.')
        linhaSeparacao()
        deslogaPersonagem(None)
        if entraPersonagem(listaPersonagemPresenteRecuperado):
            listaPersonagemPresenteRecuperado=retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado)
        else:
            print(f'Todos os personagens foram verificados!')
            linhaSeparacao()
            break
        menu=retorna_menu()

def recuperaPresente():
    evento=0
    print(f'Buscando recompensa diária...')
    while evento<2:
        telaInteira=retorna_atualizacao_tela()
        metadeAltura=telaInteira.shape[0]//2
        metadeLargura=telaInteira.shape[1]//4
        alturaFrame=80
        y=-261
        larguraFrame=150
        for x in range(8):
            frameTela=telaInteira[metadeAltura+y:metadeAltura+y+alturaFrame,metadeLargura:metadeLargura+larguraFrame]
            # frameTratado=manipula_imagem.retornaImagemCoresInvertidas(frameTela)
            frameTratado=manipula_imagem.transforma_caracteres_preto(frameTela)
            contadorPixelPreto=np.sum(frameTratado==0)
            if contadorPixelPreto>800 and contadorPixelPreto<2200:
                textoReconhecido=manipula_imagem.reconhece_texto(frameTratado)
                # manipula_imagem.mostra_imagem(0,frameTratado,None)
                if textoReconhecido!=None:
                    print(f'Texto reconhecido: {textoReconhecido}.')
                    if textoReconhecido.replace(' ','').lower()=='pegar':
                        centroX=metadeLargura+larguraFrame//2
                        centroY=metadeAltura+y+alturaFrame//2
                        manipula_teclado.click_mouse_esquerdo(1,centroX,centroY)
                        manipula_teclado.posiciona_mouse_esquerdo(telaInteira.shape[1]//2,metadeAltura)
                        if verifica_erro(None)!=0:
                            evento=2
                            break
                        manipula_teclado.click_especifico(1,'f2')
                        manipula_teclado.click_continuo(8,'up')
                        manipula_teclado.click_especifico(1,'left')
                        linhaSeparacao()
                        break
                    elif 'pegarem'in textoReconhecido.replace(' ','').lower():
                        manipula_teclado.click_continuo(8,'up')
                        manipula_teclado.click_especifico(1,'left')
                        linhaSeparacao()
                        break
                else:
                    print(f'Ocorreu algum erro ao reconhecer presente!')
                    linhaSeparacao()
            y+=80
        evento+=1
    manipula_teclado.click_especifico(2,'f1')#sai do menu recupera recompensas

def reconheceMenuRecompensa(menu):
    print(f'Entrou em recuperaPresente.')
    linhaSeparacao()
    if menu==menu_loja_milagrosa:
        manipula_teclado.click_especifico(1,'down')
        manipula_teclado.click_especifico(1,'enter')
        recuperaPresente()
    elif menu==menu_rec_diarias:
        recuperaPresente()
    else:
        print(f'Recompensa diária já recebida!')
        linhaSeparacao()

def retornaNomePersonagem(posicao):
    nome=None
    print(f'Verificando nome personagem...')
    posicaoNome=[[2,33,169,21],[197,354,170,27]]
    telaInteira=retorna_atualizacao_tela()
    frameNomePersonagem=telaInteira[posicaoNome[posicao][1]:posicaoNome[posicao][1]+posicaoNome[posicao][3],posicaoNome[posicao][0]:posicaoNome[posicao][0]+posicaoNome[posicao][2]]
    frameNomePersonagemTratado=manipula_imagem.transforma_caracteres_preto(frameNomePersonagem)
    # manipula_imagem.mostra_imagem(0,frameNomePersonagemTratado,None)
    nomePersonagemReconhecido=manipula_imagem.reconhece_texto(frameNomePersonagemTratado)
    if nomePersonagemReconhecido!=None:
        nomePersonagemReconhecidoTratado=unidecode(nomePersonagemReconhecido)
        if nomePersonagemReconhecidoTratado!='':
            nome=nomePersonagemReconhecidoTratado
            print(f'Personagem reconhecido: {nomePersonagemReconhecidoTratado}')
            linhaSeparacao()
    return nome

def entraPersonagem(listaPersonagemPresenteRecuperado):
    confirmacao=False
    print(f'Buscando próximo personagem...')
    manipula_teclado.click_especifico(1,'enter')
    time.sleep(1)
    erro=verifica_erro(None)
    while erro!=0:
        if erro==5:
            time.sleep(1)
        erro=verifica_erro(None)
    else:
        manipula_teclado.click_especifico(1,'f2')
        if len(listaPersonagemPresenteRecuperado)==1:
            manipula_teclado.click_continuo(8,'left')
        else:
            manipula_teclado.click_especifico(1,'right')
        nomePersonagem=retornaNomePersonagem(1)               
        while True:
            nomePersonagemPresenteado=None
            for nomeLista in listaPersonagemPresenteRecuperado:
                if nomePersonagem==nomeLista and nomePersonagem!=None:
                    nomePersonagemPresenteado=nomeLista
                    break
            if nomePersonagemPresenteado!=None:
                manipula_teclado.click_especifico(1,'right')
                nomePersonagem=retornaNomePersonagem(1)
            if nomePersonagem==None:
                print(f'Fim da lista de personagens!')
                linhaSeparacao()
                manipula_teclado.click_especifico(1,'f1')
                break
            else:
                manipula_teclado.click_especifico(1,'f2')
                time.sleep(1)
                erro=verifica_erro(None)
                while erro!=0:
                    if erro==7:
                        break
                    time.sleep(1.5)
                    erro=verifica_erro(None)
                confirmacao=True
                print(f'Login efetuado com sucesso!')
                linhaSeparacao()
                break
    return confirmacao
    
def usa_habilidade():
    #719:752, 85:128 137:180 189:232
    #muda p/ outra janela
    manipula_teclado.click_atalho_especifico('alt','tab')
    manipula_teclado.click_atalho_especifico('win','up')
    #cria lista com habilidades a serem usadas
    lista_habilidade = retorna_lista_habilidade_verificada()
    if len(lista_habilidade)==0:
        print(f'Erro!')
        linhaSeparacao()
    else:
        print(f'Buscando referência!')
        linhaSeparacao()
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
                                linhaSeparacao()
                                #verica se a habilidade clicada precisa de click do mouse
                                lista_habilidade_clicada.append(habilidade)
                                if verifica_habilidade_central(lista_habilidade_clicada)!=0:
                                    x,y = manipula_teclado.retorna_posicao_mouse()
                                    manipula_teclado.click_mouse_esquerdo(1,x,y)
                                    linhaSeparacao()
                        else:
                            print(f'Modelos com tamanhos diferentes. {tamanho_frame_habilidade}-{tamanho_modelo}')
                            linhaSeparacao()
                posicao_habilidade=verifica_habilidade_central(lista_habilidade)
                if posicao_habilidade!=0:
                    manipula_teclado.click_especifico_habilidade(1,posicao_habilidade)
                    linhaSeparacao()

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
            fatia = manipula_imagem.recorta_frame(f'novo_modelo_habilidade_{indice}')
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
        if (manipula_cliente.muda_quantidade_personagem(usuario_id,nova_quantidade)):
            print(f'Quantidade de personagens ativos modificada com sucesso!')
            linhaSeparacao()

def retorna_atualizacao_tela():
    screenshot = manipula_teclado.tira_screenshot()
    return manipula_imagem.retorna_imagem_colorida(screenshot)

def trata_menu(menu,dicionarioPersonagem):
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
               manipula_teclado.click_especifico(1,'left')
        elif estado_trabalho==0:
            manipula_teclado.click_especifico(1,'left')
    elif menu==menu_rec_diarias or menu==menu_loja_milagrosa:
        recebeTodasRecompensas(menu)
        dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]=False
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    elif menu==menu_principal:
        #menu principal
        manipula_teclado.click_especifico(1,'num1')
        manipula_teclado.click_especifico(1,'num7')
    elif menu==menu_personagem:
        #menu personagem
        manipula_teclado.click_especifico(1,'num7')
    elif menu==menu_trab_disponiveis:
        #menu trabalhos disponiveis
        manipula_teclado.click_especifico(1,'up')
        manipula_teclado.click_especifico(2,'left')
    elif menu==menu_trab_especifico:
        #menu trabalho específico
        manipula_teclado.click_especifico(1,'f1')
        manipula_teclado.click_continuo(3,'up')
        manipula_teclado.click_especifico(2,'left')
    elif menu==menu_ofe_diaria:
        #menu oferta diária
        manipula_teclado.click_especifico(1,'f1')
    elif menu==menu_inicial:
        #tela principal
        manipula_teclado.click_especifico(1,'f2')
        manipula_teclado.click_especifico(1,'num1')
        manipula_teclado.click_especifico(1,'num7')
    else:
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
    erro=verifica_erro(None)
    if erro==erroOutraConexao:
        dicionarioPersonagem[CHAVE_CONFIRMACAO]=False
        dicionarioPersonagem[CHAVE_UNICA_CONEXAO]=False
    return dicionarioPersonagem
    
def configura_licenca(trabalho):
    licenca=4
    if trabalho==None:
        return ''
    return trabalho[licenca]

def recebeCorrespondencia():
    manipula_teclado.click_especifico(1,'f2')
    manipula_teclado.click_especifico(1,'1')
    manipula_teclado.click_especifico(1,'9')

    

def verificaPixelCorrespondencia():
    confirmacao=False
    tela=retorna_atualizacao_tela()
    frameTela=tela[665:690,644:675]
    contadorPixelCorrespondencia=np.sum(frameTela==(173,239,247))
    if contadorPixelCorrespondencia>50:
        print(f'Há correspondencia!')
        confirmacao=True
    else:
        print(f'Não há correspondencia!')
    linhaSeparacao()
    return confirmacao

def descobreFrames():
    tela_inteira=retorna_atualizacao_tela()
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
    
    frame_menu_tratado=manipula_imagem.transforma_caracteres_preto(frameMenuOferta)
    print(manipula_imagem.reconhece_texto(frame_menu_tratado))
    manipula_imagem.mostra_imagem(0,frameMenuOferta,None)
    # manipula_imagem.mostra_imagem(0,frameMenuProfissoes,None)
    # manipula_imagem.mostra_imagem(0,frameMenuVoltar,None)
    # manipula_imagem.mostra_imagem(0,frameMenuNoticias,None)
    # manipula_imagem.mostra_imagem(0,frameMenuAvancar,None)
# descobreFrames()

def retorna_texto_sair():
    texto=None
    tela_inteira = retorna_atualizacao_tela()
    alturaTela=tela_inteira.shape[0]
    frame_jogar = tela_inteira[alturaTela-50:alturaTela-25,50:50+60]
    frame_jogar_tratado = manipula_imagem.transforma_menu_preto(frame_jogar)
    # manipula_imagem.mostra_imagem(0,frame_jogar_tratado,None)
    # print(f'Quantidade de pixels pretos: {np.sum(frame_jogar_tratado==0)}')
    contadorPixelPreto=np.sum(frame_jogar_tratado==0)
    if contadorPixelPreto>1000 and contadorPixelPreto<1100:
        texto=manipula_imagem.reconhece_texto(frame_jogar_tratado)
        if texto!=None:
            texto=texto.lower().replace(' ','')
    return texto

def retorna_lista_pixel_minimap():
    lista_pixel=[]
    xMapa=568
    yMapa=179
    somaX=1
    somaY=0
    fundo=manipula_imagem.retorna_fundo_branco()
    telaInteira=retorna_atualizacao_tela()
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
    manipula_imagem.mostra_imagem(0,fundo,'Minimapa')
    return lista_pixel

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

def linhaSeparacao():
    print(f'____________________________________________________')

def entra_usuario():
    email = input(f'Email: ')
    senha = input(f'Senha: ')
    if manipula_cliente.autenticar_usuario(email,senha):
        return True
    return False
    
def deleta_item_lista():
    lista=['a','b','c']
    print(f'{lista}')
    item=int(input(f'Deletar: '))
    del lista[item]
    print(f'{lista}')

def funcao_teste(id_personagem):
    global personagem_id_global
    personagem_id_global=id_personagem
    dicionarioPersonagem={CHAVE_ID_PERSONAGEM:id_personagem}
    listaPersonagem=[dicionarioPersonagem[CHAVE_ID_PERSONAGEM]]
    manipula_teclado.click_atalho_especifico('alt','tab')
    # deleta_item_lista()
    verifica_erro(None)
    # manipula_teclado.click_atalho_especifico('win','up')
    # lista_personagem_ativo = manipula_cliente.consulta_lista_personagem(usuario_id)
    # busca_lista_personagem_ativo(lista_personagem_ativo)
    # while not loga_personagem('caah.rm15@gmail.com','aeioukel'):
    #     continue
    # verifica_producao_recursos('Licença de produção do aprendiz')
    # manipula_teclado.click_continuo(9,'up')
    # print(retorna_texto_menu_reconhecido())
    # recupera_trabalho_concluido()
    # while True:
    # atualiza_nova_tela()
    # manipula_teclado.click_continuo(8,'up')
    # confirma_nome_trabalho('Melhorar licença comum',1)
    #     menu=retorna_menu()
    #     if menu!=11:
    #         trata_menu(menu,dicionarioPersonagem)
    #     break
    # print('Fim')
    # lista_habilidade = retorna_lista_habilidade_verificada()
    # lista_ativos = manipula_cliente.consulta_lista_personagem(usuario_id)
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
    #     manipula_cliente.mudaAtributoPersonagem(usuario_id,listaPersonagem,'espacoProducao',valor)
    # if verifica_menu_referencia():
    #     print('Achei!')
    # else:
    #     print('Não achei...')
    # retorna_tipo_erro()
    # dicionarioPersonagem=retorna_lista_profissao_verificada(dicionarioPersonagem)
    # atualiza_lista_profissao(dicionarioPersonagem)
    # while input(f'Continuar?')!='n':
    #     retorna_menu()
    verificaPixelCorrespondencia()
    # dicionarioPersonagem={CHAVE_ID_PERSONAGEM:personagem_id_global,CHAVE_ESPACO_PRODUCAO:True,CHAVE_UNICA_CONEXAO:True}
    # print(dicionarioPersonagem[CHAVE_UNICA_CONEXAO])
    # manipula_cliente.adicionar_profissao(personagem_id_global,'Teste')
    # trabalho = 'trabalhoid','Apêndice de jade ofuscada','profissaoteste','comum','Licença de produção do iniciante'
    # inicia_producao(trabalho,dicionarioPersonagem)
    # verifica_trabalho_comum(trabalho,'profissaoteste')
    # while inicia_busca_trabalho():
    #     continue
    # entra_personagem_ativo('mrninguem')
    # inicia_busca_trabalho()
    manipula_teclado.click_atalho_especifico('alt','tab')
# funcao_teste('')
# verifica_erro(None)
# entra_personagem_ativo('Raulssauro')
# recebeTodasRecompensas(menu)
# recuperaPresente()
# entraPersonagem(['tobraba','gunsa','totiste'])
# entra_personagem_ativo('tobraba')
# busca_lista_personagem_ativo_teste()
# print(retornaNomePersonagem(1))