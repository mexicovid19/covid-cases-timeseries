import os
import argparse
import pandas as pd
from typing import Dict

from utils import parse_date, load_colnames

from parsers import (
    confirmados_diarios_por_estado,
    negativos_diarios_por_estado,
    pruebas_pendientes_diarias_por_estado,
    defunciones_diarias_por_estado,
    hospitalizados_diarios_por_estado,
    uci_diarios_por_estado
)


func_dict = dict()
func_dict['covid19_mex_confirmed.csv'] = confirmados_diarios_por_estado
func_dict['covid19_mex_negative.csv'] = negativos_diarios_por_estado
func_dict['covid19_mex_awaiting.csv'] = pruebas_pendientes_diarias_por_estado
func_dict['covid19_mex_deceased.csv'] = defunciones_diarias_por_estado
func_dict['covid19_mex_hospitalised.csv'] = hospitalizados_diarios_por_estado
func_dict['covid19_mex_icu.csv'] = uci_diarios_por_estado


def write_files(main_df: pd.DataFrame, colnames: Dict[str, str], data_dir: str):
    for key, func in func_dict.items():
        df = func(main_df, colnames)
        filename = os.path.join(data_dir, key)
        df.to_csv(filename)

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parse main dataset (zip file)')
    parser.add_argument('input_file', help='file containing dataset')
    parser.add_argument('-d', '--date', type=str, default=None,
                        help="specify the date to use as yyyymmdd")
    args = parser.parse_args()
    date_filename, date_iso = parse_date(args)

    data_dir = os.path.join(os.pardir, 'data')

    # main dataset
    input_file = args.input_file
    assert input_file.endswith(f'{date_filename}.zip')

    try:
        main_df = pd.read_csv(input_file, compression='zip')
        colnames_dict = load_colnames('catalogo_entidades.csv')  # names of 32 states
        write_files(main_df, colnames_dict, data_dir)

        print(f'Successfully parsed datos_abiertos_{date_filename}.zip')
    except FileNotFoundError:
        print('ERROR: Wrong date or missing file')
