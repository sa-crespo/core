"""Support for MQTT platform config setup."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.const import (
    CONF_CLIENT_ID,
    CONF_DISCOVERY,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_USERNAME,
    Platform,
)
from homeassistant.helpers import config_validation as cv

from . import (
    alarm_control_panel as alarm_control_panel_platform,
    binary_sensor as binary_sensor_platform,
    button as button_platform,
    camera as camera_platform,
    climate as climate_platform,
    cover as cover_platform,
    device_tracker as device_tracker_platform,
    fan as fan_platform,
    humidifier as humidifier_platform,
    light as light_platform,
    lock as lock_platform,
    number as number_platform,
    scene as scene_platform,
    select as select_platform,
    sensor as sensor_platform,
    siren as siren_platform,
    switch as switch_platform,
    text as text_platform,
    update as update_platform,
    vacuum as vacuum_platform,
)
from .const import (
    CONF_BIRTH_MESSAGE,
    CONF_BROKER,
    CONF_CERTIFICATE,
    CONF_CLIENT_CERT,
    CONF_CLIENT_KEY,
    CONF_DISCOVERY_PREFIX,
    CONF_KEEPALIVE,
    CONF_TLS_INSECURE,
    CONF_TRANSPORT,
    CONF_WILL_MESSAGE,
    CONF_WS_HEADERS,
    CONF_WS_PATH,
    DEFAULT_BIRTH,
    DEFAULT_DISCOVERY,
    DEFAULT_KEEPALIVE,
    DEFAULT_PORT,
    DEFAULT_PREFIX,
    DEFAULT_PROTOCOL,
    DEFAULT_TRANSPORT,
    DEFAULT_WILL,
    SUPPORTED_PROTOCOLS,
    TRANSPORT_TCP,
    TRANSPORT_WEBSOCKETS,
)
from .util import valid_birth_will, valid_publish_topic

DEFAULT_TLS_PROTOCOL = "auto"

PLATFORM_CONFIG_SCHEMA_BASE = vol.Schema(
    {
        Platform.ALARM_CONTROL_PANEL.value: vol.All(
            cv.ensure_list,
            [alarm_control_panel_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type] # noqa: E501
        ),
        Platform.BINARY_SENSOR.value: vol.All(
            cv.ensure_list,
            [binary_sensor_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.BUTTON.value: vol.All(
            cv.ensure_list,
            [button_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.CAMERA.value: vol.All(
            cv.ensure_list,
            [camera_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.CLIMATE.value: vol.All(
            cv.ensure_list,
            [climate_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.COVER.value: vol.All(
            cv.ensure_list,
            [cover_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.DEVICE_TRACKER.value: vol.All(
            cv.ensure_list,
            [device_tracker_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.FAN.value: vol.All(
            cv.ensure_list,
            [fan_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.HUMIDIFIER.value: vol.All(
            cv.ensure_list,
            [humidifier_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.LOCK.value: vol.All(
            cv.ensure_list,
            [lock_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.LIGHT.value: vol.All(
            cv.ensure_list,
            [light_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.NUMBER.value: vol.All(
            cv.ensure_list,
            [number_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.SCENE.value: vol.All(
            cv.ensure_list,
            [scene_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.SELECT.value: vol.All(
            cv.ensure_list,
            [select_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.SENSOR.value: vol.All(
            cv.ensure_list,
            [sensor_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.SIREN.value: vol.All(
            cv.ensure_list,
            [siren_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.SWITCH.value: vol.All(
            cv.ensure_list,
            [switch_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.TEXT.value: vol.All(
            cv.ensure_list,
            [text_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.UPDATE.value: vol.All(
            cv.ensure_list,
            [update_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
        Platform.VACUUM.value: vol.All(
            cv.ensure_list,
            [vacuum_platform.PLATFORM_SCHEMA_MODERN],  # type: ignore[has-type]
        ),
    }
)


CLIENT_KEY_AUTH_MSG = (
    "client_key and client_cert must both be present in the MQTT broker configuration"
)

CONFIG_SCHEMA_ENTRY = vol.Schema(
    {
        vol.Optional(CONF_CLIENT_ID): cv.string,
        vol.Optional(CONF_KEEPALIVE, default=DEFAULT_KEEPALIVE): vol.All(
            vol.Coerce(int), vol.Range(min=15)
        ),
        vol.Required(CONF_BROKER): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_CERTIFICATE): str,
        vol.Inclusive(CONF_CLIENT_KEY, "client_key_auth", msg=CLIENT_KEY_AUTH_MSG): str,
        vol.Inclusive(
            CONF_CLIENT_CERT, "client_key_auth", msg=CLIENT_KEY_AUTH_MSG
        ): str,
        vol.Optional(CONF_TLS_INSECURE): cv.boolean,
        vol.Optional(CONF_PROTOCOL, default=DEFAULT_PROTOCOL): vol.All(
            cv.string, vol.In(SUPPORTED_PROTOCOLS)
        ),
        vol.Optional(CONF_WILL_MESSAGE, default=DEFAULT_WILL): valid_birth_will,
        vol.Optional(CONF_BIRTH_MESSAGE, default=DEFAULT_BIRTH): valid_birth_will,
        vol.Optional(CONF_DISCOVERY, default=DEFAULT_DISCOVERY): cv.boolean,
        # discovery_prefix must be a valid publish topic because if no
        # state topic is specified, it will be created with the given prefix.
        vol.Optional(
            CONF_DISCOVERY_PREFIX, default=DEFAULT_PREFIX
        ): valid_publish_topic,
        vol.Optional(CONF_TRANSPORT, default=DEFAULT_TRANSPORT): vol.All(
            cv.string, vol.In([TRANSPORT_TCP, TRANSPORT_WEBSOCKETS])
        ),
        vol.Optional(CONF_WS_PATH, default="/"): cv.string,
        vol.Optional(CONF_WS_HEADERS, default={}): {cv.string: cv.string},
    }
)

DEPRECATED_CONFIG_KEYS = [
    CONF_BIRTH_MESSAGE,
    CONF_BROKER,
    CONF_CLIENT_ID,
    CONF_DISCOVERY,
    CONF_DISCOVERY_PREFIX,
    CONF_KEEPALIVE,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_TLS_INSECURE,
    CONF_USERNAME,
    CONF_WILL_MESSAGE,
]

DEPRECATED_CERTIFICATE_CONFIG_KEYS = [
    CONF_CERTIFICATE,
    CONF_CLIENT_CERT,
    CONF_CLIENT_KEY,
]
