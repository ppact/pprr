import pandas as pd
import deba
from lib.columns import clean_column_names, set_values
from lib.clean import clean_dates, clean_names
from lib.uid import gen_uid


def clean_suspension(df):
    df.loc[:, "action_appealed"] = (
        df.action.str.lower()
        .str.strip()
        .str.replace("*", "", regex=False)
        .str.replace(r"\(|\)", "", regex=True)
        .str.replace("--", "-", regex=False)
        .str.replace(r"(\w+) & (\w+)", r"\1/\2", regex=True)
        .str.replace(r"sus?pension?n?", "suspension", regex=True)
        .str.replace(r"suspended days (\d+)", r"\1-day suspension", regex=True)
        .str.replace(r"suspension-(\w+)", r"suspension/\1", regex=True)
        .str.replace(r"(\d+) day", r"\1-day", regex=True)
        .str.replace(r"(\d+) months", r"\1-months", regex=True)
        .str.replace("suspended", "suspension", regex=False)
        .str.replace(
            "suspension from working details for 60-day",
            "60-day suspension from working detail",
            regex=False,
        )
        .str.replace(
            "detail privileges suspension for 12-months",
            "12-month suspension from detail privileges",
            regex=False,
        )
        .str.replace(
            "suspension working details for 64-days",
            "64-day suspension from working detail",
            regex=False,
        )
        .str.replace("lwop", "leave without pay", regex=False)
        .str.replace("other", "", regex=False)
    )
    return df.drop(columns="action")


def clean_on_docket(df):
    df.loc[:, "motions"] = (
        df.on_docket.str.lower()
        .str.strip()
        .str.replace(r"(\w+)---?(\w+)", r"\1-\2", regex=True)
        .str.replace(r"(\w+) - (\w+)", r"\1-\2", regex=True)
        .str.replace(
            "motion / pteition for nullity",
            "motion to petition for nullity",
            regex=False,
        )
        .str.replace(r", (\w+)", r"/\1", regex=True)
        .str.replace(r"(\w+) +(\w+)", r"\1 \2", regex=True)
        .str.replace(r"(\w+); (\w+)", r"\1/\2", regex=True)
        .str.replace("gtranted", "granted", regex=False)
        .str.replace(
            r"motion for rehearing ?(and)? ?(request)? ?(for)? oral argument/?",
            "motion for rehearing/request for oral argument",
            regex=True,
        )
        .str.replace("motion for rehearing and ", "motion for rehearing/", regex=False)
        .str.replace(
            "request for clarification", "motion for clarification", regex=False
        )
        .str.replace("motion / petition", "motion/petition", regex=False)
        .str.replace(" and petition", "/petition", regex=False)
        .str.replace("amicalbe", "amicable", regex=False)
        .str.replace(
            "request for oral argument/motion for rehearing",
            "motion for rehearing/request for oral argument",
            regex=False,
        )
        .str.replace(r"circuit ?(court)? cost$", "circuit court costs", regex=True)
        .str.replace("reheairng", "rehearing", regex=False)
        .str.replace("nonappearance", "non-apperance", regex=False)
        .str.replace("he report favors city", "", regex=False)
        .str.replace(
            "withdrawal of motion to enforce decision",
            "motion to withdraw",
            regex=False,
        )
        .str.replace(
            r"motion for summary disposition ?(and)? ?a? request ?(for)? oral argument",
            "motion for summary disposition/oral argument",
            regex=True,
        )
        .str.replace("motion to appr ", "motion to approve ", regex=False)
        .str.replace(r"^action revoked$", "disciplinary action revoked", regex=True)
        .str.replace(r"motion to dis?miss/", "motion to dismiss appeal/", regex=True)
    )
    return df.drop(columns="on_docket")


def clean_final_disposition(df):
    df.loc[:, "appeal_disposition"] = (
        df.final_disposition.str.lower()
        .str.strip()
        .str.replace(r"(\w+) - (\w+)", r"\1/\2", regex=True)
    )
    return df.drop(columns="final_disposition")


def extract_middle_name(df):
    df.loc[:, "first_name"] = df.first_name.str.lower().str.strip().fillna("")
    names = df.first_name.str.extract(r"(\w+) ?(\w{1})?")
    df.loc[:, "first_name"] = names[0].fillna("")
    df.loc[:, "middle_name"] = names[1].fillna("")
    return df


def clean_last_name(df):
    df.loc[:, "last_name"] = (
        df.last_name.str.lower()
        .str.strip()
        .fillna("")
        .str.replace(" et al", "", regex=False)
    )
    return df


def assign_agency(df):
    df.loc[:, "agency"] = "New Orleans PD"
    return df


