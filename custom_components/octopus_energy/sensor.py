from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from datetime import timedelta
import subprocess
from bs4 import BeautifulSoup
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Create sensors for Luce and Gas with user-defined interval."""
    interval = entry.data.get("update_interval", 15)
    async_add_entities([
        OctopusLuceSensor(hass, interval),
        OctopusGasSensor(hass, interval)
    ])

class OctopusLuceSensor(SensorEntity):
    def __init__(self, hass, update_interval):
        self.hass = hass
        self._attr_name = "Octopus Energy Luce Monoraria"
        self._attr_native_value = None
        self._update_interval = update_interval

    @property
    def native_value(self):
        return self._attr_native_value

    @property
    def should_poll(self):
        return True

    @property
    def scan_interval(self):
        return timedelta(minutes=self._update_interval)

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
    def __init__(self, hass, update_interval):
        self.hass = hass
        self._attr_name = "Octopus Energy Gas"
        self._attr_native_value = None
        self._update_interval = update_interval

    @property
    def native_value(self):
        return self._attr_native_value

    @property
    def should_poll(self):
        return True

    @property
    def scan_interval(self):
        return timedelta(minutes=self._update_interval)

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