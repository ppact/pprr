import pandas as pd

import bolo
from lib.columns import rearrange_personnel_columns, rearrange_event_columns
from lib import events


def fuse_events(pprr):
    builder = events.Builder()
    builder.extract_events(
        pprr,
        {
            events.OFFICER_HIRE: {
                "prefix": "hire",
                "keep": ["uid", "agency", "rank_desc", "salary", "salary_freq"],
            }
        },
        ["uid"],
    )
    return builder.to_frame()


if __name__ == "__main__":
    pprr = pd.read_csv(bolo.data("clean/pprr_gretna_pd_2018.csv"))
    post_event = pd.read_csv(bolo.data("match/post_event_gretna_pd_2020.csv"))
    events_df = rearrange_event_columns(pd.concat([post_event, fuse_events(pprr)]))
    rearrange_personnel_columns(pprr).to_csv(
        bolo.data("fuse/per_gretna_pd.csv"), index=False
    )
    events_df.to_csv(bolo.data("fuse/event_gretna_pd.csv"), index=False)
