import matplotlib.pyplot as plt
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent / "data/figures"

def create_pie_chart(input_data, color_list, labels, title, name_file, case_nr):
    plt.figure(figsize=(7, 5))
    plt.subplots_adjust(left=0, right=0.6, top=1, bottom=0)
    _,_,texts  = plt.pie(input_data, labels=None, colors=color_list,
            autopct='%1.0f%%', pctdistance=1.2)

    for text, color in zip(texts, color_list):
        text.set_color(color)

    plt.legend(loc=(1, 0.5), labels=labels, frameon=False, title=title)

    if case_nr == 1:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case1"
    elif case_nr == 2:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case2"
    elif case_nr == 3:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case3"

    plt.savefig(OUTPUT_DIR / name_file, dpi=300)
    plt.show()

    return plt



def crete_figures_total_electricity(m, h, case_nr, VALUES_FROM_MODEL = 1, create_figure = 1):

    labels = 'Network', 'PV systems'

    if VALUES_FROM_MODEL:
        total_electricity_from_PV = sum(m.P_PV[0, t]() for t in range(0, h))
        total_electricity_from_net = sum(m.P_E[t]() for t in range(0, h))
        total_electricity_from_net_week = [m.P_E[t]() for t in range(0, h)]
        total_electricity_from_PV_week = [m.P_PV[0, t]() for t in range(0, h)]
        x = [i for i in range(0, h)]
    else:
        total_electricity_from_net = 0.4
        total_electricity_from_PV = 0.6
        total_electricity_from_net_week = [0.4 for i in range(0, h)]
        total_electricity_from_PV_week = [0.6 for i in range(0, h)]
        x = [i for i in range(0, h)]


    input_data = [total_electricity_from_net, total_electricity_from_PV]
    input_data_week = [total_electricity_from_net_week, total_electricity_from_PV_week]

    color_list = ['#FFC000', '#FFE38B']
    color_list_week = ['#FFC000', '#BDD7EE']
    title = 'Electricity consumed from:'

    name_file = "Electricity consumption.png"

    if create_figure == 1:
        create_pie_chart(input_data, color_list, labels, title, name_file, case_nr)

    return input_data, color_list, labels, title

def crete_figures_electricity_use(m, h, case_nr, VALUES_FROM_MODEL = 1, create_figure = 1):
    if VALUES_FROM_MODEL:
        air_compressor = sum(m.P_C_air_E[0, t]() for t in range(0, h))
        air_separator = sum(m.P_AS_E[0, t]() for t in range(0, h))
        nitrogen_compressor = sum(m.P_C_N2_E[0, t]() for t in range(0, h))
        electrolyzer = sum(m.P_EL_E[0, t]() + m.P_EL_cooling[0, t]() for t in range(0, h))
        hydrogen_compressor = sum(m.P_C_H2_E[0, t]() for t in range(0, h))
        recycling_air_unit = sum(m.P_AP_E[0, t]() for t in range(0, h))
        ammonia_storage = sum(m.P_sto_NH3_E[0, t]() for t in range(0, h))
        if case_nr == 2:
            electricity_market = sum(m.P_E_neg[t]() for t in range(0, h))
        if case_nr == 3:
            electricity_market = sum(m.P_E_neg[t]() for t in range(0, h))
            reserves = sum(m.P_sto_E_ch[0, t]() for t in range(0, h))
    else:
        air_compressor = 1
        air_separator = 2
        nitrogen_compressor = 2
        electrolyzer = 4
        hydrogen_compressor = 5
        recycling_air_unit = 2
        ammonia_storage = 1
        reserves = 2

    if case_nr == 2:
        labels =  'Air compressor', 'Air seperator', \
                 'Nitrogen compressor', 'Ammonia storage', 'Electrolyzer', \
                 'Hydrogen compressor', 'Recycling air unit', 'Electricity market'\

        input_data = [air_compressor, air_separator, nitrogen_compressor, ammonia_storage, electrolyzer,
                      hydrogen_compressor, recycling_air_unit, electricity_market]
        color_list = ['#AFABAB', '#C00000', '#C5E0B4', '#0D6C9B', '#BDD7EE', '#FFC000', '#ED7D31', '#FFD757']
    elif case_nr == 3:
        labels =  'Air compressor', 'Air seperator', \
                 'Nitrogen compressor', 'Ammonia storage', 'Electrolyzer', \
                 'Hydrogen compressor', 'Recycling air unit', 'Electricity market', 'Storage systems'\

        input_data = [air_compressor, air_separator, nitrogen_compressor, ammonia_storage, electrolyzer,
                      hydrogen_compressor, recycling_air_unit, electricity_market, reserves]
        color_list = ['#AFABAB', '#C00000', '#C5E0B4', '#0D6C9B', '#BDD7EE', '#FFC000', '#ED7D31', '#FFD757', '#548235']
    else:
        labels = 'Air compressor', 'Air seperator',  \
                 'Nitrogen compressor', 'Ammonia storage', 'Electrolyzer',\
                 'Hydrogen compressor', 'Recycling air unit'

        input_data = [air_compressor, air_separator, nitrogen_compressor, ammonia_storage, electrolyzer,
                               hydrogen_compressor, recycling_air_unit]
        color_list = ['#AFABAB', '#C00000', '#C5E0B4', '#0D6C9B', '#BDD7EE', '#FFC000', '#ED7D31']

    print(input_data)
    title = 'Electricity consumed by:'
    name_file = "Electricity_use.png"

    if create_figure == 1:
        create_pie_chart(input_data, color_list, labels, title, name_file, case_nr)

    return input_data, color_list, labels, title

