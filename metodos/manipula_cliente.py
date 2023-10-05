import socket
import requests
import json
import time
import uuid 
from lista_chaves import *

link_database = 'https://bootwarspear-default-rtdb.firebaseio.com/'
link_storage = 'gs://bootwarspear.appspot.com'
nome_imagem_trabalho = 'imagem_trabalho.png'
tempoConeccao=1
tempoLeitura=1.5

firebaseConfig = {
    'apiKey': "AIzaSyCrQz9bYczFvF5S-HNlha48hXD7Mmiq6R8",
    'authDomain': "bootwarspear.firebaseapp.com",
    'databaseURL': "https://bootwarspear-default-rtdb.firebaseio.com",
    'projectId': "bootwarspear",
    'storageBucket': "bootwarspear.appspot.com",
    'messagingSenderId': "882438857395",
    'appId': "1:882438857395:web:1d0b926a94d0aacca086c6"}

# firebase = pyrebase.initialize_app(firebaseConfig)
# autenticacao = firebase.auth()

def autenticar_usuario(email,senha):
    try:
        entrar = autenticacao.sign_in_with_email_and_password(email,senha)
        print(autenticacao.get_account_info(entrar['idToken']))
        print(f'Conecção bem sucedida')
        return True
    except:
        print(f'Email ou senha invalidos!')
    return False

def envia_dados_servidor(coordenadas):
    cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cliente.connect(("192.168.1.22",55555))
    cliente.send(coordenadas.encode())
    print(f'Enviado!')
            
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

def adicionaVenda(dicionarioPersonagem,dicionarioVenda):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_vendas/.json'
    requisicao=retornaRequisicao(POST,caminhoRequisicao,dicionarioVenda)
    if requisicao!=None:
        print(f'Nova venda foi adicionada: {dicionarioVenda["nomeProduto"]}.')
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return dicionarioVenda

def adicionaTrabalhoDesejo(dicionarioPersonagem,dicionarioTrabalho):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/.json'
    requisicao=retornaRequisicao(POST,caminhoRequisicao,dicionarioTrabalho)
    if requisicao!=None:
        dicionarioRequisicao=requisicao.json()
        dados={'id':dicionarioRequisicao['name']}
        caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioRequisicao["name"]}/.json'
        requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
        if requisicao!=None:
            dicionarioRequisicao=requisicao.json()
            # for id in dicionarioRequisicao:
            #     print(f'Novo trabalho foi adicionado: {dicionarioRequisicao[id][CHAVE_NOME]}.')
        else:
            caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioRequisicao["name"]}/.json'
            requisicao=retornaRequisicao(DELETE,caminhoRequisicao,None)
    else:
        print(f'Limite de tentativas de conexão atingido.')
        print(f'Erro ao adicionar {dicionarioTrabalho[CHAVE_NOME]} a lista de desejo.')
    return dicionarioTrabalho

def retornaListaDicionarioProfissao(dicionarioPersonagem):
    listaDicionarioProfissao=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionarioProfissoes=requisicao.json()
        if dicionarioProfissoes!=None:
            for idProfissao in dicionarioProfissoes:
                dicionarioProfissao={CHAVE_ID:idProfissao,
                                     CHAVE_NOME:dicionarioProfissoes[idProfissao][CHAVE_NOME]}
                caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{idProfissao}.json'
                dados={CHAVE_ID:idProfissao}
                adicionaAtributoId(caminhoRequisicao,dados)
                listaDicionarioProfissao.append(dicionarioProfissao)
    return listaDicionarioProfissao
#modificado 16/01
def modificarProfissao(personagemId,profissaoId,profissao):
    dados={'nome':profissao}
    caminhoRequisicao=f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagemId}/Lista_profissoes/{profissaoId}/.json'
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
    if requisicao!=None:
        dicionarioTrabalho=requisicao.json()
        if dicionarioTrabalho!=None:
            print(f'Novo trabalho foi adicionado: {dicionarioTrabalho}')
        else:
            print(f'Resultado da dicionario: {dicionarioTrabalho}.')
    else:
        print(f'Erro ao adicionar novo trabalho!')
    return dicionarioTrabalho

