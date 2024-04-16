import matplotlib.pyplot as plt
from pathlib import Path




def create_figures_bar(m, h, case_nr, values_from_model = 1):

    #fig, axs = plt.subplots(3, 2, figsize=(20, 8))
    #fig.suptitle('Vertically stacked subplots')

    fig, ax = plt.subplots()


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
        if case_nr == 2:
            products = ['Water', 'Electricity', 'Ammonia', 'Oxygen', 'Hydrogen']
            counts = [40, 100, 30, 55, 20]
            bar_labels = ['Water (kL)', 'Electricity (MWh)', 'Ammonia (ton)', 'Oxygen (ton)', 'Hydrogen (kg)']
            bar_colors = ['#BDD7EE', '#FFC000', '#C5E0B4', '#AFABAB', '#37CBFF']





    ax.bar(products, counts, label=bar_labels, color=bar_colors, edgecolor='w')
    i = 0
    for i, bars in enumerate(ax.containers):
        bars_all = ax.bar_label(bars, label_type='center', color='w')
        if case_nr == 2:
            bars_all[5].set_color('#808080')
            bars_all[5].set_position([1,5])
        elif case_nr == 3:
            bars_all[6].set_color('#808080')
            bars_all[6].set_position([1,5])

    #ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    #ax.set_ylabel('fruit supply')
    plt.ylabel(None)
    ax.set_title('Bought and sold products')
    ax.legend(title='Products')
    #ax.axis(color='w')
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')

    if case_nr == 1:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case1"
    elif case_nr == 2:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case2"
    elif case_nr == 3:
        OUTPUT_DIR = Path(__file__).parent.parent / "data/figures - case3"
    plt.savefig(OUTPUT_DIR / "products", dpi=300)
    plt.show()




if __name__ == '__main__':
    create_figures_bar(1, 1, 2, 0)



