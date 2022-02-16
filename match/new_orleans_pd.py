from lib.date import combine_date_columns
from lib.path import data_file_path
from datamatch import (
    ThresholdMatcher,
    JaroWinklerSimilarity,
    DateSimilarity,
    ColumnsIndex,
)
from lib.post import extract_events_from_post, load_for_agency
import pandas as pd
import sys

sys.path.append("../")


def match_pprr_against_post(pprr_ipm, post):
    dfa = pprr_ipm[["uid", "first_name", "last_name"]]
    dfa.loc[:, "hire_date"] = combine_date_columns(
        pprr_ipm, "hire_year", "hire_month", "hire_day"
    )
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])
    dfa.loc[:, "lc"] = dfa.last_name.fillna("").map(lambda x: x[:1])
    dfa = dfa.drop_duplicates(subset=["uid"]).set_index("uid")

    dfb = post[["uid", "first_name", "last_name"]]
    dfb.loc[:, "hire_date"] = combine_date_columns(
        post, "hire_year", "hire_month", "hire_day"
    )
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])
    dfb.loc[:, "lc"] = dfb.last_name.fillna("").map(lambda x: x[:1])
    dfb = dfb.drop_duplicates(subset=["uid"]).set_index("uid")

    matcher = ThresholdMatcher(
        ColumnsIndex(["fc", "lc"]),
        {
            "first_name": JaroWinklerSimilarity(),
            "last_name": JaroWinklerSimilarity(),
            "hire_date": DateSimilarity(),
        },
        dfa,
        dfb,
        show_progress=True,
    )
    decision = 0.803
    matcher.save_pairs_to_excel(
        data_file_path(
            "match/pppr_ipm_new_orleans_pd_1946_2018_v_post_pprr_2020_11_06.xlsx"
        ),
        decision,
    )

    matches = matcher.get_index_pairs_within_thresholds(decision)
    return extract_events_from_post(post, matches, "New Orleans PD")


def match_award_to_pprr_ipm(award, pprr_ipm):
    dfa = (
        award[["uid", "first_name", "last_name"]]
        .drop_duplicates()
        .set_index("uid", drop=True)
    )
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])
    dfa.loc[:, "lc"] = dfa.last_name.fillna("").map(lambda x: x[:1])

    dfb = (
        pprr_ipm[["uid", "first_name", "last_name"]]
        .drop_duplicates()
        .set_index("uid", drop=True)
    )
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])
    dfb.loc[:, "lc"] = dfb.last_name.fillna("").map(lambda x: x[:1])

    matcher = ThresholdMatcher(
        ColumnsIndex(["fc", "lc"]),
        {"first_name": JaroWinklerSimilarity(), "last_name": JaroWinklerSimilarity()},
        dfa,
        dfb,
        show_progress=True,
    )
    decision = 0.93
    matcher.save_pairs_to_excel(
        data_file_path(
            "match/new_orleans_pd_award_2016_2021_v_pprr_ipm_new_orleans_pd_1946_2018.xlsx"
        ),
        decision,
    )
    matches = matcher.get_index_pairs_within_thresholds(lower_bound=decision)

    match_dict = dict(matches)
    award.loc[:, "uid"] = award.uid.map(lambda x: match_dict.get(x, x))
    return award


def match_lprr_to_pprr_ipm(lprr, pprr_ipm):
    dfa = lprr[["uid", "first_name", "last_name", "middle_name"]]
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])
    dfa.loc[:, "lc"] = dfa.last_name.fillna("").map(lambda x: x[:1])
    dfa = dfa.drop_duplicates(subset=["uid"]).set_index("uid")

    dfb = pprr_ipm[["uid", "first_name", "last_name", "middle_name"]]
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])
    dfb.loc[:, "lc"] = dfb.last_name.fillna("").map(lambda x: x[:1])
    dfb = dfb.drop_duplicates(subset=["uid"]).set_index("uid")

    matcher = ThresholdMatcher(
        ColumnsIndex(["fc", "lc"]),
        {
            "first_name": JaroWinklerSimilarity(),
            "last_name": JaroWinklerSimilarity(),
            "middle_name": JaroWinklerSimilarity(),
        },
        dfa,
        dfb,
        show_progress=True,
    )
    decision = 0.80
    matcher.save_pairs_to_excel(
        data_file_path(
            "match/new_orleans_lprr_2000_2016_v_pprr_ipm_new_orleans_pd_1946_2018.xlsx"
        ),
        decision,
    )
    matches = matcher.get_index_clusters_within_thresholds(lower_bound=decision)
    match_dict = dict(matches)

    lprr.loc[:, "uid"] = lprr.uid.map(lambda x: match_dict.get(x, x))
    return lprr