def modificaProfissao(dicionarioPersonagem,dicionarioProfissao):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/{dicionarioProfissao[CHAVE_ID]}/.json'
    dicionarioNomeProfissao={CHAVE_NOME:dicionarioProfissao[CHAVE_NOME]}
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dicionarioNomeProfissao)
    if requisicao!=None:
        print(f'{dicionarioNomeProfissao} foi modificado!')

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
                print(f'{dicionarioTrabalho} foi adicionado.')
            else:
                print(f'Erro ao cadastrar novo trabalho!')
                caminhoRequisicao=f'{link_database}/Lista_trabalhos/{dicionarioRequisicao["name"]}/.json'
                requisicao=retornaRequisicao(DELETE,caminhoRequisicao,None)
        else:
            print(f'Resultado da dicionario: {dicionarioRequisicao}.')
    else:
        print(f'Erro ao cadastrar novo trabalho!')

def retornaIdPersonagemAtivo(dicionarioPersonagem):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            for id in dicionarioRequisicao:
                if dicionarioRequisicao[id]['estado']==1:
                    return id
        else:
            print(f'Resultado da dicionario: {dicionarioRequisicao}.')
    else:
        print(f'Erro verificar personagem ativo!')

def retornaDicionarioDadosPersonagem(dicionarioPersonagem):
    dadosPersonagem={}
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            dadosPersonagem[CHAVE_ID]=dicionarioRequisicao[CHAVE_ID]
            dadosPersonagem[CHAVE_NOME]=dicionarioRequisicao[CHAVE_NOME]
            dadosPersonagem[CHAVE_EMAIL]=dicionarioRequisicao[CHAVE_EMAIL]
            dadosPersonagem[CHAVE_SENHA]=dicionarioRequisicao[CHAVE_SENHA]
            dadosPersonagem[CHAVE_ESTADO]=dicionarioRequisicao[CHAVE_ESTADO]
            dadosPersonagem[CHAVE_USO]=dicionarioRequisicao[CHAVE_USO]
            dadosPersonagem[CHAVE_ESPACO_PRODUCAO]=dicionarioRequisicao[CHAVE_ESPACO_PRODUCAO]
        else:
            print(f'Resultado da dicionario: {dicionarioRequisicao}.')
    else:
        print(f'Resultado da requisição: {requisicao}.')
    return dadosPersonagem

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

def retornaListaDicionariosTrabalhosDesejados(dicionarioPersonagemAtributos):
    listaDicionarioTrabalhoDesejado=[]
    listaDicionariosOrdenada=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            for trabalhoDesejadoId in dicionarioRequisicao:
                dicionarioTrabalhoDesejado=dicionarioRequisicao[trabalhoDesejadoId]
                dicionarioTrabalhoDesejado[CHAVE_ID]=trabalhoDesejadoId
                listaDicionarioTrabalhoDesejado.append(dicionarioTrabalhoDesejado)
                listaDicionariosOrdenada=sorted(listaDicionarioTrabalhoDesejado,key=lambda dicionario:dicionario[CHAVE_PROFISSAO])
        else:
            print(f'Resultado do dicionario: {dicionarioRequisicao}.')  
    else:
        print(f'Resultado da requisição: {requisicao}.')
    return listaDicionariosOrdenada

def defineListaDicionarioPersonagem(dicionarioPersonagem):
    print(f'Definindo lista de personagem.')
    dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=[]
    listaPersonagem=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            for personagemId in dicionarioRequisicao:
                personagem={
                    CHAVE_ID:personagemId,
                    CHAVE_EMAIL:dicionarioRequisicao[personagemId][CHAVE_EMAIL],
                    CHAVE_ESPACO_PRODUCAO:dicionarioRequisicao[personagemId][CHAVE_ESPACO_PRODUCAO],
                    CHAVE_ESTADO:dicionarioRequisicao[personagemId][CHAVE_ESTADO],
                    CHAVE_NOME:dicionarioRequisicao[personagemId][CHAVE_NOME],
                    CHAVE_SENHA:dicionarioRequisicao[personagemId][CHAVE_SENHA],
                    CHAVE_USO:dicionarioRequisicao[personagemId][CHAVE_USO]
                }
                listaPersonagem.append(personagem)
            dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]=sorted(listaPersonagem,key=lambda dicionario:(dicionario[CHAVE_EMAIL],dicionario[CHAVE_NOME]))
        else:
            print(f'Resultado do dicionario: {dicionarioRequisicao}.') 
    else:
        print(f'Resultado da requisição: {requisicao}.')
    # print(f'{D}:Lista de personagens:')
    # for personagem in dicionarioPersonagem[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
    #     print(f'{D}:{personagem[CHAVE_NOME]}.')
    return dicionarioPersonagem

