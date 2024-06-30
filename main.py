import time, sys
from metodos.manipula_funcoes import *
from metodos.manipula_cliente import *
from metodos.Utilitarios import *

dicionarioUsuario = {}

def exibirSubTitulo(subTitulo):
    limpaTela()
    print(f'{subTitulo}\n')

def exibirMensagemOpcaoInvalida():
    print(f'Opção inválida!')
    input(f'Digite qualquer tecla para voltar ao menu.')

def mostraMenuListaDesejo():
    exibirSubTitulo('Lista de trabalhos desejados:')
    dicionarioUsuario = mostraListaDesejo(dicionarioUsuario)
    exibirOpcoesListaDesejos()
    return defineOpcaoListaDesejoSelecionada() 

def defineOpcaoListaDesejoSelecionada():
    opcaoLista = input(f'Sua escolha: ')
    linhaSeparacao()
    if opcaoInvalida(opcaoLista,2):
        exibirMensagemOpcaoInvalida()
        mostraMenuListaDesejo()
    return int(opcaoLista)

def exibirOpcoesListaDesejos():
    print(f'1 - Iniciar a busca.')
    print(f'2 - Excluir trabalho da lista.')
    print(f'0 - Voltar.')

def defineLicenca():
    exibirSubTitulo('Qual o tipo da licença de produção desejada?')
    exibirOpcoesLicencas()
    return defineOpcaoLicencaSelecionada()

def exibirOpcoesLicencas():
    print(f'{"Índice".ljust(6)}|Licença')
    print(f'{"1".ljust(6)}|Licença do iniciante')
    print(f'{"2".ljust(6)}|Licença do aprendiz')
    print(f'{"3".ljust(6)}|Licença do mestre')
    print(f'{"4".ljust(6)}|Licença do principiante')
    print(f'{"0".ljust(6)}|Voltar\n')

def defineOpcaoLicencaSelecionada():
    opcaoLicenca = input('Sua escolha: ')
    if opcaoInvalida(opcaoLicenca,4):
        exibirMensagemOpcaoInvalida()
        defineLicenca()
    else:
        opcaoLicenca=int(opcaoLicenca)
        if opcaoLicenca==0:
            licenca=None
        elif opcaoLicenca==1:
            licenca=CHAVE_LICENCA_INICIANTE
        elif opcaoLicenca==2:
            licenca=CHAVE_LICENCA_APRENDIZ
        elif opcaoLicenca==3:
            licenca=CHAVE_LICENCA_MESTRE
        elif opcaoLicenca==4:
            licenca=CHAVE_LICENCA_PRINCIPIANTE
    return licenca

def defineRaridade():
    exibirSubTitulo('Qual a raridade da produção?')
    exibirOpcoesRaridades()
    return defineOpcaoRaridadeSelecionada()

def defineOpcaoRaridadeSelecionada():
    opcaoRaridade = input('Sua escolha: ')
    linhaSeparacao()
    if opcaoInvalida(opcaoRaridade, 4):
        exibirMensagemOpcaoInvalida()
        defineRaridade()
    else:
        opcaoRaridade = int(opcaoRaridade)
        if opcaoRaridade == 0:
            tipoRaridade = None
        if opcaoRaridade == 1:
            tipoRaridade = CHAVE_RARIDADE_COMUM
        elif opcaoRaridade == 2:
            tipoRaridade = CHAVE_RARIDADE_MELHORADO
        elif opcaoRaridade == 3:
            tipoRaridade = CHAVE_RARIDADE_RARO
        elif opcaoRaridade == 4:
            tipoRaridade = CHAVE_RARIDADE_ESPECIAL
    return tipoRaridade

def exibirOpcoesRaridades():
    print(f'{"Índice".ljust(6)}|Raridade')
    print(f'{"1".ljust(6)}|Comum')
    print(f'{"2".ljust(6)}|Melhorado')
    print(f'{"3".ljust(6)}|Raro')
    print(f'{"4".ljust(6)}|Especial')
    print(f'{"0".ljust(6)}|Voltar\n')

def defineRecorrencia():
    exibirSubTitulo('Trabalho é recorrente?')
    exibirOpcoesRecorrencia()
    return definirOpcaoRecorrenciaSelecionada()

def definirOpcaoRecorrenciaSelecionada():
    opcaoRecorrencia=input('Sua escolha: ')
    linhaSeparacao()
    if opcaoInvalida(opcaoRecorrencia,2):
        exibirMensagemOpcaoInvalida()
        defineRecorrencia()
    else:
        opcaoRecorrencia=int(opcaoRecorrencia)
        if opcaoRecorrencia==0:
            recorrencia=None
        elif opcaoRecorrencia==1:
            recorrencia=True
        elif opcaoRecorrencia==2:
            recorrencia=False
    return recorrencia

