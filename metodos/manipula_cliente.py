import requests
import json
import time
import uuid 
from metodos.lista_chaves import *

link_database = 'https://bootwarspear-default-rtdb.firebaseio.com/'
link_storage = 'gs://bootwarspear.appspot.com'
nome_imagem_trabalho = 'imagem_trabalho.png'
tempoConeccao=1
tempoLeitura=1.5
            
def retornaRequisicao(tipoRequisicao,caminhoRequisicao,dados):
    requisicaoRetorno=None
    for x in range(10):
        try:
            if tipoRequisicao==GET:
                # print(f'{D}:Fez requisição GET!')
                requisicao=requests.get(caminhoRequisicao,timeout=(tempoConeccao,tempoLeitura))
            elif tipoRequisicao==POST:
                # print(f'{D}:Fez requisição POST!')
                requisicao=requests.post(caminhoRequisicao,data=json.dumps(dados),timeout=(tempoConeccao,tempoLeitura))
            elif tipoRequisicao==PATCH:
                # print(f'{D}:Fez requisição PATCH!')
                requisicao=requests.patch(caminhoRequisicao,data=json.dumps(dados),timeout=(tempoConeccao,tempoLeitura))
            elif tipoRequisicao==DELETE:
                # print(f'{D}:Fez requisição DELETE!')
                requisicao=requests.delete(caminhoRequisicao,timeout=(tempoConeccao,tempoLeitura))
            requisicaoRetorno=requisicao
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
        except requests.exceptions.ReadTimeout:
            print(f'Erro ReadTimeout!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return requisicaoRetorno

def adicionaVenda(dicionarioPersonagem, dicionarioVenda):
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_vendas/.json'
    requisicao = retornaRequisicao(POST,caminhoRequisicao,dicionarioVenda)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        if dicionarioRequisicao:
            idProdutoVendido = dicionarioRequisicao['name']
            caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_vendas/{idProdutoVendido}.json'
            requisicao = retornaRequisicao(PATCH, caminhoRequisicao, dados = {'id':idProdutoVendido})
            if requisicao:
                dicionarioVenda[CHAVE_ID] = idProdutoVendido
                print(f'Nova venda foi adicionada: {dicionarioVenda["nomeProduto"]}.')
                return dicionarioVenda
            else:
                print(f'Falha ao adicionar ({dicionarioVenda["nomeProduto"]}).')
                requisicao = retornaRequisicao(DELETE, caminhoRequisicao, None)
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return {}

def retornaListaDicionariosTrabalhosEstoque(dicionarioPersonagemAtributos):
    listaDicionarioEstoque=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao:
            for chave in dicionarioRequisicao:
                # print(f'{D}:{dicionarioRequisicao[chave]}')
                listaDicionarioEstoque.append(dicionarioRequisicao[chave])
        else:
            print(f'Resultado dicionario: {dicionarioRequisicao}.')
    else:
        print(f'Resultado requisição: {requisicao}.')
    return listaDicionarioEstoque

def retornaListaDicionariosTrabalhosVendidos(dicionarioPersonagem):
    print(f'Definindo lista dicionários produtos vendidos...')
    listaDicionariosTrabalhosVendidos = []
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_vendas/.json'
    requisicao = retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        if dicionarioRequisicao:
            for chave in dicionarioRequisicao:
                # print(f'{D}:{dicionarioRequisicao[chave]}')
                caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_vendas/{chave}.json'
                if not CHAVE_ID in dicionarioRequisicao[chave]:
                    requisicao = retornaRequisicao(PATCH, caminhoRequisicao, dados = {'id':chave})
                if dicionarioRequisicao[chave]['valorProduto']=="":
                    print(F'{D}: Valor do produto ({dicionarioRequisicao[chave]}) está vazia.')
                    requisicao = retornaRequisicao(PATCH, caminhoRequisicao, dados = {'valorProduto':0})
                listaDicionariosTrabalhosVendidos.append(dicionarioRequisicao[chave])
        else:
            print(f'Resultado dicionario: {dicionarioRequisicao}.')
    else:
        print(f'Resultado requisição: {requisicao}.')
    return listaDicionariosTrabalhosVendidos

def excluiTrabalhoVendido(dicionarioPersonagem, dicionarioTrabalhoVendido):
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_vendas/{dicionarioTrabalhoVendido[CHAVE_ID]}/.json'
    requisicao = retornaRequisicao(DELETE, caminhoRequisicao, None)
    if requisicao:
        print(f'{dicionarioTrabalhoVendido["nomeProduto"]} foi removido!')
        return True
    else:
        print(f'Erro a remover {dicionarioTrabalhoVendido["nomeProduto"]}!')
    return False

def adicionaTrabalhoEstoque(dicionarioPersonagem, dicionarioTrabalho):
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/.json'
    requisicao = retornaRequisicao(POST, caminhoRequisicao, dicionarioTrabalho)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        dados = {'id':dicionarioRequisicao['name']}
        caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{dicionarioRequisicao["name"]}/.json'
        requisicao = retornaRequisicao(PATCH, caminhoRequisicao, dados)
        if requisicao:
            dicionarioRequisicao = requisicao.json()
            dicionarioTrabalho[CHAVE_ID] = dicionarioRequisicao[CHAVE_ID]
            return dicionarioTrabalho
        else:
            caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{dicionarioRequisicao["name"]}/.json'
            requisicao = retornaRequisicao(DELETE,caminhoRequisicao,None)
    return {}

def adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioTrabalho):
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/.json'
    requisicao = retornaRequisicao(POST, caminhoRequisicao, dicionarioTrabalho)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        dados = {'id':dicionarioRequisicao['name']}
        caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioRequisicao["name"]}/.json'
        requisicao = retornaRequisicao(PATCH,caminhoRequisicao,dados)
        if requisicao:
            dicionarioRequisicao = requisicao.json()
            dicionarioTrabalho[CHAVE_ID] = dicionarioRequisicao[CHAVE_ID]
            print(f'Novo trabalho ({dicionarioTrabalho[CHAVE_NOME]}) foi adicionado a lista de desejo!')
            return dicionarioTrabalho
        else:
            caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioRequisicao["name"]}/.json'
            requisicao = retornaRequisicao(DELETE,caminhoRequisicao,None)
    else:
        print(f'Limite de tentativas de conexão atingido.')
        print(f'Erro ao adicionar {dicionarioTrabalho[CHAVE_NOME]} a lista de desejo.')
    return {}

