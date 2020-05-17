import sys
sys.path.append('../..')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FuncFormatter
from methods import test_locally_with_noise, get_backend_from_name
import re
from mpl_toolkits.axes_grid1 import host_subplot
from consts import SHOTS


parameter_sets = [
    {
        'n': 4,
        't': 1,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_1011_01_n=4_t=1',
        'pair': 1
    },
    {
        'n': 4,
        't': 1,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_1011_23_n=4_t=1',
        'pair': 0
    },
    {
        'n': 4,
        't': 2,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_1011_134_n=4_t=2',
        'pair': 3
    },
    {
        'n': 4,
        't': 2,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_1011_234_n=4_t=2',
        'pair': 2
    },
    {
        'n': 10,
        't': 1,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_pi/4_n=10_t=1',
        'pair': 5
    },
    {
        'n': 10,
        't': 1,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_pi/4_23_n=10_t=1',
        'pair': 4
    },
    {
        'n': 10,
        't': 2,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_pi/4_134_n=10_t=2',
        'pair': 7
    },
    {
        'n': 10,
        't': 2,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_pi/4_234_n=10_t=2',
        'pair': 6
    },
    {
        'n': 10,
        't': 3,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_pi/4_0134_n=10_t=3',
        'pair': 9
    },
    {
        'n': 10,
        't': 3,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_pi/4_4320_n=10_t=3',
        'pair': 8
    }
]


def set_axes(axis, n, t):
    axis.yaxis.set_ticks(range(n))
    axis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: "{}".format(x + 1)))
    axis.xaxis.set_ticks(range(2 ** t))
    axis.xaxis.set_major_formatter(StrMethodFormatter("{{x:0{}b}}".format(t)))
    if n % t:
        sec_axis = axis.twin()
        sec_axis.xaxis.set_ticks(np.arange((2 ** ((-n) % t) - 1) / 2, 2 ** t, 2 ** ((-n) % t)))
        sec_axis.xaxis.set_major_formatter(
            FuncFormatter(
                lambda x, pos: "{{:0{}b}}".format(n % t).format(pos)))
        sec_axis.yaxis.set_visible(False)


def make_array(jobs, n, t):
    dict_key_format_format = "{{:0{}b}}"
    counts = []
    results = [job.result() for job in jobs]
    for i, result in zip(reversed(range(n, 0, -t)), results):
        k = min(i, t)
        dict_key_format = dict_key_format_format.format(k)
        for _ in range(min(i, t)):
            counts.append([result.get_counts()[dict_key_format.format(j)[::-1]]
                           for j in range(2 ** k) for _ in range(2 ** (t - k))])
    return np.array(counts)


def plot(array, n, t, experiment_name, vmax, plot_labels=False, save_val=False, save_plot=False):
    figure = plt.figure()
    axis = host_subplot(1, 1, 1, figure=figure)
    plt.xticks(rotation=45)
    set_axes(axis, n, t)

    if plot_labels:
        for (j, i), count in np.ndenumerate(array):
            axis.text(i, j, "{:.2f}%".format(100 * count / SHOTS), ha='center', va='center', fontsize=5)

    axis.set_ylabel("Miejsce po przecinku")
    axis.set_xlabel("Wartość grupy bitów")

    if save_val:
        bits = ""
        for i in reversed(range(n, 0, -t)):
            bits += "{{:0{}b}}".format(min(i, t)).format(array[i - 1][::2 ** (max(t - i, 0))].argmax())
        with open("../../../../Fizyka-licencjat/Pomiary/pe_steps.txt", "a") as f:
            f.write("{}\t{}\t{}%\n".format(experiment_name, bits, 100 * vmax / SHOTS))

    axis.pcolormesh(np.arange(2 ** t + 1) - 0.5, np.arange(n + 1) - 0.5, array, cmap='viridis', vmin=0, vmax=vmax)
    axis.axis('image')
    axis.invert_yaxis()

    if save_plot:
        plt.savefig("../../../../Fizyka-licencjat/Pomiary/{}.pdf".format(experiment_name.replace("/", "")),
                    transparent=True, bbox_inches='tight', pad_inches=0)

    plt.show()


def get_jobs(backend_name, job_base_name, n, t, **kwargs):
    backend = get_backend_from_name(backend_name)
    return [backend.jobs(job_name=re.escape("{}_{}".format(job_base_name, range(max(i - t, 0), i))))[0]
                for i in reversed(range(n, 0, -t))]


def main():
    for parameter_set in parameter_sets:
        backend_name = parameter_set['backend_name']
        job_base_name = parameter_set['job_base_name']
        n = parameter_set['n']
        t = parameter_set['t']

        jobs = get_jobs(**parameter_set)
        array = make_array(jobs, n, t)
        vmax = array.max()

        if 'pair' in parameter_set:
            pair_jobs = get_jobs(**parameter_sets[parameter_set['pair']])
            pair_array = make_array(pair_jobs, n, t)
            vmax = max(vmax, pair_array.max())

        plot(array, n, t, "pe_steps_{}_n={}_t={}_{}".format(backend_name, n, t, job_base_name).replace("/", ""),
             vmax=vmax)


if __name__ == '__main__':
    main()