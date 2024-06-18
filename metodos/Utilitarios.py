from unidecode import unidecode
from metodos.lista_chaves import *

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

def ehValorNumerico(valor):
    return valor.isdigit()

def ehValorAlfabetico(valor):
    return valor.isalpha()

def trabalhoEhParaProduzir(dicionarioTrabalhoDesejado):
    return dicionarioTrabalhoDesejado[CHAVE_ESTADO] == CODIGO_PARA_PRODUZIR

def trabalhoEhProduzindo(dicionarioTrabalhoDesejado):
    return dicionarioTrabalhoDesejado[CHAVE_ESTADO] == CODIGO_PRODUZINDO

def trabalhoEhColecaoRecursosAvancados(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'grandecoleçãoderecursosavançados')or
            textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'coletaemmassaderecursosavançados'))

def trabalhoEhColecaoRecursosComuns(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'grandecoleçãoderecursoscomuns')

def trabalhoEhMelhoriaCatalisadorComposto(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadocatalizadoramplificado'))

def trabalhoEhMelhoriaCatalisadorComum(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadocatalizadorcomum'))

def trabalhoEhMelhoriaSubstanciaComposta(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadasubstânciacomposta'))

def trabalhoEhMelhoriaSubstanciaComum(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadasubstânciacomum'))

def trabalhoEhMelhoriaEssenciaComposta(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadaessênciacomposta'))

def trabalhoEhMelhoriaEssenciaComum(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhoriadaessênciacomum'))

def trabalhoEhProducaoLicenca(dicionarioTrabalho):
    return (textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'melhorarlicençacomum')or
            textoEhIgual(dicionarioTrabalho[CHAVE_NOME],'licençadeproduçãodoaprendiz'))


def requisitoRaridadecomumProfissaoEstadoproduzirSatisteito(dicionarioTrabalho, trabalhoListaDesejo):
    return raridadeTrabalhoEhComum(trabalhoListaDesejo)and profissaoEIgual(dicionarioTrabalho, trabalhoListaDesejo)and estadoTrabalhoEParaProduzir(trabalhoListaDesejo)

def estadoTrabalhoEParaProduzir(trabalhoListaDesejo):
    return trabalhoListaDesejo[CHAVE_ESTADO]==CODIGO_PARA_PRODUZIR

def profissaoEIgual(dicionarioTrabalho, trabalhoListaDesejo):
    return textoEhIgual(trabalhoListaDesejo[CHAVE_PROFISSAO],dicionarioTrabalho[CHAVE_PROFISSAO])

def raridadeTrabalhoEhComum(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE],CHAVE_RARIDADE_COMUM)

def raridadeTrabalhoEhMelhorado(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_MELHORADO)

def raridadeTrabalhoEhRaro(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO)

def raridadeTrabalhoEhEspecial(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_ESPECIAL)

def primeiraBusca(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO] == -1

def trabalhoEhProducaoRecursos(dicionarioTrabalhoLista):
    listaProducaoRecurso = [
        'melhorarlicençacomum',
        'licençadeproduçãodoaprendiz',
        'grandecoleçãoderecursoscomuns',
        'grandecoleçãoderecursosavançados',
        'coletaemmassaderecursosavançados',
        'melhoriadaessênciacomum',
        'melhoriadasubstânciacomum',
        'melhoriadocatalizadorcomum',
        'melhoriadaessênciacomposta',
        'melhoriadasubtânciacomposta',
        'melhoriadocatalizadoramplificado',
        'criaresferadoaprendiz','produzindoavarinhademadeira','produzindocabeçadocajadodejade',
        'produzindocabeçadecajadodeônix','criaresferadoneófito','produzindoavarinhadeaço',
        'extraçãodelascas','manipulaçãodelascas','fazermódoaprendiz',
        'preparandolascasdequartzo','manipulaçãodeminériodecobre','fazermódoprincipiante',
        'adquirirtesouradoaprendiz','produzindofioresistente','fazendotecidodelinho',
        'fazendotecidodecetim','comprartesouradoprincipiante','produzindofiogrosso',
        'adquirirfacadoaprendiz','recebendoescamasdaserpente','concluindocouroresistente',
        'adquirirfacadoprincipiante','recebendoescamasdolagarto','curtindocourogrosso',
        'adquirirmarretãodoaprendiz','forjandoplacasdecobre','fazendoplacasdebronze',
        'adquirirmarretãodoprincipiante','forjandoplacasdeferro','fazendoanéisdeaço',
        'adquirirmoldedoaprendiz','extraçãodepepitasdecobre','recebendogemadassombras',
        'adquirirmoldedoprincipiante','extraçãodepepitasdeprata','recebendogemadaluz',
        'adquirirpinçadoaprendiz','extraçãodejadebruta','recebendoenergiainicial',
        'adquirirpinçasdoprincipiante','extraçãodeônixextraordinária','recebendoéterinicial',
        'adquirirfuradordoaprendiz','produzindotecidodelicado','extraçãodesubstânciainstável',
        'adquirirfuradordoprincipiante','produzindotecidodenso','extraçãodesubstânciaestável',
        'recebendofibradebronze','recebendoprata','recebendoinsígniadeestudante',
        'recebendofibradeplatina','recebendoâmbar','recebendodistintivodeaprendiz']
    for recurso in listaProducaoRecurso:
        if textoEhIgual(recurso,dicionarioTrabalhoLista[CHAVE_NOME_PRODUCAO]):
            print(f'{dicionarioTrabalhoLista[CHAVE_NOME]} é recurso!')
            linhaSeparacao()
            return True
    print(f'{dicionarioTrabalhoLista[CHAVE_NOME]} não é recurso!')
    linhaSeparacao()
    return False

def linhaSeparacao():
    print(f'____________________________________________________')