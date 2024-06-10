from modelos.objetoTrabalho import Trabalho

class TrabalhoProducao(Trabalho):
    def __init__(self, id = '', trabalhoId='', nome='', nomeProducao='', experiencia=..., profissao='', raridade='', nivel=..., estado = ..., recorrencia = bool, tipo_licenca = '') -> None:
        super().__init__(trabalhoId, nome, nomeProducao, experiencia, profissao, raridade, nivel)
        self._id = id
        self._estado = estado
        self._recorrencia = recorrencia
        self._tipo_licenca = tipo_licenca