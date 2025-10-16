import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.circuit.library import Initialize
from qiskit.quantum_info import Statevector

# --- New Quantum Circuit Definitions (Multi-Ship, One-Hot Encoding) ---
# --- Maritime Path Overlap Detection using Quantum Parity Check ---

def add_maritime_oracle(qc, n_lanes, n_ships, ship_regs, ancilla_qubits, F_qubit):
    """
    Adds the oracle gates that mark states with collisions directly to the quantum circuit.
    A collision occurs if any two ships are in the same lane.
    
    The logic: For every pair of ships (A, B) and every lane (L):
    1. Compute Parity: anc = shipA[L] XOR shipB[L]
    2. If parity is 0 for ALL lanes, it means the ships occupy different lanes (no collision).
    3. Since we want to mark the collision states, the oracle is slightly inverted:
       Collision is detected when, for any lane L, shipA[L]=1 AND shipB[L]=1 (Parity=0).
    
    The implementation here uses the XOR method to identify the shared lane.
    """
    ancilla_index = 0

    # Compare each pair of ships
    for i in range(n_ships):
        for j in range(i + 1, n_ships):
            shipA = ship_regs[i]
            shipB = ship_regs[j]
            anc = ancilla_qubits[ancilla_index]

            # Compute the bitwise XOR sum of the two ship registers into the ancilla.
            # If the ships are in the same lane (e.g., both 0010), the XOR sum is 0000.
            # If the ships are in different lanes (e.g., 0100 and 0010), the XOR sum is 0110.
            for lane in range(n_lanes):
                # anc = shipA[lane] XOR shipB[lane] XOR anc
                qc.cx(shipA[lane], anc)
                qc.cx(shipB[lane], anc)

            # If the XOR sum is 0, the ships occupy the same set of lanes, meaning COLLISION
            # The current anc is |0> only if XOR sum was 0.
            # We use this |0> state to flip the final flag qubit F.
            
            # FIX: Use 'label=' to prevent the string from being interpreted as a qubit index.
            qc.barrier(label=f"CollisionCheck_{i+1}_{j+1}")

            # If anc = 0 (Collision state), flip F_qubit
            qc.x(anc) # Flip anc to |1> if collision happened
            qc.cx(anc, F_qubit[0]) # Flip F if anc is |1> (i.e., if original anc was |0>)
            qc.x(anc) # Flip anc back

            # Uncompute ancilla for reuse
            for lane in range(n_lanes):
                qc.cx(shipB[lane], anc)
                qc.cx(shipA[lane], anc)

            ancilla_index += 1


def maritime_overlap_multi(n_lanes: int, n_ships: int) -> QuantumCircuit:
    """
    Builds the multi-ship, one-hot encoded collision detection circuit.
    """
    ship_qubits_count = n_lanes * n_ships
    # Calculate required ancilla qubits for pair-wise comparison (n choose 2)
    ancilla_qubits_count = n_ships * (n_ships - 1) // 2 
    F_qubit_count = 1
    total_qubits = ship_qubits_count + ancilla_qubits_count + F_qubit_count

    qc = QuantumCircuit(total_qubits, F_qubit_count)

    # Assign qubit indices
    ship_regs = [list(range(i * n_lanes, (i + 1) * n_lanes)) for i in range(n_ships)]
    ancilla_qubits = list(range(ship_qubits_count, ship_qubits_count + ancilla_qubits_count))
    F_qubit = [total_qubits - 1]

    # ==========================================================
    # 1️⃣ One-hot Uniform Initialization
    # ==========================================================
    # Creates a superposition over all possible lane positions (0001, 0010, 0100, 1000)
    # This prepares the input register for each ship.
    one_hot_state = np.zeros(2**n_lanes, dtype=complex)
    for j in range(n_lanes):
        one_hot_state[2**j] = 1 / math.sqrt(n_lanes)

    init_gate = Initialize(Statevector(one_hot_state))

    qc.barrier(label="INIT_SUPERPOSITION")
    for reg in ship_regs:
        qc.append(init_gate, reg)

    # ==========================================================
    # 2️⃣ Apply Oracle (Collision Detection)
    # ==========================================================
    qc.barrier(label="ORACLE_START")
    add_maritime_oracle(qc, n_lanes, n_ships, ship_regs, ancilla_qubits, F_qubit)
    qc.barrier(label="ORACLE_END")

    # ==========================================================
    # 3️⃣ Measurement
    # ==========================================================
    qc.measure(F_qubit, 0)

    return qc

