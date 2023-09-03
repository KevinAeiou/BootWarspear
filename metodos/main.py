import time, sys
from manipula_funcoes import *
from manipula_cliente import *

nome_arquivo_lista_profissoes = 'arquivos/lista_profissoes.txt'
nome_arquivo_lista_trabalho = 'arquivos\lista_trabalho_desejado.txt'

def mostraMenuListaDesejo(dicionarioUsuario):
    print(f'Lista de trabalhos desejados:')
    dicionarioUsuario=defineListaDesejo(dicionarioUsuario)
    if not listaEstaVazia(dicionarioUsuario[CHAVE_LISTA_DESEJO]):
        mostraListaDesejo(dicionarioUsuario)
    else:
        print(f'A lista está vazia.')
        linhaSeparacao()
    print(f'1 - Iniciar a busca.')
    print(f'2 - Excluir trabalho da lista.')
    print(f'0 - Voltar.')
    opcaoLista = input(f'Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoLista,2):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoLista=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoLista = int(opcaoLista)
        if opcaoLista==0:
            return 0
    return dicionarioUsuario,opcaoLista

def opcaoInvalida(opcaoLista,tamanhoMenu):
    return not opcaoLista.isdigit() or int(opcaoLista)<0 or int(opcaoLista)>tamanhoMenu

def defineLicenca():
    print(f'Qual o tipo da licença de produção desejada?')
    print(f'1 - Licença do iniciante.')
    print(f'2 - Licença do aprendiz.')
    print(f'3 - Licença do mestre.')
    print(f'4 - Licença do principiante.')
    print(f'0 - Voltar.')
    opcaoLicenca = input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoLicenca,4):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoLicenca=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoLicenca=int(opcaoLicenca)
        if opcaoLicenca==0:
            licenca=None
        if opcaoLicenca==1:
            licenca='Licença de produção do iniciante'
        elif opcaoLicenca==2:
            licenca='Licença de produção do aprendiz'
        elif opcaoLicenca==3:
            licenca='Licença de produção do mestre'
        elif opcaoLicenca==4:
            licenca='Licença de produção do principiante'
    return licenca

def defineRaridade():
    print(f'Qual a raridade da produção?')
    print(f'1 - Comum.')
    print(f'2 - Raro.')
    print(f'3 - Especial.')
    print(f'0 - Voltar.')
    opcaoRaridade=input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoRaridade,3):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoRaridade=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoRaridade=int(opcaoRaridade)
        if opcaoRaridade==0:
            tipoRaridade=None
        elif opcaoRaridade==1:
            tipoRaridade='Comum'
        elif opcaoRaridade==2:
            tipoRaridade='Raro'
        elif opcaoRaridade==3:
            tipoRaridade='Especial'
    return tipoRaridade

def defineRecorrencia():
    print(f'Trabalho é recorrente?')
    print(f'1 - Sim.')
    print(f'2 - Não.')
    print(f'0 - Voltar.')
    opcaoRecorrencia=input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoRecorrencia,2):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoRecorrencia=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoRecorrencia=int(opcaoRecorrencia)
        if opcaoRecorrencia==0:
            recorrencia=None
        elif opcaoRecorrencia==1:
            recorrencia=True
        elif opcaoRecorrencia==2:
            recorrencia=False
    return recorrencia

def mostraMenuHabilidade():
    print(f'Habilidade.')
    print(f'1 - Usa habilidade.')
    print(f'2 - Cadastra nova habilidade.')
    print(f'0 - Voltar.')
    opcaoHabilidade=input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoHabilidade,2):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoHabilidade=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoHabilidade=int(opcaoHabilidade)
        if opcaoHabilidade==0:
            return 0
    return opcaoHabilidade

