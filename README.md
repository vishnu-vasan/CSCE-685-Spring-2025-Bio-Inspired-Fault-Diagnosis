# Leveraging Biological Network Models to Enhance Fault Diagnosis in Integrated Circuits

# CSCE 685 - Spring '25:
# 234009303 - Vishnuvasan Raghuraman
# Advisor - Prof. Dr. Duncan Walker
# Fault Diagnosis in Digital Circuits Inspired by Biological Networks

## Overview
This project implements a simple yet powerful approach to fault modeling, Bayesian fault diagnosis, and sensitivity analysis in digital circuits, inspired by concepts from Gene Regulatory Networks (GRNs).

`stuck-at` faults in logic circuits are modeled, and fault probabilities inferred from observed outputs using Bayesian updating, and sensitivity analysis performed to quantify the criticality of different gates.

## Project Structure
- `scripts/` : Core Python scripts for fault modeling, diagnosis, and sensitivity analysis.
- `notebooks/` : Main demonstration notebook (`main.ipynb`) showing the full workflow.
- `figures/` : Generated diagrams, sensitivity plots, and other visualizations.

## How to Run
1. Install required libraries:
   ```bash
   pip install matplotlib networkx
   ```
2. Open and run `notebooks/main.ipynb` to see the full demonstration.
3. (Optional) You can run individual scripts directly:
   ```bash
   python scripts/fault_modeling.py
   python scripts/bayesian_diagnosis.py
   python scripts/sensitivity_analysis.py
   ```

## Dependencies
- Python 3.x
- matplotlib
- networkx

## Acknowledgements
Inspired by biological fault analysis principles commonly used in Gene Regulatory Networks (GRNs).
