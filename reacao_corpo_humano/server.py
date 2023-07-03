import mesa
from globulo_branco import GlobuloBranco
from dengue import Dengue
from model import SimulacaoModel

from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer

from config import width, height, num_globulos

class VidaElement(TextElement):
    """
    Retornar a vida para a interface com 2 casas decimais
    """
    def render(self, model):
        return "Vida: {}".format(round(model.vida, 2))

# Shape de cada tipo de agente
def agent_portrayal(agent):
    if isinstance(agent, Dengue):
        return {
            "Shape": "assets/virus.png",
            "scale": 0.9,
            "Layer": 0,
        }
    elif isinstance(agent, GlobuloBranco):
        return {
            "Shape": "assets/globulo-branco.png",
            "scale": 0.9,
            "Layer": 0,
        }
    
# Criação do modelo e grade de visualização
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
vida_element = VidaElement()

# Criação do gráfico
situation_chart = mesa.visualization.ChartModule([
    {"Label": "Glóbulos Brancos", "Color": "blue"},
    {"Label": "Dengues", "Color": "red"}
])

# Parâmetros do que será mostrado na tela
params = {
    "width": width,
    "height": height,
    "num_globulos": num_globulos,
    "dano_vida": mesa.visualization.Slider("Dano de Vida da Dengue", 0.1, 0.0, 1.0, 0.1),
    "adicao_vida": mesa.visualization.Slider("Adição de Vida dos Glóbulos Brancos", 0.1, 0.0, 1.0, 0.1),
    "taxa_rep_dengue": mesa.visualization.Slider("Taxa de reprodução da Dengue", 0.1, 0.0, 1.0, 0.1),
    "taxa_rep_globulos": mesa.visualization.Slider("Taxa de reprodução dos Glóbulos Brancos", 0.1, 0.0, 1.0, 0.1),
    "dano_dengue": mesa.visualization.Slider("Dano da Dengue nos Glóbulos Brancos", 0.1, 0.0, 1.0, 0.1),
    "dano_globulos": mesa.visualization.Slider("Dano dos Glóbulos Brancos na dengue", 0.1, 0.0, 1.0, 0.1),
}

# Configuração do servidor de visualização
server = ModularServer(
    SimulacaoModel,
    [grid, situation_chart, vida_element],
    "Simulação de Dengue no Corpo",
    params
)

server.port = 8521