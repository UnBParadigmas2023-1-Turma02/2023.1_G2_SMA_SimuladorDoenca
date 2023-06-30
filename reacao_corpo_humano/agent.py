import mesa

class Dengue(mesa.Agent):
    def __init__(self, unique_id, model, dano_vida, taxa_reproducao):
        super().__init__(unique_id, model)
        # Atributos específicos do agente Dengue
        self.dano_vida = dano_vida  # Quantidade de "vida" removida a cada etapa
        self.taxa_reproducao = taxa_reproducao

    def step(self):
        neighbor_cells = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        empty_cells = [cell for cell in neighbor_cells if self.model.grid.is_cell_empty(cell)]
        if empty_cells and self.random.random() < self.taxa_reproducao:
            offspring_pos = self.random.choice(empty_cells)
            offspring = Dengue(self.model.next_id(), self.model, self.dano_vida, self.taxa_reproducao)
            self.model.grid.place_agent(offspring, offspring_pos)
            self.model.schedule.add(offspring)

        self.model.vida -= self.dano_vida

class GlobuloBranco(mesa.Agent):
    def __init__(self, unique_id, model, adicao_vida, taxa_reproducao):
        super().__init__(unique_id, model)
        # Atributos específicos do agente Glóbulo Branco
        self.adicao_vida = adicao_vida  # Quantidade de "vida" fornecida ao ser humano
        self.taxa_reproducao = taxa_reproducao

    def step(self):
        neighbor_cells = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        empty_cells = [cell for cell in neighbor_cells if self.model.grid.is_cell_empty(cell)]
        if empty_cells and self.random.random() < self.taxa_reproducao:
            offspring_pos = self.random.choice(empty_cells)
            offspring = GlobuloBranco(self.model.next_id(), self.model, self.adicao_vida, self.taxa_reproducao)
            self.model.grid.place_agent(offspring, offspring_pos)
            self.model.schedule.add(offspring)

        self.model.vida += self.adicao_vida