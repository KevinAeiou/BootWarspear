import pyrebase
from metodos.lista_chaves import *

link_database = 'https://bootwarspear-default-rtdb.firebaseio.com/'
link_storage = 'gs://bootwarspear.appspot.com'

firebaseConfig = {
    'apiKey': "AIzaSyCrQz9bYczFvF5S-HNlha48hXD7Mmiq6R8",
    'authDomain': "bootwarspear.firebaseapp.com",
    'databaseURL': "https://bootwarspear-default-rtdb.firebaseio.com",
    'projectId': "bootwarspear",
    'storageBucket': "bootwarspear.appspot.com",
    'messagingSenderId': "882438857395",
    'appId': "1:882438857395:web:1d0b926a94d0aacca086c6"}

firebase = pyrebase.initialize_app(firebaseConfig)
autenticacao = firebase.auth()

def autenticaUsuario(email, senha):
    try:
        entrar = autenticacao.sign_in_with_email_and_password(email,senha)
        print(f'Conecção bem sucedida')
        return entrar[CHAVE_LOCAL_ID]
    except:
        print(f'Email ou senha invalidos!')
    return None

def criaUsuario(email, senha):
    try:
        autenticacao.create_user_with_email_and_password(email, senha)
    except:
        print(f'Erro ao cadastrar usuário!')
    return None