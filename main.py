from ServiceCenter import ServiceCenter, WORK_HOURS_FRAMES
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

START_DATE = start_date = datetime.datetime(2025, 10, 13, 9)
WORK_HOURS = 9
WORK_DAYS = 5

def get_client_arrived_stats(service):
    _, _, patches  = plt.hist(service.statistics.df['Clients Arrived'], bins=range(0, 10), edgecolor='white', label='Clients Occurance')
    plt.title('Histogram of Hourly Client Arrivals')
    plt.xlabel('Clients per hour')
    plt.xticks(range(0, 11))
    plt.ylabel('Frequency (in hours amount)')
    
    for p in patches:
        height = p.get_height()
        x_pos = p.get_x() 
        plt.text(
            p.get_x() + p.get_width() / 2, 
            height + 0.1,                  
            f"{int(x_pos)} Client(s)",                   
            ha='center',                   
            va='bottom',
            fontsize = 8,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3')               
        )
        
    plt.legend()
    plt.show()

def get_queue_length_stats(service):
    service.statistics.df['Time'] = pd.to_datetime(service.statistics.df['Time'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(service.statistics.df['Time'], service.statistics.df['Queue length'],  linestyle='--', color='lightblue')
    plt.scatter(service.statistics.df['Time'], service.statistics.df['Queue length'], color='blue', label='Queue Size')
    ax = plt.gca()
    ax.set_xlim(START_DATE, service.statistics.df['Time'].max())
    plt.xticks(rotation=45)
    plt.title('Queue Length Over Time')
    plt.xlabel('Time (Month, Day, Time)')
    plt.ylabel('Clients in Queue')
    plt.tight_layout()
    plt.legend()
    plt.show()

def get_arrived_vs_rejected_stats(service):
    totals = service.statistics.df[['Clients Arrived', 'Lost Clients']].sum()
    ax = totals.plot(kind='bar', color=['limegreen', 'lightcoral'])
    plt.title('Total Clients Arrived vs Rejected')
    
    for p in ax.patches:
        height = p.get_height()
        ax.text(
            p.get_x() + p.get_width() / 2, 
            height / 2,                  
            int(height),                   
            ha='center',                   
            va='bottom',
            fontsize = 16,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3')                                 
        )
    
    plt.xticks(rotation=45, fontsize=7)
    plt.ylabel('Clients Amount')
    arrived_patch = mpatches.Patch(color='limegreen', label='Clients Arrived')
    lost_patch = mpatches.Patch(color='lightcoral', label='Lost Clients')
    plt.legend(handles=[arrived_patch, lost_patch])
    plt.show()

def get_profit_stats(service):
    plt.figure(figsize=(10, 5))
    plt.plot_date(service.statistics.df['Time'], service.statistics.df['Profit'].cumsum(), label="Service Center's profit")
    ax = plt.gca()
    ax.set_xlim(START_DATE, service.statistics.df['Time'].max())
    plt.title('Cumulative Profit Over Time')
    plt.xlabel('Time (Month, Day, Time)')
    plt.ylabel('Profit (imaginary units)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

def run_simulation():
    service = ServiceCenter(START_DATE)
    work_hours_in_week = WORK_HOURS * WORK_DAYS
    i = 0

    service.get_general_info()

    while i < work_hours_in_week:
        if service.current_time.hour == WORK_HOURS_FRAMES.get("17-18")[1]:
            service.next_day()
        elif service.current_time.hour == WORK_HOURS_FRAMES.get("17-18")[1] and service.current_time.weekday() == 4:
            break
        else:
            service.next_hour()
            i += 1
        service.client_arrived()
        service.service_client()
        service.get_intermediate_info()
        service.get_general_info()
    
    print(f"---------- [ LOGS ] ----------")
    print(service.statistics.df)
    print(f"---------- [ END OF LOGS ] ----------")
    print(f"---------- [ PROFIT ] ----------")
    print(f"Profit after full working week:  {service.statistics.df['Profit'].sum()} 💸")
    print(f"---------- [ ------ ] ----------")
    print(f"---------- [ Clients ] ----------")
    print(f"Lost Clients after full working week:  {service.statistics.df['Lost Clients'].sum()} 💔")
    print(f"Lost Clients after full working week:  {service.statistics.df['Clients Arrived'].sum()} 😃")
    print(f"---------- [ ------ ] ----------")

    get_client_arrived_stats(service)
    get_queue_length_stats(service)
    get_arrived_vs_rejected_stats(service)
    get_profit_stats(service)

run_simulation()