def create_figures_hydrogen_use(m, h, case_nr, VALUES_FROM_MODEL = 1, create_figure = 1):



    if VALUES_FROM_MODEL:
        hydrogen_to_storage = sum(m.P_C_H2_sto_H2[0, t]() for t in range(0, h))
        hydrogen_to_ammonia_plant = sum(m.P_C_H2_AP[0, t]() for t in range(0, h))
        if case_nr in [2, 3]:
            hydrogen_to_market = sum(m.P_H2[t]() for t in range(0, h))

    else:
        hydrogen_to_storage = 0.4
        hydrogen_to_ammonia_plant = 0.6

    if case_nr in [2, 3]:
        labels = 'Hydrogen storage', 'Ammonia plant', ' Hydrogen market'
        input_data = [hydrogen_to_storage, hydrogen_to_ammonia_plant, hydrogen_to_market]
        color_list = ['#002060', '#BDD7EE','#76ABDC']
        title = 'Hydrogen from hydrogen compressor to:'
    else:
        labels = 'Hydrogen storage', 'Ammonia plant'
        input_data = [hydrogen_to_storage, hydrogen_to_ammonia_plant]
        color_list = ['#76ABDC', '#BDD7EE']
        title = 'Hydrogen from hydrogen compressor to:'

    name_file = "Hydrogen_use.png"

    if create_figure == 1:
        create_pie_chart(input_data, color_list, labels, title, name_file, case_nr)

    return input_data, color_list, labels, title

def create_figures_nitrogen_use(m, h, case_nr, VALUES_FROM_MODEL = 1, create_figure = 1):
    labels = 'Nitrogen storage', 'Ammonia plant'

    if VALUES_FROM_MODEL:
        nitrogen_to_storage = sum(m.P_C_N2_sto_N2[0, t]() for t in range(0, h))
        nitrogen_to_ammonia_plant = sum(m.P_C_N2_AP[0, t]() for t in range(0, h))
    else:
        nitrogen_to_storage = 0.4
        nitrogen_to_ammonia_plant = 0.6

    input_data = [nitrogen_to_storage, nitrogen_to_ammonia_plant]

    color_list = ['#ED7D31', '#F6BC94']

    title='Nitrogen from nitrogen compressor to:'

    name_file = "Nitrogen_use.png"

    if create_figure == 1:
        create_pie_chart(input_data, color_list, labels, title, name_file, case_nr)

    return input_data, color_list, labels, title

def create_figures_ammonia_use(m, h, case_nr, VALUES_FROM_MODEL = 1, create_figure = 1):
    labels = 'Ammonia storage', 'Ammonia load'

    if VALUES_FROM_MODEL:
        ammonia_to_storage = sum(m.P_AP_sto_NH3[0, t]() for t in range(0, h))
        ammonia_to_load = sum(m.P_AP_load[0, t]() for t in range(0, h))
    else:
        ammonia_to_storage = 0.4
        ammonia_to_load = 0.6

    input_data = [ammonia_to_storage, ammonia_to_load]

    color_list = ['#C00000', '#FF8F8F']

    title='Ammonia from the ammonia plant to:'

    name_file = "Ammonia_use.png"

    if create_figure == 1:
        create_pie_chart(input_data, color_list, labels, title, name_file, case_nr)

    return input_data, color_list, labels, title

