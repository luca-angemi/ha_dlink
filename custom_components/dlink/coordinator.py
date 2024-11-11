"""Coordinator for Dlink."""

import logging
import urllib

from datetime import datetime, timedelta

from pyW215.pyW215 import SmartPlug
from homeassistant.util import dt as dt_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class DlinkCoordinator(DataUpdateCoordinator[dict[str, datetime]]):
    """Class to manage fetching Dlink data."""
    
    config_entry: ConfigEntry
    logging.getLogger("pyW215").setLevel(logging.ERROR)

    def __init__(self, hass: HomeAssistant, smartplug) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=2),
        )
        self.hass = hass
        self.smartplug = smartplug
        self.state: str | None = None
        self.temperature: str = ""
        self.current_consumption: str = ""
        self.total_consumption: str = ""
        self.available = False
        self._n_tried = 0
        self._last_tried: datetime | None = None


    def _update_data(self) -> None:
        """Fetch data from Dlink API via sync functions."""
        if self._last_tried is not None:
            last_try_s = (dt_util.now() - self._last_tried).total_seconds() / 60
            retry_seconds = min(self._n_tried * 2, 10) - last_try_s
            if self._n_tried > 0 and retry_seconds > 0:
                _LOGGER.debug("Waiting %s s to retry", retry_seconds)
                return

        _state = "unknown"

        try:
            self._last_tried = dt_util.now()
            _state = self.smartplug.state
        except urllib.error.HTTPError:
            _LOGGER.error("D-Link connection problem")
        if _state == "unknown":
            self._n_tried += 1
            self.available = False
            _LOGGER.debug("Failed to connect to D-Link switch")
            return

        self.state = _state
        self.available = True

        self.temperature = self.smartplug.temperature
        self.model_name = self.smartplug.model_name
        self.current_consumption = self.smartplug.current_consumption
        self.total_consumption = self.smartplug.total_consumption
        self._n_tried = 0


#        data = {}
#        
#        if self.smartplug.state != 'N/A':
#            data["state"] = self.smartplug.state
#        data["available"] = True
#        if self.smartplug.temperature != 'N/A':
#            data["temperature"] = self.smartplug.temperature
#        if self.smartplug.current_consumption != 'N/A':
#            data["current_consumption"] = self.smartplug.current_consumption
#        if self.smartplug.total_consumption != 'N/A':
#            data["total_consumption"] = self.smartplug.total_consumption
#        data["model_name"] = self.smartplug.model_name
#        return data

    async def _async_update_data(self) -> dict[str, datetime]:
        """Fetch data from Dlink API."""
        return await self.hass.async_add_executor_job(self._update_data)