def mostraMenuCadastrar():
    print(f'Cadastro.')
    print(f'1 - Cadastrar trabalho.')
    print(f'2 - Cadastrar habilidade.')
    print(f'0 - Voltar.')
    opcaoCadastro = input(f'Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoCadastro,2):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoCadastro=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoCadastro=int(opcaoCadastro)
        if opcaoCadastro==0:
            return 0
    return opcaoCadastro

def defineNivel():
    print(f'Define nível.')
    print(f'0 - Voltar.')
    nivelTrabalho=input(f'Nivel do trabalho: ')
    while opcaoInvalida(nivelTrabalho,32):
        print(f'Opção inválida! Selecione uma das opções.')
        nivelTrabalho = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        nivelTrabalho=int(nivelTrabalho)
        if nivelTrabalho==0:
            return None
        return nivelTrabalho

def defineProfissao(dicionarioUsuario):
    print(f'Define de profissão.')
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]=retornaListaDicionarioProfissao(dicionarioUsuario)
    if listaEstaVazia(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]):
        linhaSeparacao()
        menu(dicionarioUsuario)
    else:    
        mostraLista(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO])
        opcaoProfissao=input('Profissão escolhida: ')
        linhaSeparacao()
        while opcaoInvalida(opcaoProfissao,len(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO])):
            print(f'Opção inválida! Selecione uma das opções.')
            opcaoProfissao=input(f'Sua escolha: ')
            linhaSeparacao()
        else:
            opcaoProfissao=int(opcaoProfissao)
            if opcaoProfissao==0:
                return None
            else:
                profissao=defineNomeProfissao(dicionarioUsuario, opcaoProfissao)
    return profissao

def defineNomeProfissao(dicionarioUsuario, opcaoProfissao):
    x=1
    for profissao in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
        if x==opcaoProfissao:
            profissao=profissao[CHAVE_NOME]
            break
        x+=1
    return profissao

def defineTrabalho(profissao,raridade):
    print(f'Trabalhos:')
    dicionarioTrabalho={}
    listaDicionariosTrabalhos=retornaListaDicionariosTrabalhos()
    if not listaEstaVazia(listaDicionariosTrabalhos):
        listaDicionariosTrabalhosBuscados=retornaListaDicionariosTrabalhosBuscados(listaDicionariosTrabalhos,profissao,raridade)
        if not listaEstaVazia(listaDicionariosTrabalhosBuscados):
            mostraLista(listaDicionariosTrabalhosBuscados)
            opcaoTrabalho=input(f'Trabalho escolhido: ')
            linhaSeparacao()
            while opcaoInvalida(opcaoTrabalho,len(listaDicionariosTrabalhosBuscados)):
                print(f'Opção inválida! Selecione uma das opções.')
                opcaoTrabalho=input(f'Sua escolha: ')
                linhaSeparacao()
            else:
                opcaoTrabalho=int(opcaoTrabalho)
                if opcaoTrabalho==0:
                    dicionarioTrabalho={}
                else:
                    x=1
                    for trabalho in listaDicionariosTrabalhosBuscados:
                        if x==opcaoTrabalho:
                            dicionarioTrabalho=trabalho
                            dicionarioTrabalho[CHAVE_RARIDADE]=raridade
                            dicionarioTrabalho[CHAVE_PROFISSAO]=profissao
                            break
                        x+=1
        else:
            print(f'Lista de vazia!')
            linhaSeparacao()
    else:
        print(f'Lista de vazia!')
        linhaSeparacao()
    return dicionarioTrabalho

def mostraMenuConfiuracao():
    print(f'Configurações:')
    print(f'1 - Quantidade de personagens ativos.')
    print(f'0 - Voltar.')
    opcao_configuracao = input(f'Sua escolha: ')
    linhaSeparacao()
    while not opcao_configuracao.isdigit() or int(opcao_configuracao)<0 or int(opcao_configuracao)>1:
        print(f'Opção inválida! Selecione uma das opções.')
        opcao_configuracao = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcao_configuracao = int(opcao_configuracao)
        if opcao_configuracao==0:
            return 0
    return opcao_configuracao

