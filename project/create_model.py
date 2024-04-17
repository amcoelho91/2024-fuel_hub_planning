from numpy import *
from pyomo.environ import *


def create_model(m: ConcreteModel, h: int, number_resources: int, resources: dict, case: int) -> ConcreteModel:
    ''' Create models of resources '''

    m = create_bidding_model(m, h, number_resources, case)
    m = create_market_constraints(m, h, number_resources)

    m = create_PV_model(m, h, number_resources, resources)
    m = create_storage_electrical_model(m, h, number_resources, resources)

    m = create_electrolyzer_model(m, h, number_resources, resources)
    m = create_hydrogen_load_model(m, h, number_resources, resources)
    m = create_storage_hydrogen_model(m, h, number_resources, resources, case)
    m = create_fuel_cell_model(m, h, number_resources, resources)


    #m = create_storage_electrical_model(m, h, number_resources, resources)
    #m = create_market_constraints(m, h, number_resources)

    #m = create_hydrogen_load_model(m, h, number_resources, resources)

    return m


def create_bidding_model(m: ConcreteModel(), h: int, number_resources: int, case: int) -> ConcreteModel:
    ''' Create bidding model '''
    for t in range(0, h):
        resources_power = 0

        #resources_power = resources_power + \
        #                  sum(m.P_sto_E_ch[i, t] - m.P_sto_E_dis[i, t]
        #                      for i in range(0, number_resources))

        resources_power = resources_power + \
                          sum(- m.P_PV[i, t] for i in range(0, number_resources))
        resources_power = resources_power + \
                          sum(m.P_sto_E_ch[i, t] - m.P_sto_E_dis[i, t] for i in range(0, number_resources))
        resources_power = resources_power + \
                          sum(m.P_EL_E[i, t] + m.P_EL_cooling[i, t] for i in range(0, number_resources))
        resources_power = resources_power + \
                          sum(m.P_FC_E[i, t] for i in range(0, number_resources))



        m.c1.add(m.P_E[t] == resources_power)
        #m.c1.add(m.P_E[t] <= 0)


        U_resources_power = 0
        U_resources_power = U_resources_power + \
                          sum(m.U_sto_E_dis[i, t] + m.U_sto_E_ch[i, t] +
                              m.U_PV[i, t] +
                              m.U_EL_E[i, t] +
                              m.U_FC_E[i, t]
                              for i in range(0, number_resources))
        m.c1.add(m.U_E[t] == U_resources_power)


        D_resources_power = 0
        D_resources_power = D_resources_power + \
                          sum(m.D_sto_E_dis[i, t] + m.D_sto_E_ch[i, t] +
                              m.D_PV[i, t] +
                              m.D_EL_E[i, t] +
                              m.D_FC_E[i, t]
                              for i in range(0, number_resources))
        m.c1.add(m.D_E[t] == D_resources_power)




    return m

def create_market_constraints(m: ConcreteModel(), h: int, number_resources: int) -> ConcreteModel:
    ''' Create market constraints model '''
    for i in range(0, number_resources):
        for t in range(0, h):
            m.c1.add(m.U_E[t] == 2 * m.D_E[t])

    return m

