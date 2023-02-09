import time
import cv2
import pyautogui as tecla

tela = 'boot_warspear\atualizacao_tela.png'
lista_profissoes = 'arquivos\lista_profissoes.txt'
nome_arquivo_trabalho = 'arquivos\lista_trabalho_desejado.txt'

def tira_screenshot():
    return tecla.screenshot()
#proxima posição yinicial=365, yfinal=412
def atualiza_lista_profissoes():
    contador=0
    yinicial = 295
    yfinal = 342
    print(f'Lista de profissões vazia.')
    reconhece_tela.atualiza_nova_tela()
    #reconhece profissão
    #seleciona frame para comparação
    #se contador for igual a 4
    while contador<8:
        if contador == 4:
            x=0
            for x in range(5):
                tecla.hotkey('down')
            reconhece_tela.atualiza_nova_tela()
            imagem = cv2.imread(tela)
            fatia_imagem = imagem[539:586, 181:228]
            #compara o frame com os modelos das profissões
            #fatia_imagem = cv2.cvtColor(np.array(fatia_imagem), cv2.COLOR_BGR2GRAY)
            nome_profissao = compara_frame_modelo(fatia_imagem)
            print(f'Gravou {nome_profissao}')
            inclui_nome_profissao(nome_profissao,'a')
            contador+=1
        elif contador > 4:
            tecla.hotkey('down')
            reconhece_tela.atualiza_nova_tela()
            imagem = cv2.imread(tela)
            fatia_imagem = imagem[539:586, 181:228]
            #fatia_imagem = cv2.cvtColor(np.array(fatia_imagem), cv2.COLOR_BGR2GRAY)
            #compara o frame com os modelos das profissões
            nome_profissao = compara_frame_modelo(fatia_imagem)
            print(f'Gravou {nome_profissao}')
            inclui_nome_profissao(nome_profissao,'a')
            contador+=1
        elif contador==0:
            imagem = cv2.imread(tela)
            fatia_imagem = imagem[yinicial:yfinal, 181:228]
            nome_profissao = compara_frame_modelo(fatia_imagem)
            print(f'Gravou {nome_profissao}')
            inclui_nome_profissao(nome_profissao,'w')
            yinicial = yinicial+70
            yfinal = yfinal+70
            contador+=1  
        else:
            imagem = cv2.imread(tela)
            fatia_imagem = imagem[yinicial:yfinal, 181:228]
            #fatia_imagem = cv2.cvtColor(np.array(fatia_imagem), cv2.COLOR_BGR2GRAY)
            #compara o frame com os modelos das profissões
            nome_profissao = compara_frame_modelo(fatia_imagem)
            print(f'Gravou {nome_profissao}')
            inclui_nome_profissao(nome_profissao,'a')
            yinicial = yinicial+70
            yfinal = yfinal+70
            contador+=1 

def inclui_nome_profissao(nome_profissao,a):
    y = open(lista_profissoes, 'r')
    total_linhas = len(y.readlines())
    id = total_linhas+1
    y.close()
    x = open(lista_profissoes, a, encoding='utf-8')
    escreve = x.writelines(f'{id},{nome_profissao}\n')
    x.close()

def busca_nome_profissao(id_profissao):
    with open(lista_profissoes, 'r') as arquivo:
        arquivo_conteudo = arquivo.readlines()
        ajuste = arquivo_conteudo[id_profissao-1].strip().split(',')
        nome_profissao = ajuste[1]
    return nome_profissao

def busca_trabalho(nome_trabalho):
    with open(nome_arquivo_trabalho, 'r', encoding='utf-8') as arquivo:
        conteudo_arquivo = arquivo.readlines()
        total_linhas = len(conteudo_arquivo)
    while total_linhas>0:
        conteudo_linha = conteudo_arquivo[total_linhas-1].split(',')
        if nome_trabalho == conteudo_linha[0]:
            print(f'Trabalho disponivel está na posição {total_linhas} da lista. Iniciar o trabalho')
            return total_linhas
        else:
            print(conteudo_linha[0])
            total_linhas-=1
    else:
        print(f'Trabalho não desejado.')
        return 0

def retorna_tamanho_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        conteudo_arquivo = arquivo.readlines()
        return len(conteudo_arquivo)

