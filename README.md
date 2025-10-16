# ⚓ Quantum Maritime Path Overlap Detection using Qiskit and Real-Time Simulation  

This project demonstrates how **quantum computing** can be used to detect potential **maritime path overlaps or ship collisions** by modeling navigation lanes as **quantum registers**.

---

## 🚀 Project Title  
**Quantum Maritime Path Overlap Detection using Qiskit and Real-Time Simulation**

---

## 🧭 Project Overview  
This project leverages **quantum computing principles** to identify when two or more ships occupy the same maritime lane (collision or overlap scenario).  

It uses:
- 🧠 **Qiskit** — to simulate quantum circuits that detect overlapping lane assignments (collisions).  
- 🌍 **Folium (Leaflet Map)** — to visualize ship positions and collision risks dynamically.  
- ⚙️ **Optional Real-Time Simulation** — animates ship movement and highlights collisions in red.  

---

## 🧩 Key Features  
✅ Quantum circuit that detects ship-lane overlaps (using **Toffoli-based oracle**).  
✅ Probabilistic analysis — both **theoretical** and **quantum-simulated** collision probabilities.  
✅ Interactive **map visualization** (using Folium).  
✅ Optional **animated mode** — ships move in real time; collisions flash red.  
✅ Exportable **`quantum_maritime_collision.html`** map for live web demo.  

---

## ⚗️ Tech Stack  
| Category | Tools / Libraries |
|-----------|------------------|
| Quantum Simulation | `qiskit`, `qiskit-aer` |
| Visualization | `matplotlib`, `folium` |
| Math & Randomization | `numpy`, `math`, `random` |
| Environment | Jupyter Notebook / Google Colab |

<img width="623" height="233" alt="Tech Stack" src="https://github.com/user-attachments/assets/62d931d2-5e37-437c-9651-35760eabb856" />

---

## 🧠 Concept Behind the Project  
Each ship is represented as a **quantum register** encoding which lane it occupies.  
A **quantum oracle** checks if any two ships share the same lane.  
If so, a **flag qubit (F)** is flipped → **collision detected (F=1)**.  

The algorithm can detect overlaps across all possible lane assignments **simultaneously**, leveraging **quantum parallelism**.  

---

## 🧮 Workflow  
<img width="645" height="313" alt="Workflow Diagram" src="https://github.com/user-attachments/assets/c9037f61-2e19-4d50-80bd-94a24945c4bf" />

| Step | Description |
|------|--------------|
| 1️⃣ | Define number of lanes and ships. |
| 2️⃣ | Initialize all ships into superposition (all lane combinations). |
| 3️⃣ | Apply quantum oracle to mark collision states. |
| 4️⃣ | Measure the final qubit F (1 = overlap detected). |
| 5️⃣ | Plot probabilities and visualize results on a map. |

---

## 📊 Outputs  

### 🧩 Quantum Simulation Result  
Example console output:
Measurement results for 8192 shots (F=1 means overlap detected):
{'0': 3125, '1': 5067}
Theoretical probability of collision: 0.6172
Simulated probability of collision: 0.6193

---

### 📈 Bar Chart Visualization  
<img width="623" height="233" alt="Quantum Result Chart" src="https://github.com/user-attachments/assets/151e26bf-509f-4c02-8116-34a0ae5d99c6" />

---

### 🌍 Interactive Map Output  
File generated: **`quantum_maritime_collision.html`**  
<img width="1366" height="768" alt="Interactive Map" src="https://github.com/user-attachments/assets/089f3433-3a3c-4c18-add9-4593520ee38a" />

**Legend:**  
🟦 Blue circles → Ships in safe lanes  
🟥 Red circles → Ships sharing same lane (**collision risk**)  
📊 Floating box → Displays simulated + theoretical probabilities  

---

## 🗂️ Repository Structure
📦 Quantum-Maritime-Overlap
┣ 📜 README.md
┣ 📜 quantum_maritime_collision.py
┣ 📜 quantum_maritime_overlap.ipynb
┣ 📊 quantum_maritime_collision.html
┣ 📂 assets/
┃ ┗ 📈 chart_example.png
┣ 📜 requirements.txt
┗ 📜 LICENSE

---

## ⚙️ Setup Instructions
```bash
# Clone repository
git clone https://github.com/your-username/Quantum-Maritime-Overlap.git
cd Quantum-Maritime-Overlap

# Install dependencies
pip install qiskit qiskit-aer matplotlib numpy folium

Run the simulation:
python quantum_maritime_collision.py

or open the notebook:
jupyter notebook quantum_maritime_overlap.ipynb
🌊 Future Enhancements
⏱️ Real-time animated ship movements on map
🛰️ Integration with live AIS data for real ship tracking
⚡ Quantum optimization for collision avoidance routes
📊 Web dashboard using Streamlit or Plotly
💡 Use Cases
     Early detection systems for maritime traffic congestion
     Port navigation safety research using quantum models
     Quantum computing education with a real-world scenario