def create_PV_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create PV model '''
    max_power = resources['PV']['max_power']
    PV_profile = resources['PV']['PV_profile']
    print(max_power)
    print(PV_profile)
    for i in range(0, number_resources):
        for t in range(0, h):
            m.c1.add(m.P_PV[i, t] <= m.Planning_P_PV[i] * PV_profile[t])
            #m.c1.add(m.P_PV[i, t] == m.P_PV_sto_E[i, t] + m.P_PV_EL[i, t] + m.P_PV_market[i, t])
            m.c1.add(m.U_PV[i, t] <= m.Planning_P_PV[i] - m.P_PV[i, t])
            m.c1.add(m.D_PV[i, t] <= m.P_PV[i, t])
            m.c1.add(m.U_PV[i, t] == 0)
            m.c1.add(m.D_PV[i, t] == 0)

            #m.c1.add(m.Planning_P_PV[i] <= 100000 )
            m.c1.add(m.Planning_P_PV[i] <= 100000 * m.b_Planning_P_PV[i])



    return m

def create_storage_electrical_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create electrical storage model '''
    rend_sto_E = resources['electrical_storage']['efficiency']
    soc_sto_E_max = resources['electrical_storage']['max_capacity']
    soc_sto_E_min = resources['electrical_storage']['min_capacity']
    P_sto_E_dis_max = resources['electrical_storage']['max_discharging']
    P_sto_E_ch_max = resources['electrical_storage']['max_charging']
    soc_sto_E_init = resources['electrical_storage']['initial_soc']


    for i in range(0, number_resources):
        m.c1.add(m.soc_sto_E[i, 0] == soc_sto_E_init)
        m.c1.add(m.soc_sto_E[i, h] >= soc_sto_E_init)

        for t in range(0, h):
            m.c1.add(m.soc_sto_E[i, t + 1] == m.soc_sto_E[i, t] + (m.P_sto_E_ch[i, t] * rend_sto_E - m.P_sto_E_dis[i, t] / rend_sto_E))

            m.c1.add(m.soc_sto_E[i, t + 1] <= soc_sto_E_max)
            m.c1.add(m.soc_sto_E[i, t + 1] >= soc_sto_E_min)

            m.c1.add(m.P_sto_E_dis[i, t] + m.P_sto_E_dis_space[i, t] <= (1 - m.b_sto_E[i, t]) * P_sto_E_dis_max)
            m.c1.add(m.P_sto_E_ch[i, t] + m.P_sto_E_ch_space[i, t] <=  m.b_sto_E[i, t] * P_sto_E_ch_max)

            if t == h - 1:
                m.c1.add(m.U_sto_E_dis[i, t] == 0)
                m.c1.add(m.U_sto_E_ch[i, t] == 0)
                m.c1.add(m.D_sto_E_dis[i, t] == 0)
                m.c1.add(m.D_sto_E_ch[i, t] == 0)

            m.c1.add(m.U_sto_E_dis[i, t] <= P_sto_E_dis_max - m.P_sto_E_dis[i, t])
            m.c1.add(m.U_sto_E_ch[i, t] <= m.P_sto_E_ch[i, t])
            m.c1.add(m.D_sto_E_ch[i, t] <= P_sto_E_ch_max - m.P_sto_E_ch[i, t])
            m.c1.add(m.D_sto_E_dis[i, t] <= m.P_sto_E_dis[i, t])

            m.c1.add(m.U_sto_E_dis[i, t] / rend_sto_E + m.U_sto_E_ch[i, t] * rend_sto_E <= m.soc_sto_E[i, t + 1] - soc_sto_E_min)
            m.c1.add(m.D_sto_E_dis[i, t] / rend_sto_E + m.D_sto_E_ch[i, t] * rend_sto_E <= soc_sto_E_max - m.soc_sto_E[i, t + 1])

            m.c1.add(m.U_sto_E[i, t] == m.U_sto_E_ch[i, t] + m.U_sto_E_dis[i, t])
            m.c1.add(m.D_sto_E[i, t] == m.D_sto_E_ch[i, t] + m.D_sto_E_dis[i, t])

            m.c1.add(m.U_sto_E_ch[i, t] + m.U_sto_E_dis[i, t] + m.D_sto_E_ch[i, t] + m.D_sto_E_dis[i, t] <=
                m.P_sto_E_ch_space[i, t + 1] + m.P_sto_E_dis_space[i, t + 1])

            m.c1.add(m.U_sto_E_ch[i, t] + m.U_sto_E_dis[i, t] + m.D_sto_E_ch[i, t] + m.D_sto_E_dis[i, t] <=
                m.b_sto_E_space[i, t] * 10000000)

            m.c1.add(m.P_sto_E_ch_space[i, t] + m.P_sto_E_dis_space[i, t] <= (1 - m.b_sto_E_space[i, t]) * 10000000)


    return m



