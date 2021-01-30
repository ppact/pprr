import re
from .clean import float_to_int_str


PERSONEL_COLUMNS = [
    "uid",  # unique officer identifier, generated by MD5 checksum multiple columns
    "last_name",  # lowercase last name
    "middle_name",  # lowercase middle name
    "middle_initial",  # lowercase middle initial
    "first_name",  # lowercase first name
    "employee_id",  # employee ID given to the person by the agency.
    "birth_year",
    "birth_month",
    "birth_day",
    "race",
    "sex"
]

PERSONEL_HISTORY_COLUMNS = [
    "uid",  # officer unique identifier
    "badge_no",  # badge number
    "department_code",  # department code or id
    "department_desc",  # department title or description
    "rank_code",  # rank code
    "rank_desc",  # rank title or description
    "rank_year",
    "rank_month",
    "rank_day",
    "hire_year",
    "hire_month",
    "hire_day",
    "term_year",  # termination year
    "term_month",
    "term_day",
    "pay_prog_start_year",
    "pay_prog_start_month",
    "pay_prog_start_day",
    "pay_effective_year",
    "pay_effective_month",
    "pay_effective_day",
    "employment_status",
    "annual_salary",  # annual salary
    "hourly_salary",  # hourly salary
    "data_production_year",  # year of data
    "agency",  # name of agency (e.g. "New Orleans CSD")
]

COMPLAINT_COLUMNS = [
    "uid",  # officer unique identifier
    "tracking_number",  # identifier for complaint
    "occur_year",
    "occur_month",
    "occur_day",
    "occur_time",
    "receive_year",
    "receive_month",
    "receive_day",
    "investigation_complete_year",
    "investigation_complete_month",
    "investigation_complete_day",
    "investigation_status",
    "disposition",
    "rule_code",
    "rule_violation",
    "paragraph_code",
    "paragraph_violation",
    "unique_officer_allegation_id",
    "officer_ethnicity",
    "officer_gender",
    "officer_age",
    "officer_years_of_service",
    "complainant_gender",
    "complainant_ethnicity",
    "complainant_age",
    "action",  # list of actions taken separated by '; '
    "complainant_type",
    "data_production_year",  # year of data
    "agency",  # name of agency (e.g. "New Orleans CSD")
    # "Incident Type",  # ?
    # "Complaint Classification",  # ?
    # "Bureau of Complainant",  # ?
    # "Division of Complainant",  # ?
    # "Unit of Complainant",  # ?
    # "Unit Additional Details of Complainant",  # ?
    # "Working Status of Complainant",  # ?
    # "Shift of Complainant",  # ?
]


def clean_column_names(df):
    """
    Remove unnamed columns and convert to snake case
    """
    df = df[[col for col in df.columns if not col.startswith("Unnamed:")]]
    df.columns = [
        re.sub(r"[\s\W]+", "_", col.strip()).lower()
        for col in df.columns]
    return df


def rearrange_personel_columns(df):
    existing_cols = set(df.columns)
    return float_to_int_str(
        df[[col for col in PERSONEL_COLUMNS if col in existing_cols]]
        .drop_duplicates(ignore_index=True),
        ["employee_id", "birth_year", "birth_month", "birth_day"])


def rearrange_personel_history_columns(df):
    existing_cols = set(df.columns)
    return float_to_int_str(
        df[[
            col for col in PERSONEL_HISTORY_COLUMNS if col in existing_cols
        ]].drop_duplicates(ignore_index=True),
        [
            "badge_no",
            "rank_year",
            "rank_month",
            "rank_day",
            "hire_year",
            "hire_month",
            "hire_day",
            "term_year",
            "term_month",
            "term_day",
            "pay_prog_start_year",
            "pay_prog_start_month",
            "pay_prog_start_day",
            "pay_effective_year",
            "pay_effective_month",
            "pay_effective_day",
            "data_production_year"
        ])


def rearrange_complaint_columns(df):
    existing_cols = set(df.columns)
    return float_to_int_str(
        df[[col for col in COMPLAINT_COLUMNS if col in existing_cols]]
        .drop_duplicates(ignore_index=True),
        [
            "occur_year",
            "occur_month",
            "occur_day",
            "receive_year",
            "receive_month",
            "receive_day",
            "investigation_complete_year",
            "investigation_complete_month",
            "investigation_complete_day",
            "paragraph_code"
        ])
