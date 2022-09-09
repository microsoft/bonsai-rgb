from sim.color_model import ColorModel
from typing import NamedTuple, Dict, Any

class SimulatorModel:
    """
    Manages the ColorModel that represents the simulation for this sample.
    Implements the reset and step methods required for a Bonsai simulator.
    """

    def __init__(self):
        """ Perform global initialization here if needed before running episodes. """
        pass

    def reset(self, config) -> Dict[str, Any]:
        """ Reset any state from the previous episode and get ready to start a new episode. """
        self.color = ColorModel(config)
        return self.color.state

    def step(self, action) -> Dict[str, Any]:
        """ Apply the specified action and perform one simulation step. """
        self.color.color_step(action)
        # If 'sim_halted' is set to True, that indicates that the simulator is unable to continue and
        # the episode will be discarded. This simulator sets it to False because it can always continue.
        return self.color.state
