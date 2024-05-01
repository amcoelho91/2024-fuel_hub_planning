from numpy import *
from pyomo.environ import *


def create_model(m: ConcreteModel, h: int, number_resources: int, resources: dict,
                 policy_number: int, reserves_participation: int) -> ConcreteModel:
    ''' Create models of resources '''

    m = create_bidding_model(m, h, number_resources, policy_number)
    m = create_market_constraints(m, h, number_resources, reserves_participation)

    m = create_PV_model(m, h, number_resources, resources)
    m = create_storage_electrical_model(m, h, number_resources, resources)

    m = create_electrolyzer_model(m, h, number_resources, resources)
    m = create_hydrogen_load_model(m, h, number_resources, resources)
    m = create_storage_hydrogen_model(m, h, number_resources, resources)
    m = create_fuel_cell_model(m, h, number_resources, resources)

    return m



#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________
def create_bidding_model(m: ConcreteModel(), h: int, number_resources: int, policy_number: int) -> ConcreteModel:
    ''' Create bidding model '''
    m = create_green_policy(m, h, policy_number)

    m = create_bidding_model_energy(m, h, number_resources)
    m = create_bidding_model_upward(m, h, number_resources)
    m = create_bidding_model_downward(m, h, number_resources)

    return m


def create_green_policy(m: ConcreteModel(), h: int, policy_number: int = 0):
    ''' Define green hydrogen policy '''
    # 0 - no policy
    # 1 - yearly policy
    # 2 - hourly policy
    if policy_number == 1:
        #m.c1.add(sum(m.P_E[t] for t in range(0, h)) <= 0)
        m.c1.add(sum(m.P_EL_E[0, t] for t in range(0,h)) <= sum(m.P_PV[0, t] for t in range(0, h)))
    elif policy_number == 2:
        for t in range(0, h):
            #m.c1.add(m.P_E[t] <= 0)
            m.c1.add(m.P_EL_E[0, t] <= m.P_PV_EL[0, t] + m.P_storage_EL[0, t])
            if t > 0:
                m.c1.add(m.P_storage_EL[0, t] <= m.soc_PV_storage[0, t - 1])
    return m



def create_bidding_model_energy(m: ConcreteModel(), h: int, number_resources: int) -> ConcreteModel:
    ''' Create bidding model for energy '''
    for t in range(0, h):
        resources_power = 0
        resources_power = resources_power + \
                          sum(- m.P_PV[i, t] for i in range(0, number_resources))
        resources_power = resources_power + \
                          sum(m.P_sto_E_ch[i, t] - m.P_sto_E_dis[i, t] for i in range(0, number_resources))
        resources_power = resources_power + \
                          sum(m.P_EL_E[i, t] + m.P_EL_cooling[i, t] for i in range(0, number_resources))
        resources_power = resources_power + \
                          sum(-m.P_FC_E[i, t] for i in range(0, number_resources))

        m.c1.add(m.P_E[t] == m.P_network_storage[0, t] * 1.01 + m.P_network_EL[0, t] * 1.01 -
                 m.P_PV_network[0, t] - m.P_storage_network[0, t] - m.P_FC_E[0, t])
        m.c1.add(m.P_E_real[t] == m.P_network_storage[0, t] + m.P_network_EL[0, t] -
                 m.P_PV_network[0, t] - m.P_storage_network[0, t] - m.P_FC_E[0, t])
        for t in range(0, 0):
            if t == 0:
                m.c1.add(m.soc_PV_to_storage[t] == m.P_PV[0, t] - m.P_EL_E[0, t])
            else:
                m.c1.add(m.soc_PV_to_storage[t] == m.soc_PV_to_storage[t - 1] + m.P_PV[0, t] - m.P_EL_E[0, t])

    return m


def create_bidding_model_upward(m: ConcreteModel(), h: int, number_resources: int) -> ConcreteModel:
    ''' Create bidding model upward '''
    for t in range(0, h):
        U_resources_power = 0
        U_resources_power = U_resources_power + \
                          sum(m.U_sto_E_dis[i, t] + m.U_sto_E_ch[i, t] +
                              m.U_PV[i, t] +
                              m.U_EL_E[i, t] +
                              m.U_FC_E[i, t]
                              for i in range(0, number_resources))
        m.c1.add(m.U_E[t] == U_resources_power)
    return m

def create_bidding_model_downward(m: ConcreteModel(), h: int, number_resources: int) -> ConcreteModel:
    ''' Create bidding model downward'''
    for t in range(0, h):
        D_resources_power = 0
        D_resources_power = D_resources_power + \
                          sum(m.D_sto_E_dis[i, t] + m.D_sto_E_ch[i, t] +
                              m.D_PV[i, t] +
                              m.D_EL_E[i, t] +
                              m.D_FC_E[i, t]
                              for i in range(0, number_resources))
        m.c1.add(m.D_E[t] == D_resources_power)
    return m

#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

