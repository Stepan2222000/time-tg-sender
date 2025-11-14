"""
TLAPI Integration Module

Provides device fingerprint generation and official Telegram API support.
Based on: https://github.com/pyhashem/tlapi
"""

from .api import API, APIData
from .devices import (
    AndroidDevice,
    AndroidDeviceX,
    AndroidDeviceBeta,
    iOSDeivce,
    WindowsDevice,
    macOSDevice,
    LinuxDevice,
    DeviceInfo,
    SystemInfo
)
from .utils import BaseObject, BaseMetaClass
from .exception import OpenTeleException

__all__ = [
    "API",
    "APIData",
    "AndroidDevice",
    "AndroidDeviceX",
    "AndroidDeviceBeta",
    "iOSDeivce",
    "WindowsDevice",
    "macOSDevice",
    "LinuxDevice",
    "DeviceInfo",
    "SystemInfo",
    "BaseObject",
    "BaseMetaClass",
    "OpenTeleException",
]

__version__ = "0.0.2"
