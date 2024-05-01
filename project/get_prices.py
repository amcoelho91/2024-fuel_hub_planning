from pathlib import Path
from xlrd import *


INPUT_DIR = Path(__file__).parent.parent / "data_input"


def get_prices(h: int) -> dict:
    ''' Get prices data '''

    book_networks = INPUT_DIR / "2022 - Prices_8days.xls"

    wb_networks = open_workbook(book_networks)
    xl_sheet = wb_networks.sheet_by_index(0)

    energy_market = [xl_sheet.cell(1 + t, 2).value/1000 for t in range(0, h)]
    energy = [50/1000 for t in range(0, h)]
    band = [xl_sheet.cell(1 + t, 3).value/1000 for t in range(0, h)]
    upward = [xl_sheet.cell(1 + t, 4).value/1000 for t in range(0, h)]
    downward = [xl_sheet.cell(1 + t, 5).value/1000 for t in range(0, h)]
    ratio_U = [xl_sheet.cell(1 + t, 6).value for t in range(0, h)]
    ratio_D = [xl_sheet.cell(1 + t, 7).value for t in range(0, h)]

    prices = {'energy': energy,
              'energy_market': energy_market,
                'band': band,
                'upward': upward,
                'downward': downward,
                'ratio_U': ratio_U,
                'ratio_D': ratio_D,
                'hydrogen': 8,          # €/kg
                'water': 0.0014,        # €/L  ->   1.4 €/m3 = 0.0014 €/L
                'oxygen': 0.15,         # €/kg ->   150 €/ton = 0.15 €/kg
                'hydrogen': 3}       # €/kg ->   hydrogen

    return prices


if __name__ == '__main__':
    get_prices(24 * 365)
















