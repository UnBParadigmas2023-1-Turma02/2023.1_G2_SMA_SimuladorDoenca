from mesa import Agent
import random

class Pessoa(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isInfected = False
        self.timesInfected = 0

    def increase_counter_infected(self):
        if self.timesInfected == 0:
            self.timesInfected += 1
            self.calculate_probability_die(0.15)
        elif self.timesInfected == 1:
            self.timesInfected += 1
            self.calculate_probability_die(0.35)
        elif self.timesInfected == 2:
            self.timesInfected += 1
            self.calculate_probability_die(0.75)
        else:
            ... # vive para sempre ;)

    def calculate_probability_die(self, probability_die):
        if random.random() < probability_die:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

    def is_sting(self):
        self.isInfected = True 