def match_pprr_csd_to_pprr_ipm(pprr_csd, pprr_ipm):
    dfa = pprr_csd[["uid", "first_name", "last_name", "agency"]]
    dfa.loc[:, "hire_date"] = combine_date_columns(
        pprr_csd, "hire_year", "hire_month", "hire_day"
    )
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])
    dfa.loc[:, "lc"] = dfa.last_name.fillna("").map(lambda x: x[:1])
    dfa = dfa.drop_duplicates(subset=["uid"]).set_index("uid")

    dfb = pprr_ipm[["uid", "first_name", "last_name", "agency"]]
    dfb.loc[:, "hire_date"] = combine_date_columns(
        pprr_ipm, "hire_year", "hire_month", "hire_day"
    )
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])
    dfb.loc[:, "lc"] = dfb.last_name.fillna("").map(lambda x: x[:1])
    dfb = dfb.drop_duplicates(subset=["uid"]).set_index("uid")

    matcher = ThresholdMatcher(
        ColumnsIndex(["fc", "lc", "agency"]),
        {
            "first_name": JaroWinklerSimilarity(),
            "last_name": JaroWinklerSimilarity(),
            "hire_date": DateSimilarity(),
        },
        dfa,
        dfb,
        show_progress=True,
    )
    decision = 1
    matcher.save_pairs_to_excel(
        data_file_path(
            "match/pprr_new_orleans_csd_2014_v_pprr_ipm_new_orleans_pd_1946_2018.xlsx"
        ),
        decision,
    )
    matches = matcher.get_index_pairs_within_thresholds(lower_bound=decision)
    match_dict = dict(matches)

    pprr_csd.loc[:, "uid"] = pprr_csd.uid.map(lambda x: match_dict.get(x, x))
    return pprr_csd


def match_stop_and_search_to_pprr(sas, pprr_ipm):
    dfa = sas[["uid", "first_name", "last_name"]]
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])
    dfa.loc[:, "lc"] = dfa.last_name.fillna("").map(lambda x: x[:1])
    dfa = dfa.drop_duplicates(subset=["uid"]).set_index("uid")

    dfb = pprr_ipm[["uid", "first_name", "last_name"]]
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])
    dfb.loc[:, "lc"] = dfb.last_name.fillna("").map(lambda x: x[:1])
    dfb = dfb.drop_duplicates(subset=["uid"]).set_index("uid")

    matcher = ThresholdMatcher(
        ColumnsIndex(["fc", "lc"]),
        {
            "first_name": JaroWinklerSimilarity(),
            "last_name": JaroWinklerSimilarity(),
        },
        dfa,
        dfb,
        show_progress=True,
    )
    decision = 0.95

    matcher.save_pairs_to_excel(
        data_file_path(
            "match/stop_and_search_new_orleans_pd_v_pprr_new_orleans_pd_1946_2018.xlsx"
        ),
        decision,
    )
    matches = matcher.get_index_pairs_within_thresholds(lower_bound=decision)
    match_dict = dict(matches)

    sas.loc[:, "uid"] = sas.uid.map(lambda x: match_dict.get(x, x))
    return sas


if __name__ == "__main__":
    pprr_ipm = pd.read_csv(
        data_file_path("clean/pprr_new_orleans_ipm_iapro_1946_2018.csv")
    )
    pprr_csd = pd.read_csv(data_file_path("clean/pprr_new_orleans_csd_2014.csv"))
    agency = pprr_ipm.agency[0]
    post = load_for_agency("clean/pprr_post_2020_11_06.csv", agency)
    award = pd.read_csv(data_file_path("clean/award_new_orleans_pd_2016_2021.csv"))
    lprr = pd.read_csv(data_file_path("clean/lprr_new_orleans_csc_2000_2016.csv"))
    sas = pd.read_csv(data_file_path("clean/sas_new_orleans_pd_2017_2021.csv"))
    event_df = match_pprr_against_post(pprr_ipm, post)
    award = match_award_to_pprr_ipm(award, pprr_ipm)
    lprr = match_lprr_to_pprr_ipm(lprr, pprr_ipm)
    sas = match_stop_and_search_to_pprr(sas, pprr_ipm)
    pprr_csd_matched_with_ipm = match_pprr_csd_to_pprr_ipm(pprr_csd, pprr_ipm)
    award.to_csv(
        data_file_path("match/award_new_orleans_pd_2016_2021.csv"), index=False
    )
    event_df.to_csv(data_file_path("match/post_event_new_orleans_pd.csv"), index=False)
    lprr.to_csv(data_file_path("match/lprr_new_orleans_csc_2000_2016.csv"), index=False)
    pprr_csd_matched_with_ipm.to_csv(
        data_file_path("match/pprr_new_orleans_csd_2014.csv"), index=False
    )
    sas.to_csv(data_file_path("match/sas_new_orleans_pd_2017_2021.csv"), index=False)
