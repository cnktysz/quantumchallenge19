# Importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
import numpy as np
# Grover's Search without ancilla bit
def phase_oracle(circuit, register):
    # Cost: 14 
    # u3: 4
    # cx: 2
    circuit.x(register[0])
    circuit.cz(register[0],register[1])
    circuit.x(register[0])
def inversion_about_average(circuit, register):
    # Cost: 20
    # u3: 10
    # cx: 1
    circuit.h(register)
    circuit.x(register)
    circuit.h(register[1])
    circuit.cx(register[0], register[1])
    circuit.h(register[1])
    circuit.x(register)
    circuit.h(register)
def calculate_cost(qc):
    pass_ = Unroller(['u3', 'cx'])
    pm = PassManager(pass_)
    new_circuit = pm.run(qc) 
    structure = new_circuit.count_ops()
    print(structure)
    print('Cost: ' + str(structure['u3']+structure['cx']*10))    

qr = QuantumRegister(2)
cr = ClassicalRegister(2)

groverCircuit = QuantumCircuit(qr,cr)
groverCircuit.h(qr)

phase_oracle(groverCircuit,qr)
inversion_about_average(groverCircuit, qr)

groverCircuit.measure(qr,cr)

backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
results = execute(groverCircuit, backend=backend, shots=shots).result()
answer = results.get_counts()
print(answer)
	
calculate_cost(groverCircuit)
# Total Cost: 36 
# u3: 16
# cx: 2





