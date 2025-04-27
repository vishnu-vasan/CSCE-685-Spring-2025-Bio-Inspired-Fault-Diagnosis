import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import os

# ===============================
# Define logic gate functions
# ===============================

def AND(a, b):
    """Logical AND gate."""
    return a & b

def OR(a, b):
    """Logical OR gate."""
    return a | b

def NOT(a):
    """Logical NOT gate."""
    return ~a & 1  # Ensures 0/1 output

# ===============================
# Define circuit structure
# ===============================

# Each node is: (function, [input_nodes])
circuit = {
    'A': ('INPUT', []),
    'B': ('INPUT', []),
    'N1': (AND, ['A', 'B']),      # AND gate
    'N2': (NOT, ['A']),           # NOT gate
    'N3': (OR, ['N1', 'N2'])      # OR gate (final output)
}

# ===============================
# Simulation Functions
# ===============================

def evaluate(node, values, fault_node=None, fault_value=None, log=None):
    """
    Recursively evaluates a node in the circuit.
    Injects a stuck-at fault if fault_node and fault_value are given.
    """
    if node in values:
        return values[node]
    
    func, inputs = circuit[node]

    if func == 'INPUT':
        result = values[node]
    else:
        input_vals = [evaluate(inp, values, fault_node, fault_value, log) for inp in inputs]
        result = func(*input_vals)

    if node == fault_node:
        result = fault_value  # Inject fault

    values[node] = result
    if log is not None:
        log[node] = result
    return result

def simulate(inputs, fault_node=None, fault_value=None):
    """
    Simulates the circuit for given inputs.
    Optionally injects a fault at specified node with given stuck value.
    Returns a log of all node outputs.
    """
    values = {'A': inputs['A'], 'B': inputs['B']}
    log = {'A': inputs['A'], 'B': inputs['B']}
    evaluate('N3', values, fault_node, fault_value, log)
    return log

def run_simulation_over_inputs(inputs_list, fault_node=None, fault_value=None):
    """
    Runs simulations over a list of input sets.
    Returns a list of (input_set, simulation_log) tuples.
    """
    logs = []
    for input_set in inputs_list:
        log = simulate(input_set, fault_node=fault_node, fault_value=fault_value)
        logs.append((input_set, log))
    return logs

def compare_logs(healthy_log, faulty_log):
    """
    Compares healthy and faulty simulation logs.
    Returns a dictionary of nodes where outputs differ.
    """
    diffs = {}
    for node in healthy_log:
        if healthy_log[node] != faulty_log.get(node, None):
            diffs[node] = (healthy_log[node], faulty_log[node])
    return diffs

# ===============================
# Visualization Function
# ===============================

def visualize_circuit(circuit, diffs=None, save_path=None):
    """
    Visualizes the circuit using NetworkX.
    - Red nodes indicate fault-affected nodes.
    - If save_path is provided, saves the figure instead of showing.
    """
    G = nx.DiGraph()
    for node, (_, inputs) in circuit.items():
        for inp in inputs:
            G.add_edge(inp, node)

    pos = nx.spring_layout(G, seed=42)
    node_colors = ['red' if diffs and node in diffs else 'lightblue' for node in G.nodes]

    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=2000, font_size=10, arrowsize=20)
    plt.title("Circuit Visualization\n(Red = Fault-Affected Nodes)")
    
    if save_path:
        os.makedirs("../figures", exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

# ===============================
# Example Driver Code
# ===============================

if __name__ == "__main__":
    # Generate all input combinations (A,B)
    all_inputs = [{'A': a, 'B': b} for a, b in product([0, 1], repeat=2)]

    # Healthy simulation
    healthy_runs = run_simulation_over_inputs(all_inputs)

    # Faulty simulation: stuck-at-1 fault at N1
    faulty_runs = run_simulation_over_inputs(all_inputs, fault_node='N1', fault_value=1)

    # Compare and print results
    print("\n🔍 Fault Comparison per Input:")
    # Find first input combination that shows a mismatch
    for (inp_healthy, healthy_log), (inp_faulty, faulty_log) in zip(healthy_runs, faulty_runs):
        diffs = compare_logs(healthy_log, faulty_log)
        if diffs:
            print(f"\nSaving visualization for inputs {inp_healthy} (first detected mismatch)")
            visualize_circuit(circuit, diffs=diffs, save_path="figures/faulty_circuit_visualization.png")
            break
        
        # Visualize the faulty circuit (based on the last input set for example)
        diffs_example = compare_logs(healthy_runs[1][1], faulty_runs[1][1])
        visualize_circuit(circuit, diffs=diffs_example, save_path="faulty_circuit_visualization.png")

        print("\n✅ Simulation complete. Visualization saved as 'faulty_circuit_visualization.png'.")
