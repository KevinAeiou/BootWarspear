from unidecode import unidecode

def variavelExiste(variavelVerificada):
    return variavelVerificada!=None

def limpaRuidoTexto(texto):
    return unidecode(texto).replace(' ','').replace('-','').lower()

def textoEhIgual(texto1, texto2):
    return limpaRuidoTexto(texto1) == limpaRuidoTexto(texto2)

def texto1PertenceTexto2(texto1, texto2):
    return limpaRuidoTexto(texto1) in limpaRuidoTexto(texto2)

def retiraDigitos(texto):
    listaDigitos=['0','1','2','3','4','5','6','7','8','9']
    for digito in listaDigitos:
        texto = texto.replace(digito,'')
    return texto