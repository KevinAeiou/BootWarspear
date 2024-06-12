from firebase import firebase
from Utilitarios import *

meuBanco = firebase.FirebaseApplication('https://bootwarspear-default-rtdb.firebaseio.com/', None)
minhaReferencia = meuBanco.reference('/Lista_trabalhos')
snapshot = minhaReferencia.order_by_key(CHAVE_NOME).get()
for chave, valor in snapshot.items():
    print('{0} was {1} meters tall'.format(chave, valor))