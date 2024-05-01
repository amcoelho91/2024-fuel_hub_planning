from numpy import *
from pyomo.environ import *
import time

def run_optimization_model(m: ConcreteModel, h: int, number_resources: int, resources: dict, prices: dict) -> None:
    ''' Run optimization model as per the objective function '''
    c_H2O = resources['electrolyzer']['c_H2O']
    c_O2 = resources['electrolyzer']['c_O2']

    price_E = prices['energy']  # €/kWh
    price_E_market = prices['energy_market']

    price_B = prices['band'] # €/kWh
    price_E_D = prices['downward'] # €/kW
    price_E_U = prices['upward'] # €/kW
    ratio_D = prices['downward']
    ratio_U = prices['upward']
    price_hy = prices['hydrogen'] # €/kg
    price_water = prices['water'] # €/L
    price_oxyg = prices['oxygen'] # €/kg
    price_hydrogen = prices['hydrogen'] # €/kg

    P_H2O = []
    P_O2 = []
    for t in range(0, h):
        P_H2O.append(sum(m.P_EL_E[i, t] for i in range(0, number_resources)) * c_H2O)
        P_O2.append(sum(m.P_EL_E[i, t] for i in range(0, number_resources)) * c_O2)

    #---------------------------------------------------------------------------------------------------------------
    f_E = sum(price_E_market[t] * m.P_E[t] for t in range(0, h))
    f_E_reservas = sum( - price_B[t] * (m.U_E[t] + m.D_E[t]) +
                        (price_E_D[t] * ratio_D[t] * m.D_E[t] - price_E_U[t] * ratio_U[t] * m.U_E[t])
                        for t in range(0, h))
    efficiency = resources['electrolyzer']['efficiency']
    transformation_factor = resources['electrolyzer']['transformation_factor']
    f_water = price_water * sum(sum(m.P_EL_E[i, t] + ratio_D[t] * m.D_EL_E[i, t] - ratio_U[t] * m.U_EL_E[i, t]
                              for i in range(0, number_resources)) for t in range(0, h)) * transformation_factor * efficiency * c_H2O
    f_oxyg = price_oxyg * sum(sum(m.P_EL_E[i, t] + ratio_D[t] * m.D_EL_E[i, t] - ratio_U[t] * m.U_EL_E[i, t]
                              for i in range(0, number_resources)) for t in range(0, h)) * transformation_factor * efficiency * c_O2
    f_hydrogen = price_hydrogen * sum(resources['load_hydrogen'][t] for t in range(0, h))

    investment_max_value = 5 * 1000 * 1000
    f_planning = get_plannig_costs(m, h, number_resources, investment_max_value)

    m.c1.add(f_planning <= investment_max_value)
    #m.c1.add(m.b_Planning_P_sto_E[0] == 1)
    #m.c1.add(m.Planning_P_EL_E[0] == 3000)


    yearly_multiplier = 365 / (h / 24)

    #---------------------------------------------------------------------------------------------------------------
    m.value = Objective(expr= (f_E + f_E_reservas + f_water - f_oxyg - f_hydrogen) * yearly_multiplier +
                              f_planning
                        , sense=minimize)
    start_time = time.time()
    solver = SolverFactory("cplex")
    results = solver.solve(m, tee=False)

    if (results.solver.status == SolverStatus.ok) and \
            (results.solver.termination_condition == TerminationCondition.optimal):
        print("Flow optimized")
    else:
        print("Did no converge")
    print("Execution time={:.2f}".format(time.time() - start_time))
    #---------------------------------------------------------------------------------------------------------------

    f_E = sum(price_E_market[t] * m.P_E_real[t] for t in range(0, h))
    print_results(m, f_E, f_E_reservas, f_water, f_oxyg, f_hydrogen, f_planning, yearly_multiplier)

    print(value(sum(sum(m.P_EL_E[i, t]
                              for i in range(0, number_resources)) for t in range(0, h))))

    return 0


