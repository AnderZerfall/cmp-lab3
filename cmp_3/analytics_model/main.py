from ServiceCenterAnalytics import ServiceCenterAnalytics
import matplotlib.pyplot as plt
from ServiceCenterAnalytic_2 import ServiceCenterAnalytics2

def find_optimal_channels(max_channels=10):
    print("\n🔍 FINDING OPTIMAL NUMBER OF WORKERS\n")
    
    results = []
    
    for channels in range(1, max_channels + 1):
        analytics = ServiceCenterAnalytics(channels)
        result = analytics.calculate_daily_profit()
        results.append(result)
        
        print(f"Channels: {channels} | Profit: ${result['profit']:.2f} | "
              f"Served: {result['clients_served']:.1f} | "
              f"Lost: {result['clients_lost']:.1f}")
    
    # Find optimal
    optimal = max(results, key=lambda x: x['profit'])
    
    print(f"\n{'='*60}")
    print(f"✅ OPTIMAL SOLUTION")
    print(f"{'='*60}")
    print(f"🏆 Optimal number of workers: {optimal['channels']}")
    print(f"💵 Maximum daily profit: ${optimal['profit']:.2f}")
    print(f"👥 Clients served: {optimal['clients_served']:.1f}")
    print(f"📊 Utilization: {optimal['utilization']:.1f}%")
    print(f"{'='*60}\n")
    
    return optimal, results

def plot_results(results, optimal):
    channels = [r['channels'] for r in results]
    profits = [r['profit'] for r in results]
    revenues = [r['revenue'] for r in results]
    costs = [r['cost'] for r in results]
    served = [r['clients_served'] for r in results]
    lost = [r['clients_lost'] for r in results]
    utilization = [r['utilization'] for r in results]
    
    channel_labels = [f'c={c}' for c in channels]
    

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Service Center Optimization Analysis', fontsize=16,)
    
    ax1 = axes[0, 0]
    ax1.plot(channels, profits, 'b-o', linewidth=2, markersize=8, label='Profit')
    ax1.axvline(x=optimal['channels'], color='r', linestyle='--', linewidth=2, 
                label=f'Optimal: {optimal["channels"]} channels')
    ax1.axhline(y=optimal['profit'], color='g', linestyle=':', alpha=0.5)
    ax1.set_xlabel('Channels', fontsize=11)
    ax1.set_ylabel('Daily Profit (imaginary units)', fontsize=11)
    ax1.set_title('Profit vs Channels', fontsize=12)
    
    ax1.set_xticks(channels)
    ax1.set_xticklabels(channel_labels)
    
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    

    ax1.plot(optimal['channels'], optimal['profit'], 'r*', markersize=20, 
             label='Optimal Point')

    ax2 = axes[0, 1]
    ax2.plot(channels, revenues, 'g-o', linewidth=2, markersize=6, label='Raw Profit')
    ax2.plot(channels, costs, 'r-s', linewidth=2, markersize=6, label='Cost')
    ax2.axvline(x=optimal['channels'], color='orange', linestyle='--', linewidth=2, alpha=0.7)
    ax2.set_xlabel('Channels', fontsize=11)
    ax2.set_ylabel('Amount (imaginary units)', fontsize=11,)
    ax2.set_title('Raw Profit and Cost', fontsize=12,)
    ax2.set_xticks(channels)
    ax2.set_xticklabels(channel_labels)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    

    

    ax3 = axes[1, 0]
    ax3.plot(channels, served, 'b-o', linewidth=2, markersize=6, label='Served')
    ax3.plot(channels, lost, 'r-^', linewidth=2, markersize=6, label='Lost')
    ax3.axvline(x=optimal['channels'], color='orange', linestyle='--', linewidth=2, alpha=0.7)
    ax3.set_xlabel('Channels', fontsize=11,)
    ax3.set_ylabel('Clients', fontsize=11, )
    ax3.set_title('Clients Served vs Lost', fontsize=12,)
    ax3.set_xticks(channels)
    ax3.set_xticklabels(channel_labels)
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    

    ax4 = axes[1, 1]
    colors = ['red' if u > 90 else 'yellow' if u > 70 else 'green' for u in utilization]
    bars = ax4.bar(channels, utilization, color=colors, alpha=0.7, edgecolor='black')
    ax4.axvline(x=optimal['channels'], color='blue', linestyle='--', linewidth=2, 
                label=f'Optimal: {optimal["channels"]} channels')
    ax4.axhline(y=100, color='red', linestyle=':', alpha=0.5, label='100% capacity')
    ax4.set_xlabel('Number of Channels', fontsize=11, )
    ax4.set_ylabel('Utilization (%)', fontsize=11, )
    ax4.set_title('Channel Utilization Rate', fontsize=12,)
    ax4.set_ylim(0, max(utilization) * 1.1)
    ax4.set_xticks(channels)
    ax4.set_xticklabels(channel_labels)
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.legend()
    
    plt.tight_layout()
    plt.show()


def run_model():
    num_channels = 1
    
    try:
        num_channels = int(input("Enter the max number of channels: "))
        if num_channels < 1:
            print("Number of channels must be at least 1. Using default value of 1.")
    except ValueError:
        print("Invalid input. Using default value of 1.")
    
    print("\n" + "="*60)
    print("Find optimal number of workers")
    print("="*60)
    optimal, results = find_optimal_channels(max_channels=num_channels)
    
    print("\n" + "="*60)
    print("Detailed analysis of optimal solution")
    print("="*60)
    optimal_analytics = ServiceCenterAnalytics2(channels=optimal['channels'])
    optimal_analytics.print_analysis()
    
    print("\n📊 Generating visualizations...")
    plot_results(results, optimal)

run_model()