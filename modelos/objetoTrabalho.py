class Trabalho:
    def __init__(self, id = '', nome = '', nomeProducao = '', experiencia = int, profissao = '', raridade = '', nivel = int) -> None:
        self._id = id
        self._nome = nome
        self._nomeProducao = nomeProducao
        self._experiencia = experiencia
        self._profissao = profissao
        self._raridade = raridade
        self._nivel = nivel
        
    def __str__(self) -> str:
        return self._nome