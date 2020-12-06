import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import jqdatasdk as jq
import pickle
import json

PROFILE = os.path.join(BASE_DIR,"etc","profile.json")

def login():
    data = None
    with open(PROFILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    jq.auth(data["username"], data["password"])
    # jq.auth('username','password')
    print("Remains = ", jq.get_query_count())
    res = jq.get_query_count()
    print("PCT ====> ", res['spare']/res['total'] * 100, " %")

def jq_remains():
    remains = jq.get_query_count()
    remains_pct = remains["spare"] / remains["total"] * 100
    msg = "Remains : " + str(remains_pct) + " % "
    print(msg)
    return msg

