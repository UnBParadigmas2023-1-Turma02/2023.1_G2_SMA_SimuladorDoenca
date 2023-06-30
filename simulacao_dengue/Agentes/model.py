import mesa
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
        for i in range(self.num_pessoa):
            pessoa = Pessoa(i, self)
            self.schedule.add(pessoa)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pessoa, (x, y))

        # Create mosquito
        for i in range(self.num_mosquito):
            mosquito = Mosquito(i, self)
            self.schedule.add(mosquito)

            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(mosquito, (x, y))

    
    def step(self):
        self.schedule.step()
