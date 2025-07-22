'''
    -Grover Simulation
    -Author: Chase hurwitz
    -This code is created to simulate Grover's Algorithm with 4 qubits, trying to guess a target state of 4 bits.

1. Initialization: we create a quantum circuit with 4 qubits and 4 matching classical bits. 
2.  Superposition: Hadamard gates are applied to all qubits, placing them in a uniform superposition of all 16 possible solutions.
3.  Oracle Construction: We marked the target key |1011> by flipping any qubit where the target bit was 0. Then, we apply multi-controlled-Z operations, and then unflip those qubits which inverts the amplitude of the target key.
4.  Diffusion Operator: We apply another round of Hadamard, X, and multi-controlled-Z gates to reflect the amplitudes over the mean.
5.  Measurement and Simulation: We added measurement gates to all qubits and simulated the circuit 1024 times (an appropriately large number to see meaningful trends). 

'''


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt


# Parameters
n = 4

## The targest state |1011> is represented as [1,1,0,1]
## because Qiskit indexes left to right aka, Qiskit
## recognizes Big Endian format where the least significant
## byte is stored at the lowest memory address. So, [1,1,0,1] = "1011" 

target = [1, 1, 0, 1]  # The target state |1011> (see note above)

# Setup
qr = QuantumRegister(n, 'q')
cr = ClassicalRegister(n, 'c')
grover_circuit = QuantumCircuit(qr, cr)

# --- Step 1: Apply superposition ---
grover_circuit.h(qr)

# --- Step 2: Oracle for |1011> ---
# Flip qubits that are 0 in the target (i.e., q[1])
for i, bit in enumerate(target):
    if bit == 0:
        grover_circuit.x(qr[i])

# Apply multi-controlled-Z (by conjugating H and using MCX)
grover_circuit.h(qr[3])
grover_circuit.mcx(qr[0:3], qr[3])  # Control on q[0], q[1], q[2]
grover_circuit.h(qr[3])

# Unflip the X gates
for i, bit in enumerate(target):
    if bit == 0:
        grover_circuit.x(qr[i])

# --- Step 3: Diffusion operator ---
grover_circuit.h(qr)
grover_circuit.x(qr)

# Apply multi-controlled-Z
grover_circuit.h(qr[3])
grover_circuit.mcx(qr[0:3], qr[3])
grover_circuit.h(qr[3])

grover_circuit.x(qr)
grover_circuit.h(qr)


# --- Visualize Statevector BEFORE measurement ---
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_state_city

# Get statevector before measurement
state = Statevector.from_instruction(grover_circuit)

# Plot Bloch spheres
plot_bloch_multivector(state)
plt.savefig("bloch_multivector.png")
plt.close()

# Plot state city (real/imag amplitude bar plots)
plot_state_city(state, title="Statevector - Before Measurement")
plt.savefig("state_city.png")
plt.close()


# --- Step 4: Measure ---
grover_circuit.draw(output='mpl')
plt.savefig("grover_circuit.png")
plt.close()
grover_circuit.measure(qr, cr)

# --- Run simulation ---
sim = AerSimulator()
result = sim.run(grover_circuit, shots=1024).result()
counts = result.get_counts()

print("Measurement counts:", counts)
plot_histogram(counts, title="Measurement Results")
plt.savefig("grover_histogram.png")
plt.close()

