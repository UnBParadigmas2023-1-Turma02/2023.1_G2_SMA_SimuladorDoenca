import mesa
from .agent import Dengue, GlobuloBranco
from .model import SimulacaoModel

from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer

class VidaElement(TextElement):
    def render(self, model):
        return "Vida: {}".format(round(model.vida, 2))

def agent_portrayal(agent):
    if isinstance(agent, Dengue):
        return {
            "Shape": "circle",
            "Color": "red",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5
        }
    elif isinstance(agent, GlobuloBranco):
        return {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5
        }

width = 20  # Largura da grade
height = 20  # Altura da grade
num_dengue = 5  # Número de agentes Dengue
num_globulos = 10  # Número de agentes Glóbulo Branco

# Criação do modelo e grade de visualização
model = SimulacaoModel(width, height, num_dengue, num_globulos)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
vida_element = VidaElement()

params = {
    "width": width,
    "height": height,
    "num_dengue": num_dengue,
    "num_globulos": num_globulos,
}

# Configuração do servidor de visualização
server = ModularServer(
    SimulacaoModel,
    [grid, vida_element],
    "Simulação de Vírus e Glóbulos Brancos",
    params
)

server.port = 8521