def crete_figures_electrical_storage_use(m, h, case_nr, VALUES_FROM_MODEL = 1, create_figure = 1):
    if VALUES_FROM_MODEL:
        air_compressor = sum(m.P_C_air_E[0, t]() for t in range(0, h))
        air_separator = sum(m.P_AS_E[0, t]() for t in range(0, h))
        nitrogen_compressor = sum(m.P_C_N2_E[0, t]() for t in range(0, h))
        electrolyzer = sum(m.P_EL_E[0, t]() + m.P_EL_cooling[0, t]() for t in range(0, h))
        hydrogen_compressor = sum(m.P_C_H2_E[0, t]() for t in range(0, h))
        recycling_air_unit = sum(m.P_AP_E[0, t]() for t in range(0, h))
        ammonia_storage = sum(m.P_sto_NH3_E[0, t]() for t in range(0, h))
        if case_nr == 2:
            electricity_market = sum(m.P_E_neg[t]() for t in range(0, h))
        if case_nr == 3:
            electricity_market = sum(m.P_E_neg[t]() for t in range(0, h))
            reserves = sum(m.P_sto_E_ch[0, t]() for t in range(0, h))
    else:
        air_compressor = 1
        air_separator = 2
        nitrogen_compressor = 2
        electrolyzer = 4
        hydrogen_compressor = 5
        recycling_air_unit = 2
        ammonia_storage = 1
        reserves = 2

    if case_nr == 2:
        labels =  'Air compressor', 'Air seperator', \
                 'Nitrogen compressor', 'Ammonia storage', 'Electrolyzer', \
                 'Hydrogen compressor', 'Recycling air unit', 'Electricity market'\

        input_data = [air_compressor, air_separator, nitrogen_compressor, ammonia_storage, electrolyzer,
                      hydrogen_compressor, recycling_air_unit, electricity_market]
        color_list = ['#AFABAB', '#C00000', '#C5E0B4', '#0D6C9B', '#BDD7EE', '#FFC000', '#ED7D31', '#FFD757']
    elif case_nr == 3:
        labels =  'Air compressor', 'Air seperator', \
                 'Nitrogen compressor', 'Ammonia storage', 'Electrolyzer', \
                 'Hydrogen compressor', 'Recycling air unit', 'Electricity market', 'Storage systems'\

        input_data = [air_compressor, air_separator, nitrogen_compressor, ammonia_storage, electrolyzer,
                      hydrogen_compressor, recycling_air_unit, electricity_market, reserves]
        color_list = ['#AFABAB', '#C00000', '#C5E0B4', '#0D6C9B', '#BDD7EE', '#FFC000', '#ED7D31', '#FFD757', '#548235']
    else:
        labels = 'Air compressor', 'Air seperator',  \
                 'Nitrogen compressor', 'Ammonia storage', 'Electrolyzer',\
                 'Hydrogen compressor', 'Recycling air unit'

        input_data = [air_compressor, air_separator, nitrogen_compressor, ammonia_storage, electrolyzer,
                               hydrogen_compressor, recycling_air_unit]
        color_list = ['#AFABAB', '#C00000', '#C5E0B4', '#0D6C9B', '#BDD7EE', '#FFC000', '#ED7D31']

    print(input_data)
    title = 'Electricity consumed by:'
    name_file = "Electricity_use.png"

    if create_figure == 1:
        create_pie_chart(input_data, color_list, labels, title, name_file, case_nr)

    return input_data, color_list, labels, title



def create_pie_chart_all_figures(input_data, color_list, labels, title, ax, i, j):

    _,_,texts  = ax[i, j].pie(input_data, labels=None, colors=color_list,
            autopct='%1.0f%%', pctdistance=1.2)

    for text, color in zip(texts, color_list):
        text.set_color(color)

    ax[i, j].legend(loc=(1, 0.5), labels=labels, frameon=False, title=title)

def create_all_figures(m, h, case_nr):

    fig, axs = plt.subplots(3, 2, figsize=(20, 8))
    #fig.suptitle('Vertically stacked subplots')

    ###################################################################################################################
    input_data, color_list, labels, title = crete_figures_total_electricity(m, h, 0)
    create_pie_chart_all_figures(input_data, color_list, labels, title, axs, 0, 0)

    ###################################################################################################################
    input_data, color_list, labels, title = crete_figures_electricity_use(m, h, 0)
    create_pie_chart_all_figures(input_data, color_list, labels, title, axs, 0, 1)

    ###################################################################################################################
    input_data, color_list, labels, title = create_figures_hydrogen_use(m, h, 0)
    create_pie_chart_all_figures(input_data, color_list, labels, title, axs, 1, 0)

    ###################################################################################################################
    input_data, color_list, labels, title = create_figures_nitrogen_use(m, h, 0)
    create_pie_chart_all_figures(input_data, color_list, labels, title, axs, 1, 1)

    ###################################################################################################################
    input_data, color_list, labels, title = create_figures_ammonia_use(m, h, 0)
    create_pie_chart_all_figures(input_data, color_list, labels, title, axs, 2, 0)

    ###################################################################################################################
    input_data, color_list, labels, title = create_figures_ammonia_use(m, h, 0)
    create_pie_chart_all_figures([], [], [], [], axs, 2, 1)

    ###################################################################################################################
    plt.subplots_adjust(left=0, right=0.85, top=0.96, bottom=0)

    if case_nr == 1:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case1"
    elif case_nr == 2:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case2"
    elif case_nr == 3:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case3"
    plt.savefig(OUTPUT_DIR / "all_figures", dpi=300)
    plt.show()



def create_figures(m, h, case_nr, save_figure_option, show_figure_option):
    if 1:
        crete_figures_total_electricity(m, h, case_nr)
        crete_figures_electricity_use(m, h, case_nr)

        create_figures_hydrogen_use(m, h, case_nr)
        create_figures_nitrogen_use(m, h, case_nr)
        create_figures_ammonia_use(m, h, case_nr)

    #create_all_figures(m, h)


















if __name__ == '__main__':
    #crete_figures_total_electricity(1, 1)
    crete_figures_electricity_use(1, 1, 2, 0)

    #create_figures_hydrogen_use(1, 1)
    #create_figures_nitrogen_use(1, 1)
    #create_figures_ammonia_use(1, 1)

    #create_all_figures(1, 1)

    # Electricity consumed by the electrolyzer
    # Electricity used from PV
    # Electricity used from net

