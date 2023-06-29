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
        self.vida = 50
        self.current_id = 0
        self.initial_dengue_pos = (0, 0)
        self.initial_dengue_created = False

        # Inicializar agentes Glóbulo Branco
        for i in range(self.num_globulos):
            globulo = GlobuloBranco(self.next_id(), self)
            self.schedule.add(globulo)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(globulo, (x, y))

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        if not self.initial_dengue_created:
            # Inicializar primeiro agente Dengue em uma das pontas
            dengue = Dengue(self.next_id(), self)
            self.schedule.add(dengue)
            self.grid.place_agent(dengue, self.initial_dengue_pos)
            self.initial_dengue_created = True
        else:
            self.schedule.step()

        # Verificar quantidade de vida
        if self.vida > 70:
            print("Corpo curado!")
            self.running = False
        elif self.vida < 30:
            print("Corpo morto!")
            self.running = False
