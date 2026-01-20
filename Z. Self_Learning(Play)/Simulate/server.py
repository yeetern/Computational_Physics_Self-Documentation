from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from model import EcoModel, Params, Prey, Predator, Grass


def portrayal(agent):
    if agent is None:
        return

    if isinstance(agent, Grass):
        # show grass only when grown
        if not agent.grown:
            return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0, "Color": "#EEEEEE"}
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0, "Color": "#A8E6A3"}

    if isinstance(agent, Prey):
        return {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 2, "Color": "#2ECC71"}

    if isinstance(agent, Predator):
        return {"Shape": "circle", "r": 0.6, "Filled": "true", "Layer": 3, "Color": "#E74C3C"}


def make_server():
    p = Params()

    grid = CanvasGrid(portrayal, p.width, p.height, 700, 700)
    chart = ChartModule(
        [{"Label": "Prey", "Color": "Green"},
         {"Label": "Predator", "Color": "Red"},
         {"Label": "GrassCover", "Color": "Black"}]
    )

    server = ModularServer(
        EcoModel,
        [grid, chart],
        "Eco ABM (Prey-Predator-Grass)",
        {"p": p}
    )
    server.port = 8522
    return server
