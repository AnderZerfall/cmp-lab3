import pandas as pd 

class Stats(object):
    def __init__(self):
        self.df = pd.DataFrame(data=[[0,0, 0, 0, 0]],
            columns=['Time', 'Clients Arrived', 'Lost Clients', 'Queue length', 'Profit'])
    def change_info(self, time , arrived_clients, lost_clients, queue_length, price):
        new_info = pd.DataFrame(data=[[time , arrived_clients, lost_clients, queue_length, price]],
            columns=['Time', 'Clients Arrived', 'Lost Clients', 'Queue length', 'Profit'])
        self.df = pd.concat([self.df, new_info], axis = 0, ignore_index = True)