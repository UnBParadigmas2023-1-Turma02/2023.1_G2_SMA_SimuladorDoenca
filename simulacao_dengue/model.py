
import mesa
import uuid
from pessoa import Pessoa
from mosquito import Mosquito
import random

def count_health(model):
    count = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Pessoa) and agent.timesInfected == 0:
            count += 1
    return count
    
def count_light(model):
    count = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Pessoa) and agent.timesInfected == 1:
            count += 1
    return count

def count_moderate(model):
    count = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Pessoa) and agent.timesInfected ==2:
            count += 1
    return count

def count_critical(model):
    count = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Pessoa) and agent.timesInfected ==3:
            count += 1
    return count




class ContaminationModel(mesa.Model):

    def __init__(self, width, height, num_pessoa, num_mosquito):
        self.num_pessoa = num_pessoa
        self.num_mosquito = num_mosquito
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.SimultaneousActivation(self)
    
    
        # Coletor de dados para o gráfico
        self.datacollector = mesa.DataCollector(
            model_reporters={"Não infectados": count_health, "Infectados 1 vez": count_light, "Infectados 2 vezes": count_moderate, "Infectados 3 vezes": count_critical}
        )
        
        
        # Create persons
        for _ in range(self.num_pessoa):
            pessoa = Pessoa(uuid.uuid1(), self)
            self.schedule.add(pessoa)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pessoa, (x, y))

        # Create mosquito
        for _ in range(self.num_mosquito):
            mosquito = Mosquito(uuid.uuid1(), self)
            self.schedule.add(mosquito)

            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(mosquito, (x, y))
        
            
        

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        pessoas = [obj for obj in self.schedule.agents if isinstance(
            obj, Pessoa) and obj.timesInfected < 3]
        if len(pessoas) == 0:
            self.running = False
    
    