def exibirOpcoesRecorrencia():
    print(f'1 - Sim.')
    print(f'2 - Não.')
    print(f'0 - Voltar.')

def mostraMenuHabilidade():
    exibirSubTitulo('Habilidade.')
    exibirOpcoesHabilidade()
    return definirOpcaoHabilidadeSelecionada()

def definirOpcaoHabilidadeSelecionada():
    opcaoHabilidade=input('Sua escolha: ')
    linhaSeparacao()
    if opcaoInvalida(opcaoHabilidade,2):
        exibirMensagemOpcaoInvalida()
        mostraMenuHabilidade()
    else:
        opcaoHabilidade=int(opcaoHabilidade)
        return opcaoHabilidade

def exibirOpcoesHabilidade():
    print(f'1 - Usa habilidade.')
    print(f'2 - Cadastra nova habilidade.')
    print(f'0 - Voltar.')

def mostraMenuCadastrar():
    exibirSubTitulo(f'Cadastro')
    exibirOpcoesCadastro()
    return definirOpcaoCadastroSelecionada()

def definirOpcaoCadastroSelecionada():
    opcaoCadastro = input(f'Sua escolha: ')
    linhaSeparacao()
    if opcaoInvalida(opcaoCadastro,2):
        exibirMensagemOpcaoInvalida()
        mostraMenuCadastrar()
    else:
        opcaoCadastro=int(opcaoCadastro)
        return opcaoCadastro

def exibirOpcoesCadastro():
    print(f'1 - Cadastrar trabalho.')
    print(f'2 - Cadastrar habilidade.')
    print(f'0 - Voltar\n')

def defineNivel():
    exibirSubTitulo(f'Define nível')
    print(f'0 - Voltar.')
    return defineOpcaoNivelSelecionado()

def defineOpcaoNivelSelecionado():
    nivelTrabalho = input(f'Nivel do trabalho: ')
    if opcaoInvalida(nivelTrabalho, 32):
        exibirMensagemOpcaoInvalida()
        defineNivel()
    else:
        nivelTrabalho = int(nivelTrabalho)
        if nivelTrabalho == 0:
            return None
        return nivelTrabalho

def defineProfissao(dicionarioUsuario):
    exibirSubTitulo(f'Profissões')
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO] = retornaListaDicionariosProfissoes(dicionarioUsuario)
    exibirListaDeProfissoes(dicionarioUsuario)
    return defineOpcaoProfissaoSelecionada(dicionarioUsuario)

def defineOpcaoProfissaoSelecionada(dicionarioUsuario):
    opcaoProfissao = input('Profissão escolhida: ')
    if opcaoInvalida(opcaoProfissao, len(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO])):
        exibirMensagemOpcaoInvalida()
        defineProfissao(dicionarioUsuario)
    else:
        opcaoProfissao=int(opcaoProfissao)
        if opcaoProfissao==0:
            return None
        else:
            return retornaDicionarioProfissaoEscolhida(dicionarioUsuario, opcaoProfissao)

def exibirListaDeProfissoes(dicionarioUsuario):
    if tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]):
        print(f'Lista de profissões está vazia!')
    else:
        x = 1
        print(f'{"Índice".ljust(6)}|{"Profissão".ljust(22)}|{"Experiência"}')
        for dicionarioProfissao in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PROFISSAO]:
            print(f'{str(x).ljust(6)}|{dicionarioProfissao[CHAVE_NOME].ljust(22)}|{dicionarioProfissao[CHAVE_EXPERIENCIA]}')
            x += 1
    print(f'{"0".ljust(6)}|Voltar\n')

def defineTrabalho(dicionarioTrabalhoDesejado):
    exibirSubTitulo(f'Trabalhos')
    listaDicionariosTrabalhosBuscadosOrdenados = definirListaDeTrabalhos(dicionarioTrabalhoDesejado)
    exibirOpcoesTrabalhos(listaDicionariosTrabalhosBuscadosOrdenados)
    return definirOpcaoTrabalhoSelecionada(listaDicionariosTrabalhosBuscadosOrdenados)

