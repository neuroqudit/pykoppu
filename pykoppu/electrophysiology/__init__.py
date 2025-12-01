"""
Electrophysiology Package Initialization.
"""

from .base import ElectrophysiologyDriver
from .brian2 import Brian2Driver

def connect(driver_name: str = "brian2", **kwargs) -> ElectrophysiologyDriver:
    """
    Factory function to connect to a driver.
    
    Args:
        driver_name (str): Name of the driver ("brian2").
        **kwargs: Arguments for the driver constructor.
        
    Returns:
        ElectrophysiologyDriver: The connected driver.
    """
    if driver_name == "brian2":
        from ..opu.device import OPU
        opu = kwargs.get("opu", OPU())
        driver = Brian2Driver(opu=opu)
        driver.connect()
        return driver
    else:
        raise ValueError(f"Unknown driver: {driver_name}")

__all__ = ["ElectrophysiologyDriver", "Brian2Driver", "connect"]
