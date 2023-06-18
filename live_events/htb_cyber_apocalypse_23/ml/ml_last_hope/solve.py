from qiskit import QuantumCircuit
from qiskit import Aer, transpile

qc = QuantumCircuit.from_qasm_file('./quantum_artifact.qasm')
# Transpile for simulator
simulator = Aer.get_backend('aer_simulator')
circ = transpile(qc, simulator)
result = simulator.run(circ, shots=10, memory=True).result()
memory = result.get_memory(circ)
print(memory)
# HTB{a_gl1mps3_0f_h0p3}