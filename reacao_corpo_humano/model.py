import mesa
from .agent import Dengue, GlobuloBranco

from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

class SimulacaoModel(mesa.Model):
    def __init__(self, width, height, num_dengue, num_globulos, dano_vida, adicao_vida, taxa_rep_dengue, taxa_rep_globulos):
        self.num_dengue = num_dengue
        self.num_globulos = num_globulos
        self.dano_vida = dano_vida
        self.adicao_vida = adicao_vida
        self.taxa_rep_dengue = taxa_rep_dengue
        self.taxa_rep_globulos = taxa_rep_globulos
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = SimultaneousActivation(self)
        self.vida = 50
        self.current_id = 0
        self.initial_dengue_pos = (0, 0)
        self.initial_dengue_created = False

        # Inicializar agentes Glóbulo Branco
        for i in range(self.num_globulos):
            globulo = GlobuloBranco(self.next_id(), self, self.adicao_vida, self.taxa_rep_globulos)
            self.schedule.add(globulo)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(globulo, (x, y))

        self.datacollector = mesa.DataCollector(
            {
                "Dengues": lambda m: self.count_agents(m, Dengue),
                "Glóbulos Brancos": lambda m: self.count_agents(m, GlobuloBranco)
            }
        )


    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        if not self.initial_dengue_created:
            # Inicializar primeiro agente Dengue em uma das pontas
            dengue = Dengue(self.next_id(), self, self.dano_vida, self.taxa_rep_dengue)
            self.schedule.add(dengue)
            self.grid.place_agent(dengue, self.initial_dengue_pos)
            self.initial_dengue_created = True
        else:
            self.schedule.step()
            self.datacollector.collect(self)

        # Verificar quantidade de vida
        if self.vida > 95:
            print("Corpo curado!")
            self.running = False
        elif self.vida <= 0:
            print("Corpo morto!")
            self.running = False

    @staticmethod
    def count_agents(model, agent_type):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                count += 1
        return count