import model
import mosquito

import mesa


def getColorPerson(agent):
    colors = ["green", "yellow", "orange", "red"]
    if (not agent.isDead) and agent.isInfected:
        return "yellow"
    elif agent.isDead:
        return "black"
    else:
        return colors[agent.timesInfected]


def getPortrayalPerson(agent):
    if agent.isDead:
        return {
            "Shape": "cruz.png",
            "Layer": 0,
            "scale": .5,
            "id": f"Pessoa {agent.unique_id}"
        }

    return {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": getColorPerson(agent),
        "r": 0.5,
        "nr. infected": agent.timesInfected,
        "id": f"Pessoa {agent.unique_id}"

    }


def circle_portrayal_example(agent):
    if agent is None:
        return

    if (isinstance(agent, mosquito.Mosquito)):
        portrayal = {
            "Shape": "dengue.png",
            "Layer": 0,
            "scale": 1,
            "id": f"Mosquito {agent.unique_id}"
        }
    else:
        portrayal = getPortrayalPerson(agent)

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 20, 20
)

chart_element = mesa.visualization.ChartModule(
    [{"Label": "Contaminação - Dengue", "Color": "Pink"}])

model_kwargs = {"num_mosquito": mesa.visualization.Slider("Quantidade de Insetos na Cidade", 1, 1, 20, 1),
                "num_pessoa": mesa.visualization.Slider("Quantidade de Pessoas na Cidade", 1, 1, 100, 1),
                "width": 20,
                "height": 20}

server = mesa.visualization.ModularServer(
    model.ContaminationModel,
    [canvas_element],
    "Contaminação - Dengue",
    model_kwargs
)
