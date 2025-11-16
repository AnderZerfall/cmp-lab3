from enum import Enum


class DeviceType(Enum):
    SMARTPHONE = "SMARTPHONE"
    TABLET = "TABLET"
    LAPTOP = "LAPTOP"
    OTHER = "OTHER"


REPAIR_TIMES_IN_MINUTES = {
    DeviceType.SMARTPHONE: 30,
    DeviceType.TABLET: 45,
    DeviceType.LAPTOP: 60,
    DeviceType.OTHER: 90,
}

PRICE = {
    DeviceType.SMARTPHONE: 10,
    DeviceType.TABLET: 20,
    DeviceType.LAPTOP: 30,
    DeviceType.OTHER: 40,
}

POSSIBLITY = {
    DeviceType.SMARTPHONE: 0.5,
    DeviceType.TABLET: 0.2,
    DeviceType.LAPTOP: 0.2,
    DeviceType.OTHER: 0.1,
}


class Device(object):
    def __init__(self, device_type: DeviceType, is_fixed: bool = False):
        self.device_type = device_type 
        self.possibility = POSSIBLITY.get(device_type)
        self.price = PRICE.get(device_type)
        self.time_to_repair_in_minutes = REPAIR_TIMES_IN_MINUTES.get(device_type)
        self.is_fixed = is_fixed