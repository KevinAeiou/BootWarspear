import urllib

def retorna_link(mensagem):
    numero = +5592984591147
    texto = urllib.parse.quote(mensagem)
    return f'https://web.whatsapp.com/send?phone={numero}&text={texto}'