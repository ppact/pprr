import sys

sys.path.append("../")
import pandas as pd
from datamatch import JaroWinklerSimilarity, ThresholdMatcher, ColumnsIndex
from lib.path import data_file_path
from lib.post import load_for_agency, extract_events_from_post


def match_cprr_20_and_pprr(cprr, pprr):
    dfa = (
        cprr.loc[cprr.uid.notna(), ["uid", "first_name", "last_name"]]
        .drop_duplicates(subset=["uid"])
        .set_index("uid", drop=True)
    )
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])

    dfb = (
        pprr[["uid", "first_name", "last_name"]]
        .drop_duplicates()
        .set_index("uid", drop=True)
    )
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])

    matcher = ThresholdMatcher(
        ColumnsIndex("fc"),
        {
            "first_name": JaroWinklerSimilarity(),
            "last_name": JaroWinklerSimilarity(),
        },
        dfa,
        dfb,
    )
    decision = 1
    matcher.save_pairs_to_excel(
        data_file_path("match/lake_charles_pd_cprr_20_v_post_pprr_2020_11_06.xlsx"),
        decision,
    )
    matches = matcher.get_index_pairs_within_thresholds(decision)
    match_dict = dict(matches)

    cprr.loc[:, "uid"] = cprr.uid.map(lambda x: match_dict.get(x, x))
    return cprr


def match_cprr_19_and_pprr(cprr, pprr):
    dfa = (
        cprr.loc[cprr.uid.notna(), ["uid", "first_name", "last_name"]]
        .drop_duplicates(subset=["uid"])
        .set_index("uid", drop=True)
    )
    dfa.loc[:, "fc"] = dfa.first_name.fillna("").map(lambda x: x[:1])

    dfb = (
        pprr[["uid", "first_name", "last_name"]]
        .drop_duplicates()
        .set_index("uid", drop=True)
    )
    dfb.loc[:, "fc"] = dfb.first_name.fillna("").map(lambda x: x[:1])

    matcher = ThresholdMatcher(
        ColumnsIndex("fc"),
        {
            "first_name": JaroWinklerSimilarity(),
            "last_name": JaroWinklerSimilarity(),
        },
        dfa,
        dfb,
    )
    decision = 0.84
    matcher.save_pairs_to_excel(
        data_file_path("match/lake_charles_pd_cprr_2014_2019_v_pprr_2020_11_06.xlsx"),
        decision,
    )
    matches = matcher.get_index_pairs_within_thresholds(decision)
    match_dict = dict(matches)

    cprr.loc[:, "uid"] = cprr.uid.map(lambda x: match_dict.get(x, x))
    return cprr


def match_pprr_and_post(pprr, post):
    dfa = pprr[["uid", "first_name", "last_name"]]
    dfa.loc[:, "fc"] = dfa.first_name.map(lambda x: x[:1])
    dfa = dfa.drop_duplicates(subset=["uid"]).set_index("uid")

    dfb = post[["uid", "first_name", "last_name"]]
    dfb.loc[:, "fc"] = dfb.first_name.map(lambda x: x[:1])
    dfb = dfb.drop_duplicates(subset=["uid"]).set_index("uid")

    matcher = ThresholdMatcher(
        ColumnsIndex(["fc"]),
        {
            "last_name": JaroWinklerSimilarity(),
            "first_name": JaroWinklerSimilarity(),
        },
        dfa,
        dfb,
    )
    decision = 0.91
    matcher.save_pairs_to_excel(
        data_file_path(
            "match/pprr_lake_charles_pd_pprr_2017_2021_v_pprr_2020_11_06.xlsx"
        ),
        decision,
    )
    matches = matcher.get_index_pairs_within_thresholds(lower_bound=decision)
    return extract_events_from_post(post, matches, "Lake Charles PD")


if __name__ == "__main__":
    cprr_20 = pd.read_csv(data_file_path("clean/cprr_lake_charles_pd_2020.csv"))
    cprr_19 = pd.read_csv(data_file_path("clean/cprr_lake_charles_pd_2014_2019.csv"))
    pprr = pd.read_csv(data_file_path("clean/pprr_lake_charles_pd_2017_2021.csv"))
    agency = cprr_19.agency[0]
    post = load_for_agency("clean/pprr_post_2020_11_06.csv", agency)
    cprr_20 = match_cprr_20_and_pprr(cprr_20, post)
    cprr_19 = match_cprr_19_and_pprr(cprr_19, post)
    post_event = match_pprr_and_post(pprr, post)
    cprr_20.to_csv(data_file_path("match/cprr_lake_charles_pd_2020.csv"), index=False)
    cprr_19.to_csv(data_file_path("match/cprr_lake_charles_pd_2014_2019.csv"), index=False)
    post_event.to_csv(data_file_path("match/post_event_lake_charles_2020_11_06.csv"), index=False)
