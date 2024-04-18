from numpy import *
from pyomo.environ import *

def run_optimization_model(m: ConcreteModel, h: int, number_resources: int, resources: dict, prices: dict, case: int) -> None:
    ''' Run optimization model as per the objective function '''
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
        P_H2O.append(sum(m.P_EL_E[i, t] for i in range(0, number_resources)) * c_H2O)
        P_O2.append(sum(m.P_EL_E[i, t] for i in range(0, number_resources)) * c_O2)

    f_E = sum(price_E[t] * m.P_E[t]
              for t in range(0, h))
    f_E_reservas = sum(
              - price_B[t] * (m.U_E[t] + m.D_E[t]) +
              (price_E_D[t] * ratio_D[t] * m.D_E[t] -
               price_E_U[t] * ratio_U[t] * m.U_E[t]) for t in range(0, h))

    f_water = price_water * sum(m.P_EL_E[i, t] +
                                ratio_D[t] * m.D_EL_E[i, t]
                                - ratio_U[t] * m.U_EL_E[i, t] for i in range(0, number_resources)) * c_H2O
    f_oxyg = price_oxyg * sum(m.P_EL_E[i, t] +
                                ratio_D[t] * m.D_EL_E[i, t]
                                - ratio_U[t] * m.U_EL_E[i, t] for i in range(0, number_resources)) * c_O2
    f_ammonia = price_ammonia * sum(resources['load_ammonia'][0] for t in range(0, h))



    f_planning = get_plannig_costs(m, h, number_resources)

    if 1:
        for t in range(0, h):
            m.c1.add(m.U_E[t] == 0)
            m.c1.add(m.D_E[t] == 0)


    m.value = Objective(expr= (f_E + f_E_reservas + f_water - f_oxyg - f_ammonia) * 365/4 +
                              f_planning * 10000000000
                        , sense=minimize)

    solver = SolverFactory("cplex")
    results = solver.solve(m, tee=False)

    if (results.solver.status == SolverStatus.ok) and \
            (results.solver.termination_condition == TerminationCondition.optimal):
        print("Flow optimized")
    else:
        print("Did no converge")

    print("___________________________________________")
    print("cost f_E", value(f_E))
    print("cost f_E_reservas", value(f_E_reservas))
    print("cost water", value(f_water))
    print("cost f_oxyg", value(f_oxyg))
    print("final operational costs", value(f_E + f_E_reservas + f_water - f_oxyg - f_ammonia))
    print("___________________________________________")
    print("Total investment", value(f_planning)/1000000)
    print("Investment PV", value(m.Planning_P_PV[0]))
    print("Investment EL", value(m.Planning_P_EL_E[0]))
    print("Investment FC", value(m.Planning_P_FC_E[0]))
    print("Investment Electrical Sto - SOC:", value(m.Planning_soc_sto_E[0]), " P:", value(m.Planning_P_sto_E[0]))

    return 0


def get_plannig_costs(m, h, number_resources):
    f_planning = 0

    # Costs from Optimal planning of distributed hydrogen-based multi-energy systems
    fuel_cell_costs = 2255 # 10years
    electrolyzer_costs = 280 # 7 years
    PV_system_costs = 865 # 20 years
    hydrogen_storage_costs = 470 #$/kg  20 years

    discount_rate = 0.05

    for i in range(0, number_resources):
        print(number_resources)
        f_planning = ((m.b_Planning_P_PV[i] * 920 + m.Planning_P_PV[i] * 920 ) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))))
        f_planning = f_planning + ((m.b_Planning_P_FC_E[i] * 2255 + m.Planning_P_FC_E[i] * 2255 ) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-10))))
        f_planning = f_planning + ((m.b_Planning_P_EL_E[i] * 280 + m.Planning_P_EL_E[i] * 280 ) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-7))))
        f_planning = f_planning + ((m.b_Planning_P_EL_E[i] * (150 + 80) + m.Planning_soc_sto_E[i] * 150 +
                                    m.Planning_P_sto_E[i] * 80) *
                      (discount_rate/(1 - (1 + discount_rate) ** (-20))))




    return f_planning