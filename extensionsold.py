import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------
lambda_rate = 3.5   # arrivals per minute
mu = 1.5            # processing rate (per minute)
s = 3               # number of servers
num_customers = 1000

setup_time = 0.5    # minutes (~24 seconds)

# -----------------------------
# INITIALIZATION
# -----------------------------
arrival_times = []
waiting_times = []
system_times = []
service_times = []

server_available_time = [0] * s

# -----------------------------
# GENERATE ARRIVALS
# -----------------------------
current_time = 0

for i in range(num_customers):
    interarrival = np.random.exponential(1 / lambda_rate)
    current_time += interarrival
    arrival_times.append(current_time)

# -----------------------------
# SIMULATION
# -----------------------------
for i in range(num_customers):
    
    arrival = arrival_times[i]
    
    # Find next available server
    next_server = np.argmin(server_available_time)
    
    # Start time
    start = max(arrival, server_available_time[next_server])
    
    # PROCESSING TIME (random)
    process_time = np.random.exponential(1 / mu)
    
    # TOTAL SERVICE TIME = setup + processing
    total_service = setup_time + process_time
    
    finish = start + total_service
    
    # Update server availability
    server_available_time[next_server] = finish
    
    # Metrics
    waiting = start - arrival
    system = finish - arrival
    
    waiting_times.append(waiting)
    system_times.append(system)
    service_times.append(total_service)

# -----------------------------
# PERFORMANCE MEASURES
# -----------------------------
Wq = np.mean(waiting_times)
Ws = np.mean(system_times)

total_service_time = sum(service_times)
total_time = max(server_available_time) * s
rho = total_service_time / total_time

# -----------------------------
# OUTPUT
# -----------------------------
print("Average Waiting Time (Wq):", round(Wq, 3), "minutes")
print("Average Time in System (Ws):", round(Ws, 3), "minutes")
print("Server Utilization (ρ):", round(rho, 3))