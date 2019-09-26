from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
import json
import numpy as np

# Calculate the cost of a circuit
def calculate_cost(qc):
    pass_ = Unroller(['u3', 'cx'])
    pm = PassManager(pass_)
    new_circuit = pm.run(qc) 
    structure = new_circuit.count_ops()
    #print('Cost: ' + str(structure['u3']+structure['cx']*10))
    return structure

# Define registers and a quantum circuit
def adder(inputdata):
    q = QuantumRegister(8)
    c = ClassicalRegister(2)
    qc = QuantumCircuit(q,c)

    #prepare inputs for testing
    
    if inputdata[0] == 1:
        qc.x(q[0])
    if inputdata[1] == 1:
        qc.x(q[1])
    if inputdata[2] == 1:
        qc.x(q[2])

    def AND(a,b,c):
        qc.ccx(q[a], q[b], q[c])
    def OR(a,b,c):
        qc.cx(q[b], q[c])
        qc.cx(q[a], q[c])
        qc.ccx(q[a], q[b], q[c])
    def XOR(a,b,c):
        qc.cx(q[b], q[c])
        qc.cx(q[a], q[c])

    XOR(0,1,3)
    AND(0,1,4)
    qc.barrier(q)
    XOR(2,3,5)
    AND(2,3,6)
    qc.barrier(q)
    OR(4,6,7)
    qc.measure(q[5],c[0])
    qc.measure(q[7],c[1])

    #qc.draw(output='mpl',filename='lc1_circuit.png')

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1000)
    result = job.result()
    count =result.get_counts()
    for key in count:
        #print('Input:' + str(inputdata) + ' Output: ' + str(key))
        print(key+', ', end='')
    struct_ = calculate_cost(qc)
    return struct_

# TEST the circuit for all inputs
out = np.zeros(8)    
for i in range(2):
    for j in range(2):
        for k in range(2):
            if [i,j,k] == [0,0,0]:
                structure = adder([i,j,k])
            else:
                adder([i,j,k])
print('')
'''
# Print results to txt
with open('wk1_output.txt', 'w') as f:
    f.write(json.dumps(structure))
'''







