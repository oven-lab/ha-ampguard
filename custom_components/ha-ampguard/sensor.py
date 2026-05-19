"""Sensor description."""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AmpGuardEntity
from .const import DOMAIN
from .coordinator import AmpGuardDataCoordinator


@dataclass(kw_only=True, frozen=True)
class AmpGuardSensorEntityDescription(SensorEntityDescription):
    """Describes an AmpGuard sensor."""

    data_type: str
    phase: int


SENSOR_DESCRIPTIONS: tuple[AmpGuardSensorEntityDescription, ...] = (
    # Currents (A)
    AmpGuardSensorEntityDescription(
        key="current_l1",
        translation_key="current_l1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="currents",
        phase=0,
    ),
    AmpGuardSensorEntityDescription(
        key="current_l2",
        translation_key="current_l2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="currents",
        phase=1,
    ),
    AmpGuardSensorEntityDescription(
        key="current_l3",
        translation_key="current_l3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="currents",
        phase=2,
    ),
    # Voltages (V)
    AmpGuardSensorEntityDescription(
        key="voltage_l1",
        translation_key="voltage_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="voltages",
        phase=0,
    ),
    AmpGuardSensorEntityDescription(
        key="voltage_l2",
        translation_key="voltage_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="voltages",
        phase=1,
    ),
    AmpGuardSensorEntityDescription(
        key="voltage_l3",
        translation_key="voltage_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="voltages",
        phase=2,
    ),
    # Powers (W)
    AmpGuardSensorEntityDescription(
        key="power_l1",
        translation_key="power_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        data_type="powers",
        phase=0,
    ),
    AmpGuardSensorEntityDescription(
        key="power_l2",
        translation_key="power_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        data_type="powers",
        phase=1,
    ),
    AmpGuardSensorEntityDescription(
        key="power_l3",
        translation_key="power_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        data_type="powers",
        phase=2,
    ),
    # Phase angles (°)
    AmpGuardSensorEntityDescription(
        key="angle_l1",
        translation_key="angle_l1",
        native_unit_of_measurement="°",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="angles",
        phase=0,
    ),
    AmpGuardSensorEntityDescription(
        key="angle_l2",
        translation_key="angle_l2",
        native_unit_of_measurement="°",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="angles",
        phase=1,
    ),
    AmpGuardSensorEntityDescription(
        key="angle_l3",
        translation_key="angle_l3",
        native_unit_of_measurement="°",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        data_type="angles",
        phase=2,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AmpGuardSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS
    )


class AmpGuardSensor(AmpGuardEntity, SensorEntity):
    """Representation of an AmpGuard sensor."""

    entity_description: AmpGuardSensorEntityDescription

    def __init__(
        self,
        coordinator: AmpGuardDataCoordinator,
        description: AmpGuardSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.coordinator.data is None:
            return None
        values = getattr(self.coordinator.data, self.entity_description.data_type)
        return values[self.entity_description.phase]
