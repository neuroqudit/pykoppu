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
        Loads biological specifications for the Critical Regime.

        Returns:
            dict: A dictionary containing the physical parameters.
        """
        return {
            "R": 50 * 1e6,        # 50 Mohm
            "tau": 20 * 1e-3,     # 20 ms
            "v_rest": -70 * 1e-3, # -70 mV (El)
            "v_reset": -70 * 1e-3,# -70 mV (Vr)
            "v_threshold": -50 * 1e-3, # -50 mV (Vt)
            "i_offset": 0.36 * 1e-9,   # 0.36 nA
            "sigma": 2.0 * 1e-3,       # 2.0 mV
            "refractory": 5 * 1e-3     # 5 ms
        }
