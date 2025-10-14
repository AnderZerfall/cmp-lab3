from Client import Client
import datetime
import numpy as np
from Print import GREEN, RED, RESET
from Stats import Stats

MAX_QUEUE = 12
STEP = 1
WORK_HOURS_FRAMES = {
    "9-13": [9, 13],
    "13-17": [13, 17],
    "17-18": [17, 18]
}

class ServiceCenter(object):
    def __init__(self, current_time):
        self.current_time = current_time
        self.current_client = Client()
        self.served_clients = 0
        self.arrived_clients = 0
        self.lost_clients = 0
        self.profit = 0
        self.max_que = MAX_QUEUE
        self.queue = 0
        self.statistics = Stats();
    
    def next_hour(self):
        self.current_time += datetime.timedelta(hours=STEP)
    
    def next_day(self):
        new_day = self.current_time + datetime.timedelta(days=1)
        self.current_time = new_day.replace(hour=9, minute=0, second=0, microsecond=0)
        self.queue = 0;
        self.arrived_clients = 0
        self.lost_clients = 0
        self.current_client.device = None
    
    def client_arrived(self):
        is_end_of_day = self.current_time.hour == WORK_HOURS_FRAMES.get("17-18")[1]
        
        if WORK_HOURS_FRAMES.get("9-13")[0] <= self.current_time.hour < WORK_HOURS_FRAMES.get("9-13")[1]:
            hopes = 3
        elif WORK_HOURS_FRAMES.get("13-17")[0] <= self.current_time.hour < WORK_HOURS_FRAMES.get("13-17")[1]:
            hopes = 4
        elif WORK_HOURS_FRAMES.get("17-18")[0] <= self.current_time.hour <= WORK_HOURS_FRAMES.get("17-18")[1]:
            hopes = 5
        else:
            hopes = 0

        clients_amount = np.random.poisson(hopes)
        available_slots = self.max_que - self.queue

        if clients_amount > available_slots:
            accepted = available_slots
            rejected = clients_amount - available_slots
        else:
            accepted = clients_amount
            rejected = 0

        updated_queue = self.queue + accepted
        rejected = rejected + updated_queue if is_end_of_day else rejected
        
        self.lost_clients = rejected
        self.queue =  0 if is_end_of_day else updated_queue
        self.arrived_clients = clients_amount;
    
    def service_client(self):
        avaiable_time = 60 * STEP
        
        print("\n📋 Devices in Queue")
        
        while self.queue > 0 and avaiable_time > 0:
            if (not self.current_client.device or self.current_client.device.is_fixed):
                self.current_client.set_up_device();
                self.queue -= 1
                self.served_clients += 1
                self.statistics.change_info(self.current_time, self.arrived_clients, self.lost_clients,
                    self.queue, self.current_client.device.price)
            
            avaiable_time -= self.current_client.device.time_to_repair_in_minutes
            
            if (avaiable_time >= 0):
                self.current_client.device.is_fixed = True
                self.current_client.device.time_to_repair_in_minutes = 0;
                self.profit +=  self.current_client.device.price
            else:
                self.current_client.device.time_to_repair_in_minutes += avaiable_time;
                self.current_client.device.is_fixed = False
                avaiable_time = 0
            self.current_client.get_device_info();
        
        print("---------------------------------------")

    def get_general_info(self):
        print(f'----------- [ 📅 {self.current_time.strftime("%A %H:%M")} ] -----------')
        print(f"💵 Profit: {self.profit}")
        print(f"👀 Queue: {self.queue}")
        print(f"🤑 {GREEN} + Clients Served in total: {self.served_clients} {RESET}")
        print(f"💔 {RED} - Clients Lost Today: {self.lost_clients} {RESET}")
    
    def get_intermediate_info(self):
        print(f"🧔 To the center arrived {self.arrived_clients} clients in the past hour")