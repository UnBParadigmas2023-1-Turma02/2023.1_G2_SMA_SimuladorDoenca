from mesa import Agent
import random


class Pessoa(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isInfected = False
        self.timesInfected = 0
        self.infection_duration = 5
        self.infected_timer = 0

    def increase_counter_infected(self) -> None:
        match self.timesInfected:
            case 0:
                self.timesInfected += 1
                self.calculate_probability_die(0.15)
            case 1:
                self.timesInfected += 1
                self.calculate_probability_die(0.35)
            case 2:
                self.timesInfected += 1
                self.calculate_probability_die(0.75)
            case _:
                ...  # vive para sempre ;)

    def calculate_probability_die(self, probability_die) -> None:
        if random.random() < probability_die:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

    def is_sting(self) -> None:
        self.isInfected = True
        self.infected_timer = self.infection_duration

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self) -> None:
        if self.isInfected:
            if self.infected_timer > 0:
                self.infected_timer -= 1
            else:
                self.isInfected = False

        self.move()
