import re
import os

import pandas as pd
from datavalid import load_config

from .clean import float_to_int_str, names_to_title_case


datavalid_config = load_config(os.path.join(os.path.dirname(__file__), '../data'))


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Removes unnamed columns and convert column names to snake case

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    df = df[[col for col in df.columns if not col.startswith("Unnamed:")]]
    df.columns = [
        re.sub(r"[\s\W]+", "_", col.strip()).lower().strip("_")
        for col in df.columns]
    return df


def set_values(df: pd.DataFrame, value_dict: dict) -> pd.DataFrame:
    """Set entire column to a value.

    Multiple columns can be specified each as a single key in value_dict

    Examples:
        >>> df = set_values(df, {
        ...     "agency": "Brusly PD",
        ...     "data_production_year": 2020
        ... })

    Args:
        df (pd.DataFrame):
            the frame to process
        value_dict (dict):
            the mapping between column name and what value should be set
            for that column.

    Returns:
        the updated frame
    """
    for col, val in value_dict.items():
        df.loc[:, col] = val
    return df


def rearrange_personnel_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Performs final processing step for a personnel table

    This performs the following tasks:
    - discard rows with empty uid
    - discard columns not present in PERSONNEL_COLUMNS
    - drop row duplicates
    - convert name columns to title case
    - convert numeric columns to int or str

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    return datavalid_config.rearrange_columns(
        'personnel',
        df[df.uid.notna() & (df.uid != '')]
        .drop_duplicates(subset=['uid'])
        .pipe(names_to_title_case, ["first_name", "last_name", "middle_name", "middle_initial"])
        .pipe(float_to_int_str, ["birth_year", "birth_month", "birth_day"])
        .sort_values('uid')
    )


def rearrange_event_columns(df):
    """Performs final processing step for an event table

    This performs the following tasks:
    - discard columns not present in EVENT_COLUMNS
    - drop row duplicates
    - convert numeric columns to int or str

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    return datavalid_config.rearrange_columns(
        'event',
        df
        .pipe(float_to_int_str, [
            "badge_no",
            "employee_id",
            "year",
            "month",
            "day",
            "years_employed",
            "department_code",
            "rank_code"
        ])
        .sort_values(['agency', 'kind', 'event_uid'])
    )


def rearrange_allegation_columns(df):
    """Performs final processing step for a complaint table

    This performs the following tasks:
    - discard columns not present in COMPLAINT_COLUMNS
    - drop row duplicates
    - convert numeric columns to int or str

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    return datavalid_config.rearrange_columns(
        'allegation',
        df
        .pipe(float_to_int_str, ["paragraph_code"])
        .sort_values(['agency', 'allegation_uid'])
    )


def rearrange_appeal_hearing_columns(df):
    """Performs final processing step for an appeal hearing table

    This performs the following tasks:
    - discard columns not present in APPEAL_HEARING_COLUMNS
    - drop row duplicates
    - convert counsel name to title case

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    return datavalid_config.rearrange_columns(
        'appeal_hearing',
        df
        .pipe(names_to_title_case, ["counsel"])
        .sort_values(['agency', 'appeal_uid'])
    )


def rearrange_use_of_force(df):
    """Performs final processing step for a uof table

    This performs the following tasks:
    - discard columns not present in USE_OF_FORCE_COLUMNS
    - drop row duplicates
    - convert numeric columns to int or str

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    return datavalid_config.rearrange_columns(
        'use_of_force',
        df
        .pipe(float_to_int_str, [
            'citizen_age', 'citizen_age_1', 'officer_current_supervisor', 'officer_age',
            'officer_years_exp', 'officer_years_with_unit'
        ])
        .sort_values(['agency', 'uof_uid'])
    )


def rearrange_stop_and_search_columns(df):
    """Performs final processing step for a stop and search table

    This performs the following tasks:
    - discard columns not present in STOP_AND_SEARCH_COLUMNS
    - drop row duplicates
    - convert numeric columns to int or str

    Args:
        df (pd.DataFrame):
            the frame to process

    Returns:
        the updated frame
    """
    return datavalid_config.rearrange_columns(
        'stop_and_search',
        df
        .pipe(float_to_int_str, [
            "stop_and_search_year", "stop_and_search_month", "stop_and_search_day"
        ])
        .pipe(names_to_title_case, ["first_name", "last_name", "middle_name"])
        .sort_values(['agency', 'stop_and_search_uid'])
    )
