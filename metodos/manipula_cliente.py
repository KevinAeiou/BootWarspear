import socket
import requests
import json
import time

link_database = 'https://bootwarspear-default-rtdb.firebaseio.com/'
link_storage = 'gs://bootwarspear.appspot.com'
nome_imagem_trabalho = 'imagem_trabalho.png'
tempoConeccao=1
tempoLeitura=1.5

GET='get'
PATCH='patch'
POST='post'
DELETE='delete'

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

# def autenticar_usuario(email,senha):
#     try:
#         entrar = autenticacao.sign_in_with_email_and_password(email,senha)
#         print(autenticacao.get_account_info(entrar['idToken']))
#         print(f'Conecção bem sucedida')
#         return True
#     except:
#         print(f'Email ou senha invalidos!')
#     return False

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
                print('Fez requisição GET!')
                requisicao=requests.get(caminhoRequisicao,timeout=(tempoConeccao,tempoLeitura))
            elif tipoRequisicao==POST:
                print('Fez requisição POST!')
                requisicao=requests.post(caminhoRequisicao,data=json.dumps(dados),timeout=(tempoConeccao,tempoLeitura))
            elif tipoRequisicao==PATCH:
                print('Fez requisição PATCH!')
                requisicao=requests.patch(caminhoRequisicao,data=json.dumps(dados),timeout=(tempoConeccao,tempoLeitura))
            elif tipoRequisicao==DELETE:
                print('Fez requisição DELETE!')
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

