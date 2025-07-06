import argparse
from decimal import Decimal

import tabulate

from funcs import (
    get_columns_rows_from_csv,
    get_rows_filtered_by,
    use_mode
)

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True)
parser.add_argument("--where")
parser.add_argument("--aggregate")
args = parser.parse_args()
file_name: str = args.file

with open(file_name, encoding='utf-8') as csvfile:
    headers, rows = get_columns_rows_from_csv(csvfile)

headers_indexes = {
    header: index
    for index, header in enumerate(headers)
}

filter_row = rows.copy()
if args.where:
    signs = [sign for sign in args.where if sign in "><="]
    if signs:
        filter_row = get_rows_filtered_by(
            sign=signs[0],
            rows=rows,
            filter_condition=args.where,
            indices_columns=headers_indexes
        )

if args.aggregate:
    header, mode = args.aggregate.split("=")
    if mode == "avg":
        summa = sum(
            Decimal(row[headers_indexes[header]])
            for row in filter_row
        )
        length = len(filter_row)

        headers = ["avg"]
        filter_row = [[summa / length]]
    elif mode in {"min", "max"}:
        filter_row, headers = use_mode(
            column=header,
            mode_=mode,
            rows_=filter_row,
            indices_columns=headers_indexes
        )

table = tabulate.tabulate(filter_row, headers=headers, tablefmt="psql")
print(table)
