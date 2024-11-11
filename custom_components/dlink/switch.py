"""Support for D-Link Power Plug Switches."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr
from .const import ATTR_TOTAL_CONSUMPTION, DOMAIN, MANUFACTURER, ATTRIBUTION
from .entity import DLinkEntity
from .coordinator import DlinkCoordinator
from homeassistant.helpers.entity import DeviceInfo, Entity, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
SWITCH_TYPE = SwitchEntityDescription(
    key="switch",
)
from homeassistant.const import ATTR_CONNECTIONS
import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the D-Link Power Plug sensors."""
    coordinator: DlinkCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [SmartPlugSwitch(coordinator, SWITCH_TYPE)]
    async_add_entities(entities)


class SmartPlugSwitch(DLinkEntity, SwitchEntity):
    """Representation of a D-Link Smart Plug switch."""

    _attr_name = None

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.coordinator.state == "ON"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""

        def _turn_on(smartplug) -> None:
            smartplug.state = "ON"

        await self.hass.async_add_executor_job(_turn_on, self.coordinator.smartplug)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""

        def _turn_off(smartplug) -> None:
            smartplug.state = "OFF"

        await self.hass.async_add_executor_job(_turn_off, self.coordinator.smartplug)
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.available
