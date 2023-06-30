"""
Configure visualization elements and instantiate a server
"""

from .model import *  # noqa

import mesa

def update_model(model):
    # Update the model based on the slider value
    model.num_agents = model.model_kwargs["num_agents"].get_value()
    
def circle_portrayal_example(agent):
    if agent is None:
        return

    if(isinstance(agent, InsectAgent)):
        portrayal = {
            "Shape": "mosquito.png",
            "Layer": 0,
            "Scale": 10,
        }
    else:
        portrayal = {
            "Shape": "pessoa.png",
            "Layer": 0,
            "Scale": 10,
        }
    
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 10,10
)
chart_element = mesa.visualization.ChartModule([{"Label": "ExampleProject", "Color": "Pink"}])

model_kwargs = {"num_insects": mesa.visualization.Slider("Quantidade de Insetos na Cidade", 1, 1, 10, 1),
                "num_persons": mesa.visualization.Slider("Quantidade de Pessoas na Cidade", 1, 1, 10, 1), "width": 10, "height": 10}

server = mesa.visualization.ModularServer(
    ExampleProjectModel,
    [canvas_element],
    "ExampleProject",
    model_kwargs
)
