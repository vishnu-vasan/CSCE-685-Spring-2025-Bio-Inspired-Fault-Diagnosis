# === sensitivity_analysis.py ===
import matplotlib.pyplot as plt
from itertools import product
import os

# === 1. Define Logic Gate Functions ===
def AND(a, b): return a & b
def OR(a, b): return a | b
def NOT(a): return ~a & 1  # Ensures output is 0/1 only

# === 2. Define the Circuit Structure ===
# Format: node_name: (function, [input_nodes])
circuit = {
    'A': ('INPUT', []),
    'B': ('INPUT', []),
    'N1': (AND, ['A', 'B']),
    'N2': (NOT, ['A']),
    'N3': (OR, ['N1', 'N2'])  # Final output
}

# === 3. Evaluate Logic Recursively ===
def evaluate(node, values, fault_node=None, fault_value=None, log=None):
    """
    Recursively evaluate the circuit output for a node, with optional fault injection.
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

# === 4. Simulate Circuit ===
def simulate(inputs, fault_node=None, fault_value=None):
    """
    Simulate the circuit given inputs and optional fault.
    """
    values = {'A': inputs['A'], 'B': inputs['B']}
    log = {'A': inputs['A'], 'B': inputs['B']}
    evaluate('N3', values, fault_node, fault_value, log)
    return log

# === 5. Gate Sensitivity Analysis ===
def gate_sensitivity_analysis(circuit, all_inputs):
    """
    Perform fault sensitivity analysis for each gate (excluding input nodes).
    Returns sensitivity scores between 0 and 1.
    """
    fault_types = [0, 1]  # stuck-at-0, stuck-at-1
    gate_sensitivity = {}

    for gate in circuit:
        if circuit[gate][0] == 'INPUT':
            continue  # Skip inputs

        total_tests = 0
        mismatches = 0

        for fault_val in fault_types:
            for inp in all_inputs:
                healthy_log = simulate(inp)
                faulty_log = simulate(inp, fault_node=gate, fault_value=fault_val)

                if healthy_log['N3'] != faulty_log['N3']:
                    mismatches += 1
                total_tests += 1

        gate_sensitivity[gate] = mismatches / total_tests

    return gate_sensitivity

# === 6. Plot Sensitivity ===
def plot_sensitivity(sensitivity, save_path=None):
    """
    Plot sensitivity scores as a bar chart.
    If save_path is provided, saves the plot to the specified path.
    Otherwise, shows the plot interactively.
    """
    gates = list(sensitivity.keys())
    scores = list(sensitivity.values())

    plt.figure(figsize=(6, 4))
    plt.bar(gates, scores, color='tomato')
    plt.ylim(0, 1.1)
    plt.ylabel("Sensitivity Score")
    plt.title("Gate Fault Sensitivity Analysis")
    plt.grid(True, linestyle='--', alpha=0.6)

    if save_path:
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        print(f"📁 Sensitivity plot saved to: {save_path}")
    else:
        plt.show()

# === 7. Example Usage ===
def run_sensitivity_analysis(save_fig=True):
    """
    Example usage: runs sensitivity analysis and plots results.
    If save_fig is True, saves figure to figures/sensitivity_plot.png.
    """
    all_inputs = [{'A': a, 'B': b} for a, b in product([0, 1], repeat=2)]

    sensitivity = gate_sensitivity_analysis(circuit, all_inputs)

    print("\n🔬 Sensitivity Scores (1.0 = always causes fault):")
    for gate, score in sensitivity.items():
        print(f"{gate}: {score:.2f}")

    if save_fig:
        plot_sensitivity(sensitivity, save_path="../figures/sensitivity_plot.png")
    else:
        plot_sensitivity(sensitivity)

if __name__ == "__main__":
    run_sensitivity_analysis(save_fig=True)