def modificaEstadoTrabalho(dicionarioPersonagem,dicionarioTrabalho,novoEstado):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dicionarioRequisicao=requisicao.json()
        if dicionarioRequisicao!=None:
            dados={'estado':novoEstado}
            for id in dicionarioRequisicao:
                caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagem[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagem[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{id}/.json'
                if novoEstado==1:
                    if ((dicionarioTrabalho[CHAVE_NOME] in dicionarioRequisicao[id][CHAVE_NOME])and
                        (novoEstado-1==dicionarioRequisicao[id][CHAVE_ESTADO])and
                        (dicionarioTrabalho[CHAVE_PROFISSAO]in dicionarioRequisicao[id][CHAVE_PROFISSAO])and
                        (dicionarioTrabalho[CHAVE_RECORRENCIA]!=1)):
                        retornaRequisicao(PATCH,caminhoRequisicao,dados)
                        print(f'Estado do trabalho modificado para "Produzindo".')
                        break
                elif novoEstado==2:
                    if ((dicionarioTrabalho[CHAVE_NOME] in dicionarioRequisicao[id][CHAVE_NOME])and
                        (novoEstado-1==dicionarioRequisicao[id][CHAVE_ESTADO])):
                        retornaRequisicao(PATCH,caminhoRequisicao,dados)
                        print(f'Estado do trabalho modificado para "Concluído".')
                        return
            else:
                print(f'{dicionarioTrabalho[CHAVE_NOME]} não encontrado na lista.')
        else:
            print(f'Resultado do dicionario: {dicionarioRequisicao}.') 
    else:
        print(f'Resultado da requisição: {requisicao}.')

def modificaAtributoPersonagem(dicionarioPersonagemAtributos,listaPersonagemId,atributo,valor):
    dados={atributo:valor}
    for personagemId in listaPersonagemId:
        caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/.json'
        requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
        if requisicao:
            dicionarioRequisicao=requisicao.json()
            if dicionarioRequisicao!=None:
                for id in dicionarioRequisicao:
                    if personagemId==id:
                        nome=dicionarioRequisicao[id][CHAVE_NOME]
                        caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{id}/.json'
                        retornaRequisicao(PATCH,caminhoRequisicao,dados)
                        print(f'Atributo {atributo} do personagem {nome} agora é {valor}.')
                        break
            else:
                print(f'Erro ao modificar atributo!')
                print(f'Resultado do dicionario: {dicionarioRequisicao}.')
                break
        else:
            print(f'Erro ao modificar atributo!')
            print(f'Resultado da requisição: {requisicao}.')
            break

def muda_quantidade_personagem(usuario_id,nova_quantidade):
    dados={'personagem_ativo':nova_quantidade}
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/.json'
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
    if requisicao:
        return True
    return False

def excluiTrabalho(dicionarioPersonagemAtributos,dicionarioTrabalho):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{dicionarioTrabalho[CHAVE_ID]}/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None):
        print(f'Trabalho {dicionarioTrabalho[CHAVE_NOME]} exluido da lista de desejo.')
    else:
        print(f'Erro ao exluir {dicionarioTrabalho[CHAVE_NOME]} da lista de desejo.')

def excluir_lista_profissoes(dicionarioPersonagemAtributos):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_profissoes/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None):
        print(f'Lista de profissões limpa!')
    else:
        print(f'Erro ao limpar lista de profissões!')

def adicionaAtributoRecorrencia(dicionarioPersonagemAtributos):
    caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao:
        dados={'recorrencia':False}
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            if dicionario_requisicao[id][CHAVE_RECORRENCIA]==0 or dicionario_requisicao[id][CHAVE_RECORRENCIA]==1:
                nome=dicionario_requisicao[id][CHAVE_NOME]
                caminhoRequisicao=f'{link_database}/Usuarios/{dicionarioPersonagemAtributos[CHAVE_ID_USUARIO]}/Lista_personagem/{dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]}/Lista_desejo/{id}/.json'
                requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
                print(f'Atributo recorrencia atribuido a: {nome}.')
                print('____________________________________________')
        else:
            print(f'Fim da lista.')
def adicionaAtributoId(caminhoRequisicao,dados):
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
    if requisicao:
        print(f'Adicionado com sucesso!')
    else:
        print(f'Erro ao adicionar atributo id!')

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
# 0iQB1H7srqXMiufTR4HzqYQPj71hz
# adicionaAtributoRecorrencia()
# print(retornaListaPersonagemId('eEDku1Rvy7f7vbwJiVW7YMsgkIF2','caah.rm15@gmail.com'))