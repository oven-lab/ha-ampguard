"""Amp guard client."""

from dataclasses import dataclass
import logging

import websockets
from websockets.exceptions import ConnectionClosedError

from .exceptions import CannotConnect, InvalidAuth

_LOGGER = logging.getLogger(__name__)


@dataclass
class AmpGuardData:
    """Data returned by the device."""

    currents: tuple[float, float, float]  # L1, L2, L3 in A
    voltages: tuple[float, float, float]  # L1, L2, L3 in V
    powers: tuple[float, float, float]  # L1, L2, L3 in W
    angles: tuple[float, float, float]  # L1, L2, L3 in °


class AmpGuardClient:
    """Amp Guard Client."""

    def __init__(self, host: str, pin: str) -> None:
        """Initialize."""

        self._url = f"ws://{host}/ws"
        self._pin = pin
        self._ws = None

    async def connect(self):
        """Connect + authentication."""

        if self._ws:
            await self._ws.close()

        try:
            self._ws = await websockets.connect(
                self._url,
                compression="deflate",
            )
        except TimeoutError as err:
            _LOGGER.error(
                "Timed out while attempting connection to Amp Guard at %s", self._url
            )
            raise CannotConnect from err
        except ConnectionRefusedError as err:
            _LOGGER.error("Connection to Amp Guard at %s refused", self._url)
            raise CannotConnect from err

        # 1. Pre-auth
        await self._send_and_expect("?,6", "?,6")

        # 2. Authenticate
        try:
            await self._send_and_expect(f"5,{self._pin}", "5,1")
        except ValueError as e:
            _LOGGER.error("Invalid PIN")
            raise InvalidAuth from e

    async def _send_and_expect(self, to_send: str, expected_start: str):
        await self._ws.send(to_send)
        resp = await self._ws.recv()
        if not resp.startswith(expected_start):
            raise ValueError(f"Expected '{expected_start}' but got '{resp}'")
        return resp

    async def fetch(self) -> AmpGuardData:
        """Fetch latest data. Reconnects automatically if needed."""
        max_retries = 2

        for attempt in range(max_retries + 1):
            if not self._ws:
                await self.connect()

            try:
                await self._ws.send("?,1")
                resp = await self._ws.recv()
            except ConnectionClosedError as err:
                _LOGGER.warning(
                    "Connection to %s was closed (attempt %d/%d)",
                    self._url,
                    attempt + 1,
                    max_retries + 1,
                )
                await self.close()
                if attempt == max_retries:
                    _LOGGER.error("Max retries reached. Could not connect to %s", self._url)
                    raise CannotConnect("Max retries reached") from err
                continue

            if not resp.startswith("1,"):
                raise ValueError("Invalid data response")

            # Parse 12 comma-separated floats
            values = [float(x) for x in resp[2:].split(",")]
            return AmpGuardData(
                currents=tuple(values[0:3]),
                voltages=tuple(values[3:6]),
                powers=tuple(values[6:9]),
                angles=tuple(values[9:12]),
            )
        
        raise RuntimeError("Unreachable: fetch should have returned or raised")

    async def close(self):
        """Close the websocket."""

        if self._ws:
            await self._ws.close()
            self._ws = None
