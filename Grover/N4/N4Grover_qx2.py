import os
import sys

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from rtof import rtof4
from methods import test_locally_with_error_mitigation

# Mapowanie
C0 = 3
C1 = 4
C2 = 1
T = 0
A = 2
qubits_indexes_by_occurrence = [C1, C0, C2, T]

qr = QuantumRegister(5)
cr = ClassicalRegister(5)
qc = QuantumCircuit(qr, cr)
algorithm_repetition_times = 1


def rtof3(control1, control2, target):
    global qc

    qc.h(qr[target])
    qc.t(qr[target])
    qc.cx(qr[control2], qr[target])
    qc.tdg(qr[target])
    qc.cx(qr[control1], qr[target])
    qc.t(qr[target])
    qc.cx(qr[control2], qr[target])
    qc.tdg(qr[target])
    qc.h(qr[target])


def ccnot(control1, control2, target):
    global qc
    qc.ccx(qr[control1], qr[control2], qr[target])


def rtof4():
    global qc
    rtof3(C0, C1, A)

    qc.h(qr[T])
    qc.h(qr[A])
    ccnot(T, C2, A)
    qc.h(qr[T])
    qc.h(qr[A])

    rtof3(C0, C1, A)


def initialization(selected_state):
    global qc
    global qr
    global cr
    global algorithm_repetition_times

    circuit_name = 'Grover_4_' + str(selected_state) + '_' + str(algorithm_repetition_times)

    qr = QuantumRegister(5)
    cr = ClassicalRegister(5)
    qc = QuantumCircuit(qr, cr, name=circuit_name)

    qc.h(qr[C0])
    qc.h(qr[C1])
    qc.h(qr[C2])
    qc.h(qr[T])


def oracle(selected_state):
    global qubits_indexes_by_occurrence
    global qc

    xs_positions = []

    for j in range(len(selected_state)):
        if selected_state[j] == '0':
            xs_positions.append(qubits_indexes_by_occurrence[j])

    for pos in xs_positions:
        qc.x(qr[pos])

    qc.h(qr[T])
    rtof4()
    qc.h(qr[T])

    for pos in xs_positions:
        qc.x(qr[pos])


def diffusion():
    global qc

    qc.h(qr[C0])
    qc.h(qr[C1])
    qc.h(qr[C2])
    qc.h(qr[T])

    qc.x(qr[C0])
    qc.x(qr[C1])
    qc.x(qr[C2])
    qc.x(qr[T])

    qc.h(qr[T])
    rtof4()
    qc.h(qr[T])

    qc.x(qr[C0])
    qc.x(qr[C1])
    qc.x(qr[C2])
    qc.x(qr[T])

    qc.h(qr[C0])
    qc.h(qr[C1])
    qc.h(qr[C2])
    qc.h(qr[T])


states = ['{0:04b}'.format(x) for x in range(2 ** 4)]
circuits = []

# print(states)


for state in states:
    initialization(state)

    for i in range(algorithm_repetition_times):
        oracle(state)
        diffusion()

    qc.measure(qr, cr)
    circuits.append(qc)

    # test_locally(circuits, False, True, 1000)
test_locally_with_error_mitigation(circuits, True, 1000)
