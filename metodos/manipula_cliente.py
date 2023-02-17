import socket
import requests
import json
import time

link_database = 'https://bootwarspear-default-rtdb.firebaseio.com/'
link_storage = 'gs://bootwarspear.appspot.com'
nome_imagem_trabalho = 'imagem_trabalho.png'

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
#modificado 16/01
def adiciona_trabalho(personagem_id,trabalho,licenca):
    dados = {'nome':trabalho[0],'profissao':trabalho[1],'nivel':int(trabalho[3]),'tipo_licenca':licenca,'raridade':trabalho[2],'estado':0}
    for x in range(10):
        try:
            requisicao = requests.post(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo/.json',data=json.dumps(dados))
            id = requisicao.text.split(':')
            id = id[1].replace('"','').replace('}','')
            dados = {'id':id}
            requisicao = requests.patch(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_desejo/{id}/.json',data=json.dumps(dados))
            print(f'{trabalho[0]} foi adicionado!')
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
    else:
        print(f'Limite de tentativas de conexão atingido.')
#modificado 16/01
def adicionar_profissao(personagem_id,profissao):
    dados = {'nome':profissao}
    for x in range(10):
        try:
            requisicao = requests.post(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_profissoes/.json',data=json.dumps(dados))
            id = requisicao.text.split(':')
            id = id[1].replace('"','').replace('}','')
            dados = {'id':id}
            requisicao = requests.patch(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_profissoes/{id}/.json',data=json.dumps(dados))
            print(f'{profissao} foi adicionado!')
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
    else:
        print(f'Limite de tentativas de conexão atingido.')

def cadastrar_imagem_trabalho():
    dados = {'nome':nome_imagem_trabalho}
    requisicao = requests.post(f'{link_storage}/Lista_imagens_trabalhos/{nome_imagem_trabalho}')
    print(requisicao)
    print(requisicao.text)
#modificado 12/01
def cadastrar_trabalho(trabalho):
    atributos = trabalho.split(',')
    dados = {'nome':atributos[0],'profissao':atributos[1],'nivel':int(atributos[2]),'raridade':atributos[3],'estado':0}
    for x in range(10):
        try:
            requisicao = requests.post(f'{link_database}/Lista_trabalhos/.json',data=json.dumps(dados))
            id = requisicao.text.split(':')
            id = id[1].replace('"','').replace('}','')
            dados = {'id':id}
            requisicao = requests.patch(f'{link_database}/Lista_trabalhos/{id}/.json',data=json.dumps(dados))
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')

def retorna_idpersonagem_ativo(usuario_id):
    for x in range(10):
        try:
            requisicao = requests.get(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/.json')
            dicionario_requisicao = requisicao.json()
            for id in dicionario_requisicao:
                if dicionario_requisicao[id]['estado']==1:
                    return id
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')    

def consulta_dados_personagem(usuario_id,personagem_id):
    dados_personagem = []
    for x in range(10):
        try:
            requisicao = requests.get(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{personagem_id}/.json')
            dicionario_requisicao = requisicao.json()
            dados_personagem.append(dicionario_requisicao['id'])
            dados_personagem.append(dicionario_requisicao['nome'])
            dados_personagem.append(dicionario_requisicao['email'])
            dados_personagem.append(dicionario_requisicao['senha'])
            dados_personagem.append(dicionario_requisicao['estado'])
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return dados_personagem
    
#modificado 12/01
def consutar_lista(tipo_lista):
    lista = []
    for x in range(10):    
        try:
            requisicao = requests.get(f'{link_database}/Usuarios/{tipo_lista}/.json')
            dicionario_requisicao = requisicao.json()
            for id in dicionario_requisicao:
                nome = dicionario_requisicao[id]['nome']
                lista.append([id,nome])
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return lista

def consulta_lista_trabalho(nome_proficao,raridade):
    lista_profissao = []
    for x in range(10):    
        try:
            requisicao = requests.get(f'{link_database}/Lista_trabalhos/.json')
            dicionario_requisicao = requisicao.json()
            for id_trabalho in dicionario_requisicao:
                if dicionario_requisicao[id_trabalho]['profissao']==nome_proficao and dicionario_requisicao[id_trabalho]['raridade']==raridade:
                    nome_trabalho = dicionario_requisicao[id_trabalho]['nome']
                    profissao_trabalho = dicionario_requisicao[id_trabalho]['profissao']
                    raridade_trabalho = dicionario_requisicao[id_trabalho]['raridade']
                    nivel_trabalho = dicionario_requisicao[id_trabalho]['nivel']
                    lista_profissao.append([nome_trabalho,profissao_trabalho,raridade_trabalho,nivel_trabalho])
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')
    return lista_profissao

#modificado 12/01
def consultar_lista_desejo(tipo_lista):
    lista_desejo = []
    for x in range(10):
        try:
            requisicao = requests.get(f'{link_database}/Usuarios/{tipo_lista}/.json')
            dicionario_requisicao = requisicao.json()
            for id in dicionario_requisicao:
                if dicionario_requisicao[id]['estado']==0:
                    id_trabalho = dicionario_requisicao[id]['id']
                    nome_trabalho = dicionario_requisicao[id]['nome']
                    profissao_trabalho = dicionario_requisicao[id]['profissao']
                    nivel_trabalho = dicionario_requisicao[id]['nivel']
                    licenca_trabalho = dicionario_requisicao[id]['tipo_licenca']
                    raridade_trabalho = dicionario_requisicao[id]['raridade']
                    lista_desejo.append([id_trabalho,nome_trabalho, profissao_trabalho, nivel_trabalho, licenca_trabalho,raridade_trabalho])
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
    else:
        print(f'Limite de tentativas de conexão atingido.')
    #print(requisicao)
    #print(requisicao.text)
    return lista_desejo
#modificado 23/01
def muda_estado_trabalho(usuario_id,personagem_id,nome_trabalho,novo_estado):
    dados = {'estado':novo_estado}
    for x in range(10):
        try:
            requisicao = requests.get(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo/.json')
            dicionario_requisicao = requisicao.json()
            for id in dicionario_requisicao:
                if nome_trabalho in dicionario_requisicao[id]['nome'] and dicionario_requisicao[id]['estado']==novo_estado-1:
                    requisicao = requests.patch(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{personagem_id}/Lista_desejo/{id}/.json',data=json.dumps(dados))
                    print(f'Estado do trabalho mudado para {novo_estado}.')
                    break
                else:
                    print(f'{nome_trabalho} não encontrado na lista.')
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')

def muda_estado_personagem(usuario_id,personagem_id):
    
    for x in range(10):
        try:
            requisicao = requests.get(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/.json')
            dicionario_requisicao = requisicao.json()
            for id in dicionario_requisicao:
                if personagem_id == id:
                    dados = {'estado':1}
                    nome = dicionario_requisicao[id]['nome']
                    requisicao = requests.patch(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{id}/.json',data=json.dumps(dados))
                    print(f'Estado do {nome} agora é ativo.')
                else:
                    dados = {'estado':0}
                    requisicao = requests.patch(f'{link_database}/Usuarios/{usuario_id}/Lista_personagem/{id}/.json',data=json.dumps(dados))
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
            time.sleep(1)
    else:
        print(f'Limite de tentativas de conexão atingido.')

#modificado 12/01
def excluir_trabalho(trabalho_id):
    for x in range(10):
        try:
            requisicao = requests.delete(f'{link_database}/Usuarios/{trabalho_id}/.json')
            print('Trabalho exluido da lista de desejo.')
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
    else:
        print(f'Limite de tentativas de conexão atingido.')
#modificado 12/01
def excluir_lista_profissoes(personagem_id):
    for x in range(10):
        try:
            requisicao = requests.delete(f'{link_database}/Usuarios/eEDku1Rvy7f7vbwJiVW7YMsgkIF2/Lista_personagem/{personagem_id}/Lista_profissoes/.json')
            print(f'Lista de profissões limpa!')
            break
        except requests.exceptions.ConnectionError:
            print(f'Conecção recusada!')
    else:
        print(f'Limite de tentativas de conexão atingido.')

# cadastrar_trabalho('ChapéuinigualáveldeRagnar,Armaduraleve,14,Especial,')