def run_multi_ship_simulation(n_lanes: int, n_ships: int):
    """Executes the multi-ship quantum circuit using a local simulator."""
    
    # Validation check to prevent massive circuits
    if n_lanes * n_ships > 10:
        st.warning("Warning: Circuit complexity is high. Using a reduced shot count.")
        shots = 512
    else:
        shots = 1024

    qc = maritime_overlap_multi(n_lanes, n_ships)
    
    st.subheader(f"2. Simulation Execution ({n_ships} Ships, {n_lanes} Lanes)")

    # Run the simulation
    backend = AerSimulator()
    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Calculate probability of collision (Result '1' on the Flag qubit)
    collision_prob = counts.get('1', 0) / shots
    
    # --- Professional Results Box ---
    with st.container(border=True): 
        st.subheader("3. Quantum Oracle Measurement")
        
        col_m1, col_m2, col_m3 = st.columns(3)

        with col_m1:
            # Display risk status and metric
            if collision_prob > 0.01:
                st.error(f"🔴 Collision Risk Detected!")
            else:
                st.success(f"🟢 Near-Zero Collision Risk.")

        with col_m2:
            st.metric("Simulated P(Collision / Flag='1')", f"{collision_prob:.4f}", help="Probability that the collision flag qubit (F) is measured as '1' across all possible lane assignments.")
        
        with col_m3:
            st.metric("Total Qubits Used", qc.num_qubits, help=f"Ships: {n_lanes*n_ships}, Ancilla: {n_ships*(n_ships-1)//2}, Flag: 1")
            st.metric("Simulation Shots", shots)

        st.markdown(f"*(This measurement reflects the chance of **any** two ships sharing the same lane in a uniformly prepared quantum superposition of all lane states.)*")
    
    # --- Detailed Views ---
    with st.expander("View Detailed Quantum Results and Circuit Breakdown"):
        st.subheader("4. Circuit Diagram")
        st.markdown("The complexity increases exponentially with more ships/lanes.")
        st.pyplot(qc.draw(output='mpl', style={'fontsize': 8}))
        
        st.subheader("5. Measurement Histogram")
        st.markdown("The height of the '1' bar corresponds to the collision probability.")
        fig = plot_histogram(counts, title=f"F-Qubit Measurement: {n_ships} Ships, {n_lanes} Lanes")
        st.pyplot(fig)


# --- Streamlit UI and Execution ---

st.set_page_config(layout="wide", page_title="Qiskit Multi-Ship Collision Avoidance")

st.title("🚢 Q-Route: Multi-Ship Quantum Collision Management")
st.caption("Using Qiskit to calculate maritime collision risk in superposition.")
st.markdown("---")

# Main explanatory text moved to the top container
st.markdown("""
This application models a multi-ship scenario using a **Quantum Oracle** to compute the overall collision risk.
The underlying quantum circuit is initialized into a **superposition of all possible lane assignments**, and then a **parity check oracle** flags any state where two or more ships occupy the same lane (a collision).
The resulting probability of the Flag Qubit being $|1\rangle$ is the total collision risk for the given scenario.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Scenario Parameters")
    
    n_lanes = st.slider("Number of Available Lanes (N)", 2, 5, 4, key="n_lanes", help="Each lane is a qubit in the one-hot encoding for a ship's position.")
    n_ships = st.slider("Number of Ships (M)", 2, 4, 3, key="n_ships", help="The number of ships checked for pairwise collisions.")

    st.markdown("---")
    
    if st.button("Run Quantum Collision Simulation", type="primary", use_container_width=True):
        if n_ships > n_lanes:
            st.error("Cannot run simulation: The number of ships cannot exceed the number of lanes.")
        else:
            run_multi_ship_simulation(n_lanes, n_ships)

with col2:
    st.header("Quantum Circuit Architecture")
    st.info("The Oracle detects if *any* pair of ships occupies the same lane.")
    
    with st.expander("Detailed Logic Breakdown", expanded=True):
        st.markdown("""
        The system uses the **One-Hot Encoding Model** and a **Parity-Based Oracle** for collision detection.
        
        #### **1. Encoding and Initialization**
        * Each ship has a register of $N$ qubits (lanes).
        * The register is prepared in a **uniform superposition** of all valid **one-hot states** (e.g., $|0010\rangle$ or $|0100\rangle$).
        
        #### **2. Oracle Function**
        * A parity check is run for every possible pair of ships (A and B).
        * It computes the **XOR sum** of their lane registers into an ancilla qubit.
        * If the XOR sum is **zero**, it means the ships are in the **exact same lane** (collision state).
        * The oracle then flips the **Flag Qubit (F)** to $|1\rangle$ when a collision is detected.
        
        The final measurement of $F=|1\rangle$ gives the total collision risk probability.
        """)
    
    st.image("https://placehold.co/600x200/22c55e/ffffff?text=Maritime+Lane+Risk+Map+Visual", caption="Conceptual visualization of a lane risk map.")
