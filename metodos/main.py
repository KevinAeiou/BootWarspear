import time, sys
import manipula_funcoes

nome_arquivo_lista_profissoes = 'arquivos/lista_profissoes.txt'
nome_arquivo_lista_trabalho = 'arquivos\lista_trabalho_desejado.txt'

def mostra_menu_lista_desejo(personagem_id):
    print(f'Lista de trabalhos desejados:')
    manipula_funcoes.mostra_lista_desejo(f'eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo')
    print(f'1 - Iniciar a busca.')
    print(f'2 - Excluir trabalho da lista.')
    print(f'0 - Voltar.')
    opcao_lista = input(f'Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not opcao_lista.isdigit() or int(opcao_lista)<0 or int(opcao_lista)>2:
        print(f'Opção inválida! Selecione uma das opções.')
        opcao_lista = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        opcao_lista = int(opcao_lista)
        if opcao_lista==0:
            print(f'Voltar...')
            manipula_funcoes.linhaSeparacao()
            return 0
    return opcao_lista

def define_licenca():
    print(f'Qual o tipo da licença de produção desejada?')
    print(f'1 - Licença do iniciante.')
    print(f'2 - Licença do aprendiz.')
    print(f'3 - Licença do mestre.')
    print(f'4 - Licença do principiante.')
    print(f'0 - Voltar.')
    tipo_licenca = input('Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not tipo_licenca.isdigit() or int(tipo_licenca)<0 or int(tipo_licenca)>4:
        print(f'Opção inválida! Selecione uma das opções.')
        tipo_licenca = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        tipo_licenca = int(tipo_licenca)
        if tipo_licenca==0:
            return ''
        if tipo_licenca == 1:
            licenca = 'Licença de produção do iniciante'
        elif tipo_licenca == 2:
            licenca = 'Licença de produção do aprendiz'
        elif tipo_licenca == 3:
            licenca = 'Licença de produção do mestre'
        elif tipo_licenca == 4:
            licenca = 'Licença de produção do principiante'
    return licenca

def define_raridade():
    print(f'Qual a raridade da produção?')
    print(f'1 - Comum.')
    print(f'2 - Raro.')
    print(f'3 - Especial.')
    print(f'0 - Voltar.')
    raridade = input('Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not raridade.isdigit() or int(raridade)<0 or int(raridade)>3:
        print(f'Opção inválida! Selecione uma das opções.')
        raridade = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        raridade = int(raridade)
        if raridade==0:
            return ''
        elif raridade == 1:
            tipo_raridade = 'Comum'
        elif raridade == 2:
            tipo_raridade = 'Raro'
        elif raridade == 3:
            tipo_raridade = 'Especial'
    return tipo_raridade

def mostra_menu_habilidade():
    print(f'Habilidade.')
    print(f'1 - Usa habilidade.')
    print(f'2 - Cadastra nova habilidade.')
    print(f'0 - Voltar.')
    opcao_habilidade = input('Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not opcao_habilidade.isdigit() or int(opcao_habilidade)<0 or int(opcao_habilidade)>2:
        print(f'Opção inválida! Selecione uma das opções.')
        opcao_habilidade = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        opcao_habilidade = int(opcao_habilidade)
        if opcao_habilidade==0:
            return 0
    return opcao_habilidade

def mostra_menu_cadastrar():
    print(f'Cadastro.')
    print(f'1 - Cadastrar trabalho.')
    print(f'2 - Cadastrar habilidade.')
    print(f'0 - Voltar.')
    opcao_cadastro = input(f'Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not opcao_cadastro.isdigit() or int(opcao_cadastro)<0 or int(opcao_cadastro)>2:
        print(f'Opção inválida! Selecione uma das opções.')
        opcao_cadastro = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        opcao_cadastro = int(opcao_cadastro)
        if opcao_cadastro==0:
            return 0
    return opcao_cadastro

def define_profissao(personagem_id):
    print(f'Menu de profissões.')
    conteudo_lista_profissao = manipula_funcoes.mostra_lista(f"eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_profissoes")
    #conteudo_arquivo_profissao = manipula_funcoes.mostra_lista_arquivo(nome_arquivo_lista_profissoes)
    if conteudo_lista_profissao == 0:
        print(f'Erro!')
        manipula_funcoes.linhaSeparacao()
        menu(personagem_id)
        return ''
    else:
        opcao_profissao = input('Profissão escolhida: ')
        manipula_funcoes.linhaSeparacao()
        while not opcao_profissao.isdigit() or int(opcao_profissao)<0 or int(opcao_profissao)>len(conteudo_lista_profissao):
            print(f'Opção inválida! Selecione uma das opções.')
            opcao_profissao = input(f'Sua escolha: ')
            manipula_funcoes.linhaSeparacao()
        else:
            opcao_profissao = int(opcao_profissao)
            if opcao_profissao==0:
                return ''
            else:
                nome_profissao = conteudo_lista_profissao[opcao_profissao-1][1]
    return nome_profissao

def mostra_menu_trabalho(nome_profissao,tipo_raridade):
    print(f'Trabalhos:')
    conteudo_lista_trabalho = manipula_funcoes.mostra_lista_trabalho(nome_profissao,tipo_raridade)
    if conteudo_lista_trabalho == 0:
        print(f'Erro!')
        manipula_funcoes.linhaSeparacao()
        return ''
    else:
        opcao_trabalho = input(f'Trabalho escolhido: ')
        manipula_funcoes.linhaSeparacao()
        while not opcao_trabalho.isdigit() or int(opcao_trabalho)<0 or int(opcao_trabalho)>len(conteudo_lista_trabalho):
            print(f'Opção inválida! Selecione uma das opções.')
            opcao_trabalho = input(f'Sua escolha: ')
            manipula_funcoes.linhaSeparacao()
        else:
            opcao_trabalho = int(opcao_trabalho)
            if opcao_trabalho==0:
                return ''
    return conteudo_lista_trabalho[opcao_trabalho-1]

def mostra_menu_confiuracao():
    print(f'Configurações:')
    print(f'1 - Quantidade de personagens ativos.')
    print(f'0 - Voltar.')
    opcao_configuracao = input(f'Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not opcao_configuracao.isdigit() or int(opcao_configuracao)<0 or int(opcao_configuracao)>1:
        print(f'Opção inválida! Selecione uma das opções.')
        opcao_configuracao = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        opcao_configuracao = int(opcao_configuracao)
        if opcao_configuracao==0:
            return 0
    return opcao_configuracao

def menu(personagem_id):
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
    escolha = input('Sua escolha: ')
    manipula_funcoes.linhaSeparacao()
    while not escolha.isdigit() or int(escolha)<0 or int(escolha)>7:
        print(f'Opção inválida! Selecione uma das opções.')
        escolha = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        escolha = int(escolha)
        if escolha==0:#Volta ao menu anterior
            print(f'Voltar...')
            manipula_funcoes.linhaSeparacao()
            menu_personagem()
            return
        elif escolha==1:#Menu adicionar novo trabalho a lista
            raridade = define_raridade()
            if raridade!='':
                licenca = define_licenca()
                if licenca!='':
                    profissao = define_profissao(personagem_id)
                    if profissao != '':
                        trabalho = mostra_menu_trabalho(profissao,raridade)
                        if trabalho != '':
                            manipula_funcoes.adiciona_trabalho(personagem_id,trabalho,licenca)
            print(f'Voltando.')
            manipula_funcoes.linhaSeparacao() 
        elif escolha==2:#Menu lista de desejo
            opcao_lista = mostra_menu_lista_desejo(personagem_id)
            if opcao_lista == 0:#Volta ao menu anterior
                print(f'Voltar.')
                manipula_funcoes.linhaSeparacao()
            elif opcao_lista == 1:#Inicia busca
                manipula_funcoes.prepara_personagem(personagem_id)
                manipula_funcoes.linhaSeparacao()
            elif opcao_lista == 2:#Exclui trabalho da lista
                excluir_trabalho(personagem_id)
                manipula_funcoes.linhaSeparacao()
        elif escolha==3:#Menu habilidade
            opcao_habilidade = mostra_menu_habilidade()
            if opcao_habilidade == 0:#Volta ao menu anterior
                print(f'Voltar.')
                manipula_funcoes.linhaSeparacao()
            elif opcao_habilidade == 1:#Usa habilidades
                #exec(open('metodos/manipula_tela.py').read())
                manipula_funcoes.usa_habilidade()
            elif opcao_habilidade == 2:#Cadastra novo modelo de habilidade
                manipula_funcoes.recorta_novo_modelo_habilidade()
        elif escolha==4:#Atualiza lista de profissões
            manipula_funcoes.atualiza_lista_profissao(personagem_id)
        elif escolha==5:#Menu cadastro
            opcao_cadastro = mostra_menu_cadastrar()
            if opcao_cadastro == 0:#Volta ao menu anterior
                print(f'Voltar.')
                manipula_funcoes.linhaSeparacao()
            elif opcao_cadastro == 1:#Cadastra novo trabalho
                raridade = define_raridade() 
                if raridade != '':
                    profissao = define_profissao(personagem_id)
                    if profissao != '':
                        manipula_funcoes.cadastra_nome_trabalho(profissao,raridade)
            elif opcao_cadastro == 2:#Cadastra novo modelo de habilidade
                print(f'Em desenvolvimento...')
                manipula_funcoes.linhaSeparacao()
        elif escolha==6:#Menu configurações
            opcao_configuracao = mostra_menu_confiuracao()
            if opcao_configuracao == 0:#Volta ao menu anterior
                print(f'Voltar.')
                manipula_funcoes.linhaSeparacao()
            elif opcao_configuracao==1:
                manipula_funcoes.modifica_quantidade_personagem_ativo()
        elif escolha==7:#Menu teste
            manipula_funcoes.funcao_teste(personagem_id)
            manipula_funcoes.linhaSeparacao()
        menu(personagem_id)
    return

def excluir_trabalho(personagem_id):
    lista_desejo = manipula_funcoes.mostra_lista(f'eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo')
    opcao_exclui_trabalho = input(f'Qual trabalho deseja exluir?')
    manipula_funcoes.linhaSeparacao()
    while not opcao_exclui_trabalho.isdigit() or int(opcao_exclui_trabalho)<0 or int(opcao_exclui_trabalho)>len(lista_desejo):
        print(f'Opção inválida! Selecione uma das opções.')
        opcao_exclui_trabalho = input(f'Sua escolha: ')
        manipula_funcoes.linhaSeparacao()
    else:
        opcao_exclui_trabalho = int(opcao_exclui_trabalho)
        if opcao_exclui_trabalho==0:
            print(f'Voltar...')
            manipula_funcoes.linhaSeparacao()
            return
        else:
            trabalho = lista_desejo[opcao_exclui_trabalho-1]
            trabalho_id = f'eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo/{trabalho[0]}'
            manipula_funcoes.excluir_trabalho(trabalho_id)

def menu_personagem():
    print(f'Personagens.')
    conteudo_lista_personagem = manipula_funcoes.mostra_lista("eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem")
    if conteudo_lista_personagem == 0:
        print(f'Erro!')
        manipula_funcoes.linhaSeparacao()
    else:
        opcao_personagem = input('Personagem escolhido: ')
        manipula_funcoes.linhaSeparacao()
        while not opcao_personagem.isdigit() or int(opcao_personagem)<0 or int(opcao_personagem)>len(conteudo_lista_personagem):
            print(f'Opção inválida! Selecione um personagem.')
            opcao_personagem = input(f'Sua escolha: ')
            manipula_funcoes.linhaSeparacao()
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
                personagem_id = conteudo_lista_personagem[opcao_personagem-1][0]
                menu(personagem_id)

def usuario():
    print(f'Usuario.')
    print(f'1 - Entrar.')
    print(f'2 - Cadastrar.')
    print(f'0 - Sair.')
    escolha_usuario = int(input(f'Sua escolha: '))
    manipula_funcoes.linhaSeparacao()
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
            if manipula_funcoes.entra_usuario():
                menu()
        usuario()
    return
# menu_personagem()