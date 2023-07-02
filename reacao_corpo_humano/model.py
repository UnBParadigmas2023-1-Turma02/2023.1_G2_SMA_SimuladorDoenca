import mesa
import random
from .agent import Dengue, GlobuloBranco

from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

class SimulacaoModel(mesa.Model):
    def __init__(self, width, height, num_dengue, num_globulos, dano_vida, adicao_vida, taxa_rep_dengue, taxa_rep_globulos, dano_dengue, dano_globulos):
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
        self.dano_dengue = dano_dengue
        self.dano_globulos = dano_globulos

        # Inicializar agentes Glóbulo Branco
        for i in range(self.num_globulos):
            globulo = GlobuloBranco(self.next_id(), self, self.adicao_vida, self.taxa_rep_globulos, self.dano_globulos)
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
    

    def is_neighbor(self, dengue_agent, globulo_agent):
        dengue_pos = dengue_agent.pos
        globulo_pos = globulo_agent.pos

        # Verificar se as posições são adjacentes (incluindo diagonais)
        if dengue_pos is not None and globulo_pos is not None:
            if abs(dengue_pos[0] - globulo_pos[0]) <= 1 and abs(dengue_pos[1] - globulo_pos[1]) <= 1:
                return True

        return False


    def encounter(self):
        dengues = self.count_agents(self, Dengue)
        globulos = self.count_agents(self, GlobuloBranco)

        # Verificar se há dengue e glóbulos brancos no grid
        if dengues > 0 and globulos > 0:
            dengue_agents = [agent for agent in self.schedule.agents if isinstance(agent, Dengue)]
            globulo_agents = [agent for agent in self.schedule.agents if isinstance(agent, GlobuloBranco)]

            # Calcular o dano total de cada tipo de célula
            total_dano_dengue = sum(agent.dano_dengue for agent in dengue_agents)
            total_dano_globulos = sum(agent.dano_globulos for agent in globulo_agents)

            # Verificar qual célula tem o menor dano
            if total_dano_dengue > total_dano_globulos:
                # Remover o glóbulo branco com menor dano
                min_dano_globulo = min(globulo_agents, key=lambda agent: agent.dano_globulos)
                if min_dano_globulo is not None:
                    self.schedule.remove(min_dano_globulo)
                    self.grid.remove_agent(min_dano_globulo)

                    # O agente dengue ocupa o lugar do glóbulo branco
                    dengue = dengue_agents[0]
                    if min_dano_globulo.pos is not None:
                        valid_neighbors = self.grid.get_neighborhood(min_dano_globulo.pos, moore=False, include_center=False)
                        if valid_neighbors:
                            new_pos = random.choice(valid_neighbors)
                            self.grid.move_agent(dengue, new_pos)

            elif total_dano_globulos >= total_dano_dengue:
                # Remover a dengue com menor dano
                min_dano_dengue = min(dengue_agents, key=lambda agent: agent.dano_dengue)
                if min_dano_dengue is not None:
                    self.schedule.remove(min_dano_dengue)
                    self.grid.remove_agent(min_dano_dengue)

                    # O glóbulo branco ocupa o lugar da dengue
                    globulo = globulo_agents[0]
                    if min_dano_dengue.pos is not None:
                        valid_neighbors = self.grid.get_neighborhood(min_dano_dengue.pos, moore=False, include_center=False)
                        if valid_neighbors:
                            new_pos = random.choice(valid_neighbors)
                            self.grid.move_agent(globulo, new_pos)


    def step(self):
        if not self.initial_dengue_created:
            # Inicializar primeiro agente Dengue em uma das pontas
            dengue = Dengue(self.next_id(), self, self.dano_vida, self.taxa_rep_dengue, self.dano_dengue)
            self.schedule.add(dengue)
            self.grid.place_agent(dengue, self.initial_dengue_pos)
            self.initial_dengue_created = True
        else:
            self.schedule.step()
            self.datacollector.collect(self)
            dengue_agents = [agent for agent in self.schedule.agents if isinstance(agent, Dengue)]
            globulo_agents = [agent for agent in self.schedule.agents if isinstance(agent, GlobuloBranco)]

            for dengue in dengue_agents:
                for globulo in globulo_agents:
                    if self.is_neighbor(dengue, globulo):
                        self.encounter()

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