def get_plannig_costs(m: ConcreteModel, h: int, number_resources: int, investment_max_value: int) -> ConcreteModel():
    ''' Get planning costs '''
    # Costs from Optimal planning of distributed hydrogen-based multi-energy systems
    fuel_cell_costs = 2255 # €/kW 10years
    electrolyzer_costs = 280 # €/kW 7 years
    PV_system_costs = 865 # €/kW 20 years
    hydrogen_storage_costs = 470 #$/kg  20 years

    discount_rate = 0.05
    f_planning = 0
    for i in range(0, number_resources):
        print(number_resources)
        f_planning = ((m.b_Planning_P_PV[i] * 920 + m.Planning_P_PV[i] * 920 ) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))))
        f_planning = f_planning + ((m.b_Planning_P_FC_E[i] * 2255 + m.Planning_P_FC_E[i] * 2255 ) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-10))))
        f_planning = f_planning + ((m.b_Planning_P_EL_E[i] * 280 + m.Planning_P_EL_E[i] * 280 ) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-7))))
        f_planning = f_planning + ((m.b_Planning_P_sto_E[i] * (150 + 80) + m.Planning_soc_sto_E[i] * 150 +
                                    m.Planning_P_sto_E[i] * 80) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))))
        f_planning = f_planning + ((m.b_Planning_soc_sto_H2[i] * (470) + m.Planning_soc_sto_H2[i] * 470) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))))

        m.c1.add(m.Planning_P_PV[i] * 920 *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))) <= investment_max_value)
        m.c1.add(m.Planning_P_FC_E[i] * 2255 *
                      (discount_rate/(1 - (1 + discount_rate) ** (-10)))<= investment_max_value)
        m.c1.add(m.Planning_P_EL_E[i] * 280 *
                      (discount_rate/(1 - (1 + discount_rate) ** (-7)))<= investment_max_value)
        m.c1.add((m.Planning_soc_sto_E[i] * 150 + m.Planning_P_sto_E[i] * 80) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))) <= investment_max_value)
        m.c1.add(m.Planning_soc_sto_H2[i] * 470 *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20)))<= investment_max_value)


    return f_planning

def print_results(m: ConcreteModel(), f_E, f_E_reservas, f_water, f_oxyg, f_hydrogen, f_planning,
                  yearly_multiplier) -> None:
    print("___________________________________________")
    print("cost f_E (k€)={:.2f}".format(value(f_E) * yearly_multiplier / 1000))
    print("cost f_E_reservas (k€)={:.2f}".format(value(f_E_reservas) * yearly_multiplier / 1000))
    print("cost water (k€)={:.2f}".format(value(f_water) * yearly_multiplier / 1000))
    print("cost f_oxyg (k€)={:.2f}".format(value(f_oxyg) * yearly_multiplier / 1000))
    print("cost f_hydrogen (k€)={:.2f}".format(value(f_hydrogen) * yearly_multiplier / 1000))
    print("final operational costs (k€)={:.2f}".format(value(f_E + f_E_reservas + f_water - f_oxyg - f_hydrogen) *
                                                  yearly_multiplier / 1000))
    print("___________________________________________")
    print("Total investment (k€)={:.2f}".format(value(f_planning)/1000))
    print("Investment PV={:.2f}".format(value(m.Planning_P_PV[0])))
    print("Investment EL={:.2f}".format(value(m.Planning_P_EL_E[0])))
    print("Investment FC={:.2f}".format(value(m.Planning_P_FC_E[0])))
    print("Investment Electrical Sto - SOC={:.2f}".format(value(m.Planning_soc_sto_E[0])))
    print("Investment Electrical Sto - P={:.2f}".format(value(m.Planning_P_sto_E[0])))
    print("Investment Hydrogen Sto - SOC={:.2f}".format(value(m.Planning_soc_sto_H2[0])))
    print("Investment Hydrogen Sto - P={:.2f}".format(value(m.Planning_P_sto_H2[0])))