def assign_final_appeal_hearing_date(df):
    df.loc[
        (df.hearing_date_1 == "11/17/2011")
        & (df.appeal_uid == "1b36e4b575c20b622c6dd5d87c0c43cb"),
        "appeal_hearing_date",
    ] = "11/17/2011"
    df.loc[
        (df.hearing_date_1 == "5/31/2018")
        & (df.appeal_uid == "c3ec99940d680b1272c6aee1b497a3ca"),
        "appeal_hearing_date",
    ] = "5/31/2018"
    return df.drop(columns=["hearing_date_1"])


def clean():
    df = (
        pd.read_csv(deba.data("raw/new_orleans_csc/new_orleans_csc_lprr_2000_2016.csv"))
        .pipe(clean_column_names)
        .drop(
            columns=[
                "department",
                "final_disposition_docket",
                "final_disposition_docket_date",
                "hearing_date_2",
            ]
        )
        .rename(
            columns={
                "date_received": "appeal_receive_date",
                "hearing_date": "appeal_hearing_date",
                "transcript_received": "transcript_receive_date",
                "h_e_report_received": "h_e_report_receive_date",
                "final_disposition_date": "appeal_disposition_date",
                "docket_number": "docket_no",
            }
        )
        .pipe(clean_suspension)
        .pipe(clean_on_docket)
        .pipe(clean_final_disposition)
        .pipe(extract_middle_name)
        .pipe(clean_last_name)
        .pipe(assign_agency)
        .pipe(clean_names, ["first_name", "last_name"])
        .pipe(gen_uid, ["first_name", "last_name", "agency"])
        .pipe(gen_uid, ["uid", "docket_no"], "appeal_uid")
        .pipe(assign_final_appeal_hearing_date)
        .pipe(
            clean_dates,
            ["appeal_hearing_date", "appeal_disposition_date", "appeal_receive_date"],
        )
    )
    return df.astype(str)


def drop_rows_missing_names(df):
    df.loc[:, "accused_name"] = df.accused_name.str.lower().str.strip()
    return df[~(df.accused_name.fillna("") == "")]


def extract_doc_num(df):
    docs = df.docket_number.str.lower().str.strip().str.extract(r"(\w{4})$")

    df.loc[:, "docket_no"] = docs[0]
    return df.drop(columns=["docket_number"])


def split_name(df):
    names = df.accused_name.str.extract(r"(\w+) (\w+)")

    df.loc[:, "first_name"] = names[0]
    df.loc[:, "last_name"] = names[1]
    return df.drop(columns=["accused_name"])[
        ~((df.first_name == "") & (df.last_name == ""))
    ][~((df.docket_no.fillna("") == ""))]


def clean_notification_dates(df):
    df.loc[:, "decision_notification_date"] = df.decision_notification_date
    return df[~((df.decision_notification_date.fillna("") == ""))]


def extract_docket_no_from_transcripts():
    df = (
        pd.read_csv(deba.data("ner/nopd_appeals_pdfs.csv"))
        .pipe(clean_column_names)
        .pipe(extract_doc_num)
    )
    return df

def clean_transcripts():
    df = (
        pd.read_csv(deba.data("ner/nopd_appeals_pdfs.csv"))
        .pipe(clean_column_names)
        .drop(
            columns=[
                "accused_name_1",
                "accused_name_2",
                "accused_name_3",
                "appeal_hearing_date_1",
                "appeal_hearing_date_2",
                "appeal_hearing_date",
                "appeal_hearing_disposition_1",
                "appeal_hearing_disposition",
                "appeal_hearing_disposition_2",
                "appeal_hearing_disposition_3",
                "accused_name_4",
                "docket_number_1",
                "docket_number_2",
                "docket_number_3",
                "docket_number_4",
                "appeal_hearing_disposition_4",
            ]
        )
        .pipe(drop_rows_missing_names)
        .pipe(clean_notification_dates)
        .pipe(extract_doc_num)
        .pipe(split_name)
        .pipe(set_values, {"agency": "New Orleans PD"})
        .pipe(gen_uid, ["first_name", "last_name", "agency"])
        .pipe(gen_uid, ["docket_no", "uid", "decision_notification_date"], "appeal_uid")
    )
    return df.astype(str)


def concat(dfa, dfb):
    dfb = dfb[
        [
            "docket_no",
            "md5",
            "filepath",
            "filesha1",
            "fileid",
            "filetype",
            "fn",
            "file_category",
            "text",
            "pageno",
        ]
    ]
    df = pd.merge(dfa, dfb, on="docket_no", how="outer")
    return df[~((df.first_name.fillna("") == "") & (df.last_name.fillna("") == ""))]


if __name__ == "__main__":
    df_log = clean()
    df_docket_no = extract_docket_no_from_transcripts()
    df_transcripts = clean_transcripts()

    df = concat(df_log, df_docket_no)
    df_transcripts.to_csv(
        deba.data("clean/lprr_appeal_transcripts_new_orleans_csc_2012_2022.csv"),
        index=False,
    )
    df.to_csv(deba.data("clean/lprr_new_orleans_csc_2000_2016.csv"), index=False)