def definirOpcaoTrabalhoSelecionada(listaDicionariosTrabalhosBuscadosOrdenados):
    opcaoTrabalho = input(f'Trabalho melhorado escolhido: ')
    linhaSeparacao()
    if opcaoInvalida(opcaoTrabalho,len(listaDicionariosTrabalhosBuscadosOrdenados)):
        exibirMensagemOpcaoInvalida()
        defineTrabalho()
    else:
        opcaoTrabalho=int(opcaoTrabalho)
        if opcaoTrabalho != 0:
            return listaDicionariosTrabalhosBuscadosOrdenados[opcaoTrabalho - 1]
    return None

def exibirOpcoesTrabalhos(listaDicionariosTrabalhosBuscadosOrdenados):
    if tamanhoIgualZero(listaDicionariosTrabalhosBuscadosOrdenados):
        print(f'Lista de trabalhos vazia!')
        linhaSeparacao()
    else:
        indice = 1
        print(f'{"Índice".ljust(6)}|{"Nível".ljust(5)}|{"Nome".ljust(45)}|{"Trabalho necessário"}')
        for dicionarioTrabalhoBuscado in listaDicionariosTrabalhosBuscadosOrdenados:
            trabalhoNecessario = 'Indefinido' if (not CHAVE_TRABALHO_NECESSARIO in dicionarioTrabalhoBuscado) else dicionarioTrabalhoBuscado[CHAVE_TRABALHO_NECESSARIO]
            print(f'{str(indice).ljust(6)}|{str(dicionarioTrabalhoBuscado[CHAVE_NIVEL]).ljust(5)}|{dicionarioTrabalhoBuscado[CHAVE_NOME].ljust(45)}|{trabalhoNecessario}')
            indice += 1
    print(f'{"0".ljust(6)}|Voltar\n')

