from Device import Device, POSSIBLITY
import random
from Print import GREEN, RED, RESET

class Client(object):
    def __init__(self):
        self.device = None

    def set_up_device(self):
        device_types = list(POSSIBLITY.keys())
        weights = list(POSSIBLITY.values())
        device_type = random.choices(device_types, weights=weights, k=1)[0]
        
        self.device = Device(device_type)
    
    def get_device_info(self):
        color = GREEN if self.device.is_fixed else RED
        name = self.device.device_type if self.device else "-"
        repair_time = self.device.time_to_repair_in_minutes if self.device else "-"
        price = self.device.price if self.device else "-"
        is_fixed = self.device.is_fixed if self.device else "-"
        
        print(f"💻{color} {name} - {is_fixed} - {repair_time} min - {price} 💸 {RESET}")