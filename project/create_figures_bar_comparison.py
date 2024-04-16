import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np




def create_figures_bar(m, h, case_nr, values_from_model = 1):

    #fig, axs = plt.subplots(3, 2, figsize=(20, 8))
    #fig.suptitle('Vertically stacked subplots')


    fig, ax = plt.subplots(3, 2, figsize=(10, 10))
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)

    if values_from_model:
        water = round(sum(m.P_EL_C_H2[0, t]() * 10  for t in range(0, h))/1000, 0)
        electricity_bought = round(sum(m.P_E_pos[t]() for t in range(0, h))/1000, 0)
        electricity_sold = round(sum(m.P_E_neg[t]() for t in range(0, h)) / 1000, 0)
        ammonia = 36792
        oxygen = round(sum(m.P_EL_C_H2[0, t]() * 8.304 for t in range(0, h))/1000, 0)

        if case_nr == 2:
            print(case_nr)
            n_case = 13
            products = ['Water', 'Electricity \n bought', 'Electricity \n sold','Ammonia', 'Oxygen', 'Hydrogen']
            hydrogen = round(sum(m.P_H2[t]() for t in range(0, h)) / 1000, 0)
            counts = [water * n_case, electricity_bought  * n_case, electricity_sold * n_case,
                      ammonia, oxygen * n_case, hydrogen * n_case]  # multiply by 12 months

            bar_labels = ['Water (kL)', 'Electricity bought (MWh)', 'Electricity sold (MWh)','Ammonia (ton)', 'Oxygen (ton)', 'Hydrogen (ton)']
            bar_colors = ['#BDD7EE', '#FFC000', '#FFD757', '#C5E0B4', '#AFABAB', '#37CBFF']

        elif case_nr == 3:
            n_case = 13 * 7
            products = ['Water', 'Electricity \n bought', 'Electricity \n sold', 'Reserves \n sold','Ammonia', 'Oxygen', 'Hydrogen']
            hydrogen = round(sum(m.P_H2[t]() for t in range(0, h)) / 1000, 0)
            reserves = round(sum(m.U_sto_E[0, t]() + m.D_sto_E[0, t]() for t in range(0, h)) / 1000, 0)
            counts = [water * n_case, electricity_bought * n_case, electricity_sold * n_case, reserves * n_case,
                      ammonia, oxygen * n_case, hydrogen * n_case]  # multiply by 12 months

            bar_labels = ['Water (kL)', 'Electricity bought (MWh)', 'Electricity sold (MWh)', 'Reserves sold (MWh)','Ammonia (ton)', 'Oxygen (ton)', 'Hydrogen (ton)']
            bar_colors = ['#BDD7EE', '#FFC000', '#FFD757', '#FFD050', '#C5E0B4', '#AFABAB', '#37CBFF']

        else:
            products = ['Water', 'Electricity', 'Ammonia', 'Oxygen']
            counts = [water, electricity_bought, ammonia, oxygen]

            bar_labels = ['Water (kL)', 'Electricity (MWh)', 'Ammonia (ton)', 'Oxygen (ton)']
            bar_colors = ['#BDD7EE', '#FFC000', '#C5E0B4', '#AFABAB']


    else:
        if 1:
            products = ['Water', 'Electricity', 'Ammonia', 'Oxygen', 'Hydrogen']
            counts = [40, 100, 30, 55, 20]
            bar_labels = ['Water (kL)', 'Electricity (MWh)', 'Ammonia (ton)', 'Oxygen (ton)', 'Hydrogen (kg)']
            bar_colors = ['#BDD7EE', '#FFC000', '#C5E0B4', '#AFABAB', '#37CBFF']

            products_case1 = [65122, 286680, ]

            n_case = 13 * 7
            products = ['Water', 'Electricity \n bought', 'Electricity \n sold', 'Reserves \n sold','Ammonia', 'Oxygen', 'Hydrogen']
            water = 1
            electricity_bought = 1
            electricity_sold = 1
            ammonia = 1
            oxygen = 1
            hydrogen = 1
            reserves = 1
            water = [65122, 172731, 86359]
            electricity_bought = [286680, 776438, 350168]
            electricity_sold = [0, 0, 0]
            ammonia = [36792, 36792, 36792]
            oxygen = [54077, 143442, 71708]
            hydrogen = [0, 10777, 2184]
            reserves = [0, 0, 192101]
            #counts = [water * n_case, electricity_bought * n_case, electricity_sold * n_case, reserves * n_case,
            #          ammonia, oxygen * n_case, hydrogen * n_case]  # multiply by 12 months


            bar_labels = ['Case 1']
            bar_colors = ['#BDD7EE', '#FFC000', '#FFD757']

    x_axis = np.arange(len(water))
    for i in range(0, 3):
        for k in range(0, 2):
            if i == 0 and k == 0:
                counts = water
                title_bar = 'Water'
                products_bar = 'Water'
            elif i == 0 and k == 1:
                counts = electricity_bought
                title_bar = 'Electricity'
                products_bar = 'Electricity'
            elif i == 1 and k == 0:
                counts = ammonia
                title_bar = 'Ammonia'
                products_bar = 'Ammonia'
            elif i == 1 and k == 1:
                counts = oxygen
                title_bar = 'Oxygen'
                products_bar = 'Oxygen'
            elif i == 2 and k == 0:
                counts = hydrogen
                title_bar = 'Hydrogen'
                products_bar = 'Hydrogen'
            elif i == 2 and k == 1:
                counts = reserves
                title_bar = 'Reserves'
                products_bar = 'Reserves'

            ax[i][k].bar(x_axis , counts, label=['Case 1', 'Case 2', 'Case 2'], color=['#BDD7EE', '#FFC000', '#C5E0B4'], edgecolor='w', width = 1)
            #ax[i][k].bar(x_axis, counts[1], label='Case 2', color='#FFC000', edgecolor='w', width = 0.2)
            #ax[i][k].bar(x_axis , counts[2], label='Case 3', color='#C5E0B4', edgecolor='w', width = 0.2)
            ax[i][k].yaxis.set_visible(False)
            #ax.set_ylabel('fruit supply')
            plt.ylabel(None)
            plt.xlabel(None)
            ax[i][k].set_title(title_bar)
            ax[i][k].legend(title='Cases')
            #ax.axis(color='w')
            ax[i][k].grid(False)
            ax[i][k].spines['top'].set_visible(False)
            ax[i][k].spines['right'].set_visible(False)
            ax[i][k].spines['left'].set_visible(False)
            ax[i][k].spines['bottom'].set_color('#DDDDDD')
            ax[i][k].set_xticklabels([])
            ax[i][k].set_xticks([])
            for j, bars in enumerate(ax[i][k].containers):
                print(j)
                print(bars)
                ax[i][k].bar_label(bars, label_type='center', color='#808080')


    if case_nr == 1:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case1"
    elif case_nr == 2:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case2"
    elif case_nr == 3:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case3"
    plt.savefig(OUTPUT_DIR / "products_comparison", dpi=300)
    plt.show()




if __name__ == '__main__':
    create_figures_bar(1, 1, 2, 0)