def definirListaDeTrabalhos(dicionarioTrabalhoDesejado):
    listaDicionariosTrabalhos = retornaListaDicionariosTrabalhos()
    if not tamanhoIgualZero(listaDicionariosTrabalhos):
        listaDicionariosTrabalhosBuscados = []
        for dicionarioTrabalho in listaDicionariosTrabalhos:
            condicoes = (
                textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioTrabalhoDesejado[CHAVE_PROFISSAO][CHAVE_NOME])
                and textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], dicionarioTrabalhoDesejado[CHAVE_RARIDADE]))
            if condicoes:
                listaDicionariosTrabalhosBuscados.append(dicionarioTrabalho)
        return sorted(listaDicionariosTrabalhosBuscados,key=lambda dicionario:(dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
    return []

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

def menuPrincipal():
    exibirSubTitulo(f'Menu principal')
    exibirOpcoesMenuPrincipal()
    definirOpcaoMenuPrincipalSelecionada()

def definirOpcaoMenuPrincipalSelecionada():
    opcaoEscolha = input('Sua escolha: ')
    if opcaoInvalida(opcaoEscolha, tamanhoMenu = 8):
        exibirMensagemOpcaoInvalida()
        menuPrincipal()
    else:
        opcaoEscolha = int(opcaoEscolha)
        if opcaoEscolha == 0:#Volta ao menu anterior
            print(f'Voltar...')
            menuPersonagem()
        elif opcaoEscolha==1:#Menu adicionar novo trabalho a lista
            adicionarNovoTrabalhoDesejado(dicionarioUsuario)
        elif opcaoEscolha==2:#Menu lista de desejo
            opcaoLista = mostraMenuListaDesejo()
            tratrarOpcaoListaDesejoSelecionada(opcaoLista)
        elif opcaoEscolha==3:#Menu habilidade
            opcao_habilidade = mostraMenuHabilidade()
            if opcao_habilidade == 0:#Volta ao menu anterior
                print(f'Voltar.')
                linhaSeparacao()
            elif opcao_habilidade == 1:#Usa habilidades
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
                                                    for dicionarioPersonagem in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
                                                        dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = dicionarioPersonagem
                                                        dicionarioPersonagem[CHAVE_ID_USUARIO] = dicionarioUsuarioModificacao[CHAVE_ID_USUARIO]
                                                        dicionarioPersonagem[CHAVE_LISTA_DESEJO] = retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagem)
                                                        for dicionarioTrabalhoDesejado in dicionarioPersonagem[CHAVE_LISTA_DESEJO]:
                                                            if textoEhIgual(dicionarioTrabalhoDesejado[CHAVE_NOME], dicionarioTrabalhoEscolhido[CHAVE_NOME]):
                                                                caminhoRequisicao = f'Usuarios/{dicionarioUsuarioModificacao[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalhoDesejado[CHAVE_ID]}/.json'
                                                                modificaAtributo(caminhoRequisicao, dados)
                                                        listaDicionarioTrabalhoEstoque = retornaListaDicionariosTrabalhosEstoque(dicionarioPersonagem)
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
                        raridade = defineRaridade()
                        if variavelExiste(raridade):
                            while True:
                                # dicionarioTrabalhoMelhoradoEscolhido = defineTrabalho(dicionarioProfissao, 'melhorado')
                                dicionarioTrabalhoMelhoradoEscolhido = None
                                listaDicionariosTrabalhos = retornaListaDicionariosTrabalhos()
                                if not tamanhoIgualZero(listaDicionariosTrabalhos):
                                    listaDicionariosTrabalhosBuscados = []
                                    for dicionarioTrabalho in listaDicionariosTrabalhos:
                                        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioProfissao[CHAVE_NOME])and
                                            textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], raridade)):
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
                                                    raridade2 = None
                                                    if textoEhIgual(raridade, CHAVE_RARIDADE_MELHORADO):
                                                        raridade2 = CHAVE_RARIDADE_COMUM
                                                    elif textoEhIgual(raridade, CHAVE_RARIDADE_RARO):
                                                        raridade2 = CHAVE_RARIDADE_MELHORADO
                                                    for dicionarioTrabalho in listaDicionariosTrabalhos:
                                                        if (textoEhIgual(dicionarioTrabalho[CHAVE_PROFISSAO], dicionarioTrabalhoMelhoradoEscolhido[CHAVE_PROFISSAO])and
                                                            dicionarioTrabalho[CHAVE_NIVEL] == dicionarioTrabalhoMelhoradoEscolhido[CHAVE_NIVEL]and
                                                            textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], raridade2)):
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
                    else:
                        break
        elif opcaoEscolha==7:
            funcao_teste(dicionarioUsuario)
            linhaSeparacao()
        elif opcaoEscolha == 8:
            while True:
                listaDicionarioEstoque = retornaListaDicionariosTrabalhosEstoque(dicionarioUsuario)
                listaDicionarioEstoqueOrdenado = sorted(listaDicionarioEstoque,
                                                        key=lambda dicionario:(
                                                            dicionario[CHAVE_PROFISSAO], dicionario[CHAVE_NIVEL],dicionario[CHAVE_NOME]))
                indice = 1
                for dicionarioEstoque in listaDicionarioEstoqueOrdenado:
                    if CHAVE_PROFISSAO in dicionarioEstoque:
                        print(f'{dicionarioEstoque[CHAVE_PROFISSAO]} - Nível {dicionarioEstoque[CHAVE_NIVEL]} - {dicionarioEstoque[CHAVE_QUANTIDADE]} und - {dicionarioEstoque[CHAVE_NOME]}.')
                        if indice < len(listaDicionarioEstoqueOrdenado):
                            if dicionarioEstoque[CHAVE_PROFISSAO] != listaDicionarioEstoqueOrdenado[indice][CHAVE_PROFISSAO]:
                                linhaSeparacao()
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
                                        while opcaoInvalida(novaQuantidade, 9999):
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
        menuPrincipal()

def tratrarOpcaoListaDesejoSelecionada(opcaoLista):
    if opcaoLista == 0:#Volta ao menu anterior
        print(f'Voltar.')
    elif opcaoLista == 1:#Inicia busca
        preparaPersonagem(dicionarioUsuario)
    elif opcaoLista == 2:#Exclui trabalho da lista
        menuExcluiTrabalho()

def adicionarNovoTrabalhoDesejado(dicionarioUsuario):
    dicionarioTrabalho = {}
    dicionarioTrabalho[CHAVE_RARIDADE] = defineRaridade()
    if variavelExiste(dicionarioTrabalho[CHAVE_RARIDADE]):
        dicionarioTrabalho[CHAVE_PROFISSAO] = defineProfissao(dicionarioUsuario)
        if variavelExiste(dicionarioTrabalho[CHAVE_PROFISSAO]):
            dicionarioTrabalho = defineTrabalho(dicionarioTrabalho)
            if variavelExiste(dicionarioTrabalho):
                dicionarioTrabalho[CHAVE_LICENCA] = defineLicenca()
                if variavelExiste(dicionarioTrabalho[CHAVE_LICENCA]):
                    dicionarioTrabalho[CHAVE_RECORRENCIA] = defineRecorrencia()
                    if variavelExiste(dicionarioTrabalho[CHAVE_RECORRENCIA]):
                        dicionarioTrabalho[CHAVE_ESTADO] = 0
                        adicionaTrabalhoDesejo(dicionarioUsuario,dicionarioTrabalho)

