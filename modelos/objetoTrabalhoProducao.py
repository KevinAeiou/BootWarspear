from modelos.objetoTrabalho import Trabalho

class TrabalhoProducao(Trabalho):
    def __init__(self, id = '', trabalhoId='', nome='', nomeProducao='', experiencia=..., profissao='', raridade='', nivel=..., estado = ..., recorrencia = bool, tipo_licenca = '') -> None:
        super().__init__(trabalhoId, nome, nomeProducao, experiencia, profissao, raridade, nivel)
        self._id = id
        self._estado = estado
        self._recorrencia = recorrencia
        self._tipo_licenca = tipo_licenca

    @property
    def estado(self):
        if self._estado == 0:
            return 'Para produzir'
        if self._estado == 1:
            return 'Produzindo'
        if self._estado == 2:
            return 'Concluído'