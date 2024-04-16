import matplotlib.pyplot as plt
from pathlib import Path
from random import *
import numpy as np


OUTPUT_DIR = Path(__file__).parent.parent / "data/figures"
VALUES_FROM_MODEL = 1





def create_pie_chart_soc(input_data, x, color_list, labels, name_file, max_soc, case_nr):
    plt.figure(figsize=(15, 5))
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)

    plt.plot(x, input_data[1], color="#C00000", label=labels[1], linewidth=2)
    plt.scatter(x, input_data[0],  c = input_data[0], vmin=0, vmax=max_soc, cmap=color_list, zorder=2, s=3)
    #plt.plot(x, input_data[0], color='#FFE36D', label=labels[0], linewidth=0.5, zorder=1)
    plt.plot(x, input_data[0], color='#D8DBDB', label=labels[0], linewidth=0.5, zorder=1)

    plt.colorbar()
    plt.xlabel('Time (h)')
    plt.ylabel('State-of-charge (%)')
    plt.xlim(right=len(x))  # adjust the right leaving left unchanged
    plt.xlim(left=0)
    plt.xticks(np.arange(min(x), max(x) + 2, 24 * 30))
    plt.ylim(top=100)  # adjust the right leaving left unchanged
    plt.ylim(bottom=0)


    #plt.legend(loc=(1, 0.5), labels=labels, frameon=False)

    plt.grid(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    if case_nr == 1:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case1"
    elif case_nr == 2:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case2"
    elif case_nr == 3:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case3"
    plt.savefig(OUTPUT_DIR / name_file, dpi=300)
    plt.show()

    return plt

def create_figures_hydrogen_soc(m, h, resources, case_nr, VALUES_FROM_MODEL, create_figure = 1):
    labels = 'State-of-charge', 'Maximum state-of-charge'


    if VALUES_FROM_MODEL:
        max_soc = resources['hydrogen_storage']['max_capacity']
        print(m.soc_sto_H2[0, 0](), max_soc)
        hydrogen_to_storage = [m.soc_sto_H2[0, t]()/max_soc * 100 for t in range(0, h)]
        print(hydrogen_to_storage)
        hydrogen_to_ammonia_plant = [100 for t in range(0, h)]
        x = [i for i in range(0, h)]
        max_soc = 100
    else:
        hydrogen_to_storage = [random() * 100 for i in range(0, h)]
        if 1:
            hydrogen_to_storage = [1]

        hydrogen_to_ammonia_plant = [100 for i in range(0, h)]
        x = [i for i in range(0, h)]
        max_soc = 100

    input_data = [hydrogen_to_storage, hydrogen_to_ammonia_plant]

    color_list = 'Blues'
    name_file = "Hydrogen_soc.png"
    print(x)
    print(min(x))
    if create_figure == 1:
        create_pie_chart_soc(input_data, x, color_list, labels, name_file, max_soc, case_nr)

    return input_data, color_list, labels

def create_figures_nitrogen_soc(m, h, resources, case_nr, VALUES_FROM_MODEL, create_figure = 1):
    labels = 'State-of-charge', 'Maximum state-of-charge'


    if VALUES_FROM_MODEL:
        max_soc = resources['nitrogen_storage']['max_capacity']
        print(m.soc_sto_H2[0, 0](), max_soc)
        hydrogen_to_storage = [m.soc_sto_N2[0, t]()/max_soc * 100 for t in range(0, h)]
        #hydrogen_to_storage = [hydrogen_to_storage[t] for t in range(48, h - 24 * 6)]
        print(hydrogen_to_storage)
        hydrogen_to_ammonia_plant = [100 for t in range(0, h)]
        #hydrogen_to_ammonia_plant = [100 for t in range(48, h - 24 * 6)]
        x = [i for i in range(0, h)]
        #x = [i - 48 for i in range(48, h - 24 * 6)]
        max_soc = 100
    else:
        hydrogen_to_storage = [random() * 100 for i in range(0, h)]
        if 1:
            hydrogen_to_storage = [1]
        hydrogen_to_ammonia_plant = [100 for i in range(0, h)]
        x = [i for i in range(0, h)]
        max_soc = 100

    input_data = [hydrogen_to_storage, hydrogen_to_ammonia_plant]

    color_list = 'Oranges'
    name_file = "Nitrogen_soc.png"

    if create_figure == 1:
        create_pie_chart_soc(input_data, x, color_list, labels, name_file, max_soc, case_nr)

    return input_data, color_list, labels

def create_figures_ammonia_soc(m, h, resources, case_nr, VALUES_FROM_MODEL, create_figure = 1):
    labels = 'State-of-charge', 'Maximum state-of-charge'


    if VALUES_FROM_MODEL:
        max_soc = resources['ammonia_storage']['max_capacity']
        print(m.soc_sto_H2[0, 0](), max_soc)
        hydrogen_to_storage = [m.soc_sto_NH3[0, t]()/max_soc * 100 for t in range(0, h)]
        print(hydrogen_to_storage)
        hydrogen_to_ammonia_plant = [100 for t in range(0, h)]
        x = [i for i in range(0, h)]
        max_soc = 100
    else:
        hydrogen_to_storage = [random() * 100 for i in range(0, h)]
        if 1:
            hydrogen_to_storage = [1]
        hydrogen_to_ammonia_plant = [100 for i in range(0, h)]
        x = [i for i in range(0, h)]
        max_soc = 100

    input_data = [hydrogen_to_storage, hydrogen_to_ammonia_plant]

    color_list = 'RdPu'
    name_file = "Ammonia_soc.png"

    if create_figure == 1:
        create_pie_chart_soc(input_data, x, color_list, labels, name_file, max_soc, case_nr)

    return input_data, color_list, labels

def create_figures_electricity_soc(m, h, resources, case_nr, VALUES_FROM_MODEL, create_figure = 1):
    labels = 'State-of-charge', 'Maximum state-of-charge'


    if VALUES_FROM_MODEL:
        max_soc = resources['electrical_storage']['max_capacity']
        print(m.soc_sto_E[0, 0](), max_soc)
        electricity_to_storage = [m.soc_sto_E[0, t]()/max_soc * 100 for t in range(0, h)]
        print(electricity_to_storage)
        hydrogen_to_ammonia_plant = [100 for t in range(0, h)]

        x = [i for i in range(0, h)]
        max_soc = 100
    else:
        electricity_to_storage = [random() * 100 for i in range(0, h)]
        if 1:
            electricity_to_storage = [1]

        hydrogen_to_ammonia_plant = [100 for i in range(0, h)]
        x = [i for i in range(0, h)]
        max_soc = 100

    input_data = [electricity_to_storage, hydrogen_to_ammonia_plant]

    color_list = 'Wistia'
    name_file = "Electricity_soc.png"
    print(x)
    print(min(x))
    if create_figure == 1:
        create_pie_chart_soc(input_data, x, color_list, labels, name_file, max_soc, case_nr)

    return input_data, color_list, labels


def create_pie_chart_pv(input_data, x, color_list, labels, name_file, max_soc, case_nr):
    plt.figure(figsize=(15, 5))
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)

    plt.plot(x, input_data[1], color="#C00000", label=labels[1], linewidth=2)
    plt.scatter(x, input_data[0],  c = input_data[0], vmin=0, vmax=max_soc, cmap='YlOrRd', zorder=2, s=3)
    #plt.plot(x, input_data[0], color='#FFE36D', label=labels[0], linewidth=0.5, zorder=1)
    plt.plot(x, input_data[0], color='#D8DBDB', label=labels[0], linewidth=0.5, zorder=1)

    plt.colorbar()
    plt.xlabel('Time (h)')
    plt.ylabel('Power (MW)')
    plt.xlim(right=len(x))  # adjust the right leaving left unchanged
    plt.xlim(left=0)
    plt.xticks(np.arange(min(x), max(x) + 2, 24 * 30))

    #plt.legend(loc=(1, 0.5), labels=labels, frameon=False)

    plt.grid(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    if case_nr == 1:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case1"
    elif case_nr == 2:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case2"
    elif case_nr == 3:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case3"
    plt.savefig(OUTPUT_DIR / name_file, dpi=300)

    plt.show()

    return plt

def create_figures_pv(m, h, resources, case_nr, VALUES_FROM_MODEL, create_figure = 1):
    labels = 'State-of-charge', 'Maximum state-of-charge'


    if VALUES_FROM_MODEL:
        max_soc = resources['PV']['max_power']
        print(m.P_PV[0, 0]()/1000, max_soc)
        PV = [m.P_PV[0, t]()/1000 for t in range(0, h)]
        PV_max = [max_soc/1000 for t in range(0, h)]
        x = [i for i in range(0, h)]
        print(PV)
        max_soc = max_soc/1000
    else:
        max_soc = 50
        PV = [random() * 100 for i in range(0, h)]
        PV = [1]
        PV = [PV[t]/10 for t in range(0, len(PV))]
        print(PV)
        PV_max = [max_soc for i in range(0, h)]
        x = [i for i in range(0, h)]

    input_data = [PV, PV_max]

    color_list = ['#76ABDC', '#BDD7EE']

    name_file = "PV_generation.png"

    if create_figure == 1:
        create_pie_chart_pv(input_data, x, color_list, labels, name_file, max_soc, case_nr)

    return input_data, color_list, labels




def create_figures_SOC(m, h, resources, case_nr, VALUES_FROM_MODEL = 1):
    if 1:
        create_figures_electricity_soc(m, h, resources, case_nr, VALUES_FROM_MODEL)
        create_figures_ammonia_soc(m, h, resources, case_nr, VALUES_FROM_MODEL)
        create_figures_nitrogen_soc(m, h, resources, case_nr, VALUES_FROM_MODEL)
        create_figures_hydrogen_soc(m, h, resources, case_nr, VALUES_FROM_MODEL)
        create_figures_pv(m, h, resources, case_nr, VALUES_FROM_MODEL)




if __name__ == '__main__':
    create_figures_SOC(1, 24 * 365, 1, 0)





