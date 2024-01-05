import time, sys
from manipula_funcoes import *
from manipula_cliente import *

def mostraMenuListaDesejo(dicionarioUsuario):
    print(f'Lista de trabalhos desejados:')
    listaDesejo = retornaListaDicionariosTrabalhosDesejados(dicionarioUsuario)
    if not tamanhoIgualZero(listaDesejo):
        mostraListaDesejo(listaDesejo)
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
    return dicionarioUsuario,opcaoLista

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
    tipoRaridade = None
    print(f'Qual a raridade da produção?')
    print(f'1 - Comum.')
    print(f'2 - Melhorado.')
    print(f'3 - Raro.')
    print(f'4 - Especial.')
    print(f'0 - Voltar.')
    opcaoRaridade = input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoRaridade, 4):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoRaridade = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoRaridade = int(opcaoRaridade)
        if opcaoRaridade != 0:
            if opcaoRaridade == 1:
                tipoRaridade = 'Comum'
            elif opcaoRaridade == 2:
                tipoRaridade = 'Melhorado'
            elif opcaoRaridade == 3:
                tipoRaridade = 'Raro'
            elif opcaoRaridade == 4:
                tipoRaridade = 'Especial'
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
    if tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]):
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
                dicionarioProfissao=retornaDicionarioProfissaoEscolhida(dicionarioUsuario, opcaoProfissao)
    return dicionarioProfissao