def create_market_constraints(m: ConcreteModel(), h: int, number_resources: int,
                              reserves_participation: int) -> ConcreteModel:
    ''' Create market constraints model '''
    for i in range(0, number_resources):
        for t in range(0, h):
            m.c1.add(m.U_E[t] == 2 * m.D_E[t])

    if 1 - reserves_participation:
        for t in range(0, h):
            m.c1.add(m.U_E[t] == 0)
            m.c1.add(m.D_E[t] == 0)

    return m

#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________
def create_PV_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create PV model '''
    max_power = resources['PV']['max_power']
    PV_profile = resources['PV']['PV_profile']
    print(max_power)
    print(PV_profile)
    for i in range(0, number_resources):
        for t in range(0, h):
            m.c1.add(m.P_PV[i, t] <= m.Planning_P_PV[i] * PV_profile[t])
            m.c1.add(m.P_PV[i, t] == m.P_PV_storage[i, t] + m.P_PV_network[i, t] + m.P_PV_EL[i, t])
            m.c1.add(m.U_PV[i, t] <= m.Planning_P_PV[i] - m.P_PV[i, t])
            m.c1.add(m.D_PV[i, t] <= m.P_PV[i, t])
            m.c1.add(m.U_PV[i, t] == 0)
            m.c1.add(m.D_PV[i, t] == 0)

            #m.c1.add(m.Planning_P_PV[i] <= 100000 )
            m.c1.add(m.Planning_P_PV[i] <= 20 * 1000 * m.b_Planning_P_PV[i])



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
        soc_sto_E_max = m.Planning_soc_sto_E[i]
        soc_sto_E_min = m.Planning_soc_sto_E[i] * 0.05
        soc_sto_E_init = m.Planning_soc_sto_E[i] * 0.6


        m.c1.add(m.soc_sto_E[i, 0] == soc_sto_E_init)
        m.c1.add(m.soc_sto_E[i, h] >= soc_sto_E_init)
        m.c1.add(m.soc_PV_storage[i, 0] == soc_sto_E_init)


        for t in range(0, h):
            m.c1.add(m.soc_sto_E[i, t + 1] == m.soc_sto_E[i, t] + (m.P_sto_E_ch[i, t] * rend_sto_E - m.P_sto_E_dis[i, t] / rend_sto_E))

            m.c1.add(m.soc_sto_E[i, t + 1] <= soc_sto_E_max)
            m.c1.add(m.soc_sto_E[i, t + 1] >= soc_sto_E_min)

            m.c1.add(m.P_sto_E_ch[i, t] == m.P_PV_storage[i, t] + m.P_network_storage[i, t])
            m.c1.add(m.P_sto_E_dis[i, t] == m.P_storage_EL[i, t] + m.P_storage_network[i, t])
            m.c1.add(m.P_sto_E_dis[i, t] + m.P_sto_E_dis_space[i, t] <= (1 - m.b_sto_E[i, t]) * 30 * 1000)
            m.c1.add(m.P_sto_E_ch[i, t] + m.P_sto_E_ch_space[i, t] <=  m.b_sto_E[i, t] * 30 * 1000)
            m.c1.add(m.P_sto_E_dis[i, t] + m.P_sto_E_dis_space[i, t] <= m.Planning_P_sto_E[i])
            m.c1.add(m.P_sto_E_ch[i, t] + m.P_sto_E_ch_space[i, t] <= m.Planning_P_sto_E[i])

            m.c1.add(m.Planning_P_sto_E[i] <= m.b_Planning_P_sto_E[i] * 30 * 1000)
            m.c1.add(m.Planning_soc_sto_E[i] <= m.b_Planning_P_sto_E[i] * 30 * 1000)

            m.c1.add(m.Planning_P_sto_E[i] <= m.Planning_soc_sto_E[i])

            m.c1.add(m.soc_PV_storage[i, t + 1] == m.soc_PV_storage[i, t] + (
                        m.P_PV_storage[i, t] * rend_sto_E - m.P_storage_EL[i, t] / rend_sto_E))

            if t == h - 1:
                m.c1.add(m.U_sto_E_dis[i, t] == 0)
                m.c1.add(m.U_sto_E_ch[i, t] == 0)
                m.c1.add(m.D_sto_E_dis[i, t] == 0)
                m.c1.add(m.D_sto_E_ch[i, t] == 0)

            m.c1.add(m.U_sto_E_dis[i, t] <= m.Planning_P_sto_E[i] - m.P_sto_E_dis[i, t])
            m.c1.add(m.U_sto_E_ch[i, t] <= m.P_sto_E_ch[i, t])
            m.c1.add(m.D_sto_E_ch[i, t] <= m.Planning_P_sto_E[i] - m.P_sto_E_ch[i, t])
            m.c1.add(m.D_sto_E_dis[i, t] <= m.P_sto_E_dis[i, t])

            m.c1.add(m.U_sto_E_dis[i, t] / rend_sto_E + m.U_sto_E_ch[i, t] * rend_sto_E <= m.soc_sto_E[i, t + 1] - soc_sto_E_min)
            m.c1.add(m.D_sto_E_dis[i, t] / rend_sto_E + m.D_sto_E_ch[i, t] * rend_sto_E <= soc_sto_E_max - m.soc_sto_E[i, t + 1])

            m.c1.add(m.U_sto_E[i, t] == m.U_sto_E_ch[i, t] + m.U_sto_E_dis[i, t])
            m.c1.add(m.D_sto_E[i, t] == m.D_sto_E_ch[i, t] + m.D_sto_E_dis[i, t])

            m.c1.add(m.U_sto_E_ch[i, t] + m.U_sto_E_dis[i, t] + m.D_sto_E_ch[i, t] + m.D_sto_E_dis[i, t] <=
                m.P_sto_E_ch_space[i, t + 1] + m.P_sto_E_dis_space[i, t + 1])

            m.c1.add(m.U_sto_E_ch[i, t] + m.U_sto_E_dis[i, t] + m.D_sto_E_ch[i, t] + m.D_sto_E_dis[i, t] <=
                m.b_sto_E_space[i, t] * 30 * 1000)

            m.c1.add(m.P_sto_E_ch_space[i, t] + m.P_sto_E_dis_space[i, t] <= (1 - m.b_sto_E_space[i, t]) * 30 * 1000)


    return m



def create_electrolyzer_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create electrolyzer model '''
    efficiency = resources['electrolyzer']['efficiency']
    maximum_power = resources['electrolyzer']['max_power']
    transformation_factor = resources['electrolyzer']['transformation_factor']
    cooling_power = resources['electrolyzer']['cooling_power']

    for j in range(0, number_resources):
        for t in range(0, h):
            m.c1.add(m.P_EL_E[j, t] == m.P_PV_EL[j, t] + m.P_storage_EL[j, t] + m.P_network_EL[j, t])
            m.c1.add(m.P_EL_H2[j, t] == transformation_factor * efficiency * m.P_EL_E[j, t])
            m.c1.add(m.P_EL_H2[j, t] == m.P_EL_load[j, t] + m.P_EL_sto_H2[j, t] * 1)
            m.c1.add(m.P_EL_cooling[j, t] == 0)
            m.c1.add(m.P_EL_E[j, t] <= m.Planning_P_EL_E[j])
            m.c1.add(m.P_EL_E[j, t] <= 100 * 1000)

            m.c1.add(m.U_EL_E[j, t] <= m.P_EL_E[j, t])
            m.c1.add(m.D_EL_E[j, t] <= m.Planning_P_EL_E[j] - m.P_EL_E[j, t])
            m.c1.add(m.U_EL_H2[j, t] == transformation_factor * efficiency * m.U_EL_E[j, t])
            m.c1.add(m.D_EL_H2[j, t] == transformation_factor * efficiency * m.D_EL_E[j, t])
            m.c1.add(m.U_EL_H2[j, t] == m.U_EL_sto_H2[j, t] * 1)
            m.c1.add(m.D_EL_H2[j, t] == m.D_EL_sto_H2[j, t] * 1)

        m.c1.add(m.Planning_P_EL_E[j] <=  100 * 1000 * m.b_Planning_P_EL_E[j])


    return m