def retornaListaDicionariosProfissoes(dicionarioPersonagemAtributos):
    listaDicionarioProfissao = []
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/.json'
    requisicao = retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao != None:
        dicionarioProfissoes = requisicao.json()
        if dicionarioProfissoes != None:
            for idProfissao in dicionarioProfissoes:
                dicionarioProfissao = {
                    CHAVE_ID:idProfissao,
                    CHAVE_PRIORIDADE:dicionarioProfissoes[idProfissao][CHAVE_PRIORIDADE],
                    CHAVE_EXPERIENCIA:dicionarioProfissoes[idProfissao][CHAVE_EXPERIENCIA],
                    CHAVE_NOME:dicionarioProfissoes[idProfissao][CHAVE_NOME]}
                listaDicionarioProfissao.append(dicionarioProfissao)
    return listaDicionarioProfissao

def cadastraNovoTrabalho(dicionarioTrabalho):
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/.json'
    requisicao=retornaRequisicao(POST,caminhoRequisicao,dicionarioTrabalho)
    if requisicao!=None:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            dados={'id':dicionarioRequisicao['name']}
            caminhoRequisicao=f'{link_database}/Lista_trabalhos/{dicionarioRequisicao["name"]}/.json'
            requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
            if requisicao!=None:
                dicionarioTrabalho[CHAVE_ID] = dados[CHAVE_ID]
                print(f'{dicionarioTrabalho} foi adicionado.')
                return dicionarioTrabalho
            else:
                print(f'Erro ao cadastrar novo trabalho!')
                caminhoRequisicao=f'{link_database}/Lista_trabalhos/{dicionarioRequisicao["name"]}/.json'
                requisicao=retornaRequisicao(DELETE,caminhoRequisicao,None)
        else:
            print(f'Resultado da dicionario: {dicionarioRequisicao}.')
    else:
        print(f'Erro ao cadastrar novo trabalho!')
    return {}

