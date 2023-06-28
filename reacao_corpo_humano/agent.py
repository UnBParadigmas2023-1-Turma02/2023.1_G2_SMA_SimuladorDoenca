import mesa

class Dengue(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Atributos específicos do agente Dengue
        self.taxa_reproducao = 0.1  # Taxa de reprodução
        self.dano_vida = 1  # Quantidade de "vida" removida a cada etapa

    def step(self):
        print('Dengue')
        # Lógica de movimento e interação dos agentes Dengue
        # Implemente aqui o comportamento dos vírus, como movimento e reprodução
        # Considere interações com glóbulos brancos ou outros agentes do ambiente

class GlobuloBranco(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Atributos específicos do agente Glóbulo Branco
        self.velocidade_movimento = 1  # Velocidade de movimento
        self.adicao_vida = 1  # Quantidade de "vida" fornecida ao ser humano

    def step(self):
        print('Globulo Branco')
        # Lógica de movimento e interação dos agentes Glóbulo Branco
        # Implemente aqui o comportamento dos glóbulos brancos, como movimento em direção aos vírus
        # Considere interações com vírus ou outros agentes do ambiente