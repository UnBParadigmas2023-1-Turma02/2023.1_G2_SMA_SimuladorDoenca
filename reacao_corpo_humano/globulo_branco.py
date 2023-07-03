import mesa

class GlobuloBranco(mesa.Agent):
    """
    Classe que identifica o agente Glóbulo Branco
    Tem os atributos de:
    - unique_id: ID único.
    - adicao_vida: quanto de vida cada glóbulo branco adiciona ao corpo.
    - taxa_reprodução: taxa de reprodução de 0 a 1.
    - dano_globulos: dano que um glóbulo branco dá a um vírus da dengue
    """
    def __init__(self, unique_id, model, adicao_vida, taxa_reproducao, dano_globulos):
        super().__init__(unique_id, model)
        self.adicao_vida = adicao_vida
        self.taxa_reproducao = taxa_reproducao
        self.dano_globulos = dano_globulos

    def step(self):
        """
        A cada step do modelo, analisa as células vizinhas e vazias de cada globulo branco.
        A depender da taxa de reprodução, pode adicionar um novo globulo branco em uma célula vizinha e vazia.
        Também cada glóbulo dá a quantidade de vida.
        """
        celulas_vizinhas = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        celulas_vazias = [cell for cell in celulas_vizinhas if self.model.grid.is_cell_empty(cell)]
        if celulas_vazias:
            if self.random.random() < self.taxa_reproducao:
                novo_globuloBranco = GlobuloBranco(self.model.next_id(), self.model, self.adicao_vida, self.taxa_reproducao, self.dano_globulos)
                self.model.grid.place_agent(novo_globuloBranco, self.random.choice(celulas_vazias))
                self.model.schedule.add(novo_globuloBranco)

        # Adiciona vida ao modelo
        self.model.vida += self.adicao_vida