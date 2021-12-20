import sys
sys.path.append('../')
import pandas as pd
from datamatch import JaroWinklerSimilarity, ThresholdMatcher, ColumnsIndex
from lib.path import data_file_path


def assign_uid_from_post(cprr, post):
    dfa = cprr.loc[cprr.uid.notna(), ['uid', 'first_name', 'last_name']].drop_duplicates(subset=['uid'])\
        .set_index('uid', drop=True)
    dfa.loc[:, 'fc'] = dfa.first_name.fillna('').map(lambda x: x[:1])

    dfb = post[['uid', 'first_name', 'last_name']].drop_duplicates()\
        .set_index('uid', drop=True)
    dfb.loc[:, 'fc'] = dfb.first_name.fillna('').map(lambda x: x[:1])

    matcher = ThresholdMatcher(ColumnsIndex('fc'), {
        'first_name': JaroWinklerSimilarity(),
        'last_name': JaroWinklerSimilarity(),
    }, dfa, dfb)
    decision = 0.88
    matcher.save_pairs_to_excel(data_file_path(
        "match/cprr_denham_springs_pd_2016_2021_v_post_pprr_2020_11_06.xlsx"), decision)
    matches = matcher.get_index_pairs_within_thresholds(decision)
    match_dict = dict(matches)

    cprr.loc[:, 'uid'] = cprr.uid.map(lambda x: match_dict.get(x, x))
    return cprr


if __name__ == '__main__':
    cprr = pd.read_csv(data_file_path('clean/cprr_denham_springs_pd_2016_2021.csv'))
    post = pd.read_csv(data_file_path('clean/pprr_post_2020_11_06.csv'))
    cprr = assign_uid_from_post(cprr, post)
    cprr.to_csv(
        data_file_path('match/cprr_denham_springs_pd_2016_2021.csv'),
        index=False)
