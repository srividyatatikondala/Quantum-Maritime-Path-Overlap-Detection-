"""
Quantum Maritime Path Overlap Detection
---------------------------------------
Detects potential ship-lane overlaps using Quantum Computing.
Implements a Toffoli-based oracle and visualizes results.
"""

# 🧠 Imports
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import folium

# -----------------------------------------------------------
# 🧩 1. Quantum Oracle Definition
# -----------------------------------------------------------
def add_maritime_oracle(qc, n_lanes, n_ships, ship_regs, ancilla_qubits, F_qubit):
    """
    Adds the oracle gates that mark states with collisions directly to the quantum circuit.
    A collision occurs if any two ships occupy the same lane.
    """
    pair_index = 0
    for i in range(n_ships):
        for k in range(i + 1, n_ships):
            for j in range(n_lanes):
                # Check if ship i and ship k are in the same lane j
                controls = [ship_regs[i][j], ship_regs[k][j]]
                target = ancilla_qubits[pair_index]
                qc.ccx(controls[0], controls[1], target)
            pair_index += 1

    # If any pair shares a lane → flip final flag qubit (F)
    qc.mcx(ancilla_qubits, F_qubit[0])

    # Uncompute oracle to reset ancillas
    pair_index = 0
    for i in range(n_ships):
        for k in range(i + 1, n_ships):
            for j in range(n_lanes):
                controls = [ship_regs[i][j], ship_regs[k][j]]
                target = ancilla_qubits[pair_index]
                qc.ccx(controls[0], controls[1], target)
            pair_index += 1


# -----------------------------------------------------------
# ⚙️ 2. Maritime Overlap Circuit Construction
# -----------------------------------------------------------
def maritime_overlap_multi(n_lanes=4, n_ships=3):
    """
    Quantum circuit to detect overlaps between multiple ships.
    """
    ship_qubits_count = n_lanes * n_ships
    ancilla_qubits_count = n_ships * (n_ships - 1) // 2
    F_qubit_count = 1
    total_qubits = ship_qubits_count + ancilla_qubits_count + F_qubit_count

    qc = QuantumCircuit(total_qubits, F_qubit_count)

    ship_regs = [list(range(i * n_lanes, (i + 1) * n_lanes)) for i in range(n_ships)]
    ancilla_qubits = list(range(ship_qubits_count, ship_qubits_count + ancilla_qubits_count))
    F_qubit = [total_qubits - 1]

    # Initialize superposition for ships’ possible lane states
    for reg in ship_regs:
        qc.h(reg)

    add_maritime_oracle(qc, n_lanes, n_ships, ship_regs, ancilla_qubits, F_qubit)

    # Measure the final overlap flag
    qc.measure(F_qubit, 0)
    return qc


# -----------------------------------------------------------
# 🚀 3. Run Simulation
# -----------------------------------------------------------
if __name__ == "__main__":
    N_LANES = 4
    N_SHIPS = 3

    qc = maritime_overlap_multi(n_lanes=N_LANES, n_ships=N_SHIPS)
    backend = AerSimulator()
    shots = 8192
    qc_transpiled = transpile(qc, backend)
    result = backend.run(qc_transpiled, shots=shots).result()
    counts = result.get_counts()

    print(f"\n🔹 Measurement results for {shots} shots (F=1 means overlap detected):")
    print(counts)

    # --- Theoretical Probability ---
    total_states = N_LANES ** N_SHIPS
    if N_LANES >= N_SHIPS:
        no_collision_states = math.factorial(N_LANES) / math.factorial(N_LANES - N_SHIPS)
    else:
        no_collision_states = 0
    collision_states = total_states - no_collision_states
    prob_collision_theoretical = collision_states / total_states

    # --- Simulated Probability ---
    agg_counts = {'0': 0, '1': 0}
    for outcome, count in counts.items():
        agg_counts[outcome] += count
    prob_collision_simulated = agg_counts.get('1', 0) / shots

    print(f"\n📊 Theoretical probability of collision: {prob_collision_theoretical:.4f}")
    print(f"📈 Simulated probability of collision (F=1): {prob_collision_simulated:.4f}")

    # -----------------------------------------------------------
    # 🎨 4. Visualization
    # -----------------------------------------------------------
    plt.figure(figsize=(7, 5))
    outcomes = list(agg_counts.keys())
    probabilities = [agg_counts[o]/shots for o in outcomes]
    colors = ['#2ca02c' if o=='0' else '#d62728' for o in outcomes]
    bars = plt.bar(outcomes, probabilities, color=colors, zorder=2)
    plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
    plt.xlabel("F (Final Overlap Flag)", fontsize=12)
    plt.ylabel("Probability", fontsize=12)
    plt.title(f"Maritime Path Overlap Detection ({N_SHIPS} Ships, {N_LANES} Lanes)", fontsize=14)
    plt.xticks([0, 1], [f"No Overlap (F=0)\n{agg_counts.get('0', 0)} counts",
                        f"Overlap Detected (F=1)\n{agg_counts.get('1', 0)} counts"])
    plt.ylim(0, 1)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2%}', ha='center', va='bottom')
    plt.show()

    # -----------------------------------------------------------
    # 🌍 5. Folium Map Visualization
    # -----------------------------------------------------------
    print("\nGenerating interactive map...")
    center_coord = [15.3, 73.8]
    m = folium.Map(location=center_coord, zoom_start=8, tiles="CartoDB positron")

    # Define lane coordinates
    lane_start_lat, lane_end_lat = center_coord[0] - 0.5, center_coord[0] + 0.5
    lane_lons = np.linspace(center_coord[1] - 0.5, center_coord[1] + 0.5, N_LANES)

    # Draw lanes on map
    for i, lon in enumerate(lane_lons):
        folium.PolyLine(
            locations=[[lane_start_lat, lon], [lane_end_lat, lon]],
            tooltip=f"Lane {i}",
            color='gray',
            dash_array='5, 5'
        ).add_to(m)

    # Simulate one possible scenario
    ship_positions = {}
    lane_assignments = [random.randint(0, N_LANES - 1) for _ in range(N_SHIPS)]
    collision_lanes = {lane for lane in lane_assignments if lane_assignments.count(lane) > 1}

    for i in range(N_SHIPS):
        ship_name = f"Ship-{chr(65+i)}"
        assigned_lane = lane_assignments[i]
        lat = random.uniform(lane_start_lat, lane_end_lat)
        lon = lane_lons[assigned_lane]
        is_collision = assigned_lane in collision_lanes
        color = "red" if is_collision else "blue"

        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=f"<b>{ship_name}</b><br>Lane: {assigned_lane}<br>Status: {'Collision Risk' if is_collision else 'Clear'}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # Quantum results box
    text_to_display = f"""
        <div style="position: fixed; top: 10px; left: 10px; z-index:9999;
        font-size:14px; background-color: rgba(255, 255, 255, 0.8);
        padding: 5px; border-radius: 5px; border: 1px solid grey;">
            <b>Quantum Simulation Results</b><br>
            ({N_SHIPS} Ships, {N_LANES} Lanes)<br>
            Simulated Collision Prob: <b>{prob_collision_simulated:.2%}</b><br>
            Theoretical Collision Prob: <b>{prob_collision_theoretical:.2%}</b>
        </div>
    """
    m.get_root().html.add_child(folium.Element(text_to_display))

    map_filename = "quantum_maritime_collision.html"
    m.save(map_filename)
    print(f"✅ Interactive map saved as {map_filename}")
