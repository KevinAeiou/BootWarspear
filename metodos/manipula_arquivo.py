from pyautogui import hotkey, sleep

novo_modelo_raro = 'novo_modelo_raro.png'
caminho_arquivo_lista_desejo = 'arquivos\lista_trabalho_desejado.txt'

def retorna_conteudo_arquivo(caminho_arquivo):
    with open(caminho_arquivo,'r',encoding='utf-8') as arquivo:
        return arquivo.readlines()

def mostra_lista(conteudo_arquivo):
    quant_trabalho_desejado = len(conteudo_arquivo)
    for x in range(quant_trabalho_desejado):
        conteudo_linha = conteudo_arquivo[x].split(',')
        print(f'{x+1} - {conteudo_linha[0].upper()}')
    print(f'0 - Voltar.')
    
def seta_ponteiro():
    for x in range(10):
        hotkey('up')
    sleep(2)
    hotkey('left')
    sleep(2)
    hotkey('down')
    sleep(2)
    #entra na primeira profissão
    hotkey('enter')
    sleep(2)
    hotkey('up')
    sleep(2)

def retorna_quantidade_trabalho_estoque():
    quant_trabalho = 0
    return quant_trabalho

def compara_string_lista(texto, nome_profissao):
    nome_arquivo_profissao = f'profissao_{nome_profissao}.txt'
    with open(nome_arquivo_profissao, encoding='utf-8') as arquivo:
        lista_trabalho = arquivo.readlines()
    for x in lista_trabalho:
        if x == texto:
            return True
    return False

def cria_lista_trabalho_desejado(indice, lista):
    lista_trabalho_dessejado = []
    lista_trabalho_dessejado.append(lista[indice])
    return lista_trabalho_dessejado

def retorna_conteudo_linha_lista(caminho_arquivo_lista,indice_arquivo,indice_linha):
    conteudo_arquivo = retorna_conteudo_arquivo(caminho_arquivo_lista)
    conteudo_linha = conteudo_arquivo[indice_arquivo].split(',')
    return conteudo_linha[indice_linha]

def inclui_linha(linha, caminho_arquivo):
    conteudo_arquivo = retorna_conteudo_arquivo(caminho_arquivo)
    total_linhas = len(conteudo_arquivo)
    if total_linhas==0:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(f'{linha}\n')
        print(f'{linha} adicionado!')
        print('____________________________________')
    else:
        with open(caminho_arquivo, 'a', encoding='utf-8') as arquivo:
            arquivo.writelines(f'{linha}\n')
        print(f'{linha} adicionado!')
        print('____________________________________')

def exclui_nome_trabalho(posicao):
    conteudo_arquivo = retorna_conteudo_arquivo(caminho_arquivo_lista_desejo)
    ponteiro = 0
    with open(caminho_arquivo_lista_desejo, 'w',encoding='utf-8') as arquivo_escrito:
        for linha in conteudo_arquivo:
            if ponteiro != posicao:
                arquivo_escrito.write(linha)
            ponteiro+=1
    print(f'Deletado.')

def limpa_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'w') as arquivo:
        pass