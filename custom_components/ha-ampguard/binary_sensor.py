"""Support for AmpGuard binary sensors."""

from dataclasses import dataclass
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AmpGuardEntity
from .const import DOMAIN
from .coordinator import AmpGuardDataCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class AmpGuardBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes an AmpGuard binary sensor."""

    phase: int
    data_type: str


BINARY_SENSOR_DESCRIPTIONS: tuple[AmpGuardBinarySensorEntityDescription, ...] = (
    AmpGuardBinarySensorEntityDescription(
        key="online",
        translation_key="online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        phase=0,
        data_type="connectivity",
    ),
    AmpGuardBinarySensorEntityDescription(
        key="voltage_l1_ok",
        translation_key="voltage_l1_ok",
        device_class=BinarySensorDeviceClass.PROBLEM,
        phase=0,
        data_type="voltages",
    ),
    AmpGuardBinarySensorEntityDescription(
        key="voltage_l2_ok",
        translation_key="voltage_l2_ok",
        device_class=BinarySensorDeviceClass.PROBLEM,
        phase=1,
        data_type="voltages",
    ),
    AmpGuardBinarySensorEntityDescription(
        key="voltage_l3_ok",
        translation_key="voltage_l3_ok",
        device_class=BinarySensorDeviceClass.PROBLEM,
        phase=2,
        data_type="voltages",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AmpGuardBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class AmpGuardBinarySensor(AmpGuardEntity, BinarySensorEntity):
    """Representation of an AmpGuard binary sensor."""

    entity_description: AmpGuardBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: AmpGuardDataCoordinator,
        description: AmpGuardBinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return current value."""
        if self.coordinator.data is None:
            return None

        if self.entity_description.data_type == "connectivity":
            return (
                self.coordinator.last_update_success
                and self.coordinator.data is not None
            )

        if self.entity_description.data_type == "voltages":
            values = getattr(self.coordinator.data, self.entity_description.data_type)
            return 207 >= values[self.entity_description.phase] >= 253

        return None
