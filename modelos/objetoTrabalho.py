class Trabalho:
    listaTrabalhos = []
    def __init__(self, id = '', nome = '', nomeProducao = '', experiencia = int, profissao = '', raridade = '', nivel = int) -> None:
        self._id = id
        self._nome = nome
        self._nomeProducao = nomeProducao
        self._experiencia = experiencia
        self._profissao = profissao
        self._raridade = raridade
        self._nivel = nivel
        Trabalho.listaTrabalhos.append(self)
        
    def __str__(self) -> str:
        return self._nome
    
    @classmethod
    def mostraListaTrabalhos(cls):
        print(f'{"Nome".ljust(45)} | {"XP".ljust(5)} | {"Profissão".ljust(22)} | {"Raridade".ljust(9)} | Nível')
        for trabalho in cls.listaTrabalhos:
            print(f'{trabalho._nome.ljust(45)} | {str(trabalho._experiencia).ljust(5)} | {trabalho._profissao.ljust(22)} | {trabalho._raridade.ljust(9)} | {trabalho._nivel}')