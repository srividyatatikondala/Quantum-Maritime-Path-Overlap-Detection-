# Quantum-Maritime-Path-Overlap-Detection-
This project demonstrates how quantum computing can be used to detect potential maritime path overlaps or ship collisions by modeling navigation lanes as quantum registers.
🚀 Project Title

Quantum Maritime Path Overlap Detection using Qiskit and Real-Time Simulation

🧭 Project Overview

This project demonstrates how quantum computing can be used to detect potential maritime path overlaps or ship collisions by modeling navigation lanes as quantum registers.

It uses:

🧠 Qiskit to simulate quantum circuits that detect overlapping lane assignments (collisions).
🌍 Folium (Leaflet map) to visualize ship positions and collision risks dynamically.
⚙️ Optional real-time simulation that animates ship movement and highlights collisions in red.

🧩 Key Features

✅ Quantum circuit that detects ship-lane overlaps (using Toffoli-based oracle).

✅ Probabilistic analysis — both theoretical and quantum-simulated collision probabilities.

✅ Interactive map visualization (using Folium).

✅ Optional animated mode: ships move in real-time; collisions flash red.

✅ Exportable quantum_maritime_collision.html map for live web demo.

⚗️ Tech Stack

<img width="650" height="257" alt="image" src="https://github.com/user-attachments/assets/814d4eeb-5bda-4a7c-bbfb-c11889ca671c" />

🧠 Concept Behind the Project

Each ship is represented as a quantum register encoding which lane it occupies.

A quantum oracle checks if any two ships share the same lane.

If so, a flag qubit (F) is flipped → collision detected (F=1).
The algorithm can detect overlaps across all possible lane assignments simultaneously, leveraging quantum parallelism. 

🧮 Workflow
<img width="645" height="313" alt="image" src="https://github.com/user-attachments/assets/c9037f61-2e19-4d50-80bd-94a24945c4bf" />


📊 Outputs

Quantum Simulation Result

Example console output:

Measurement results for 8192 shots (F=1 means overlap detected):
{'0': 3125, '1': 5067}
Theoretical probability of collision: 0.6172
Simulated probability of collision: 0.6193


Bar Chart Visualization

Interactive Map Output

File generated: quantum_maritime_collision.html

Blue circles → ships in safe lanes

Red circles → ships sharing same lane (collision risk)

Live result box with simulated + theoretical probabilities
