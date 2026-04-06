import numpy as np

# =========================================================
# CORE SIMULATION FUNCTION
# =========================================================
def simulate(
    lambda_rate=3.5,
    mu_regular=1.5,
    mu_precheck=2.5,
    s=3,
    num_customers=3000,
    
    # Extensions (toggle on/off)
    setup_time=0,
    queue_type="common",   # "common" or "separate"
    priority=False,
    rush_hour=False,
    machine_failure=False
):
    
    # -----------------------------
    # EXTENSION PARAMETERS
    # -----------------------------
    p_precheck = 0.3
    
    rush_start, rush_end = 200, 400
    lambda_rush = lambda_rate * 1.5
    
    break_start, break_end = 200, 350
    
    # -----------------------------
    # INITIALIZATION
    # -----------------------------
    arrival_times = []
    customer_types = []
    
    waiting_times = []
    system_times = []
    service_times = []
    
    server_available_time = [0] * s
    server_finish_times = [0] * s  # for separate queues
    
    # -----------------------------
    # GENERATE ARRIVALS
    # -----------------------------
    current_time = 0
    
    for _ in range(num_customers):
        
        # Rush hour adjustment
        if rush_hour and rush_start <= current_time <= rush_end:
            lam = lambda_rush
        else:
            lam = lambda_rate
        
        interarrival = np.random.exponential(1 / lam)
        current_time += interarrival
        arrival_times.append(current_time)
        
        # Customer type
        if priority and np.random.rand() < p_precheck:
            customer_types.append("priority")
        else:
            customer_types.append("regular")
    
    # -----------------------------
    # SIMULATION
    # -----------------------------
    for i in range(num_customers):
        
        arrival = arrival_times[i]
        
        # Active servers (machine failure)
        if machine_failure and (200 <= arrival <= 350):
            active_servers = list(range(max(1, s - 1)))
        else:
            active_servers = list(range(s))
        
        # -----------------------------
        # COMMON QUEUE
        # -----------------------------
        if queue_type == "common":
            
            chosen_server = min(active_servers, key=lambda j: server_available_time[j])
            start = max(arrival, server_available_time[chosen_server])
            
        # -----------------------------
        # SEPARATE QUEUES
        # -----------------------------
        else:
            
            chosen_server = min(active_servers, key=lambda j: server_finish_times[j])
            start = max(arrival, server_finish_times[chosen_server])
        
        # -----------------------------
        # SERVICE TIME
        # -----------------------------
        if priority and customer_types[i] == "priority":
            mu = mu_precheck
        else:
            mu = mu_regular
        
        process_time = np.random.exponential(1 / mu)
        total_service = setup_time + process_time
        finish = start + total_service
        
        # Update server time
        if queue_type == "common":
            server_available_time[chosen_server] = finish
        else:
            server_finish_times[chosen_server] = finish
        
        # Metrics
        waiting = start - arrival
        system = finish - arrival
        
        waiting_times.append(waiting)
        system_times.append(system)
        service_times.append(total_service)
    
    # -----------------------------
    # PERFORMANCE METRICS
    # -----------------------------
    Wq = np.mean(waiting_times)
    Ws = np.mean(system_times)
    
    total_time = max(server_available_time + server_finish_times)
    rho = sum(service_times) / (total_time * s)
    
    return Wq, Ws, rho


# =========================================================
# HELPER: AVERAGE MULTIPLE RUNS (OPTIONAL)
# =========================================================
def run_avg(n=5, **kwargs):
    results = [simulate(**kwargs) for _ in range(n)]
    return np.mean(results, axis=0)


# =========================================================
# SCENARIO COMPARISON (REQUIRED)
# =========================================================
print("\n=== SCENARIO COMPARISON ===")

baseline = run_avg(
    setup_time=0,
    queue_type="common",
    priority=False,
    rush_hour=False,
    machine_failure=False
)

peak_separate = run_avg(
    setup_time=0.4,
    queue_type="separate",
    priority=False,
    rush_hour=True,
    machine_failure=False
)

peak_common = run_avg(
    setup_time=0.4,
    queue_type="common",
    priority=False,
    rush_hour=True,
    machine_failure=False
)

print(f"Baseline: Wq={baseline[0]:.3f}, Ws={baseline[1]:.3f}, ρ={baseline[2]:.3f}")
print(f"Peak + Separate: Wq={peak_separate[0]:.3f}, Ws={peak_separate[1]:.3f}, ρ={peak_separate[2]:.3f}")
print(f"Peak + Common: Wq={peak_common[0]:.3f}, Ws={peak_common[1]:.3f}, ρ={peak_common[2]:.3f}")


# =========================================================
# SENSITIVITY ANALYSIS
# =========================================================

print("\n=== SENSITIVITY ANALYSIS: Arrival Rate (λ) ===")

for lam in [2.5, 3.0, 3.5, 4.0, 4.5]:
    result = run_avg(lambda_rate=lam)
    print(f"λ={lam}: Wq={result[0]:.3f}, Ws={result[1]:.3f}, ρ={result[2]:.3f}")


print("\n=== SENSITIVITY ANALYSIS: Number of Servers (s) ===")

for servers in [2, 3, 4, 5]:
    result = run_avg(s=servers)
    print(f"s={servers}: Wq={result[0]:.3f}, Ws={result[1]:.3f}, ρ={result[2]:.3f}")