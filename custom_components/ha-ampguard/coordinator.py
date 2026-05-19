"""Amp guard data coordinator."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import AmpGuardClient
from .const import DOMAIN
from .exceptions import CannotConnect, InvalidAuth

_LOGGER = logging.getLogger(__name__)


class AmpGuardDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data."""

    def __init__(
        self, hass: HomeAssistant, client: AmpGuardClient, update_interval: timedelta
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch Data."""
        try:
            return await self.client.fetch()
        except CannotConnect as err:
            raise UpdateFailed("Cannot connect to AmpGuard") from err
        except InvalidAuth as err:
            raise UpdateFailed("Invalid PIN") from err
        except ValueError as err:
            _LOGGER("Got invalid response from ampguard.")
            await self.client.close()
            raise UpdateFailed("Invalid response from AmpGuard.") from err
        except Exception as err:
            _LOGGER.exception("Unknown failure fetching data")
            raise UpdateFailed(f"Unexpected error fetching data: {err}") from err
