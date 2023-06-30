from mesa import Agent

class Pessoa(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isInfected = False
        self.timesInfected = 0

    def increase_counter_infected(self):
        if self.timesInfected < 3:
            self.timesInfected += 1
        else:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

    def is_sting(self):
        self.isInfected = True 

