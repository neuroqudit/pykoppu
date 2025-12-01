"""
Electrophysiology Package Initialization.
"""

from .base import ElectrophysiologyDriver
from .brian2 import Brian2Driver

from typing import Any, Optional

def connect(driver_name: str = "brian2", opu: Optional[Any] = None, **kwargs) -> ElectrophysiologyDriver:
    """
    Factory function to connect to a driver.
    
    Args:
        driver_name (str): Name of the driver ("brian2").
        opu (OPU): The OPU instance.
        **kwargs: Arguments for the driver constructor.
        
    Returns:
        ElectrophysiologyDriver: The connected driver.
    """
    if driver_name == "brian2":
        from ..opu.device import OPU
        if opu is None:
            opu = kwargs.get("opu", OPU())
        driver = Brian2Driver(opu=opu)
        driver.connect()
        return driver
    else:
        raise ValueError(f"Unknown driver: {driver_name}")

__all__ = ["ElectrophysiologyDriver", "Brian2Driver", "connect"]
