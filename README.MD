
# HA AmpGuard

Home Assistant custom integration for AmpGuard devices. Monitor your electrical usage in real-time with voltage, current, phase angle, and status sensors.

## Installation

1. Add this repository to HACS as a custom repository
2. Search for "HA AmpGuard" and install
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "Amp Guard" and select it
3. Enter your Amp Guard device IP address and PIN code
4. Complete the setup

## Sensors

The integration exposes the following sensors:

- **Voltage** - Current voltage reading
- **Current** - Current consumption
- **Angle** - Phase angle
- **Status** - Connection and voltage status

## Requirements

- Home Assistant with HACS installed
- AmpGuard device on your local network