def create_electrolyzer_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create electrolyzer model '''
    efficiency = resources['electrolyzer']['efficiency']
    maximum_power = resources['electrolyzer']['max_power']
    transformation_factor = resources['electrolyzer']['transformation_factor']
    cooling_power = resources['electrolyzer']['cooling_power']

    for j in range(0, number_resources):
        for t in range(0, h):
            #m.c1.add(m.P_EL_E[j, t] == m.P_PV_EL[j, t] + m.P_sto_E_EL[j, t])
            m.c1.add(m.P_EL_H2[j, t] == transformation_factor * efficiency * m.P_EL_E[j, t])
            m.c1.add(m.P_EL_H2[j, t] == m.P_EL_load[j, t] + m.P_EL_sto_H2[j, t] * 1)
            m.c1.add(m.P_EL_cooling[j, t] == 0)
            m.c1.add(m.P_EL_E[j, t] <= m.Planning_P_EL_E[j])
            m.c1.add(m.P_EL_E[j, t] <= 2500)

            m.c1.add(m.U_EL_E[j, t] <= m.P_EL_E[j, t])
            m.c1.add(m.D_EL_E[j, t] <= m.Planning_P_EL_E[j] - m.P_EL_E[j, t])
            m.c1.add(m.U_EL_H2[j, t] == transformation_factor * efficiency * m.U_EL_E[j, t])
            m.c1.add(m.D_EL_H2[j, t] == transformation_factor * efficiency * m.D_EL_E[j, t])
            m.c1.add(m.U_EL_H2[j, t] == m.U_EL_sto_H2[j, t] * 1 + m.U_EL_load[j, t])
            m.c1.add(m.D_EL_H2[j, t] == m.D_EL_sto_H2[j, t] * 1 + m.D_EL_load[j, t])

        m.c1.add(m.Planning_P_EL_E[j] <= 1000000 * m.b_Planning_P_EL_E[j])


    return m



def create_storage_hydrogen_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict, case: int) -> ConcreteModel:
    ''' Create hydrogen storage model '''
    efficiency = resources['hydrogen_storage']['efficiency']
    max_soc = resources['hydrogen_storage']['max_capacity']
    min_soc = resources['hydrogen_storage']['min_capacity']
    max_power_dis = resources['hydrogen_storage']['max_discharging']
    max_power_ch = resources['hydrogen_storage']['max_charging']
    soc_initial = resources['hydrogen_storage']['initial_soc']

    for i in range(0, number_resources):
        m.c1.add(m.soc_sto_H2[i, 0] == soc_initial)
        m.c1.add(m.soc_sto_H2[i, h] >= soc_initial)

        for t in range(0, h):
            m.c1.add(m.soc_sto_H2[i, t + 1] == m.soc_sto_H2[i, t] +
                     (m.P_sto_H2_ch[i, t] * efficiency - m.P_sto_H2_dis[i, t] / efficiency))
            m.c1.add(m.soc_sto_H2[i, t] <= max_soc)
            m.c1.add(m.soc_sto_H2[i, t] >= min_soc)
            m.c1.add(m.P_sto_H2_ch[i, t] == m.P_EL_sto_H2[i, t])
            m.c1.add(m.P_sto_H2_dis[i, t] == m.P_sto_H2_FC[i, t] * 1 + m.P_sto_H2_load[i, t])
            m.c1.add(m.P_sto_H2_ch[i, t] <= max_power_ch)
            m.c1.add(m.P_sto_H2_dis[i, t] <= max_power_dis)


            m.c1.add(m.U_EL_sto_H2[i, t] <= m.P_sto_H2_ch[i, t])
            m.c1.add(m.D_EL_sto_H2[i, t] <= max_power_ch - m.P_sto_H2_ch[i, t])

            m.c1.add(m.D_sto_H2_FC[i, t] <= m.P_sto_H2_FC[i, t])
            m.c1.add(m.U_sto_H2_FC[i, t] <= max_power_ch - m.P_sto_H2_dis[i, t])


            m.c1.add(m.U_EL_sto_H2[i, t] <= max_power_ch - m.P_sto_H2_dis[i, t])

            m.c1.add(m.D_EL_sto_H2[i, t] + m.D_sto_H2_FC[i, t] * 1 <= max_soc - m.soc_sto_H2[i, t])
            m.c1.add(m.U_EL_sto_H2[i, t] + m.U_sto_H2_FC[i, t] * 1 <= m.soc_sto_H2[i, t] - min_soc)

    return m


def create_fuel_cell_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create electrolyzer model '''
    efficiency = resources['fuel_cell']['efficiency']
    maximum_power = resources['fuel_cell']['max_power']
    transformation_factor = resources['fuel_cell']['transformation_factor']

    for j in range(0, number_resources):
        for t in range(0, h):
            m.c1.add(m.P_FC_E[j, t] == (efficiency / transformation_factor) * m.P_sto_H2_FC[j, t])
            m.c1.add(m.P_FC_E[j, t] <= m.Planning_P_FC_E[j])

            m.c1.add(m.U_FC_E[j, t] == (efficiency / transformation_factor) * m.U_sto_H2_FC[j, t])
            m.c1.add(m.D_FC_E[j, t] == (efficiency / transformation_factor) * m.D_sto_H2_FC[j, t])
            m.c1.add(m.U_FC_E[j, t] <= m.Planning_P_FC_E[j] - m.P_FC_E[j, t])
            m.c1.add(m.D_FC_E[j, t] <= m.P_FC_E[j, t])

        m.c1.add(m.Planning_P_FC_E[j] <= 1000000 * m.b_Planning_P_FC_E[j])



    return m


def create_hydrogen_load_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create ammonia load model '''
    for i in range(0, number_resources):
        for t in range(0, h):
            #m.c1.add(resources['load_ammonia'][0]/100 == m.P_EL_load[i, t] + m.P_sto_H2_load[i, t] * 0)
            m.c1.add(resources['load_ammonia'][0] / 100 == m.P_EL_load[i, t] + m.P_sto_H2_load[i, t] * 1 - m.U_EL_load[i, t])
            m.c1.add(resources['load_ammonia'][0] / 100 == m.P_EL_load[i, t] + m.P_sto_H2_load[i, t] * 1 + m.D_EL_load[i, t])

    return m


