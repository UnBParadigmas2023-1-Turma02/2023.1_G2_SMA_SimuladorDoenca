import random
from mesa import Agent
from pessoa import Pessoa


class Mosquito(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def sting(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        persons = [obj for obj in cellmates if isinstance(obj, Pessoa)]
        if len(persons) > 0:
            person = random.choice(persons)
            if not person.isInfected and person.timesInfected < 3:
                person.is_sting()
                person.increase_counter_infected()

    def step(self):
        self.move()
        self.sting()
