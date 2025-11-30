"""
Device module for OPU.
"""

class OPU:
    """
    Represents an Organoid Processing Unit.

    Attributes:
        capacity (int): The capacity of the OPU.
        neuron_model (dict): The neuron model configuration.
    """

    def __init__(self, capacity: int, neuron_model: dict):
        """
        Initializes the OPU.

        Args:
            capacity (int): The capacity of the OPU.
            neuron_model (dict): The neuron model configuration.
        """
        self.capacity = capacity
        self.neuron_model = neuron_model

    def _load_bio_specs(self):
        """
        Loads biological specifications.
        """
        pass
