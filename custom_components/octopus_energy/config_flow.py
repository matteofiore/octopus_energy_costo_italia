import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

# Schema per il form di configurazione
STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Optional("name", default="Octopus Energy"): str,
})

class OctopusEnergyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestione del Config Flow per Octopus Energy."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Step iniziale per la configurazione dall’UI."""
        errors = {}

        if user_input is not None:
            # Qui puoi salvare eventuali dati o token se servono
            return self.async_create_entry(
                title=user_input.get("name", "Octopus Energy"),
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