def menu(dicionarioUsuario):
    print(f'Menu')
    print(f'Opções:')
    print(f'1 - Produzir item.')
    print(f'2 - Lista de desejo.')
    print(f'3 - Usar habilidade.')
    print(f'4 - Atualizar lista de profissões.')
    print(f'5 - Cadastrar.')
    print(f'6 - Configurações.')
    print(f'7 - Temporario.')
    print(f'0 - Voltar.')
    opcaoEscolha=input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoEscolha,7):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoEscolha=input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoEscolha=int(opcaoEscolha)
        if opcaoEscolha==0:#Volta ao menu anterior
            print(f'Voltar...')
            linhaSeparacao()
            menuPersonagem(dicionarioUsuario)
            return
        elif opcaoEscolha==1:#Menu adicionar novo trabalho a lista
            raridade=defineRaridade()
            if variavelExiste(raridade):
                profissao=defineProfissao(dicionarioUsuario)
                if variavelExiste(profissao):
                    dicionarioTrabalho=defineTrabalho(profissao,raridade)
                    if not listaEstaVazia(dicionarioTrabalho):
                        licenca=defineLicenca()
                        if variavelExiste(licenca):
                            dicionarioTrabalho[CHAVE_LICENCA]=licenca
                            recorrencia=defineRecorrencia()
                            if variavelExiste(recorrencia):
                                dicionarioTrabalho[CHAVE_RECORRENCIA]=recorrencia
                                adicionaTrabalhoDesejo(dicionarioUsuario,dicionarioTrabalho)
        elif opcaoEscolha==2:#Menu lista de desejo
            dicionarioUsuario,opcaoLista=mostraMenuListaDesejo(dicionarioUsuario)
            if opcaoLista == 0:#Volta ao menu anterior
                print(f'Voltar.')
                linhaSeparacao()
            elif opcaoLista == 1:#Inicia busca
                preparaPersonagem(dicionarioUsuario)
                linhaSeparacao()
            elif opcaoLista == 2:#Exclui trabalho da lista
                menuExcluiTrabalho(dicionarioUsuario)
                linhaSeparacao()
        elif opcaoEscolha==3:#Menu habilidade
            opcao_habilidade = mostraMenuHabilidade()
            if opcao_habilidade == 0:#Volta ao menu anterior
                print(f'Voltar.')
                linhaSeparacao()
            elif opcao_habilidade == 1:#Usa habilidades
                #exec(open('metodos/manipula_tela.py').read())
                usa_habilidade()
            elif opcao_habilidade == 2:#Cadastra novo modelo de habilidade
                recorta_novo_modelo_habilidade()
        elif opcaoEscolha==4:#Atualiza lista de profissões
            pass
            # atualiza_lista_profissao(dicionarioUsuario)
        elif opcaoEscolha==5:#Menu cadastro
            opcao_cadastro = mostraMenuCadastrar()
            if opcao_cadastro == 0:#Volta ao menu anterior
                print(f'Voltar.')
                linhaSeparacao()
            elif opcao_cadastro == 1:#Cadastra novo trabalho
                raridade=defineRaridade() 
                if variavelExiste(raridade):
                    profissao=defineProfissao(dicionarioUsuario)
                    if variavelExiste(profissao):
                        nivel=defineNivel()
                        if variavelExiste(nivel):
                            defineNovoTrabalho(raridade,profissao,nivel)
            elif opcao_cadastro == 2:#Cadastra novo modelo de habilidade
                print(f'Em desenvolvimento...')
                linhaSeparacao()
        elif opcaoEscolha==6:#Menu configurações
            opcao_configuracao = mostraMenuConfiuracao()
            if opcao_configuracao == 0:#Volta ao menu anterior
                print(f'Voltar.')
                linhaSeparacao()
            elif opcao_configuracao==1:
                modifica_quantidade_personagem_ativo()
        elif opcaoEscolha==7:#Menu teste
            funcao_teste(dicionarioUsuario)
            linhaSeparacao()
        menu(dicionarioUsuario)
    return

def defineDicionarioTrabalho(dicionarioUsuario,opcaoExclui):
    dicionarioTrabalhoExclui={}
    contador=1
    for dicionarioTrabalho in dicionarioUsuario[CHAVE_LISTA_DESEJO]:
        if contador==opcaoExclui:
            dicionarioTrabalhoExclui=dicionarioTrabalho
            return dicionarioTrabalhoExclui
        contador+=1
    else:
        print(f'Erro ao definir dicionarioTrabalho!')
        linhaSeparacao()
    return dicionarioTrabalhoExclui

