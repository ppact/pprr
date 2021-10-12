import sys

import pandas as pd

from lib.path import data_file_path
from lib.columns import rearrange_event_columns
from lib.personnel import fuse_personnel
from lib.uid import ensure_uid_unique
from lib import events

sys.path.append('../')


def fuse_events(pprr):
    builder = events.Builder()
    builder.extract_events(pprr, {
        events.OFFICER_HIRE: {
            'prefix': 'hire', 'parse_date': True, 'keep': [
                'uid', 'agency', 'department_desc', 'badge_no', 'employment_status'
            ],
            'merge_cols': ['department_desc', 'badge_no', 'employment_status']
        },
        events.OFFICER_PAY_EFFECTIVE: {
            'prefix': 'salary', 'parse_date': True, 'keep': [
                'uid', 'agency', 'rank_desc', 'salary', 'salary_freq'
            ]
        },
        events.OFFICER_LEFT: {
            'prefix': 'termination', 'parse_date': True, 'keep': [
                'uid', 'agency'
            ]
        }
    }, ['uid'])
    return builder.to_frame(output_duplicated_events=True)


if __name__ == '__main__':
    pprr_09 = pd.read_csv(data_file_path('clean/pprr_slidell_pd_2009.csv'))
    pprr_19 = pd.read_csv(data_file_path('clean/pprr_slidell_pd_2019.csv'))
    pprr_csd = pd.read_csv(data_file_path('clean/pprr_slidell_csd_2010_2019.csv'))
    post_event = pd.read_csv(data_file_path(
        'match/post_event_slidell_pd_2020.csv'
    ))
    events_df = rearrange_event_columns(pd.concat([
        post_event,
        fuse_events(pd.concat([pprr_09, pprr_19, pprr_csd]))
    ]))
    ensure_uid_unique(events_df, 'event_uid', True)
    fuse_personnel(pprr_csd, pprr_09, pprr_19).to_csv(data_file_path(
        "fuse/per_slidell_pd.csv"), index=False)
    events_df.to_csv(data_file_path(
        "fuse/event_slidell_pd.csv"), index=False)
