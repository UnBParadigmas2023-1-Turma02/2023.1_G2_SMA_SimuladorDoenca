#coleta informacoes da situacao de cada grupo de pessoas
from mesa import Model

class Status:
    @staticmethod
    def numero_infectados(model):
        return sum
    @staticmethod
    def numero_graves(model):
        return sum
    @staticmethod
    def numero_curados(model):
        return sum
    @staticmethod
    def numero_mortos(model):
        return sum
    @staticmethod
    def mortalidade(model):
        mortos = Status.numero_mortos(model)
        infectados = Status.numero_infectados(model)  
        curados = Status.numero_curados(model)
        return mortos / (mortos + infectados + curados)