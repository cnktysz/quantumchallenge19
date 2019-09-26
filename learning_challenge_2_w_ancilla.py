# Importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
import numpy as np
import json
def phase_oracle(circuit, register,oracle_register):
    # Cost: 73
    # u3: 13
    # cx: 6
    circuit.h(oracle_register)
    circuit.x(register[0])
    circuit.ccx(register[0],register[1],oracle_register)
    circuit.x(register[0])
    circuit.h(oracle_register)
def inversion_about_average(circuit, register):
    """Apply inversion about the average step of Grover's algorithm."""
    # Cost: 16
    # u3: 6
    # cx: 1
    circuit.ry(np.pi/2,register)
    circuit.h(register[1])
    circuit.cx(register[0], register[1])
    circuit.h(register[1])
    circuit.ry(-np.pi/2,register)
def calculate_cost(qc):
    pass_ = Unroller(['u3', 'cx'])
    pm = PassManager(pass_)
    new_circuit = pm.run(qc) 
    structure = new_circuit.count_ops()
    #print(structure)
    #print('Cost: ' + str(structure['u3']+structure['cx']*10))  
    return structure  

qr = QuantumRegister(3)
cr = ClassicalRegister(3)

groverCircuit = QuantumCircuit(qr,cr)
groverCircuit.h(qr[0:2])
groverCircuit.x(qr[2])

phase_oracle(groverCircuit, qr,qr[2])
inversion_about_average(groverCircuit, qr[0:2])

groverCircuit.measure(qr,cr)

backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
results = execute(groverCircuit, backend=backend, shots=shots).result()
answer = results.get_counts()

# Print the most probable output
sorted(answer.items(), key=lambda x: x[1], reverse=True)
out = list(answer.keys())[0]
print(out)

struct_ = calculate_cost(groverCircuit)
# Total Cost: 92 
# u3: 22
# cx: 7

with open('wk2_output.txt', 'w') as f:
    f.write(json.dumps(struct_))




