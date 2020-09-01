import os
import argparse
import csv
import pandas as pd
from typing import Dict

from utils import parse_date
from parse_main_dataset import func_dict, load_colnames

totals_files = []
for file in func_dict.keys():
    base, ext = os.path.splitext(file)
    totals_files.append(base + '_totals' + ext)

assert totals_files == ['covid19_mex_confirmed_totals.csv',
                        'covid19_mex_negative_totals.csv',
                        'covid19_mex_awaiting_totals.csv',
                        'covid19_mex_deceased_totals.csv',
                        'covid19_mex_hospitalised_totals.csv',
                        'covid19_mex_icu_totals.csv']


# csv unix format without any quotes
csv.register_dialect('unixnq', delimiter=',', lineterminator='\n',
                     quoting=csv.QUOTE_NONE)


def write_processed(input_dir: str, date_iso: str, output_dir: str):
    for i, key in enumerate(func_dict.keys()):
        input_filename = os.path.join(input_dir, key)
        input_df = pd.read_csv(input_filename).drop(columns='Fecha')
        row = input_df.cumsum().tail(1)

        f = totals_files[i]
        filename = os.path.join(output_dir, f)

        with open(filename, 'a') as f:
            writer = csv.writer(f, 'unixnq')
            writer.writerow([date_iso] + row.values[0].tolist())

    return None


def write_raw(main_df: pd.DataFrame, colnames: Dict[str, str],
              date_iso: str, output_dir: str):
    for i, func in enumerate(func_dict.values()):
        input_df = func(main_df, colnames)
        row = input_df.cumsum().tail(1).values[0]  # still has index
        # TODO: clean up the groupby call (get rid of ENTIDAD_UM, make Fecha the
        # index)

        f = totals_files[i]
        filename = os.path.join(output_dir, f)

        out_df = pd.read_csv(filename, index_col='Fecha')
        out_df.index = pd.to_datetime(out_df.index)
        out_df.loc[pd.to_datetime(date_iso)] = row

        out_df.sort_index().to_csv(filename)

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='parse main dataset (zip file) and update totals')
    parser.add_argument('-f', dest='input_file', default=None,
                        help='file containing dataset')
    parser.add_argument('-d', '--date', type=str, default=None,
                        help="specify the date to use as yyyymmdd")
    args = parser.parse_args()
    date_filename, date_iso, flag = parse_date(args, return_flag=True)

    data_dir = os.path.join(os.pardir, 'data')
    output_dir = os.path.join(data_dir, 'daily_totals', '')

    if flag:
        # We are reading a date that is not the latest; we calculate dfs using
        # raw data
        input_file = args.input_file
        assert input_file is not None, 'need to provide input file'
        assert input_file.endswith(f'{date_filename}.zip')
        # input_file = os.path.join(data_dir, 'raw', f'datos_abiertos_{date_filename}.zip')
        main_df = pd.read_csv(input_file, compression='zip')
        colnames_dict = load_colnames('catalogo_entidades.csv')
        write_raw(main_df, colnames_dict, date_iso, output_dir)
    else:
        pass
        # We are reading yesterday's totals; the dfs have been processed and
        # stored in the main tidy csv files
        write_processed(data_dir, date_iso, output_dir)

    print(f'Successfully updated daily totals for date {date_iso}')
