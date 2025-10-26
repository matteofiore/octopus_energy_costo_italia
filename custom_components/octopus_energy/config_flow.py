import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Optional("name", default="Octopus Energy"): str,
    vol.Optional("update_interval"): vol.All(int, vol.Range(min=1, max=1440)),
})

class OctopusEnergyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Octopus Energy."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Se l'utente non inserisce update_interval, lo rimuoviamo
            update_interval = user_input.get("update_interval")
            data = {
                "name": user_input.get("name", "Octopus Energy"),
            }
            if update_interval:
                data["update_interval"] = update_interval

            return self.async_create_entry(
                title=data["name"],
                data=data,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )