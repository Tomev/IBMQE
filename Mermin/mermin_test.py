import sys
sys.path.append('../') # where Qconfig.py is placed

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from methods import run_main_loop
import numpy as np

def get_mermin_circuits():
    # 3 - qubits 
    # quantum circuit to make GHZ state 
    q3 = QuantumRegister(3)
    c3 = ClassicalRegister(3)
    ghz3 = QuantumCircuit(q3, c3)
    ghz3.h(q3[0])
    ghz3.cx(q3[0],q3[1])
    ghz3.cx(q3[0],q3[2])

    # quantum circuit to measure XXX
    measureXXX = QuantumCircuit(q3, c3)
    measureXXX.h(q3[0])
    measureXXX.h(q3[1])
    measureXXX.h(q3[2])
    measureXXX.measure(q3[0], c3[0])
    measureXXX.measure(q3[1], c3[1])
    measureXXX.measure(q3[2], c3[2])
    ghzXXX = ghz3+measureXXX

    # quantum circuit to measure XYY
    measureXYY = QuantumCircuit(q3, c3)
    measureXYY.s(q3[1]).inverse()
    measureXYY.s(q3[2]).inverse()
    measureXYY.h(q3[0])
    measureXYY.h(q3[1])
    measureXYY.h(q3[2])
    measureXYY.measure(q3[0], c3[0])
    measureXYY.measure(q3[1], c3[1])
    measureXYY.measure(q3[2], c3[2])
    ghzXYY = ghz3+measureXYY

    # quantum circuit to measure q YXY
    measureYXY = QuantumCircuit(q3, c3)
    measureYXY.s(q3[0]).inverse()
    measureYXY.s(q3[2]).inverse()
    measureYXY.h(q3[0])
    measureYXY.h(q3[1])
    measureYXY.h(q3[2])
    measureYXY.measure(q3[0], c3[0])
    measureYXY.measure(q3[1], c3[1])
    measureYXY.measure(q3[2], c3[2])
    ghzYXY = ghz3+measureYXY

    # quantum circuit to measure q YYX
    measureYYX = QuantumCircuit(q3, c3)
    measureYYX.s(q3[0]).inverse()
    measureYYX.s(q3[1]).inverse()
    measureYYX.h(q3[0])
    measureYYX.h(q3[1])
    measureYYX.h(q3[2])
    measureYYX.measure(q3[0], c3[0])
    measureYYX.measure(q3[1], c3[1])
    measureYYX.measure(q3[2], c3[2])
    ghzYYX = ghz3+measureYYX

    circuits = [ghzXXX, ghzYYX, ghzYXY, ghzXYY]

    return circuits

# Prepare circuits here.
mermin_circuits = get_mermin_circuits()

print('Circuit prepared for execution.')

# Assign circuits to run here.
run_main_loop(mermin_circuits)
