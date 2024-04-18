from numpy import *
from pyomo.environ import *


def create_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the optimization model '''
    m = create_objective_function_variables(m, h, number_resources)
    m = create_PV_variables(m, h, number_resources)
    m = create_storage_electrical_variables(m, h, number_resources)

    m = create_electrolyzer_variables(m, h, number_resources)
    m = create_fuel_cell_variables(m, h, number_resources)
    m = create_storage_H2_variables(m, h, number_resources)
    m = create_load_variables(m, h, number_resources)

    return m

def create_PV_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the PV model'''
    m.P_PV = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_PV = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_PV = Var(arange(number_resources), arange(h), domain=NonNegativeReals)

    m.Planning_P_PV = Var(arange(number_resources), domain=NonNegativeReals)
    m.b_Planning_P_PV = Var(arange(number_resources), domain=Binary)

    return m

def create_storage_electrical_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the electrical storage model'''
    m.soc_sto_E = Var(arange(number_resources), arange(h + 1), domain=NonNegativeReals)
    m.P_sto_E_ch = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_sto_E_dis = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_sto_E_ch_space = Var(arange(number_resources), arange(h + 1), domain=NonNegativeReals)
    m.P_sto_E_dis_space = Var(arange(number_resources), arange(h + 1), domain=NonNegativeReals)
    m.U_sto_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_sto_E_ch = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_sto_E_dis = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_sto_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_sto_E_ch = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_sto_E_dis = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.b_sto_E = Var(arange(number_resources), arange(h), domain=Binary)
    m.b_sto_E_space = Var(arange(number_resources), arange(h), domain=Binary)

    m.Planning_soc_sto_E = Var(arange(number_resources), domain=NonNegativeReals)
    m.Planning_P_sto_E = Var(arange(number_resources), domain=NonNegativeReals)
    m.b_Planning_P_sto_E = Var(arange(number_resources), domain=Binary)

    return m

def create_electrolyzer_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the electrolyzer model '''
    m.P_EL_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_EL_H2 = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_EL_sto_H2 = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_EL_cooling = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_EL_load = Var(arange(number_resources), arange(h), domain=NonNegativeReals)

    m.U_EL_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_EL_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_EL_H2 = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_EL_H2 = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_EL_sto_H2 = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_EL_sto_H2 = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_EL_load = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_EL_load = Var(arange(number_resources), arange(h), domain=NonNegativeReals)

    m.Planning_P_EL_E = Var(arange(number_resources), domain=NonNegativeReals)
    m.b_Planning_P_EL_E = Var(arange(number_resources), domain=Binary)

    return m


def create_fuel_cell_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the fuel cell model '''
    m.P_FC_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_sto_H2_FC = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_sto_H2_FC = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_sto_H2_FC = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.U_FC_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.D_FC_E = Var(arange(number_resources), arange(h), domain=NonNegativeReals)

    m.Planning_P_FC_E = Var(arange(number_resources), domain=NonNegativeReals)
    m.b_Planning_P_FC_E = Var(arange(number_resources), domain=Binary)

    return m


def create_storage_H2_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the hydrogen storage model '''
    m.soc_sto_H2 = Var(arange(number_resources), arange(h + 1), domain=NonNegativeReals)
    m.P_sto_H2_ch = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_sto_H2_dis = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_sto_H2_market = Var(arange(number_resources), arange(h), domain=NonNegativeReals)
    m.P_sto_H2_load = Var(arange(number_resources), arange(h), domain=NonNegativeReals)

    m.Planning_soc_sto_H2 = Var(arange(number_resources), domain=NonNegativeReals)
    m.Planning_P_sto_H2 = Var(arange(number_resources), domain=NonNegativeReals)
    m.b_Planning_soc_sto_H2 = Var(arange(number_resources), domain=Binary)

    return m


def create_load_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the ammonia load model '''
    m.P_load = Var(arange(number_resources), arange(h), domain=NonNegativeReals)

    return m

def create_objective_function_variables(m: ConcreteModel, h: int, number_resources: int) -> ConcreteModel:
    ''' Create variables for the objective function '''
    m.P_E = Var(arange(h), domain=Reals)
    m.U_E = Var(arange(h), domain=NonNegativeReals)
    m.D_E = Var(arange(h), domain=NonNegativeReals)
    m.P_H2 = Var(arange(h), domain=NonNegativeReals)
    m.P_NH3 = Var(arange(h), domain=NonNegativeReals)

    return m



