import mesa
import random
from globulo_branco import GlobuloBranco
from dengue import Dengue

from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

from config import vida

class SimulacaoModel(mesa.Model):
    """
    Classe que implementa o modelo de Simulação.
    Atributos:
    - width: comprimento do grid
    - height: altura do grid
    - num_globulos: quantidade inicial de globulos brancos
    - dano_vida: dano de vida dos vírus
    - adicao_vida: adicao de vida dos globulos
    - taxa_rep_dengue: taxa de reprodução dos vírus
    - taxa_rep_globulos: taxa de reprodução dos globulos
    - dano_dengue: dano de cada vírus em globulos brancos
    - dano_globulos: dano de cada globulo branco em vírus da dengue.
    """
    def __init__(self, width, height, num_globulos, dano_vida, adicao_vida, taxa_rep_dengue, taxa_rep_globulos, dano_dengue, dano_globulos):
        self.num_globulos = num_globulos
        self.dano_vida = dano_vida
        self.adicao_vida = adicao_vida
        self.taxa_rep_dengue = taxa_rep_dengue
        self.taxa_rep_globulos = taxa_rep_globulos
        self.dano_dengue = dano_dengue
        self.dano_globulos = dano_globulos

        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = SimultaneousActivation(self)

        # Quantidade de vida inicial
        self.vida = vida

        # ID inicial
        self.current_id = 0

        # Inicializar agentes Glóbulo Branco (forma aleatoria no grid)
        for _ in range(self.num_globulos):
            globulo = GlobuloBranco(self.next_id(), self, self.adicao_vida, self.taxa_rep_globulos, self.dano_globulos)
            self.schedule.add(globulo)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(globulo, (x, y))

        # Inicializar agente da dengue (no canto do grid)
        dengue = Dengue(self.next_id(), self, self.dano_vida, self.taxa_rep_dengue, self.dano_dengue)
        self.schedule.add(dengue)
        self.grid.place_agent(dengue, (0, 0))

        # Coletor de dados para o gráfico
        self.datacollector = mesa.DataCollector(
            {
                "Dengues": lambda m: self.count_agents(m, Dengue),
                "Glóbulos Brancos": lambda m: self.count_agents(m, GlobuloBranco)
            }
        )


    def next_id(self):
        """
        Adiciona mais um ao valor do ID do agente a ser colocado no Grid
        """
        self.current_id += 1
        return self.current_id
    

    def is_neighbor(self, dengue_agent, globulo_agent):
        """
        Verifica se um agente da dengue e de globulo branco sao vizinhos
        """
        dengue_pos = dengue_agent.pos
        globulo_pos = globulo_agent.pos

        # Verificar se as posições são adjacentes (incluindo diagonais)
        if dengue_pos is not None and globulo_pos is not None:
            if abs(dengue_pos[0] - globulo_pos[0]) <= 1 and abs(dengue_pos[1] - globulo_pos[1]) <= 1:
                return True

        return False


    def encounter(self):
        """
        Lógica de interação entre vírus da Dengue e Globulos Brancos (embate entre eles)
        """
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

            # Verificar qual célula tem o menor dano
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
        """
        Realiza cada step:
        - Coleta dados
        - Faz a interação de 'embate' entre dengue e globulos brancos
        - Verifica a quantidade de vida, podendo parar se curou o corpo ou morreu
        """
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
        """
        Conta quantos agente de uma instância (dengue e globulos brancos) existem
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                count += 1
        return count