def exibirOpcoesMenuPrincipal():
    print(f'1 - Produzir item.')
    print(f'2 - Lista de desejo.')
    print(f'3 - Usar habilidade.')
    print(f'4 - Atualizar lista de profissões.')
    print(f'5 - Cadastrar.')
    print(f'6 - Configurações.')
    print(f'7 - Temporario.')
    print(f'8 - Estoque.')
    print(f'0 - Voltar.\n')

def menuExcluiTrabalho():
    exibirSubTitulo('Lista todos trabalho desejados')
    mostraListaDesejoComIndice(dicionarioUsuario)
    opcaoExclui = input(f'Qual trabalho deseja exluir?')
    if opcaoInvalida(opcaoExclui, len(dicionarioUsuario[CHAVE_LISTA_DESEJO])):
        exibirMensagemOpcaoInvalida()
        menuExcluiTrabalho()
    else:
        opcaoExclui = int(opcaoExclui)
        if opcaoExclui != 0:
            dicionarioTrabalho = dicionarioUsuario[CHAVE_LISTA_DESEJO][opcaoExclui-1]
            excluiTrabalhoListaDesejos(dicionarioUsuario, dicionarioTrabalho)
            del dicionarioUsuario[CHAVE_LISTA_DESEJO][opcaoExclui-1]

def menuPersonagem():
    exibirSubTitulo('Personagens')
    definirListaDePersonagens()
    exibirListaDePersonagens()
    definirOpcaoPersonagemSelecionado()

def exibirListaDePersonagens():
    if tamanhoIgualZero(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]):
        print(f'Lista de personagens está vazia!')
    else:
        x = 1
        print(f'{"Índice".ljust(6)}|{"Nome".ljust(20)}|{"Estado".ljust(10)}|{"Uso".ljust(10)}|{"Espaço produção".ljust(3)}')
        for dicionarioPersonagem in dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
            estado = 'Ativado' if dicionarioPersonagem[CHAVE_ESTADO] else 'Desativado'
            uso = 'Ocupado' if dicionarioPersonagem[CHAVE_USO] else 'Desocupado'
            print(f'{str(x).ljust(6)}|{dicionarioPersonagem[CHAVE_NOME].ljust(20)}|{estado.ljust(10)}|{uso.ljust(10)}|{str(dicionarioPersonagem[CHAVE_ESPACO_PRODUCAO]).ljust(3)}')
            x += 1
    print(f'{"0 -".ljust(6)} Voltar\n')

def definirOpcaoPersonagemSelecionado():
    opcaoPersonagem = input('Personagem escolhido: ')
    if opcaoInvalida(opcaoPersonagem, len(dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM])):
        exibirMensagemOpcaoInvalida()
        menuPersonagem()
    else:
        opcaoPersonagem = int(opcaoPersonagem)
        if opcaoPersonagem == 0:
            menuUsuarios()
        else:
            dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM][opcaoPersonagem]
            if variavelExiste(dicionarioUsuario[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                menuPrincipal()
            else:
                menuPersonagem()

def definirListaDePersonagens():
    listaDicionariosPersonagens = retornaListaDicionariosPersonagens(dicionarioUsuario)
    dicionarioUsuario[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = sorted(listaDicionariosPersonagens,key=lambda dicionario:(dicionario[CHAVE_EMAIL],dicionario[CHAVE_NOME]))

def menuUsuarios():
    exibirSubTitulo('Usuários')
    exibirOpcoesUsuarios()
    escolherUsuario()

def escolherUsuario():
    opcaoUsuario = input('Usuário escolhido: ')
    while opcaoInvalida(opcaoUsuario, 2):
        input(f'Opção inválida! Clique qualquer tecla para voltar ao menu.')
        menuUsuarios()
    else:
        opcaoUsuario = int(opcaoUsuario)
        if opcaoUsuario == 0:
            finalizaApp()
        elif opcaoUsuario==1:
            dicionarioUsuario[CHAVE_ID_USUARIO]='eEDku1Rvy7f7vbwJiVW7YMsgkIF2'
            menuPersonagem()
        elif opcaoUsuario==2:
            dicionarioUsuario[CHAVE_ID_USUARIO]='LA2UjmX7oBX3AlRJfmdWAD41OWg2'
            menuPersonagem()

def exibirOpcoesUsuarios():
    print(f'1 - Usuario')
    print(f'2 - Usuario teste')
    print(f'0 - Sair\n')

def finalizaApp():
    print(f'Saindo...')

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
    menuUsuarios()