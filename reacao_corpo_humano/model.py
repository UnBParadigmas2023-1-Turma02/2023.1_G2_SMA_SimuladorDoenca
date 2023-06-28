import mesa
from .agent import Dengue, GlobuloBranco

from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

class SimulacaoModel(mesa.Model):
    def __init__(self, width, height, num_dengue, num_globulos):
        self.num_dengue = num_dengue
        self.num_globulos = num_globulos
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = SimultaneousActivation(self)

        # Inicializar primeiro agente Dengue em uma das pontas
        dengue = Dengue(0, self)
        self.schedule.add(dengue)
        self.grid.place_agent(dengue, (0, 0))

        # Inicializar os demais agentes Dengue ao lado de um agente Dengue existente
        for i in range(1, self.num_dengue):
            neighbor = self.schedule.agents[0]  # Obtém o primeiro agente Dengue
            dengue = Dengue(i, self)
            self.schedule.add(dengue)
            x, y = self.grid.get_neighborhood(neighbor.pos, moore=True, include_center=False)[0]
            self.grid.place_agent(dengue, (x, y))

        # Inicializar agentes Glóbulo Branco
        for i in range(self.num_globulos):
            globulo = GlobuloBranco(i + self.num_dengue, self)
            self.schedule.add(globulo)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(globulo, (x, y))

    def step(self):
        self.schedule.step()