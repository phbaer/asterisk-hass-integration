from asterisk.ami import AMIClient

from .const import CLIENT, DOMAIN


class AsteriskDeviceEntity:
    """Base entity for Asterisk devices."""

    def __init__(self, hass, entry, device):
        """Initialize the sensor."""
        self._hass = hass
        self._device = device
        self._entry = entry
        self._unique_id_prefix = f"{entry.entry_id}_{device['extension']}"
        self._ami_client: AMIClient = hass.data[DOMAIN][entry.entry_id][CLIENT]
        self._name: str
        self._unique_id: str

    def _schedule_update_ha_state(self):
        """Schedule a state update for this entity.
        
        This is a helper method to properly update entity state from
        synchronous event callbacks. It uses async_write_ha_state() which
        is the modern way to update entity state in Home Assistant.
        """
        if hasattr(self, "async_write_ha_state"):
            # Use modern async_write_ha_state if available
            self.async_write_ha_state()
        elif hasattr(self, "schedule_update_ha_state"):
            # Fallback to legacy method for older Home Assistant versions
            self.schedule_update_ha_state()

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._unique_id_prefix)},
            "name": f"{self._device['tech']}/{self._device['extension']}",
            "manufacturer": "Asterisk",
            "model": self._device["tech"],
            "via_device": (DOMAIN, f"{self._entry.entry_id}_server"),
        }

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id
