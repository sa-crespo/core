"""The Crespo integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "crespo"


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Crespo integration."""
    hass.states.set("crespo.world", "Sebastian")

    # Return boolean to indicate that initialization was successful.
    return True
