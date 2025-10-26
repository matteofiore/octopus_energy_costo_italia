from homeassistant.helpers.entity import Entity
import subprocess
from bs4 import BeautifulSoup
import logging

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([OctopusLuceSensor(), OctopusGasSensor()])

class OctopusLuceSensor(Entity):
    def __init__(self):
        self._state = None

    def update(self):
        self._state = self.get_price('kWh')

    def get_price(self, unit):
        try:
            result = subprocess.run(['curl', '-k', 'https://octopusenergy.it/le-nostre-tariffe'], capture_output=True, text=True)
            html_content = result.stdout
            soup = BeautifulSoup(html_content, 'html.parser')
            for label in soup.find_all(string=lambda t: t and 'Materia prima' in t):
                prezzo_tag = label.find_next('p')
                if prezzo_tag:
                    prezzo = prezzo_tag.get_text(strip=True)
                    if unit in prezzo:
                        return prezzo
            return None
        except Exception as e:
            _LOGGER.error(f"Error fetching luce price: {e}")
            return None

    @property
    def name(self):
        return "Octopus Luce Monoraria"

    @property
    def state(self):
        return self._state

class OctopusGasSensor(Entity):
    def __init__(self):
        self._state = None

    def update(self):
        self._state = self.get_price('Smc')

    def get_price(self, unit):
        try:
            result = subprocess.run(['curl', '-k', 'https://octopusenergy.it/le-nostre-tariffe'], capture_output=True, text=True)
            html_content = result.stdout
            soup = BeautifulSoup(html_content, 'html.parser')
            for label in soup.find_all(string=lambda t: t and 'Materia prima' in t):
                prezzo_tag = label.find_next('p')
                if prezzo_tag:
                    prezzo = prezzo_tag.get_text(strip=True)
                    if unit in prezzo:
                        return prezzo
            return None
        except Exception as e:
            _LOGGER.error(f"Error fetching gas price: {e}")
            return None

    @property
    def name(self):
        return "Octopus Gas"

    @property
    def state(self):
        return self._state
