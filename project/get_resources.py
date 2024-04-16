from numpy import *
from pyomo.environ import *
import pandas as pd
from pathlib import Path
import json

INPUT_DIR = Path(__file__).parent.parent / "data_input"


def get_resources(case_nr: int) -> dict:
    ''' Get resources data '''

    electrical_storage = {'efficiency': 0.9,
                        'initial_soc': 500000 * 0.7,
                        'max_capacity': 500000,
                        'min_capacity': 500,
                        'max_discharging': 25000,
                        'max_charging': 25000,
                         }


    PV =            {"max_power": 40000 * 0.5,              # kW
                     "PV_profile": get_PV_profile(case_nr)}  # profile (%)



    electrolyzer = {    'efficiency': 0.78,
                        'max_power': 2500 * 1,                   # kW    ############################################################################################
                        'transformation_factor': 25.35/1000,  # kg H2/kWh -> 25.35 kg H2/MWh
                        'c_H2O': 10,                          # 10 L/kg H2
                        'c_O2': 8.304,                        # 8.304 kg O2 / kg H2
                        'cooling_power': 962                  # kW
                    }

    hydrogen_compressor = {'alpha': 1.79,       # kW/kg
                           'max_power': 1267.5 * 1, # kg
                         }



    hydrogen_storage = {'efficiency': 1,
                        'max_capacity': 100,   # kg
                        'min_capacity': 10,    # kg
                        'max_discharging': 40, # kg/h
                        'max_charging': 40,    # kg/h
                        'initial_soc': 80      # kg
                        }

    fuel_cell = {'efficiency': 0.6,
                 'max_power': 10000}


    load_ammonia = [4200 for i in range(0, 24)]

    resources = {       'PV': PV,
                        'electrical_storage': electrical_storage,
                        'electrolyzer': electrolyzer,
                        'fuel_cell': fuel_cell,
                        'hydrogen_compressor': hydrogen_compressor,
                        'hydrogen_storage': hydrogen_storage,


                        'load_ammonia': load_ammonia
                 }

    return resources



def get_PV_profile(case_nr) -> list:
    ''' Load PV data from JSON and read the swflx values'''

    if case_nr == 1:
        ''' Gets the data from JSON and transforms it '''
        with open(INPUT_DIR / "Montijo.json", encoding='utf-8') as inputfile:
            df = pd.read_json(inputfile)

        PV_profile = []
        PV_profile_data = []
        test_date = df['data'][0]['datetime']
        for i in range(0, len(df)):
            if 1:
                if df['data'][i]['datetime']  != test_date and df['data'][i]['datetime'][0:4] == '2022':
                    test_date = df['data'][i]['datetime']
                    PV_profile_data.append([df['data'][i]['datetime'][0:10],
                                            df['data'][i]['datetime'][11:],
                                            df['data'][i]['variable']['swflx'],
                                            df['data'][i]['variable']['swflx']/1030]) # 1030 is the maximum swflx, used to
                                                                                      # put PV in percentage
                    PV_profile.append(df['data'][i]['variable']['swflx'])
        PV_profile.append(0)
        pd.DataFrame(PV_profile_data).to_csv(INPUT_DIR / 'PV_profile_data.csv')

        PV_profile = [i/max(PV_profile) for i in PV_profile]

    elif case_nr == 2:
        ''' Loads the data from excel file '''
        df = pd.read_csv(INPUT_DIR / 'PV_profile_data_short.csv')
        PV_profile = df['2'].values.tolist()
        PV_profile = [i/max(PV_profile) for i in PV_profile]
        PV_profile.reverse()
    else:
        ''' Loads the data from excel file '''
        df = pd.read_csv(INPUT_DIR / 'PV_profile_data_4days.csv')
        PV_profile = df['2'].values.tolist()
        PV_profile = [i/max(PV_profile) for i in PV_profile]
        PV_profile.reverse()

    print(PV_profile)
    print(max(PV_profile))
    return PV_profile
