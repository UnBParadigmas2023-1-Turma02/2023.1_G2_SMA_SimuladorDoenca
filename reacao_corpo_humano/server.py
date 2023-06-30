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
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
vida_element = VidaElement()

situation_chart = mesa.visualization.ChartModule([
    {"Label": "Glóbulos Brancos", "Color": "blue"},
    {"Label": "Dengues", "Color": "red"}
])

params = {
    "width": width,
    "height": height,
    "num_dengue": num_dengue,
    "num_globulos": num_globulos,
    "dano_vida": mesa.visualization.Slider("Dano de Vida da Dengue", 0.1, 0.0, 1.0, 0.1),
    "adicao_vida": mesa.visualization.Slider("Adição de Vida dos Glóbulos Brancos", 0.1, 0.0, 1.0, 0.1),
    "taxa_rep_dengue": mesa.visualization.Slider("Taxa de reprodução da Dengue", 0.1, 0.0, 1.0, 0.1),
    "taxa_rep_globulos": mesa.visualization.Slider("Taxa de reprodução dos Glóbulos Brancos", 0.1, 0.0, 1.0, 0.1),
}

# Configuração do servidor de visualização
server = ModularServer(
    SimulacaoModel,
    [grid, situation_chart, vida_element],
    "Simulação de Dengue no Corpo",
    params
)

server.port = 8521