def adiciona_trabalho(personagem_id,trabalho,licenca,estado):
    trabalho_adicionado=[]
    dados = ({'nome':trabalho[1],
              'profissao':trabalho[2],
              'raridade':trabalho[5],
              'nivel':int(trabalho[3]),
              'tipo_licenca':licenca,
              'estado':estado,
              'recorrencia':0})
    for x in range(10):
        try:
            requisicao = requests.post(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo/.json',data=json.dumps(dados))
            dicionarioId=requisicao.json()
            id=dicionarioId['name']
            dados = {'id':id}
            requisicao = requests.patch(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo/{id}/.json',data=json.dumps(dados))
            requisicao = requests.get(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo/{id}/.json')
            dicionario_requisicao = requisicao.json()
            id_trabalho = dicionario_requisicao['id']
            nome_trabalho = dicionario_requisicao['nome']
            profissao_trabalho = dicionario_requisicao['profissao']
            nivel_trabalho = dicionario_requisicao['nivel']
            licenca_trabalho = dicionario_requisicao['tipo_licenca']
            raridade_trabalho = dicionario_requisicao['raridade']
            recorrencia_trabalho=dicionario_requisicao['recorrencia']
            estado_trabalho=dicionario_requisicao['estado']

            trabalho_adicionado.append([id_trabalho,
                                nome_trabalho,
                                profissao_trabalho,
                                nivel_trabalho,
                                licenca_trabalho,
                                raridade_trabalho,
                                recorrencia_trabalho,
                                estado_trabalho])
            print(f'{nome_trabalho} foi adicionado!')
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return trabalho_adicionado
#modificado 16/01
def modificarProfissao(personagemId,profissaoId,profissao):
    dados={'nome':profissao}
    caminhoRequisicao=f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagemId}/Lista_profissoes/{profissaoId}/.json'
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
    if requisicao!=None:
        print(f'{profissao} foi modificado!')

def cadastrar_imagem_trabalho():
    dados={'nome':nome_imagem_trabalho}
    caminhoRequisicao=f'{link_storage}/Lista_imagens_trabalhos/{nome_imagem_trabalho}'
    requisicao = retornaRequisicao(POST,caminhoRequisicao,dados)
    if requisicao!=None:
        print(requisicao)
        print(requisicao.text)
#modificado 12/01
def cadastrar_trabalho(trabalho):
    dados = {
        'nome':trabalho[0],
        'profissao':trabalho[1],
        'nivel':trabalho[2],
        'raridade':trabalho[3],
        'estado':0,
        'recorrencia':0}
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/.json'
    requisicao=retornaRequisicao(POST,caminhoRequisicao,dados)
    if requisicao!=None:
        dicionarioId=requisicao.json()
        id=dicionarioId['name']
        dados = {'id':id}
        caminhoRequisicao=f'{link_database}/Lista_trabalhos/{id}/.json'
        retornaRequisicao(PATCH,caminhoRequisicao,dados)

def retorna_idpersonagem_ativo(usuario_id):
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            if dicionario_requisicao[id]['estado']==1:
                return id 

def consulta_dados_personagem(usuario_id,personagem_id):
    dados_personagem=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{personagem_id}/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        dados_personagem.append(dicionario_requisicao['id'])
        dados_personagem.append(dicionario_requisicao['nome'])
        dados_personagem.append(dicionario_requisicao['email'])
        dados_personagem.append(dicionario_requisicao['senha'])
        dados_personagem.append(dicionario_requisicao['estado'])
    return dados_personagem
#modificado 12/01
def consutar_lista(tipo_lista):
    lista=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{tipo_lista}/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            nome=dicionario_requisicao[id]['nome']
            lista.append([id,nome])
    return lista

def consulta_lista_trabalho(nome_proficao,raridade):
    lista_profissao=[]
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        for id_trabalho in dicionario_requisicao:
            if dicionario_requisicao[id_trabalho]['profissao']==nome_proficao and dicionario_requisicao[id_trabalho]['raridade']==raridade:
                nome_trabalho = dicionario_requisicao[id_trabalho]['nome']
                profissao_trabalho = dicionario_requisicao[id_trabalho]['profissao']
                raridade_trabalho = dicionario_requisicao[id_trabalho]['raridade']
                nivel_trabalho = dicionario_requisicao[id_trabalho]['nivel']
                lista_profissao.append([nome_trabalho,profissao_trabalho,raridade_trabalho,nivel_trabalho])
    return lista_profissao

#modificado 12/01
def consulta_lista_desejo(tipo_lista):
    lista_desejo=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{tipo_lista}/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            if dicionario_requisicao[id]['estado']==0:
                id_trabalho = dicionario_requisicao[id]['id']
                nome_trabalho = dicionario_requisicao[id]['nome']
                profissao_trabalho = dicionario_requisicao[id]['profissao']
                nivel_trabalho = dicionario_requisicao[id]['nivel']
                licenca_trabalho = dicionario_requisicao[id]['tipo_licenca']
                raridade_trabalho = dicionario_requisicao[id]['raridade']
                recorrencia_trabalho=dicionario_requisicao[id]['recorrencia']
                estado_trabalho=dicionario_requisicao[id]['estado']
                lista_desejo.append([id_trabalho,
                                    nome_trabalho,
                                    profissao_trabalho,
                                    nivel_trabalho,
                                    licenca_trabalho,
                                    raridade_trabalho,
                                    recorrencia_trabalho,
                                    estado_trabalho])
    return lista_desejo

def consulta_lista_personagem(usuario_id):
    lista_personagem=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            if dicionario_requisicao[id]['estado']==1:
                id_personagem=dicionario_requisicao[id]['id']
                nome_personagem=dicionario_requisicao[id]['nome']
                email_personagem=dicionario_requisicao[id]['email']
                senha_personagem=dicionario_requisicao[id]['senha']
                espacoProducaoPersonagem=dicionario_requisicao[id]['espacoProducao']
                lista_personagem.append([id_personagem,nome_personagem,email_personagem,senha_personagem,espacoProducaoPersonagem])
    return lista_personagem

def muda_estado_trabalho(usuario_id,personagem_id,trabalho,novo_estado):
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        dados={'estado':novo_estado}
        for id in dicionario_requisicao:
            caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo/{id}/.json'
            if novo_estado==1:
                if ((trabalho[1] in dicionario_requisicao[id]['nome'])and
                    (novo_estado-1==dicionario_requisicao[id]['estado'])and
                    (trabalho[2]in dicionario_requisicao[id]['profissao'])and
                    (trabalho[6]!=1)):
                    retornaRequisicao(PATCH,caminhoRequisicao,dados)
                    print(f'Estado do trabalho modificado para "Produzindo".')
                    break
            elif novo_estado==2:
                if ((trabalho[1] in dicionario_requisicao[id]['nome'])and
                    (novo_estado-1==dicionario_requisicao[id]['estado'])):
                    retornaRequisicao(PATCH,caminhoRequisicao,dados)
                    print(f'Estado do trabalho modificado para "Concluído".')
                    return
        else:
            print(f'{trabalho[1]} não encontrado na lista.')

def mudaAtributoPersonagem(usuario_id,listaPersonagemId,atributo,valor):
    dados={atributo:valor}
    for personagem_id in listaPersonagemId:
        caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/.json'
        requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
        if requisicao!=None:
            dicionarioRequisicao=requisicao.json()
            for id in dicionarioRequisicao:
                if personagem_id==id:
                    nome=dicionarioRequisicao[id]['nome']
                    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{id}/.json'
                    retornaRequisicao(PATCH,caminhoRequisicao,dados)
                    print(f'Atributo {atributo} do personagem {nome} agora é {valor}.')
                    break
        else:
            break  

def retornaListaPersonagemId(usuario_id,personagemEmail):
    listaPersonagemId=[]
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            if personagemEmail==dicionario_requisicao[id]['email']:
                listaPersonagemId.append(id)
    return listaPersonagemId

def muda_quantidade_personagem(usuario_id,nova_quantidade):
    dados={'personagem_ativo':nova_quantidade}
    caminhoRequisicao=f'{link_database}/Usuarios/{usuario_id}/.json'
    requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
    if requisicao!=None:
        return True
    return False
#modificado 12/01
def excluir_trabalho(trabalho_id):
    caminhoRequisicao=f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{trabalho_id}/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None)!=None:
        print('Trabalho exluido da lista de desejo.')
    else:
        print('Erro ao exluir da lista de desejo.')
#modificado 12/01
def excluir_lista_profissoes(personagem_id):
    caminhoRequisicao=f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_profissoes/.json'
    if retornaRequisicao(DELETE,caminhoRequisicao,None):
        print(f'Lista de profissões limpa!')
    else:
        print(f'Erro ao limpar lista de profissões!')

def adicionaAtributoRecorrencia():
    caminhoRequisicao=f'{link_database}/Lista_trabalhos/.json'
    requisicao=retornaRequisicao(GET,caminhoRequisicao,None)
    if requisicao!=None:
        dados={'recorrencia':0}
        dicionario_requisicao=requisicao.json()
        for id in dicionario_requisicao:
            nome=dicionario_requisicao[id]['nome']
            caminhoRequisicao=f'{link_database}/Lista_trabalhos/{id}/.json'
            requisicao=retornaRequisicao(PATCH,caminhoRequisicao,dados)
            print(f'Atributo recorrencia atribuido a: {nome}.')
            print('____________________________________________')
        else:
            print(f'Fim da lista.')

# adicionaAtributoRecorrencia()
# print(retornaListaPersonagemId('eEDku1Rvy7f7vbwJiVW7YMsgkIF2','caah.rm15@gmail.com'))