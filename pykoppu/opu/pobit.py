"""
Pobit module.
"""

class Pobit:
    """
    Represents a Probabilistic Bit (Pobit).

    Attributes:
        index (int): The index of the pobit.
        label (str): The label of the pobit.
    """

    def __init__(self, index: int, label: str):
        """
        Initializes the Pobit.

        Args:
            index (int): The index of the pobit.
            label (str): The label of the pobit.
        """
        self.index = index
        self.label = label