def compara_frame_modelo(frame_comparacao):
    i=0
    #define lista com nomes das profissoes
    nome_profissoes = ['aneis','amuletos','corpo_corpo','leve','longo_alcance','mantos','pesada','tecido']
    while i < 8:
        #forma o nome da profissão que será comparada
        nome_profissao = 'modelos\modelo_profissao_'+nome_profissoes[i]+'.png'
        #abre o modelo para comparação
        modelo_comparacao = cv2.imread(nome_profissao)
        #modelo_comparacao = cv2.cvtColor(np.array(modelo_comparacao), cv2.COLOR_BGR2GRAY)
        diferenca = cv2.subtract(modelo_comparacao, frame_comparacao)
        b,g,r = cv2.split(diferenca)
        if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
            #reconhece o nivel que a profissão encontrada está
            print(f'Modelo e frame identicos!')
            return nome_profissoes[i]
        else:
            i+=1
    return 'Desconhecido'

def inicia_trabalho(posicao):
    time.sleep(1)
    while posicao>=0:
        tecla.hotkey('down')
        print('Baixo.')
        time.sleep(1)
        posicao-=1
    else:
        tecla.hotkey('f2')
        print('F2.')
        print('____________________________________')
        time.sleep(1) 

def retorna_menu_profissao_especifica(indice):
    time.sleep(0.5)
    for x in range(indice):
        tecla.hotkey('down')
        print('Baixo.')
        time.sleep(0.5)
    tecla.hotkey('enter')
    print('Enter.')
    time.sleep(2)
    tecla.hotkey('up')
    print('Cima.')
    time.sleep(0.5)
    print('____________________________________')

def vai_inicio_fila():
    for posicao_personagem in range(10):
        tecla.press('left')

def entra_secao(email,senha):
    click_especifico(1,'f2')
    click_especifico(1,0)
    click_especifico(1,'f2')
    click_especifico(1,'down')
    for x in range(30):
        tecla.press('backspace')
    tecla.write(email)
    click_especifico(1,'down')
    tecla.write(senha)
    click_especifico(2,'down')
    click_especifico(1,'enter')
    time.sleep(5)

def entra_personagem(personagem):
    click_especifico(1,'f2')

def encerra_secao():
    click_especifico(1,'f2')
    click_especifico(1,8)
    click_especifico(1,5)
    click_especifico(1,'f2')

def click_para_cima(clicks):
    time.sleep(1)
    for x in range(clicks):
        tecla.hotkey('up')
        print('Cima.')
        time.sleep(1)
    print('____________________________________')
    time.sleep(1)

def click_f2(clicks):
    time.sleep(1)
    for x in range(clicks):
        tecla.hotkey('F2')
        print('F2.')
        time.sleep(3)
    print('____________________________________')
    time.sleep(1)

def click_enter(clicks):
    time.sleep(1)
    for x in range(clicks):
        tecla.hotkey('enter')
        print('Enter.')
        time.sleep(2)
    print('____________________________________')
    time.sleep(1)

def click_especifico(clicks,tecla_esp):
    time.sleep(0.5)
    for x in range(clicks):
        if isinstance(tecla_esp,int):
            tecla_esp+=1
            tecla_num=f'num{tecla_esp}'
        else:
            tecla_num = tecla_esp
        tecla.hotkey(tecla_num)
        print(f'{tecla_esp}.')
        time.sleep(1)
    
def click_atalho_especifico(tecla1,tecla2):
    time.sleep(1)
    tecla.hotkey(tecla1,tecla2)
    print(f'{tecla1}+{tecla2}')
    time.sleep(1)

def click_especifico_habilidade(clicks,tecla_esp):
    time.sleep(0.5)
    for x in range(clicks):
        if isinstance(tecla_esp,int):
            tecla_esp+=1
            tecla_num=f'num{tecla_esp}'
        else:
            tecla_num = tecla_esp
        tecla.keyDown('alt')
        tecla.hotkey(tecla_num)
        tecla.keyUp('alt')
        print(f'{tecla_esp}.')
        time.sleep(0.5)

def click_mouse_esquerdo(clicks,x_tela,y_tela):
    time.sleep(1)
    for x in range(clicks):
        tecla.leftClick(x_tela,y_tela)
        print(f'Click em {x_tela}:{y_tela}.')
        time.sleep(2)

def retorna_posicao_mouse():
    return tecla.position()