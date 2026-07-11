import pandas as pd
import heapq
import matplotlib.pyplot as plt
import copy
import os
import sys

# BASE_DIR setup to work as both script and exe
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def schedule_jobs(file_path, bay2, bay3):
    LOADING_TIME = 10 * 60

    # 1. Initialize Machines Dynamically
    machines_bay2 = [(0, f"Bay2_Machine_{i+1}", 0) for i in range(bay2)]
    machines_bay3 = [(0, f"Bay3_Machine_{i+1}", 0) for i in range(bay3)]
    all_machines = machines_bay2 + machines_bay3
    heapq.heapify(all_machines)

    # 2. Read CSV
    try:
        df = pd.read_excel(file_path)
        df.rename(columns=lambda x: x.strip().replace('\n', ' '), inplace=True)
        df['BAY'] = pd.to_numeric(df['BAY'], errors='coerce').fillna(0).astype(int)
        df['BATCHES'] = pd.to_numeric(df['BATCHES'], errors='coerce').fillna(0).astype(int)
        df['PLATING IN SECONDS'] = pd.to_numeric(df['PLATING IN SECONDS'], errors='coerce').fillna(0)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return [], 0, {}

    # 3. Create Job List
    jobs = []
    for _, row in df.iterrows():
        for i in range(row['BATCHES']):
            jobs.append({
                'Part Number': f"{row['PART NUMBER']}_Batch_{i+1}",
                'Processing Time': row['PLATING IN SECONDS'],
                'Bay': row['BAY']
            })

    jobs_bay2 = sorted([j for j in jobs if j['Bay'] == 2], key=lambda x: x['Processing Time'], reverse=True)
    jobs_bay3 = sorted([j for j in jobs if j['Bay'] == 3], key=lambda x: x['Processing Time'], reverse=True)

    # 4. Scheduling Logic
    schedule = []
    transporter_free_at = 0
    total_jobs = len(jobs_bay2) + len(jobs_bay3)
    
    while len(schedule) < total_jobs:
        m_finish, m_id, m_work = heapq.heappop(all_machines)
        target_list = jobs_bay2 if 'Bay2' in m_id else jobs_bay3
        
        if target_list:
            job = target_list.pop(0)
            load_start = max(m_finish, transporter_free_at)
            proc_start = load_start + LOADING_TIME
            end_time = proc_start + job['Processing Time']
            
            schedule.append({'Machine': m_id, 'Part Number': job['Part Number'], 
                             'Loading Start': load_start, 'Processing Start': proc_start, 
                             'End Time': end_time, 'Processing Time': job['Processing Time']})
            
            transporter_free_at = proc_start
            heapq.heappush(all_machines, (end_time, m_id, m_work + job['Processing Time']))
        else:
            heapq.heappush(all_machines, (m_finish, m_id, m_work))
            break 

    # 5. Dynamic Utilization Calculation
    total_time = max((e['End Time'] for e in schedule), default=0)
    machine_utilization = {}
    if total_time > 0:
        all_m_ids = [f"Bay2_Machine_{i+1}" for i in range(bay2)] + [f"Bay3_Machine_{i+1}" for i in range(bay3)]
        for m_id in all_m_ids:
            busy = sum(e['Processing Time'] for e in schedule if e['Machine'] == m_id)
            machine_utilization[m_id] = (busy / total_time) * 100

    return schedule, total_time, machine_utilization

if __name__ == '__main__':
    # Catch dynamic inputs from main.py via sys.argv
    b2 = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    b3 = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    input_file = os.path.join(BASE_DIR, "output", "scheduler_input.xlsx")
    final_schedule, total_time, util = schedule_jobs(input_file, b2, b3)

    # Save Output
    if final_schedule:
        output_excel = os.path.join(BASE_DIR, "output", "scheduler_output.xlsx")
        # Create DataFrame
        
         # Create DataFrame
        df_out = pd.DataFrame(final_schedule)

        # Rename columns
        df_out.rename(
            columns={
                "Machine": "Load",
                "Part Number": "Part"
            },
            inplace=True
        )

        # Keep only first 2 columns
        df_out = df_out[["Load", "Part"]]
        

        df_out["Load Start Time"] = ""
        df_out["Load End Time"] = ""
        df_out["Comments"] = ""

        with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
            df_out.to_excel(
                writer,
                index=False,
                sheet_name="Scheduler Output"
            )

        print(f"Schedule generated for {b2} Bay2 tanks and {b3} Bay3 tanks.")

        # Print Summary
        bay2_util = sum(u for m, u in util.items() if "Bay2" in m) / b2 if b2 > 0 else 0
        bay3_util = sum(u for m, u in util.items() if "Bay3" in m) / b3 if b3 > 0 else 0
        print(f"Bay 2 Avg Utilization: {bay2_util:.2f}%")
        print(f"Bay 3 Avg Utilization: {bay3_util:.2f}%")