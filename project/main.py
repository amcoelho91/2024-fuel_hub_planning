from pyomo.environ import *

from get_resources import *
from get_prices import *
from create_variables import *
from create_model import *
from run_optimization_model import *
from save_results import *
from create_figures import *
from create_figures_bar import *
from create_figures_SOC import *
from save_results2 import *

from termcolor import colored, cprint


def main():
    ''' Function of the aggregator optimization model '''

    h = 24 * 1 * 8

    policy_number = 1  # 0 - no policy || 1 - yearly policy || 2 - hourly policy
    reserves_participation = 0  # 0 - no participation || 1 - participation

    number_resources = 1

    #----------------------------------------------------------------------------------------

    print("... Get data ...")
    resources = get_resources(h)
    prices = get_prices(h)

    # Create pyomo model
    print("... Create model  ...")
    m = ConcreteModel()
    m.c1 = ConstraintList()

    # Run aggregator model
    m = create_variables(m, h, number_resources)
    m = create_model(m, h, number_resources, resources, policy_number, reserves_participation)
    print("... Run model ...")
    run_optimization_model(m, h, number_resources, resources, prices)

    print("... Save results ...")
    #save_results(m, h, 2, prices, resources, number_resources)
    save_results2(m, h, 2, prices, resources, number_resources)

    print("")
    show_figure_option = 1
    save_figure_option = 1
    #create_figures(m, h, case_nr, save_figure_option, show_figure_option)
    #create_figures_bar(m, h, case_nr)
    #create_figures_SOC(m, h, resources, case_nr)

    return 0


if __name__ == '__main__':
    main()