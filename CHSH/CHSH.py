from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, QISKitError
import methods
from methods import consts
import time
import numpy as np


def get_chsh_circuits():
    # Creating registers
    q = QuantumRegister(2)
    c = ClassicalRegister(2)

    # quantum circuit to make an entangled bell state
    bell = QuantumCircuit(q, c)
    bell.h(q[0])
    bell.cx(q[0], q[1])

    # quantum circuit to measure q in the standard basis
    measure_zz = QuantumCircuit(q, c)
    measure_zz.measure(q[0], c[0])
    measure_zz.measure(q[1], c[1])

    # quantum circuit to measure q in the superposition basis
    measure_xx = QuantumCircuit(q, c)
    measure_xx.h(q[0])
    measure_xx.h(q[1])
    measure_xx.measure(q[0], c[0])
    measure_xx.measure(q[1], c[1])

    # quantum circuit to measure ZX
    measure_zx = QuantumCircuit(q, c)
    measure_zx.h(q[0])
    measure_zx.measure(q[0], c[0])
    measure_zx.measure(q[1], c[1])

    # quantum circuit to measure XZ
    measure_xz = QuantumCircuit(q, c)
    measure_xz.h(q[1])
    measure_xz.measure(q[0], c[0])
    measure_xz.measure(q[1], c[1])

    measure = [measure_zz, measure_zx, measure_xx, measure_xz]

    real_chsh_circuits = []
    real_x = []

    real_steps = 10

    for step in range(real_steps):

        theta = 2.0 * np.pi * step / 10
        bell_middle = QuantumCircuit(q, c)
        bell_middle.ry(theta, q[0])

        for m in measure:
            real_chsh_circuits.append(bell + bell_middle + m)

        real_x.append(theta)

    return real_chsh_circuits


# Prepare circuits here.
chsh_circuits = get_chsh_circuits()

print('Circuit prepared for execution.')

# Assign circuits to run here.
circuits = chsh_circuits

current_backend_index = 0

for iteration_number in range(0, consts.ITERATIONS_NUMBER):

    print('Iteration number: ', iteration_number)

    current_credits_number = methods.get_current_credits()

    # In case there are to little credits
    while current_credits_number < 3:
        print("Current credits number is", current_credits_number,
              'which is less than 3. Waiting 10 minutes to continue.')
        time.sleep(600)
        current_credits_number = methods.get_current_credits()

    print('Getting available backends...')
    available_backends = methods.get_available_remote_backends_names()

    # Actual execution call
    # IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
    if __name__ == '__main__':
        try:
            backend = methods.get_backend_name_from_number(current_backend_index)

            while not available_backends.__contains__(backend):
                print(backend, ': Currently not available.')
                current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)
                backend = methods.get_backend_name_from_number(current_backend_index)
                print('Refreshing available backends list...')
                available_backends = methods.get_available_remote_backends_names()
                print('Trying another backend: ', backend)

            print("Executing quantum program on backend:", backend)
            methods.execute(circuits, backend)

            print("Program send for execution to ", backend, '.')
            current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)

        except QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))