def create_storage_hydrogen_model(m: ConcreteModel(), h: int, number_resources: int, resources: dict) -> ConcreteModel:
    ''' Create hydrogen storage model '''
    efficiency = resources['hydrogen_storage']['efficiency']
    max_soc = resources['hydrogen_storage']['max_capacity']
    min_soc = resources['hydrogen_storage']['min_capacity']
    max_power_dis = resources['hydrogen_storage']['max_discharging']
    max_power_ch = resources['hydrogen_storage']['max_charging']
    soc_initial = resources['hydrogen_storage']['initial_soc']


    for i in range(0, number_resources):
        max_soc = m.Planning_soc_sto_H2[i]
        min_soc = m.Planning_soc_sto_H2[i] * 0.05
        soc_initial = m.Planning_soc_sto_H2[i] * 0.6
        max_power_dis = m.Planning_P_sto_H2[i]
        max_power_ch = m.Planning_P_sto_H2[i]

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

            m.c1.add(m.Planning_soc_sto_H2[i] <= 1000000 * m.b_Planning_soc_sto_H2[i])
            m.c1.add(m.Planning_P_sto_H2[i] <= 1000000 * m.b_Planning_soc_sto_H2[i])
            m.c1.add(m.Planning_P_sto_H2[i] <= m.Planning_soc_sto_H2[i])




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
            m.c1.add(resources['load_hydrogen'][t] == m.P_EL_load[i, t] + m.P_sto_H2_load[i, t] * 1)
            m.c1.add(resources['load_hydrogen'][t] == m.P_EL_load[i, t] + m.P_sto_H2_load[i, t] * 1)

    return m