def menuExcluiTrabalho(dicionarioUsuario):
    mostraLista(dicionarioUsuario[CHAVE_LISTA_DESEJO])
    opcaoExclui=input(f'Qual trabalho deseja exluir?')
    linhaSeparacao()
    while opcaoInvalida(opcaoExclui,len(dicionarioUsuario[CHAVE_LISTA_DESEJO])):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoExclui = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoExclui = int(opcaoExclui)
        if opcaoExclui==0:
            return
        else:
            dicionarioTrabalho=defineDicionarioTrabalho(dicionarioUsuario,opcaoExclui)
            excluiTrabalho(dicionarioUsuario,dicionarioTrabalho)

def menuPersonagem(dicionarioUsuario):
    print(f'Personagens.')
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=defineListaDicionarioPersonagem(dicionarioUsuario)
    if listaEstaVazia(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]):
        menuTeste()
        return
    else:
        mostraLista(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM])
        opcaoPersonagem=input('Personagem escolhido: ')
        linhaSeparacao()
        while opcaoInvalida(opcaoPersonagem,len(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM])):
            print(f'Opção inválida! Selecione um personagem.')
            opcaoPersonagem=input(f'Sua escolha: ')
            linhaSeparacao()
        else:
            opcaoPersonagem=int(opcaoPersonagem)
            if opcaoPersonagem==0:
                menuTeste()
            else:
                dicionarioUsuario=defineChaveIdPersonagem(dicionarioUsuario,opcaoPersonagem)
                menu(dicionarioUsuario)

def defineChaveIdPersonagem(dicionarioUsuario,opcaoPersonagem):
    x=1
    for personagem in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        if x==opcaoPersonagem:
            dicionarioUsuario[CHAVE_ID_PERSONAGEM]=personagem[CHAVE_ID]
            break
        x+=1
    return dicionarioUsuario

def menuTeste():
    dicionarioUsuario={CHAVE_ID_USUARIO:None,
                       CHAVE_ID_PERSONAGEM:None,
                       CHAVE_NOME:None,
                       CHAVE_LISTA_DICIONARIO_PERSONAGEM:[]}
    print(f'Menu teste.')
    print(f'1 - Usuario')
    print(f'2 - Usuario teste')
    print(f'0 - Sair')
    opcao_personagem = input('Usuario escolhido: ')
    linhaSeparacao()
    while not opcao_personagem.isdigit() or int(opcao_personagem)<0 or int(opcao_personagem)>2:
        print(f'Opção inválida! Selecione um personagem.')
        opcao_personagem = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcao_personagem = int(opcao_personagem)
        if opcao_personagem==0:
            print(f'Saindo...')
            for i in range(0,10):
                sys.stdout.write(f'\r{i}')
                sys.stdout.flush()
                time.sleep(1)
            exit()
        else:
            if opcao_personagem==1:
                dicionarioUsuario[CHAVE_ID_USUARIO]='eEDku1Rvy7f7vbwJiVW7YMsgkIF2'
            elif opcao_personagem==2:
                dicionarioUsuario[CHAVE_ID_USUARIO]='LA2UjmX7oBX3AlRJfmdWAD41OWg2'
            menuPersonagem(dicionarioUsuario)

def usuario():
    print(f'Usuario.')
    print(f'1 - Entrar.')
    print(f'2 - Cadastrar.')
    print(f'0 - Sair.')
    escolha_usuario = int(input(f'Sua escolha: '))
    linhaSeparacao()
    while escolha_usuario<0 or escolha_usuario>3:
        print(f'Opção inválida! Selecione uma das opções.')
        escolha_usuario = int(input(f'Sua escolha: '))
    else:
        if escolha_usuario==0:
            print(f'Saindo...')
            for i in range(0,10):
                sys.stdout.write('\r{i}'.format(i))
                sys.stdout.flush()
                time.sleep(1)
                exit()
        elif escolha_usuario == 1:
            if entra_usuario():
                pass
        usuario()
    return
menuTeste()