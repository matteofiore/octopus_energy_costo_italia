from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
import functools
import subprocess
from bs4 import BeautifulSoup
import logging
from datetime import timedelta

SCAN_INTERVAL = timedelta(minutes=15)  # aggiorna ogni 15 minuti

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Create two sensors: one for Luce Monoraria, one for Gas."""
    async_add_entities([OctopusLuceSensor(hass), OctopusGasSensor(hass)])

class OctopusLuceSensor(SensorEntity):
    def __init__(self, hass):
        self.hass = hass
        self._attr_name = "Octopus Energy Luce Monoraria"
        self._attr_native_value = None

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        price = await self.hass.async_add_executor_job(self._fetch_price, 'kWh')
        self._attr_native_value = price

    def _fetch_price(self, unit):
        try:
            result = subprocess.run(['curl', '-k', 'https://octopusenergy.it/le-nostre-tariffe'],
                                    capture_output=True, text=True)
            soup = BeautifulSoup(result.stdout, 'html.parser')
            for label in soup.find_all(string=lambda t: t and 'Materia prima' in t):
                price_tag = label.find_next('p')
                if price_tag:
                    price = price_tag.get_text(strip=True)
                    if unit in price:
                        return price
        except Exception as e:
            _LOGGER.error(f"Error fetching Luce price: {e}")
        return None

class OctopusGasSensor(SensorEntity):
    def __init__(self, hass):
        self.hass = hass
        self._attr_name = "Octopus Energy Gas"
        self._attr_native_value = None

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        price = await self.hass.async_add_executor_job(self._fetch_price, 'Smc')
        self._attr_native_value = price

    def _fetch_price(self, unit):
        try:
            result = subprocess.run(['curl', '-k', 'https://octopusenergy.it/le-nostre-tariffe'],
                                    capture_output=True, text=True)
            soup = BeautifulSoup(result.stdout, 'html.parser')
            for label in soup.find_all(string=lambda t: t and 'Materia prima' in t):
                price_tag = label.find_next('p')
                if price_tag:
                    price = price_tag.get_text(strip=True)
                    if unit in price:
                        return price
        except Exception as e:
            _LOGGER.error(f"Error fetching Gas price: {e}")
        return None