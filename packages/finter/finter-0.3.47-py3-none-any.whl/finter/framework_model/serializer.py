import pickle
import re

"""
[('content.dart.api.disclosure.bonus_issue.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.br_issue.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.buyback.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.buyback_disposal.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.buyback_trust.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.bw.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.cb.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.coco.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.division.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.division_merge.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.eb.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.major_stock.1d', dtype('O'), str, None),
 ('content.dart.api.disclosure.merge.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.reduction.1d', dtype('O'), dict, None),
 ('content.dart.api.disclosure.rights_issue.1d', dtype('O'), dict, None)]
"""
DART_CM_LIST = [
    'content.dart.api.disclosure.bonus_issue.1d',
    'content.dart.api.disclosure.br_issue.1d',
    'content.dart.api.disclosure.buyback.1d',
    'content.dart.api.disclosure.buyback_disposal.1d',
    'content.dart.api.disclosure.buyback_trust.1d',
    'content.dart.api.disclosure.bw.1d',
    'content.dart.api.disclosure.cb.1d',
    'content.dart.api.disclosure.coco.1d',
    'content.dart.api.disclosure.division.1d',
    'content.dart.api.disclosure.division_merge.1d',
    'content.dart.api.disclosure.eb.1d',
    # 'content.dart.api.disclosure.major_stock.1d', # str이여서 parquet serialize 추가 안함.
    'content.dart.api.disclosure.merge.1d',
    'content.dart.api.disclosure.reduction.1d',
    'content.dart.api.disclosure.rights_issue.1d'
]


def is_serializer_target(identity_name):
    target = [
        "content.fnguide.ftp.financial*",
        "content\.fnguide\.ftp\.consensus\.krx-spot-[\w]+_[aq]\.1d",
        "content.fred.api.economy*"
    ]
    target.extend(DART_CM_LIST)
    pattern = re.compile("|".join(target))

    if pattern.match(identity_name):
        return True
    return False


def deserialize_bytes(value):
    if not isinstance(value, bytes):
        return value
    try:
        return pickle.loads(value)
    except:
        return value


def apply_deserialization(df):
    for column in df.columns:
        df[column] = df[column].apply(deserialize_bytes)
    return df
