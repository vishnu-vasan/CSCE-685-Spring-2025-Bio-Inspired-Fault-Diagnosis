# === bayesian_diagnosis.py ===
from typing import List, Dict

# ==================================
# Logic Simulation Function
# ==================================

def simulate_logic(inputs: Dict[str, int], fault_states: Dict[str, int]) -> int:
    """
    Simulate the circuit logic based on inputs and optional fault states.
    Circuit Logic:
    - X = A AND B
    - Y = NOT A
    - Z = X OR Y
    """
    A = inputs['A']
    B = inputs['B']

    X = fault_states.get('X') if 'X' in fault_states else (A and B)
    Y = fault_states.get('Y') if 'Y' in fault_states else (~A & 1)  # NOT A, ensure 0/1
    Z = X or Y

    return Z

# ==================================
# Bayesian Update Function
# ==================================

def bayesian_update(fault_probs: Dict[str, float], observations: List[Dict]) -> Dict[str, float]:
    """
    Update fault probabilities using Bayesian inference based on a series of observations.
    """
    fault_probs = fault_probs.copy()  # Avoid modifying original

    for idx, obs in enumerate(observations):
        A, B = obs['inputs']
        Z_obs = obs['Z_observed']

        print(f"\n🔎 Processing Observation {idx+1}: Inputs (A={A}, B={B}), Observed Z={Z_obs}")

        likelihoods = {}
        for fault_type in fault_probs:
            gate, stuck_val = fault_type.split('_')
            stuck_val = int(stuck_val)

            # Simulate output assuming a fault at this gate
            inputs = {'A': A, 'B': B}
            faulty_output = simulate_logic(inputs, {gate: stuck_val})

            likelihoods[fault_type] = 1.0 if faulty_output == Z_obs else 0.01

        # Bayesian update
        for fault_type in fault_probs:
            fault_probs[fault_type] *= likelihoods[fault_type]

        # Normalize
        total = sum(fault_probs.values())
        for k in fault_probs:
            fault_probs[k] /= total

    return fault_probs

# ==================================
# Example Usage: Running Diagnosis
# ==================================

def run_bayesian_fault_diagnosis():
    """
    Example demonstration of Bayesian fault diagnosis for a simple circuit.
    """
    # Define prior fault probabilities
    fault_probs = {
        'X_0': 0.005,  # X stuck-at-0
        'X_1': 0.005,  # X stuck-at-1
        'Y_0': 0.005,  # Y stuck-at-0
        'Y_1': 0.005   # Y stuck-at-1
    }

    # Observations
    observations = [
        {'inputs': (1, 1), 'Z_observed': 0},  # Unexpected output
        {'inputs': (0, 0), 'Z_observed': 1}   # Normal output
    ]

    # Run Bayesian update
    updated_fault_probs = bayesian_update(fault_probs, observations)

    # Print results
    print("\n📊 Updated Fault Probabilities after Observations:")
    for fault, prob in updated_fault_probs.items():
        print(f"{fault}: {prob * 100:.4f}%")

if __name__ == "__main__":
    run_bayesian_fault_diagnosis()
