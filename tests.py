import csv
from decimal import Decimal

import pytest

from funcs import (
    get_rows_filtered_by,
    get_columns_rows_from_csv,
    use_mode
)

with open("data.csv", encoding="utf-8") as csvfile:
    headers, rows = get_columns_rows_from_csv(csvfile)


headers_indexes = {
    header: index
    for index, header in enumerate(headers)
}
# print(headers_indexes)
#
# a = use_mode(
#         column="rating",
#         mode_="max",
#         rows_=rows,
#         indices_columns=headers_indexes
#     )
# print(a)

def test_filter_columns() -> None:
    arguments_func = {
        "rows": rows,
        "indices_columns": headers_indexes
    }
    assert len(get_rows_filtered_by(
        sign=">",
        filter_condition="rating>4.7",
        **arguments_func
    )) == 2

    assert len(get_rows_filtered_by(
        sign="<",
        filter_condition="price<1000",
        **arguments_func
    )) == 3

    assert len(get_rows_filtered_by(
        sign="=",
        filter_condition="brand=xiaomi",
        **arguments_func
    )) == 2


def test_mode() -> None:
    data, mode = use_mode(
        column="rating",
        mode_="max",
        rows_=rows,
        indices_columns=headers_indexes
    )
    assert (data[0][0] == Decimal('4.9') and mode[0] == "max")
    # assert (data[0][0] == Decimal('4.4') and mode[0] == "min")




