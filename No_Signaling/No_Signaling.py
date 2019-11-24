import sys
sys.path.append('..')
from CHSH.CHSH import get_chsh_circuits
from SanityCheck.SanityCheck import get_sc_circuits
from Mermin.mermin_test import get_mermin_circuits
from methods import run_main_loop, run_main_loop_with_chsh_test, test_locally

circuits = get_sc_circuits() + get_chsh_circuits() + get_mermin_circuits()

#run_main_loop(circuits)
#run_main_loop_with_chsh_test(circuits)
test_locally(circuits, False, True, 1)