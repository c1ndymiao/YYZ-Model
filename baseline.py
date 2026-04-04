import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------
lambda_rate = 3.5   # arrivals per minute
mu = 1.5            # service rate (customers per minute)
s = 3               # number of servers
num_customers = 1000

# -----------------------------
# INITIALIZATION
# -----------------------------
arrival_times = []
service_times = []
start_times = []
finish_times = []
waiting_times = []
system_times = []

# Track when each server becomes available
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
    
    # Choose the server that becomes free the earliest
    next_server = np.argmin(server_available_time)
    
    # Service starts when both passenger arrives AND server is free
    start = max(arrival, server_available_time[next_server])
    
    # Generate service time
    service = np.random.exponential(1 / mu)
    
    finish = start + service
    
    # Update server availability
    server_available_time[next_server] = finish
    
    # Record values
    waiting = start - arrival
    system = finish - arrival
    
    service_times.append(service)
    start_times.append(start)
    finish_times.append(finish)
    waiting_times.append(waiting)
    system_times.append(system)

# -----------------------------
# PERFORMANCE MEASURES
# -----------------------------
Wq = np.mean(waiting_times)
Ws = np.mean(system_times)

# Utilization
total_service_time = sum(service_times)
total_time = max(finish_times) * s
rho = total_service_time / total_time

# -----------------------------
# OUTPUT RESULTS
# -----------------------------
print("Average Waiting Time (Wq):", round(Wq, 3), "minutes")
print("Average Time in System (Ws):", round(Ws, 3), "minutes")
print("Server Utilization (ρ):", round(rho, 3))