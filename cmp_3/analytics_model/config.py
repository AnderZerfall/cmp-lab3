from enum import Enum

WORK_DAYS = 5

WORKER_PAYMENT = 100

MAX_QUEUE = 12


WORK_HOURS_FRAMES = {
    "9-13": [9, 13],
    "13-17": [13, 17],
    "17-18": [17, 18]
}


CLIENT_HOPES = {
    (9, 13): 3,
    (13, 17): 4,
    (17, 18): 5
}

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

POSSIBILITY = {
    DeviceType.SMARTPHONE: 0.5,
    DeviceType.TABLET: 0.2,
    DeviceType.LAPTOP: 0.2,
    DeviceType.OTHER: 0.1,
}