import mesa
import uuid
from pessoa import Pessoa
from mosquito import Mosquito
import random


class ContaminationModel(mesa.Model):

    def __init__(self, width, height, num_pessoa, num_mosquito):
        self.num_pessoa = num_pessoa
        self.num_mosquito = num_mosquito
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)

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

    
    def step(self):
        self.schedule.step()
