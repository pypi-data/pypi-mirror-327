from __future__ import annotations

__doc__ = """
Configurable constants for controlling column and row limitations.
"""
__all__ = [
    "GOOGLE_SHEETS_ROW_LIMIT",
    "EXCEL_ROW_LIMIT",
    "GOOGLE_SHEETS_COL_LIMIT",
    "EXCEL_COL_LIMIT",
]

from typing import Type

from attrs import Attribute

from .exceptions import ColumnLimitExceeded, RowLimitExceeded

#: Maximum number of rows for worksheets in Google Sheets.
GOOGLE_SHEETS_ROW_LIMIT: int = 10_000_000

#: Maximum number of rows for worksheets in Microsoft Excel.
EXCEL_ROW_LIMIT: int = 1_048_576

#: Maximum number of columns for worksheets in Google Sheets.
GOOGLE_SHEETS_COL_LIMIT: int = 18_278

#: Maximum number of columns for worksheets in Microsoft Excel.
EXCEL_COL_LIMIT: int = 16_384


def _validate_buffer_arg(
    instance: Type["RangeName"], attribute: Type[Attribute], value: int
):
    """Validates that the buffer attribute is of type str or int, and that, if
    int, the value must be greater than or equal to zero, and, if str, the value
    must be alphabetical.

    Parameters
    ----------
    instance : RangeName
        ``RangeName`` object.
    attribute : Attribute
        ``attrs.Attribute`` object.
    value : int
        Parameter to validate.

    Raises
    ------
    ValueError : Exception
        Raised if ``buffer`` is not of type int or str, or if less than zero or
        non-alphabetical.
    """

    if not (isinstance(value, str) or isinstance(value, int)):
        raise ValueError(
            f"buffer must be <type 'int'> or <type 'str'> but <type '{type(value)}'> was provided"
        )

    match isinstance(value, int):
        case True:
            if not value >= 0:
                raise ValueError(
                    "buffer must be greater than or equal to zero"
                )
        case False:
            if not value.isalpha():
                raise ValueError(
                    "buffer must only include alphabetical characters"
                )


def _validate_rows_arg(
    instance: Type["RangeName"], attribute: Type[Attribute], value: int
):
    """Validates that the rows argument does not exceed platform limits per
    the source and override_row_limit arguments.

    Parameters
    ----------
    instance : RangeName
        ``RangeName`` object.
    attribute : Attribute
        ``attrs.Attribute`` object.
    value : int
        Parameter to validate.

    Raises
    ------
    RowLimitExceeded : Exception
        Raised if the ``rows`` argument exceeds the predetermined limit set by
        the ``GOOGLE_SHEETS_ROW_LIMIT`` and ``EXCEL_ROW_LIMIT`` constants.
    """

    _value = value + instance.header_rows_size

    match instance.override_row_limit:
        case True:
            rows_limit = _value
        case False:
            rows_limit = (
                GOOGLE_SHEETS_ROW_LIMIT
                if instance.source == "google_sheets"
                else EXCEL_ROW_LIMIT
            )

    if _value > rows_limit:
        message = f"The row limit of {rows_limit} was exceeded by {_value - rows_limit} rows!"
        raise RowLimitExceeded(message) from None


def _validate_cols_arg(
    instance: Type["RangeName"], attribute: Type[Attribute], value: int
):
    """Validates that the ``cols`` argument does not exceed platform limits per
    the ``source`` and ``override_col_limit`` arguments.

    Parameters
    ----------
    instance : RangeName
        ``RangeName`` object.
    attribute : Attribute
        ``attrs.Attribute`` object.
    value : int
        Parameter to validate.

    Raises
    ------
    ColumnLimitExceeded : Exception
        Raised if the ``cols`` argument exceeds the predetermined limit set by
        the ``GOOGLE_SHEETS_COL_LIMIT`` and ``EXCEL_COL_LIMIT`` constants.
    """

    match instance.override_col_limit:
        case True:
            cols_limit = value
        case False:
            cols_limit = (
                GOOGLE_SHEETS_COL_LIMIT
                if instance.source == "google_sheets"
                else EXCEL_COL_LIMIT
            )

    if value > cols_limit:
        message = f"The column limit of {cols_limit} was exceeded by {value - cols_limit} columns!"
        raise ColumnLimitExceeded(message) from None