def retornaDicionarioUsuario(dicionarioUsuario):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioUsuario[CHAVE_ID_USUARIO]}/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            for id in dicionarioRequisicao:
                dicionarioUsuario[CHAVE_NOME]=dicionarioRequisicao[id][CHAVE_NOME]
        else:
            print(f'Resultado do dicionário: {dicionarioRequisicao}.')
    else:
        print(f'Resultado da requisição: {requisicao}.')
    return dicionarioUsuario

def retornaListaDicionariosTrabalhos():
    listaDicionariosOrdenada=[]
    listaDicionariosTrabalhos=[]
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            for trabalhoId in dicionarioRequisicao:
                dicionarioTrabalho=dicionarioRequisicao[trabalhoId]
                dicionarioTrabalho[CHAVE_ID]=trabalhoId
                listaDicionariosTrabalhos.append(dicionarioTrabalho)
            listaDicionariosOrdenada=sorted(listaDicionariosTrabalhos,key=lambda dicionario:dicionario[CHAVE_NOME])
        else:
            print(f'Resultado do dicionário: {dicionarioRequisicao}.')
    else:
        print(f'Resultado da requisição: {requisicao}.')
    return listaDicionariosTrabalhos

def defineChaveListaDicionariosTrabalhosDesejados(dicionarioPersonagemAtributos):
    listaDicionarioTrabalhoDesejado = []
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/.json'
    requisicao = retornaRequisicao(GET, caminhoRequisicao, None)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        if dicionarioRequisicao != None:
            for trabalhoDesejadoId in dicionarioRequisicao:
                dicionarioTrabalhoDesejado = dicionarioRequisicao[trabalhoDesejadoId]
                dicionarioTrabalhoDesejado[CHAVE_ID] = trabalhoDesejadoId
                listaDicionarioTrabalhoDesejado.append(dicionarioTrabalhoDesejado)
        else:
            print(f'Resultado do dicionario: {dicionarioRequisicao}.')  
    else:
        print(f'Resultado da requisição: {requisicao}.')
    dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO] = listaDicionarioTrabalhoDesejado
    return dicionarioPersonagemAtributos

def retornaListaDicionariosPersonagens(dicionarioPersonagem):
    print(f'Definindo lista de personagem.')
    listaDicionariosPersonagens = []
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/.json'
    requisicao = retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        if dicionarioRequisicao != None:
            for personagemId in dicionarioRequisicao:
                personagem = {
                    CHAVE_ID:personagemId,
                    CHAVE_NOME:dicionarioRequisicao[personagemId][CHAVE_NOME],
                    CHAVE_EMAIL:dicionarioRequisicao[personagemId][CHAVE_EMAIL],
                    CHAVE_SENHA:dicionarioRequisicao[personagemId][CHAVE_SENHA],
                    CHAVE_ESPACO_PRODUCAO:dicionarioRequisicao[personagemId][CHAVE_ESPACO_PRODUCAO],
                    CHAVE_ESTADO:dicionarioRequisicao[personagemId][CHAVE_ESTADO],
                    CHAVE_USO:dicionarioRequisicao[personagemId][CHAVE_USO]}
                listaDicionariosPersonagens.append(personagem)
            listaDicionariosPersonagens = sorted(listaDicionariosPersonagens,key=lambda dicionario:(dicionario[CHAVE_EMAIL],dicionario[CHAVE_NOME]))
        else:
            print(f'Resultado do dicionario: {dicionarioRequisicao}.') 
    else:
        print(f'Resultado da requisição: {requisicao}.')
    return listaDicionariosPersonagens

