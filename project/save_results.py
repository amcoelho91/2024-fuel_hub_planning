import xlwt
from numpy import *
from pyomo.environ import *
from pathlib import Path
from time import *

OUTPUT_DIR = Path(__file__).parent.parent / "data"

def save_results(m: ConcreteModel(), h: int, case_nr: int, prices: dict, resources: dict, number_resources: int) -> None:
    ''' Save results into excel file'''
    book = xlwt.Workbook()

    book = save_energy(m, h, case_nr, book)
    #book = save_costs(m, h, case_nr, prices, resources, number_resources, book)
    save_excel(book, case_nr)


def save_excel(book, case_nr: int) -> None:
    ''' Save excel '''
    flag_excel = 1
    iter = 0
    while flag_excel > 0:
        try:
            if flag_excel == 1:
                book.save(OUTPUT_DIR / f"outputs_case{case_nr}.xls")
            else:
                book.save(OUTPUT_DIR / f"outputs_case{case_nr}_v{iter}.xls")
            flag_excel = 0
        except:
            flag_excel = 2
            print("")
            time_start = time()
            while (time() - time_start < 15):
                sleep(1)
                print("CLOSE EXCEL!")




def save_energy(m: ConcreteModel(), h: int, case: int, book: xlwt.Workbook) -> xlwt.Workbook:
    ''' Save energy results'''
    sh1 = book.add_sheet("CHP net")


    # ____________________________________ First title ____________________________________
    n = 0
    n += 1
    sh1.write(0, n + 1, "Net-load")
    n += 1
    n += 1
    sh1.write(0, n + 1, "PV")

    n += 1
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")
    n += 1
    sh1.write(0, n + 1, "Electrical storage system")

    n += 1
    n += 1
    sh1.write(0, n + 1, "Electrolyzer")
    n += 1

    # ____________________________________ Second title ____________________________________

    n = 0
    n += 1
    sh1.write(1, n + 1, "Total")
    n += 1
    n += 1
    sh1.write(1, n + 1, "PV generation (kW)")


    n += 1
    n += 1
    sh1.write(1, n + 1, "soc (kWh)")
    n += 1
    sh1.write(1, n + 1, "charging (kW)")
    n += 1
    sh1.write(1, n + 1, "discharging (kW)")
    n += 1
    sh1.write(1, n + 1, "Upward")
    n += 1
    sh1.write(1, n + 1, "Upward ch")
    n += 1
    sh1.write(1, n + 1, "Upward dis")
    n += 1
    sh1.write(1, n + 1, "Downward")
    n += 1
    sh1.write(1, n + 1, "Downward ch")
    n += 1
    sh1.write(1, n + 1, "Downward dis")










    # ____________________________________ Results ____________________________________
    for t in range(0, h):
        n = 0
        n += 1
        sh1.write(t + 2, n + 1, m.P_E[t].value)
        n += 1
        n += 1

        sh1.write(t + 2, n + 1, m.P_PV[0, t].value)


        n += 1
        n += 1
        sh1.write(t + 2, n + 1, m.soc_sto_E[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.P_sto_E_ch[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.P_sto_E_dis[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.U_sto_E[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.U_sto_E_ch[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.U_sto_E_dis[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.D_sto_E[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.D_sto_E_ch[0, t].value)
        n += 1
        sh1.write(t + 2, n + 1, m.D_sto_E_dis[0, t].value)


    return book


def save_costs(m: ConcreteModel(), h: int, case_nr: int, prices: dict, resources: dict,
               number_resources: int, book: xlwt.Workbook) -> xlwt.Workbook:
    ''' Save costs results'''
    sh1 = book.add_sheet("Costs")

    c_H2O = resources['electrolyzer']['c_H2O']
    c_O2 = resources['electrolyzer']['c_O2']

    price_E = prices['energy']
    price_E_market = prices['energy_market']
    price_B = prices['band']
    price_E_D = prices['downward']
    price_E_U = prices['upward']
    ratio_D = prices['downward']
    ratio_U = prices['upward']
    price_hy = prices['hydrogen']
    price_water = prices['water']
    price_oxyg = prices['oxygen']
    price_ammonia = prices['ammonia']

    P_H2O = []
    P_O2 = []
    for t in range(0, h):
        P_H2O.append(sum(m.P_EL_E[i, t]()/1000 for i in range(0, number_resources)) * c_H2O)
        P_O2.append(sum(m.P_EL_E[i, t]()/1000 for i in range(0, number_resources)) * c_O2)

    if case_nr == 3:
        f_E = sum(price_E[t] * m.P_E_pos[t]() - price_E_market[t] * m.P_E_neg[t]() for t in range(0, h))/1000
        f_E_reservas = sum(
                  - price_B[t] * (m.U_sto_E[0, t]() + m.D_sto_E[0, t]()) +
                  (price_E_D[t] * ratio_D[t] * m.D_sto_E[0, t]() -
                   price_E_U[t] * ratio_U[t] * m.U_sto_E[0, t]()) for t in range(0, h)) / 1000
        f_hy = price_hy * sum(m.P_H2[t]() for t in range(0, h))/1000
    elif case_nr == 2:
        f_E = sum(price_E[t] * m.P_E_pos[t]() - price_E_market[t] * m.P_E_neg[t]() for t in range(0, h))/1000
        f_hy = price_hy * sum(m.P_H2[t]() for t in range(0, h))/1000
    else:
        f_E = sum(price_E[t] * m.P_E_pos[t]() for t in range(0, h))/1000
        f_hy = price_hy * sum(m.P_H2[t]() for t in range(0, h))/1000
        f_E_reservas= 0

    f_water = price_water * sum(m.P_EL_E[i, t]() for i in range(0, number_resources)) * c_H2O/1000
    f_oxyg = price_oxyg * sum(m.P_EL_E[i, t]() for i in range(0, number_resources)) * c_O2/1000
    f_ammonia = price_ammonia * sum(resources['load_ammonia'][0] for t in range(0, h))/1000

    n = 0
    n += 1
    sh1.write(0, n + 1, "Total costs (k€)")
    n += 1
    sh1.write(0, n + 1, "Electricity energy (k€)")
    n += 1
    sh1.write(0, n + 1, "Electricity reserves (k€)")
    n += 1
    sh1.write(0, n + 1, "Hydrogen (k€)")
    n += 1
    sh1.write(0, n + 1, "Water (k€)")
    n += 1
    sh1.write(0, n + 1, "Oxygen (k€)")
    n += 1
    sh1.write(0, n + 1, "Ammonia (k€)")
    n += 1

    if case_nr == 1:
        n = 0
        n += 1
        n_case = 7 * 13
        sh1.write(1, n + 1, (f_E - f_hy + f_water - f_oxyg - f_ammonia) * n_case)
        n += 1
        sh1.write(1, n + 1, f_E * n_case)
        n += 1
        sh1.write(1, n + 1, f_E_reservas * n_case)
        n += 1
        sh1.write(1, n + 1, f_hy * n_case)
        n += 1
        sh1.write(1, n + 1, f_water * n_case)
        n += 1
        sh1.write(1, n + 1, f_oxyg * n_case)
        n += 1
        sh1.write(1, n + 1, f_ammonia * n_case)
        n += 1
    elif case_nr == 2:
        n_case = 13
        n = 0
        n += 1
        sh1.write(1, n + 1, (f_E - f_hy + f_water - f_oxyg - f_ammonia) * n_case)
        n += 1
        sh1.write(1, n + 1, f_E * n_case)
        n += 1
        sh1.write(1, n + 1, f_E_reservas * n_case)
        n += 1
        sh1.write(1, n + 1, f_hy * n_case)
        n += 1
        sh1.write(1, n + 1, f_water * n_case)
        n += 1
        sh1.write(1, n + 1, f_oxyg * n_case)
        n += 1
        sh1.write(1, n + 1, f_ammonia * n_case)
        n += 1

    else:
        n_case = 7 * 13
        n = 0
        n += 1
        sh1.write(1, n + 1, (f_E + f_E_reservas - f_hy + f_water - f_oxyg - f_ammonia) * n_case )
        n += 1
        sh1.write(1, n + 1, f_E * n_case)
        n += 1
        sh1.write(1, n + 1, f_E_reservas * n_case)
        n += 1
        sh1.write(1, n + 1, f_hy * n_case)
        n += 1
        sh1.write(1, n + 1, f_water * n_case)
        n += 1
        sh1.write(1, n + 1, f_oxyg * n_case)
        n += 1
        sh1.write(1, n + 1, f_ammonia * n_case)
        n += 1

    return book



