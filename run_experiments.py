import subprocess
import re
import os
import argparse
import numpy as np
import csv

DATA_FILES = {
    "A": "data/data_100_5.json",
    "B": "data/data_150_6.json",
    "C": "data/data_200_7.json",
}
RESULTS_DIR = "results"

def ensure_results_dir():
    """Create the results directory if it doesn't exist."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def parse_glouton_recuit_output(output):
    """Parses the output of the RecuitSimule script."""
    glouton_costs = [float(c) for c in re.findall(r"Fin de glouton\. Meilleure solution: (\d+\.\d+)", output)]
    recuit_costs = [float(c) for c in re.findall(r"Fin du recuit simulé\. Meilleure solution: (\d+\.\d+)", output)]
    exec_times = [float(t) for t in re.findall(r"Terminé en (\d+\.\d+) secondes", output)]
    
    g_times = exec_times[::2]
    rs_times = exec_times[1::2]

    return {
        'G_avg_cost': np.mean(glouton_costs) if glouton_costs else -1,
        'G_best_cost': np.min(glouton_costs) if glouton_costs else -1,
        'G_avg_time': np.mean(g_times) if g_times else -1,
        'RS_avg_cost': np.mean(recuit_costs) if recuit_costs else -1,
        'RS_best_cost': np.min(recuit_costs) if recuit_costs else -1,
        'RS_avg_time': np.mean(rs_times) if rs_times else -1,
    }

def parse_genetique_output(output):
    """Parses the output of the Genetique script."""
    cost_match = re.search(r"COUT MEILLEURE SOLUTION: (\d+\.?\d*)", output)
    time_match = re.search(r"Terminé en (\d+\.\d+) secondes", output)
    return {
        'cost': float(cost_match.group(1)) if cost_match else -1,
        'time': float(time_match.group(1)) if time_match else -1
    }

def parse_tabu_output(output):
    """Parses the output of the Tabu script."""
    cost_match = re.search(r"COUT MEILLEURE SOLUTION: (\d+\.\d+)", output)
    faisabilite_match = re.search(r"RESPECTE CONDITION: (True|False)", output)
    time_match = re.search(r"Terminé en (\d+\.\d+) secondes", output)
    return {
        'cost': float(cost_match.group(1)) if cost_match else -1,
        'faisable': faisabilite_match.group(1) if faisabilite_match else "N/A",
        'time': float(time_match.group(1)) if time_match else -1
    }
    
def print_header(title):
    print("\n" + "="*80)
    print(f"--- {title} ---")
    print("="*80)


# A class to record  the start time and end time of experiments. Takes the name of the experiment and has methods to compute duration and print results
class ExperimentTimer:
    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = subprocess.run(["date", "+%s"], capture_output=True, text=True).stdout.strip()
        self.start_time = int(self.start_time)

    def stop(self):
        self.end_time = subprocess.run(["date", "+%s"], capture_output=True, text=True).stdout.strip()
        self.end_time = int(self.end_time)

    def duration(self):
        if self.start_time is None or self.end_time is None:
            return None
        return self.end_time - self.start_time

    def print_duration(self):
        total_duration = self.duration()
        if total_duration is None:
            print("Experiment timer was not properly started and stopped.")
            return
        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Total duration for {self.name}: {hours}h {minutes}m {seconds}s")


def run_section_4_1_1():
    print_header("Section 4.1.1: Impact de RandFactor")
    csv_path = os.path.join(RESULTS_DIR, "4.1.1_randfactor.csv")
    rand_factors = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.5, 0.75, 1.0]

    timer = ExperimentTimer("Section 4.1.1")
    timer.start()
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Network', 'RandFactor', 'G_Avg_Cost', 'RS_Avg_Cost', 'G_Best_Cost', 'RS_Best_Cost', 'G_Time', 'RS_Time'])
        
        for net_name, filepath in DATA_FILES.items():
            print(f"\n--- Running for Network {net_name} ---")
            for rf in rand_factors:
                print(f"RandFactor: {rf}...")
                cmd = ["python", "RecuitSimule/main.py", filepath, "-r", str(rf), "-n", "5"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                parsed = parse_glouton_recuit_output(result.stdout)
                writer.writerow([net_name, rf, parsed['G_avg_cost'], parsed['RS_avg_cost'], parsed['G_best_cost'], parsed['RS_best_cost'], parsed['G_avg_time'], parsed['RS_avg_time']])
    print(f"\nResults for section 4.1.1 saved to {csv_path}")
    timer.stop()
    timer.print_duration()

def run_section_4_1_2():
    print_header("Section 4.1.2: TFactor et TPalier")
    csv_path = os.path.join(RESULTS_DIR, "4.1.2_tfactor_tpalier.csv")
    rand_factor = 0.4
    tfactors = [0.95, 0.99, 0.995]
    tpaliers = [150, 200, 250, 300]

    timer = ExperimentTimer("Section 4.1.2")
    timer.start()
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Network', 'TFactor', 'TPalier', 'Avg_Cost', 'Best_Cost', 'Time'])
        
        for net_name, filepath in DATA_FILES.items():
            print(f"\n--- Running for Network {net_name} ---")
            for tf in tfactors:
                for tp in tpaliers:
                    print(f"TFactor: {tf}, TPalier: {tp}...")
                    cmd = ["python", "RecuitSimule/main.py", filepath, "-r", str(rand_factor), "-f", str(tf), "-p", str(tp), "-n", "5"]
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    parsed = parse_glouton_recuit_output(result.stdout)
                    writer.writerow([net_name, tf, tp, parsed['RS_avg_cost'], parsed['RS_best_cost'], parsed['RS_avg_time']])
    print(f"\nResults for section 4.1.2 saved to {csv_path}")
    timer.stop()
    timer.print_duration()

def run_section_4_2_1():
    print_header("Section 4.2.1: Influence du nombre de générations (Génétique)")
    csv_path = os.path.join(RESULTS_DIR, "4.2.1_generations.csv")
    generations = [1, 10, 20, 30, 40, 50]
    networks = {"A": DATA_FILES["A"], "B": DATA_FILES["B"], "C": DATA_FILES["C"]}

    timer = ExperimentTimer("Section 4.2.1")
    timer.start()

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Network', 'Generations', 'Time', 'Cost'])
        for net_name, filepath in networks.items():
            for gen in generations:
                print(f"Running GA for Network {net_name} with {gen} generations...")
                cmd = ["python", "Genetique/main.py", filepath, "-g", str(gen)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                parsed = parse_genetique_output(result.stdout)
                writer.writerow([net_name, gen, parsed['time'], parsed['cost']])
    print(f"\nResults for section 4.2.1 saved to {csv_path}")

    timer.stop()
    timer.print_duration()

def run_section_4_2_2():
    print_header("Section 4.2.2: Influence du nombre de cycles (Génétique)")
    csv_path = os.path.join(RESULTS_DIR, "4.2.2_cycles.csv")
    cycles = [1, 5, 10]
    networks = {"A": DATA_FILES["A"], "B": DATA_FILES["B"], "C": DATA_FILES["C"]}

    timer = ExperimentTimer("Section 4.2.2")
    timer.start()
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Network', 'Cycles', 'Time', 'Cost'])
        for net_name, filepath in networks.items():
            for cyc in cycles:
                print(f"Running GA for Network {net_name} with {cyc} cycles...")
                cmd = ["python", "Genetique/main.py", filepath, "-c", str(cyc)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                parsed = parse_genetique_output(result.stdout)
                writer.writerow([net_name, cyc, parsed['time'], parsed['cost']])
    print(f"\nResults for section 4.2.2 saved to {csv_path}")
    timer.stop()
    timer.print_duration()

def run_section_4_2_3():
    print_header("Section 4.2.3: Influence des probabilités de croisement et mutation (Génétique)")
    csv_path = os.path.join(RESULTS_DIR, "4.2.3_probabilities.csv")
    cross_probs = [0.1, 0.5, 0.9, 0.95]
    mut_probs = [0.05, 0.1, 0.2, 0.9]
    filepath = DATA_FILES["A"]

    timer = ExperimentTimer("Section 4.2.3")
    timer.start()
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Mutation_Prob', 'Crossover_Prob', 'Cost'])
        for mut in mut_probs:
            for cross in cross_probs:
                print(f"Running GA for Réseau A with mutation={mut}, cross={cross}...")
                cmd = ["python", "Genetique/main.py", filepath, "-m", str(mut), "-k", str(cross)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                parsed = parse_genetique_output(result.stdout)
                writer.writerow([mut, cross, parsed['cost']])
    print(f"\nResults for section 4.2.3 saved to {csv_path}")
    timer.stop()
    timer.print_duration()

def run_section_4_3_1():
    print_header("Section 4.3.1: Influence de la taille de la liste taboue (Tabu)")
    csv_path = os.path.join(RESULTS_DIR, "4.3.1_tabu_size.csv")
    tabu_sizes = [5, 7, 9, 11, 13, 15]

    timer = ExperimentTimer("Section 4.3.1")
    timer.start()

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Tabu_Size', 'Memories_Active', 'Network', 'Cost', 'Time', 'Feasible'])
        for size in tabu_sizes:
            for mem_active in [False, True]:
                for net_name, filepath in DATA_FILES.items():
                    cmd = ["python", "Tabu/main.py", filepath, "-t", str(size)]
                    if mem_active:
                        cmd.extend(["-m", "-l"])
                    
                    print(f"Running Tabu: Network {net_name}, Size={size}, Mems={'ON' if mem_active else 'OFF'}")
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    parsed = parse_tabu_output(result.stdout)
                    writer.writerow([size, mem_active, net_name, parsed['cost'], parsed['time'], parsed['faisable']])
    print(f"\nResults for section 4.3.1 saved to {csv_path}")
    timer.stop()
    timer.print_duration()

def run_section_4_3_2():
    print_header("Section 4.3.2: Influence des composantes de mémoire (Tabu)")
    csv_path = os.path.join(RESULTS_DIR, "4.3.2_memory_components.csv")
    tabu_size = 9
    scenarios = { "Aucune": [], "Moyen Terme": ["-m"], "Long Terme": ["-l"], "Moyen et long terme": ["-m", "-l"] }

    timer = ExperimentTimer("Section 4.3.2")
    timer.start()
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Scenario', 'Network', 'Cost', 'Time', 'Feasible'])
        for name, flags in scenarios.items():
            for net_name, filepath in DATA_FILES.items():
                cmd = ["python", "Tabu/main.py", filepath, "-t", str(tabu_size)] + flags
                print(f"Running Tabu: Network {net_name}, Scenario='{name}'")
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                parsed = parse_tabu_output(result.stdout)
                writer.writerow([name, net_name, parsed['cost'], parsed['time'], parsed['faisable']])
    print(f"\nResults for section 4.3.2 saved to {csv_path}")
    timer.stop()
    timer.print_duration()

def main():
    ensure_results_dir()
    parser = argparse.ArgumentParser(description="Run experiments for INF6405 TP2.")
    parser.add_argument(
        '--section', 
        type=str, 
        choices=['4.1', '4.1.1', '4.1.2', '4.2', '4.2.1', '4.2.2', '4.2.3', '4.3', '4.3.1', '4.3.2', 'all'],
        default='all',
        help='Which section of the experimental work to run.'
    )
    args = parser.parse_args()

    timer = ExperimentTimer("All experiments")
    timer.start()

    if args.section in ['4.1', '4.1.1', 'all']: run_section_4_1_1()
    if args.section in ['4.1', '4.1.2', 'all']: run_section_4_1_2()
    if args.section in ['4.2', '4.2.1', 'all']: run_section_4_2_1()
    if args.section in ['4.2', '4.2.2', 'all']: run_section_4_2_2()
    if args.section in ['4.2', '4.2.3', 'all']: run_section_4_2_3()
    if args.section in ['4.3', '4.3.1', 'all']: run_section_4_3_1()
    if args.section in ['4.3', '4.3.2', 'all']: run_section_4_3_2()

    timer.stop()
    timer.print_duration()

if __name__ == "__main__":
    main()
