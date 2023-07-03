import mesa
import uuid
from pessoa import Pessoa
from mosquito import Mosquito
import random


class ContaminationModel(mesa.Model):

    def _init_(self, width, height, num_pessoa, num_mosquito):
        self.num_pessoa = num_pessoa
        self.num_mosquito = num_mosquito
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.SimultaneousActivation(self)

        # Create persons
        for _ in range(self.num_pessoa):
            pessoa = Pessoa(uuid.uuid1(), self)
            print("Criando pessoa")
            print(pessoa.unique_id)
            self.schedule.add(pessoa)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pessoa, (x, y))

        # Create mosquito
        for _ in range(self.num_mosquito):
            print("Criando mosquito")
            mosquito = Mosquito(uuid.uuid1(), self)
            self.schedule.add(mosquito)

            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(mosquito, (x, y))

         # Coletor de dados para o gráfico
        self.datacollector = mesa.DataCollector(
            {
                "Infectados": lambda m: self.count_agents(m, Pessoa),
                "Não Infectados": lambda m: self.count_agents(m, Pessoa)
            }
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        pessoas = [obj for obj in self.schedule.agents if isinstance(
            obj, Pessoa) and obj.timesInfected < 3]
        if len(pessoas) == 0:
            self.running = False

    @staticmethod
    def count_agents(model, agent_class):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_class) and agent.timesInfected >= 1:
                count += 1
        return count