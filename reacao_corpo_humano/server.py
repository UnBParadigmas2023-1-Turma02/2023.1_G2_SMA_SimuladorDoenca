import mesa
from .agent import Dengue, GlobuloBranco
from .model import SimulacaoModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

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

width = 10  # Largura da grade
height = 10  # Altura da grade
num_dengue = 5  # Número de agentes Dengue
num_globulos = 10  # Número de agentes Glóbulo Branco

# Criação do modelo e grade de visualização
model = SimulacaoModel(width, height, num_dengue, num_globulos)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

# Configuração do servidor de visualização
server = ModularServer(
    SimulacaoModel,
    [grid],
    "Simulação de Vírus e Glóbulos Brancos",
    {"width": width, "height": height, "num_dengue": num_dengue, "num_globulos": num_globulos}
)