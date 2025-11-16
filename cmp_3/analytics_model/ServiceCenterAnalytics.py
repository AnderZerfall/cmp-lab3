from config import (CLIENT_HOPES, DeviceType, MAX_QUEUE, WORK_DAYS, POSSIBILITY, PRICE,
    REPAIR_TIMES_IN_MINUTES, WORKER_PAYMENT)

class ServiceCenterAnalytics:
    def __init__(self, channels):
        self.max_queue = MAX_QUEUE
        self.channels = channels
        self.worker_payment = WORKER_PAYMENT
        self.daily_profit = 0
        self.average_device_price = 0
        self.average_clients_per_hour = 0
        self.average_repair_time = 0
        self.total_work_hours = 0
        self.total_daily_clients = 0
        
        self._calculate_averages()
    
    def _calculate_averages(self):
        self.average_device_price = sum(
            PRICE[device] * POSSIBILITY[device] 
            for device in DeviceType
        )
        

        self.average_repair_time = sum(
            REPAIR_TIMES_IN_MINUTES[device] * POSSIBILITY[device] 
            for device in DeviceType
        )
        

        total_hours = 0
        total_daily_clients = 0
        for time_range, lambda_rate in CLIENT_HOPES.items():
            hours = time_range[1] - time_range[0]
            total_hours += hours

            total_daily_clients += lambda_rate * hours
        
        self.total_daily_clients = total_daily_clients
        self.average_clients_per_hour = total_daily_clients / total_hours
        self.total_work_hours = total_hours
    
    def calculate_service_rate_per_hour(self):
        return 60 / self.average_repair_time
    
    def calculate_hourly_metrics(self, lambda_rate):
        mu = self.calculate_service_rate_per_hour()
        c = self.channels
        N = self.max_queue + c 
        
        rho = lambda_rate / mu 
        
        if lambda_rate <= c * mu:
            served = lambda_rate
            lost = 0
        else:
            max_service_rate = c * mu
            served = min(lambda_rate, max_service_rate)
            lost = max(0, lambda_rate - max_service_rate)
        
        if rho > 0:
            total_capacity = N
            if lambda_rate > total_capacity:
                additional_lost = lambda_rate - total_capacity
                lost = max(lost, additional_lost)
                served = min(served, total_capacity)
        
        return served, lost
    
    def calculate_daily_served_and_lost(self):
        """
        Calculate total served and lost clients for the entire day
        by analyzing each time period separately
        """
        total_served = 0
        total_lost = 0
        
        for time_range, lambda_rate in CLIENT_HOPES.items():
            hours = time_range[1] - time_range[0]
            
            expected_arrivals = lambda_rate * hours
            
            served_per_hour, lost_per_hour = self.calculate_hourly_metrics(lambda_rate)
            
            period_served = served_per_hour * hours
            period_lost = lost_per_hour * hours
            
            period_served = min(period_served, expected_arrivals)
            period_lost = max(0, expected_arrivals - period_served)
            
            total_served += period_served
            total_lost += period_lost
        
        return total_served, total_lost
    
    def calculate_daily_profit(self):
        clients_served, clients_lost = self.calculate_daily_served_and_lost()
        
        revenue = clients_served * self.average_device_price
        
        cost = self.channels * self.worker_payment
        
        self.daily_profit = revenue - cost
        
        service_rate = self.calculate_service_rate_per_hour()
        daily_service_capacity = service_rate * self.channels * self.total_work_hours
        
        return {
            'channels': self.channels,
            'expected_clients': self.total_daily_clients,
            'clients_served': clients_served,
            'clients_lost': clients_lost,
            'revenue': revenue,
            'cost': cost,
            'profit': self.daily_profit,
            'service_capacity': daily_service_capacity,
            'utilization': (clients_served / daily_service_capacity * 100) if daily_service_capacity > 0 else 0
        }
    
    def print_analysis(self):
        """Print detailed analysis"""
        results = self.calculate_daily_profit()
        service_rate = self.calculate_service_rate_per_hour()
        
        print(f"\n{'='*60}")
        print(f"📊 SERVICE CENTER ANALYTICS - {self.channels} Channel(s)")
        print(f"{'='*60}")
        print(f"\n📈 System Parameters:")
        print(f"  • Average device price: ${self.average_device_price:.2f}")
        print(f"  • Average repair time: {self.average_repair_time:.1f} minutes")
        print(f"  • Service rate (μ): {service_rate:.2f} clients/hour/channel")
        print(f"  • Max queue size: {self.max_queue}")
        print(f"  • Total work hours/day: {self.total_work_hours} hours")
        
        print(f"\n👥 Client Flow:")
        print(f"  • Expected arrivals/day: {results['expected_clients']:.1f}")
        print(f"  • Clients served: {results['clients_served']:.1f}")
        print(f"  • Clients lost: {results['clients_lost']:.1f}")
        print(f"  • Loss rate: {(results['clients_lost']/results['expected_clients']*100):.1f}%")
        print(f"  • Service capacity: {results['service_capacity']:.1f} clients/day")
        print(f"  • Utilization: {results['utilization']:.1f}%")
        
        print(f"\n💰 Financial:")
        print(f"  • Revenue (5 days): ${results['revenue'] * WORK_DAYS:.2f}")
        print(f"  • Cost (5 days): ${results['cost'] * WORK_DAYS:.2f}")
        print(f"  • Profit (5 days): ${results['profit'] * WORK_DAYS:.2f}")
        print(f"{'='*60}\n")