def modificaAtributoPersonagem(dicionarioPersonagemAtributos, listaPersonagemId, atributo, valor):
    dados = {atributo:valor}
    for personagemId in listaPersonagemId:
        caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/.json'
        requisicao = retornaRequisicao(GET,caminhoRequisicao,None)
        if requisicao:
            dicionarioRequisicao=requisicao.json()
            if dicionarioRequisicao!=None:
                for id in dicionarioRequisicao:
                    if personagemId==id:
                        nome=dicionarioRequisicao[id][CHAVE_NOME]
                        caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{id}/.json'
                        retornaRequisicao(PATCH,caminhoRequisicao,dados)
                        print(f'Atributo {atributo} do personagem {nome} agora é {valor}.')
                        for dicionarioPersonagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
                            if dicionarioPersonagem[CHAVE_ID] == personagemId:
                                dicionarioPersonagem[atributo] = valor
                                break
                        break
            else:
                print(f'Erro ao modificar atributo!')
                print(f'Resultado do dicionario: {dicionarioRequisicao}.')
                break
        else:
            print(f'Erro ao modificar atributo!')
            print(f'Resultado da requisição: {requisicao}.')
            break
    return dicionarioPersonagemAtributos

def excluiTrabalhoListaDesejos(dicionarioPersonagemAtributos, dicionarioTrabalho):
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalho[CHAVE_ID]}/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None):
        pass
    else:
        print(f'Erro ao exluir {dicionarioTrabalho[CHAVE_NOME]} da lista de desejo.')

def excluiTrabalhoListaEstoque(dicionarioPersonagemAtributos, dicionarioTrabalho):
    caminhoRequisicao = f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_estoque/{dicionarioTrabalho[CHAVE_ID]}/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None):
        pass
    else:
        print(f'Erro ao exluir {dicionarioTrabalho[CHAVE_NOME]} da lista de desejo.')

def excluiTrabalhoListaTrabalhos(dicionarioTrabalho):
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/{dicionarioTrabalho[CHAVE_ID]}/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None):
        pass
        # print(f'Trabalho id: {dicionarioTrabalho[CHAVE_ID]} - {dicionarioTrabalho[CHAVE_NOME]} exluido da lista de desejo.')
    else:
        print(f'Erro ao exluir {dicionarioTrabalho[CHAVE_NOME]} da lista de desejo.')

def retornaTrabalhoCaminhoEspecifico(idEspecifico):
    caminhoRequisicao = f'{link_database}/Lista_trabalhos/{idEspecifico}/.json'
    requisicao = retornaRequisicao(GET, caminhoRequisicao, None)
    if requisicao:
        dicionarioRequisicao = requisicao.json()
        if dicionarioRequisicao != None:
            return dicionarioRequisicao
    else:
        print(f'Erro requisicao: {requisicao}...')
    return {}

def modificaAtributo(caminhoRequisicao, dados):
    caminhoRequisicao = f'{link_database}/{caminhoRequisicao}'
    requisicao = retornaRequisicao(PATCH, caminhoRequisicao, dados)
    if requisicao:
        print(f'Adicionado com sucesso!')
    else:
        print(f'Erro ao adicionar atributo {dados}!')

def adicionaNovaProfissao(dicionarioPersonagem,novaProfissao):
    tamanho=len(dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PROFISSAO])
    random=uuid.uuid1()
    id=str(tamanho)+random.hex
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/.json'
    requisicao=retornaRequisicao(POST,caminhoRequisicao,novaProfissao)
    if requisicao:
        print(f'{novaProfissao[CHAVE_NOME]} foi adicionada ao personagem {dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME]} com sucesso.')
    else:
        print(f'Erro ao adicionar nova profissão!')

def adicionaAtributoTrabalhoNecessario(dicionarioUsuario):
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/{dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_ID]}/.json'
    trabalhoNecessario=dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO][CHAVE_NOME]
    if CHAVE_TRABALHO_NECESSARIO in dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO]:
        trabalhoNecessario=dicionarioUsuario[CHAVE_DICIONARIO_TRABALHO_DESEJADO][CHAVE_TRABALHO_NECESSARIO]+','+dicionarioUsuario[CHAVE_TRABALHO_NECESSARIO][CHAVE_NOME]
    dados={CHAVE_TRABALHO_NECESSARIO:trabalhoNecessario}
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
    if requisicao:
        print(f'Raridade de {dicionarioUsuario[CHAVE_PROFISSAO]}:{dicionarioUsuario[CHAVE_NOME]}.')
    else:
        print(f'Erro ao modificar raridade de {dicionarioUsuario[CHAVE_NOME]}.')