def defineTrabalho(profissao,raridade):
    print(f'Trabalhos:')
    dicionarioTrabalho={}
    listaDicionariosTrabalhos=retornaListaDicionariosTrabalhos()
    if not tamanhoIgualZero(listaDicionariosTrabalhos):
        listaDicionariosTrabalhosBuscados=retornaListaDicionariosTrabalhosBuscados(listaDicionariosTrabalhos,profissao[CHAVE_NOME],raridade)
        if not tamanhoIgualZero(listaDicionariosTrabalhosBuscados):
            indice = 1
            for dicionarioTrabalhoBuscado in listaDicionariosTrabalhosBuscados:
                if CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalhoBuscado:
                    print(f'{indice} - Nível {dicionarioTrabalhoBuscado[CHAVE_NIVEL]} : {dicionarioTrabalhoBuscado[CHAVE_NOME]} <-- {dicionarioTrabalhoBuscado[CHAVE_TRABALHO_NECESSARIO]}.')
                else:
                    print(f'{indice} - Nível {dicionarioTrabalhoBuscado[CHAVE_NIVEL]} : {dicionarioTrabalhoBuscado[CHAVE_NOME]}.')
                if indice + 1 <= len(listaDicionariosTrabalhosBuscados):
                    if dicionarioTrabalhoBuscado[CHAVE_NIVEL] != listaDicionariosTrabalhosBuscados[indice][CHAVE_NIVEL]:
                        linhaSeparacao()
                indice += 1
            print(f'0 - Voltar.')
            opcaoTrabalho = input(f'Trabalho melhorado escolhido: ')
            linhaSeparacao()
            while opcaoInvalida(opcaoTrabalho,len(listaDicionariosTrabalhosBuscados)):
                print(f'Opção inválida! Selecione uma das opções.')
                opcaoTrabalho=input(f'Sua escolha: ')
                linhaSeparacao()
            else:
                opcaoTrabalho=int(opcaoTrabalho)
                if opcaoTrabalho != 0:
                    dicionarioTrabalho = listaDicionariosTrabalhosBuscados[opcaoTrabalho - 1]
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
    print(f'2 - Define prioridade profissão.')
    print(f'3 - Modifica atributo trabalho.')
    print(f'4 - Adiciona atributo trabalho necessário.')
    print(f'0 - Voltar.')
    opcaoConfiguracao = input(f'Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoConfiguracao, 4):
        print(f'Opção inválida! Selecione uma das opções.')
        opcaoConfiguracao = input(f'Sua escolha: ')
        linhaSeparacao()
    else:
        opcaoConfiguracao = int(opcaoConfiguracao)
    return opcaoConfiguracao

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
    print(f'8 - Estoque.')
    print(f'0 - Voltar.')
    opcaoEscolha=input('Sua escolha: ')
    linhaSeparacao()
    while opcaoInvalida(opcaoEscolha,8):
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
                dicionarioProfissao=defineProfissao(dicionarioUsuario)
                if variavelExiste(dicionarioProfissao):
                    dicionarioTrabalhoMelhoradoEscolhido=defineTrabalho(dicionarioProfissao,raridade)
                    if not tamanhoIgualZero(dicionarioTrabalhoMelhoradoEscolhido):
                        licenca=defineLicenca()
                        if variavelExiste(licenca):
                            dicionarioTrabalhoMelhoradoEscolhido[CHAVE_LICENCA]=licenca
                            recorrencia=defineRecorrencia()
                            if variavelExiste(recorrencia):
                                dicionarioTrabalhoMelhoradoEscolhido[CHAVE_RECORRENCIA]=recorrencia
                                dicionarioTrabalhoMelhoradoEscolhido[CHAVE_ESTADO]=0
                                adicionaTrabalhoDesejo(dicionarioUsuario,dicionarioTrabalhoMelhoradoEscolhido)
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
                    dicionarioProfissao=defineProfissao(dicionarioUsuario)
                    if variavelExiste(dicionarioProfissao):
                        nivel=defineNivel()
                        if variavelExiste(nivel):
                            defineNovoTrabalho(raridade,dicionarioProfissao,nivel)
            elif opcao_cadastro == 2:#Cadastra novo modelo de habilidade
                print(f'Em desenvolvimento...')
                linhaSeparacao()
        elif opcaoEscolha==6:#Menu configurações
            opcaoConfiguracao = mostraMenuConfiuracao()
            if opcaoConfiguracao == 0:#Volta ao menu anterior
                print(f'Voltar.')
                linhaSeparacao()
            elif opcaoConfiguracao == 1:
                pass
            elif opcaoConfiguracao == 2:
                definePrioridadeProfissao(dicionarioUsuario)
                pass
            elif opcaoConfiguracao == 3: # Modifica atributo trabalho
                raridade = defineRaridade()
                if variavelExiste(raridade):
                    dicionarioProfissao = defineProfissao(dicionarioUsuario)
                    if variavelExiste(dicionarioProfissao):
                        while True:
                            dicionarioTrabalhoMelhoradoEscolhido = defineTrabalho(dicionarioProfissao, raridade)
                            if not tamanhoIgualZero(dicionarioTrabalhoMelhoradoEscolhido):
                                dicionarioTrabalhoEscolhido = {
                                    CHAVE_NOME:dicionarioTrabalhoMelhoradoEscolhido[CHAVE_NOME],
                                    CHAVE_PROFISSAO:dicionarioTrabalhoMelhoradoEscolhido[CHAVE_PROFISSAO],
                                    CHAVE_RARIDADE:dicionarioTrabalhoMelhoradoEscolhido[CHAVE_RARIDADE],
                                    CHAVE_NIVEL:dicionarioTrabalhoMelhoradoEscolhido[CHAVE_NIVEL],
                                    CHAVE_EXPERIENCIA:dicionarioTrabalhoMelhoradoEscolhido[CHAVE_EXPERIENCIA]}
                                while True:
                                    indice = 1
                                    for atributo in dicionarioTrabalhoEscolhido:
                                        print(f'{indice} - {atributo} : {dicionarioTrabalhoEscolhido[atributo]}.')
                                        indice +=1
                                    print(f'0 - Voltar.')
                                    linhaSeparacao()
                                    opcaoAtributo = input(f'Opção de atributo:')
                                    while opcaoInvalida(opcaoAtributo, len(dicionarioTrabalhoEscolhido)):
                                        print(f'Opção inválida! Selecione uma das opções.')
                                        opcaoAtributo = input(f'Sua escolha: ')
                                        linhaSeparacao()
                                    else:
                                        opcaoAtributo = int(opcaoAtributo)
                                        if opcaoAtributo != 0:
                                            contador = 1
                                            chaveAtributoEscolhido = None
                                            for atributo in dicionarioTrabalhoEscolhido:
                                                if contador == opcaoAtributo:
                                                    chaveAtributoEscolhido = atributo
                                                    tipoAtributo = type(dicionarioTrabalhoEscolhido[atributo])
                                                    break
                                                contador += 1
                                            if variavelExiste(chaveAtributoEscolhido):
                                                novoValorAtributo = input(f'Novo valor do atributo {chaveAtributoEscolhido}: ')
                                                novoValorAtributo = tipoAtributo(novoValorAtributo)
                                                if CHAVE_TRABALHO_NECESSARIO == chaveAtributoEscolhido:
                                                    caminhoRequisicao = f'Lista_trabalhos/{dicionarioTrabalhoMelhoradoEscolhido[CHAVE_ID]}/.json'
                                                    dados = {chaveAtributoEscolhido:novoValorAtributo}
                                                    print(f'Manter trabalho: {dicionarioTrabalhoEscolhido[CHAVE_TRABALHO_NECESSARIO]}?')
                                                    if retornaInputConfirmacao():
                                                        novoValorAtributo = dicionarioTrabalhoEscolhido[chaveAtributoEscolhido]+ ',' + novoValorAtributo
                                                        dados = {chaveAtributoEscolhido:novoValorAtributo}
                                                    modificaAtributo(caminhoRequisicao, dados)
                                                else:
                                                    dados = {chaveAtributoEscolhido:novoValorAtributo}
                                                    caminhoRequisicao = f'Lista_trabalhos/{dicionarioTrabalhoMelhoradoEscolhido[CHAVE_ID]}/.json'
                                                    modificaAtributo(caminhoRequisicao, dados)
                                                listaIdUsuarios = ['LA2UjmX7oBX3AlRJfmdWAD41OWg2','eEDku1Rvy7f7vbwJiVW7YMsgkIF2']
                                                for idUsuario in listaIdUsuarios:
                                                    dicionarioUsuarioModificacao = {CHAVE_ID_USUARIO:idUsuario}
                                                    listaDicionariosPersonagens = retornaListaDicionariosPersonagens(dicionarioUsuarioModificacao)
                                                    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = sorted(listaDicionariosPersonagens,key=lambda dicionario:(dicionario[CHAVE_EMAIL],dicionario[CHAVE_NOME]))
                                                    for dicionarioPersonagem in dicionarioUsuarioModificacao[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
                                                        dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = dicionarioPersonagem
                                                        dicionarioPersonagem[CHAVE_ID_USUARIO] = dicionarioUsuarioModificacao[CHAVE_ID_USUARIO]
                                                        dicionarioPersonagem = defineListaDesejo(dicionarioPersonagem)
                                                        for dicionarioTrabalhoDesejado in dicionarioPersonagem[CHAVE_LISTA_DESEJO]:
                                                            if textoEhIgual(dicionarioTrabalhoDesejado[CHAVE_NOME], dicionarioTrabalhoEscolhido[CHAVE_NOME]):
                                                                caminhoRequisicao = f'Usuarios/{dicionarioUsuarioModificacao[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalhoDesejado[CHAVE_ID]}/.json'
                                                                modificaAtributo(caminhoRequisicao, dados)
                                                        listaDicionarioTrabalhoEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioPersonagem)
                                                        for dicionarioTrabalhoEstoque in listaDicionarioTrabalhoEstoque:
                                                            if textoEhIgual(dicionarioTrabalhoEstoque[CHAVE_NOME], dicionarioTrabalhoEscolhido[CHAVE_NOME]):
                                                                if chaveAtributoEscolhido in dicionarioTrabalhoEstoque:
                                                                    caminhoRequisicao = f'Usuarios/{dicionarioUsuarioModificacao[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{dicionarioTrabalhoEstoque[CHAVE_ID]}/.json'
                                                                    modificaAtributo(caminhoRequisicao, dados)
                                                                    break
                                                dicionarioTrabalhoEscolhido[chaveAtributoEscolhido] = novoValorAtributo
                                                print(f'Valor do atributo {chaveAtributoEscolhido} modificado para {novoValorAtributo}.')
                                                linhaSeparacao()
                                        else:
                                            break
                            else:
                                break
            elif opcaoConfiguracao == 4: # Adiciona atributo trabalho necessário
                while True:
                    dicionarioProfissao = defineProfissao(dicionarioUsuario)
                    if variavelExiste(dicionarioProfissao):
                        while True:
                            # dicionarioTrabalhoMelhoradoEscolhido = defineTrabalho(dicionarioProfissao, 'melhorado')
                            dicionarioTrabalhoMelhoradoEscolhido = None
                            listaDicionariosTrabalhos = retornaListaDicionariosTrabalhos()
                            if not tamanhoIgualZero(listaDicionariosTrabalhos):
                                listaDicionariosTrabalhosBuscados = []
                                for dicionarioTrabalho in listaDicionariosTrabalhos:
                                    if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioProfissao[CHAVE_NOME])and
                                        textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], 'melhorado')):
                                        listaDicionariosTrabalhosBuscados.append(dicionarioTrabalho)
                                if not tamanhoIgualZero(listaDicionariosTrabalhosBuscados):
                                    listaDicionariosTrabalhosBuscados = sorted(listaDicionariosTrabalhosBuscados,key=lambda dicionario:(dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
                                    print(f'Trabalhos melhorados de {dicionarioProfissao[CHAVE_NOME]}:')
                                    indice = 1
                                    for dicionarioTrabalhoBuscado in listaDicionariosTrabalhosBuscados:
                                        if CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalhoBuscado:
                                            print(f'{indice} - Nível {dicionarioTrabalhoBuscado[CHAVE_NIVEL]} : {dicionarioTrabalhoBuscado[CHAVE_NOME]} <-- {dicionarioTrabalhoBuscado[CHAVE_TRABALHO_NECESSARIO]}.')
                                        else:
                                            print(f'{indice} - Nível {dicionarioTrabalhoBuscado[CHAVE_NIVEL]} : {dicionarioTrabalhoBuscado[CHAVE_NOME]}.')
                                        if indice + 1 <= len(listaDicionariosTrabalhosBuscados):
                                            if dicionarioTrabalhoBuscado[CHAVE_NIVEL] != listaDicionariosTrabalhosBuscados[indice][CHAVE_NIVEL]:
                                                linhaSeparacao()
                                        indice += 1
                                    print(f'0 - Voltar.')
                                    opcaoTrabalho = input(f'Trabalho melhorado escolhido: ')
                                    linhaSeparacao()
                                    while opcaoInvalida(opcaoTrabalho, len(listaDicionariosTrabalhosBuscados)):
                                        print(f'Opção inválida! Selecione uma das opções.')
                                        opcaoTrabalho = input(f'Trabalho melhorado escolhido: ')
                                        linhaSeparacao()
                                    else:
                                        opcaoTrabalho = int(opcaoTrabalho)
                                        nomeTrabalhoComum = None
                                        if opcaoTrabalho != 0:
                                            dicionarioTrabalhoMelhoradoEscolhido = listaDicionariosTrabalhosBuscados[opcaoTrabalho - 1]
                                            while True:
                                                listaDicionariosTrabalhosBuscados = []
                                                for dicionarioTrabalho in listaDicionariosTrabalhos:
                                                    if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioTrabalhoMelhoradoEscolhido[CHAVE_PROFISSAO])and
                                                        dicionarioTrabalho[CHAVE_NIVEL] == dicionarioTrabalhoMelhoradoEscolhido[CHAVE_NIVEL]and
                                                        textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], 'comum')):
                                                        listaDicionariosTrabalhosBuscados.append(dicionarioTrabalho)
                                                if not tamanhoIgualZero(listaDicionariosTrabalhosBuscados):
                                                    listaDicionariosTrabalhosBuscados = sorted(listaDicionariosTrabalhosBuscados,key=lambda dicionario:(dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
                                                    print(f'{dicionarioTrabalhoMelhoradoEscolhido[CHAVE_NOME]} nível {dicionarioTrabalhoMelhoradoEscolhido[CHAVE_NIVEL]}:')
                                                    indice = 1
                                                    for dicionarioTrabalhoBuscado in listaDicionariosTrabalhosBuscados:
                                                        print(f'{indice} - Nível {dicionarioTrabalhoBuscado[CHAVE_NIVEL]} : {dicionarioTrabalhoBuscado[CHAVE_NOME]}.')
                                                        indice += 1
                                                    print(f'0 - Voltar.')
                                                    opcaoTrabalho = input(f'Trabalho comum escolhido: ')
                                                    linhaSeparacao()
                                                    while opcaoInvalida(opcaoTrabalho, len(listaDicionariosTrabalhosBuscados)):
                                                        print(f'Opção inválida! Selecione uma das opções.')
                                                        opcaoTrabalho = input(f'Trabalho comum escolhido: ')
                                                        linhaSeparacao()
                                                    else:
                                                        opcaoTrabalho = int(opcaoTrabalho)
                                                        nomeTrabalhoComum = None
                                                        if opcaoTrabalho != 0:
                                                            nomeTrabalhoComum = listaDicionariosTrabalhosBuscados[opcaoTrabalho - 1][CHAVE_NOME]
                                                            caminhoRequisicao = f'Lista_trabalhos/{dicionarioTrabalhoMelhoradoEscolhido[CHAVE_ID]}/.json'
                                                            dados = {CHAVE_TRABALHO_NECESSARIO:nomeTrabalhoComum}
                                                            if CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalhoMelhoradoEscolhido:
                                                                if not tamanhoIgualZero(dicionarioTrabalhoMelhoradoEscolhido[CHAVE_TRABALHO_NECESSARIO]):
                                                                    print(f'Manter trabalho {dicionarioTrabalhoMelhoradoEscolhido[CHAVE_TRABALHO_NECESSARIO]}?')
                                                                    if retornaInputConfirmacao():
                                                                        nomeTrabalhoComum = dicionarioTrabalhoMelhoradoEscolhido[CHAVE_TRABALHO_NECESSARIO] + ',' + nomeTrabalhoComum
                                                                        dados = {CHAVE_TRABALHO_NECESSARIO:nomeTrabalhoComum}
                                                            dicionarioTrabalhoMelhoradoEscolhido[CHAVE_TRABALHO_NECESSARIO] = nomeTrabalhoComum
                                                            modificaAtributo(caminhoRequisicao, dados)
                                                            linhaSeparacao()
                                                        else:
                                                            break
                                                else:
                                                    print(f'Lista de vazia!')
                                                    linhaSeparacao()
                                                    break
                                        else:
                                            break
                                else:
                                    break
                    else:
                        break
        elif opcaoEscolha==7:
            funcao_teste(dicionarioUsuario)
            linhaSeparacao()
        elif opcaoEscolha == 8:
            while True:
                listaDicionarioEstoque = retornaListaDicionarioTrabalhoEstoque(dicionarioUsuario)
                listaDicionarioEstoqueOrdenado = sorted(listaDicionarioEstoque,
                                                        key=lambda dicionario:(dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
                indice = 1
                for dicionarioEstoque in listaDicionarioEstoqueOrdenado:
                    if CHAVE_PROFISSAO in dicionarioEstoque:
                        print(f'{dicionarioEstoque[CHAVE_PROFISSAO]} - {dicionarioEstoque[CHAVE_QUANTIDADE]} und - {dicionarioEstoque[CHAVE_NOME]}.')
                        if indice < len(listaDicionarioEstoqueOrdenado):
                            if dicionarioEstoque[CHAVE_PROFISSAO] != listaDicionarioEstoqueOrdenado[indice][CHAVE_PROFISSAO]:
                                linhaSeparacao()
                                pass
                    else:
                        print(f'{dicionarioEstoque[CHAVE_QUANTIDADE]} und - {dicionarioEstoque[CHAVE_NOME]}.')
                    indice += 1
                linhaSeparacao()
                print(f'1 - Modificar quantidade.')
                print(f'0 - Voltar.')
                opcaoEstoque = input(f'Sua escolha: ')
                linhaSeparacao()
                while opcaoInvalida(opcaoEstoque,1):
                    print(f'Opção inválida! Selecione uma das opções.')
                    opcaoEstoque = input(f'Sua escolha: ')
                    linhaSeparacao()
                else:
                    opcaoEstoque = int(opcaoEstoque)
                    if opcaoEstoque != 0:
                        if opcaoEstoque == 1:
                            while True:
                                indice = 1
                                for dicionarioEstoque in listaDicionarioEstoqueOrdenado:
                                    print(f'{indice} - {dicionarioEstoque[CHAVE_NOME]}.')
                                    indice += 1
                                print(f'0 - Voltar.')
                                opcaoEstoque = input(f'Sua escolha: ')
                                linhaSeparacao()
                                while opcaoInvalida(opcaoEstoque, len(listaDicionarioEstoqueOrdenado)):
                                    print(f'Opção inválida! Selecione uma das opções.')
                                    opcaoEstoque = input(f'Sua escolha: ')
                                    linhaSeparacao()
                                else:
                                    opcaoEstoque = int(opcaoEstoque)
                                    if opcaoEstoque != 0:
                                        dicionarioTrabalhoEscolhido = listaDicionarioEstoqueOrdenado[opcaoEstoque - 1]
                                        for atributo in dicionarioTrabalhoEscolhido:
                                            if atributo != CHAVE_ID:
                                                print(f'{D}: {atributo} - {dicionarioTrabalhoEscolhido[atributo]}.')
                                        novaQuantidade = input(f'Nova quantidade: ')
                                        linhaSeparacao()
                                        while not ehValorNumerico(novaQuantidade) or int(novaQuantidade) < 0:
                                            print(f'Valor inválido!')
                                            novaQuantidade = input(f'Nova quantidade: ')
                                            linhaSeparacao()
                                        else:
                                            novaQuantidade = int(novaQuantidade)
                                            caminhoRequisicao = f'Usuarios/{dicionarioUsuario[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{dicionarioTrabalhoEscolhido[CHAVE_ID]}/.json'
                                            dados = {CHAVE_QUANTIDADE: novaQuantidade}
                                            modificaAtributo(caminhoRequisicao,dados)
                                            print(f'Quantidade de {dicionarioTrabalhoEscolhido[CHAVE_NOME]} modificado para: {novaQuantidade}')
                                            linhaSeparacao()
                                    else:
                                        break
                    else:
                        break
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
    listaDicionariosPersonagens = retornaListaDicionariosPersonagens(dicionarioUsuario)
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = sorted(listaDicionariosPersonagens,key=lambda dicionario:(dicionario[CHAVE_EMAIL],dicionario[CHAVE_NOME]))
    linhaSeparacao()
    if tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]):
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
                dicionarioUsuario=defineChavePersonagemEmUso(dicionarioUsuario,opcaoPersonagem)
                menu(dicionarioUsuario)

def defineChavePersonagemEmUso(dicionarioUsuario,opcaoPersonagem):
    x=1
    for personagem in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        if x==opcaoPersonagem:
            dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]=personagem
            break
        x+=1
    return dicionarioUsuario

def menuTeste():
    dicionarioUsuario={CHAVE_ID_USUARIO:None,
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

if __name__=='__main__':
    menuTeste()