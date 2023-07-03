import mesa

class Dengue(mesa.Agent):
    """
    Classe que identifica o agente Dengue
    Tem os atributos de:
    - unique_id: ID único.
    - dano_vida: quanto de vida cada vírus da Dengue tira do corpo.
    - taxa_reprodução: taxa de reprodução de 0 a 1.
    - dano_dengue: dano que um vírus da dengue dá a um glóbulo branco
    """
    def __init__(self, unique_id, model, dano_vida, taxa_reproducao, dano_dengue):
        super().__init__(unique_id, model)
        self.dano_vida = dano_vida
        self.taxa_reproducao = taxa_reproducao
        self.dano_dengue = dano_dengue

    def step(self):
        """
        A cada step do modelo, analisa as células vizinhas e vazias de cada vírus da dengue.
        A depender da taxa de reprodução, pode adicionar um novo vírus da dengue em uma célula vizinha e vazia.
        Também cada vírus retira a quantidade de vida.
        """
        celulas_vizinhas = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        celulas_vazias = [cell for cell in celulas_vizinhas if self.model.grid.is_cell_empty(cell)]
        if celulas_vazias:
            if self.random.random() < self.taxa_reproducao:
                novo_dengue = Dengue(self.model.next_id(), self.model, self.dano_vida, self.taxa_reproducao, self.dano_dengue)
                self.model.grid.place_agent(novo_dengue, self.random.choice(celulas_vazias))
                self.model.schedule.add(novo_dengue)

        # Retira vida do modelo
        self.model.vida -= self.dano_vida