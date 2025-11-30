"""
Electrophysiology module.
"""
from .brian2 import Brian2Driver

def connect(driver_type: str, opu):
    """
    Factory method to connect to a driver.

    Args:
        driver_type (str): The type of driver to connect to ("brian2").
        opu (OPU): The OPU instance.

    Returns:
        BaseDriver: The driver instance.
    """
    if driver_type == "brian2":
        return Brian2Driver(opu)
    return None
