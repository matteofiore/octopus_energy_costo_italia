from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .Octopus_energy_price_italy.const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Octopus Energy component via configuration.yaml (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Octopus Energy from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Octopus Energy config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])