"""Entity representing a D-Link Power Plug device."""

from __future__ import annotations

from homeassistant.const import ATTR_CONNECTIONS
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, MANUFACTURER
from .coordinator import DlinkCoordinator


class DLinkEntity(CoordinatorEntity[DlinkCoordinator]):
    """Representation of a D-Link Smart Plug entity."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DlinkCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer=MANUFACTURER,
            model=coordinator.model_name,
            name=coordinator.config_entry.title,
        )
        if coordinator.config_entry.unique_id:
            self._attr_device_info[ATTR_CONNECTIONS] = {
                (dr.CONNECTION_NETWORK_MAC, coordinator.config_entry.unique_id)
            }