from ServiceCenter import ServiceCenter, WORK_HOURS_FRAMES
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

START_DATE = start_date = datetime.datetime(2025, 10, 13, 9)
WORK_HOURS = 9
WORK_DAYS = 5

def get_client_arrived_stats(stats):
    _, _, patches  = plt.hist(stats.df['Clients Arrived'], bins=range(0, 10), edgecolor='white', label='Clients Occurance')
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

def get_queue_length_stats(stats):
    stats.df['Time'] = pd.to_datetime(stats.df['Time'])
    plt.figure(figsize=(10, 5))
    plt.scatter(stats.df['Time'], stats.df['Queue length'], color='blue', label='Queue Size')
    plt.plot(stats.df['Time'], stats.df['Queue length'],  linestyle='--', color='lightblue')
    ax = plt.gca()
    ax.set_xlim(START_DATE, stats.df['Time'].max())
    plt.xticks(rotation=45)
    plt.title('Queue Length Over Time')
    plt.xlabel('Time (Month, Day, Time)')
    plt.ylabel('Clients in Queue')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()

def get_arrived_vs_rejected_stats(stats):
    totals = stats.df[['Clients Arrived', 'Lost Clients']].sum()
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

def get_profit_stats(stats):
    plt.figure(figsize=(10, 5))
    plt.plot_date(stats.df['Time'], stats.df['Profit'].cumsum(), label="Service Center's profit")
    ax = plt.gca()
    ax.set_xlim(START_DATE, stats.df['Time'].max())
    plt.title('Cumulative Profit Over Time')
    plt.xlabel('Time (Month, Day, Time)')
    plt.ylabel('Profit (imaginary units)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()

def run_simulation(channels = 1):
    
    service = ServiceCenter(START_DATE, channels=channels)
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
    
    return service.statistics

def get_simulation_results():
    num_channels = 1
        
    try:
        num_channels = int(input("Enter the number of channels: "))
        if num_channels < 1:
            print("Number of channels must be at least 1. Using default value of 1.")
    except ValueError:
        print("Invalid input. Using default value of 1.")
            
    stats = run_simulation(num_channels)
    
    print(f"---------- [ LOGS ] ----------")
    print(stats.df)
    print(f"---------- [ END OF LOGS ] ----------")
    print(f"---------- [ PROFIT ] ----------")
    print(f"Profit after full working week:  {stats.df['Profit'].sum()} 💸")
    print(f"---------- [ ------ ] ----------")
    print(f"---------- [ Clients ] ----------")
    print(f"Lost Clients after full working week:  {stats.df['Lost Clients'].sum()} 💔")
    print(f"New Clients after full working week:  {stats.df['Clients Arrived'].sum()} 😃")
    print(f"---------- [ ------ ] ----------")

    get_client_arrived_stats(stats)
    get_queue_length_stats(stats)
    get_arrived_vs_rejected_stats(stats)
    get_profit_stats(stats)

def get_100_simulation_results():
    all_dfs = []
    
    num_channels = 1
        
    try:
        num_channels = int(input("Enter the number of channels: "))
        if num_channels < 1:
            print("Number of channels must be at least 1. Using default value of 1.")
    except ValueError:
        print("Invalid input. Using default value of 1.")
    
    for i in range(0, 100):
        stats = run_simulation(num_channels)
        df = stats.df.copy()
        df['Run'] = i
        all_dfs.append(df)

    combined_df = pd.concat(all_dfs, ignore_index=True)
    simulation_sums = combined_df.groupby('Run')[['Profit', 'Clients Arrived', 'Lost Clients']].sum()
    
    avg_profit = simulation_sums['Profit'].mean()
    avg_clients = simulation_sums['Clients Arrived'].mean()
    avg_lost = simulation_sums['Lost Clients'].mean()
    
    print("\n🔢 Average Results Over 100 Simulations:")
    print(f"📈 Average Profit: {avg_profit:.2f} 💸")
    print(f"👥 Average Clients Arrived: {avg_clients:.0f}")
    print(f"💔 Average Lost Clients: {avg_lost:.0f}")

get_simulation_results()
#get_100_simulation_results()