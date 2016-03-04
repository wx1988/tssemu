"""
return the result , 
plans and matching products seperately
"""
"""
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg
prod_col = db.products
import copy
from builddb.crucial.get_compatmem_by_machine import get_cm_list_mp
"""
import numpy as np

from product_api import get_match_prod
from suggest import get_current_size

from suggest import keep_old_suggestion, full_replace_suggestion


def score_plan(plan_name, prod_list, sys_info):
    # each worth 100 points,
    # * keep old
    # * double size good, 
    # min price of the best recommended products
    cur_total_cap = get_current_size(sys_info)

    score = 0
    if plan_name.startswith("ko"):
        score += 100
        cur_ps_cap = sys_info['mem_list'][0]['capacity'] / 1024
        per_stick_cap = int(plan_name.split('_')[2])
        if cur_ps_cap != per_stick_cap:
            score -= 100

    target_cap = int(plan_name.split('_')[1])
    if target_cap == 2 * cur_total_cap:
        score += 100

    min_price = np.min( [p['metadata']['price'] for p in prod_list] )
    score -= min_price

    return score

def make_suggestion2( sys_info ):
    """
    The total RAM capacity must be larger than the existing one.
    
    plan coding:
    [ko|fr]_{total_capacity}_{per_stick_capacity}
    """
    # current system information
    total_slots = sys_info['slots']
    left_slots = sys_info['slots'] - len(sys_info['mem_list'])
    cur_total_cap = get_current_size(sys_info)
    cur_per_stick_cap = sys_info['mem_list'][0]['capacity']

    mem_list, _ = get_match_prod( sys_info )
    for mem in mem_list:
        print mem['model'], mem['metadata']['capacity']*mem['metadata']['number']

    plan2prods = {}

    # keep old plans
    ko_plans = keep_old_suggestion(sys_info, mem_list)

    # separate plans based on capacity per stick
    for ts in ko_plans.keys():
    	for prod in ko_plans[ts]:
            per_stick_cap = prod['metadata']['capacity']
            # check whether the required number
            # exceed the number available slots
            if (ts - cur_total_cap) / per_stick_cap > left_slots:
                continue

            plan = "ko_%d_%d"%(ts, per_stick_cap)
            if not plan2prods.has_key(plan):
                plan2prods[plan] = []
            plan2prods[plan].append(prod)

    # full replace plans
    fr_plans = full_replace_suggestion(sys_info, mem_list)    
    # separate plans based on capacity per stick
    for ts in fr_plans.keys():
        for prod in fr_plans[ts]:
            per_stick_cap = prod['metadata']['capacity']
            # check whether the required number
            # exceed the number available slots
            if ts / per_stick_cap > left_slots:
                continue

            plan = "fr_%d_%d"%(ts, per_stick_cap)
            if not plan2prods.has_key(plan):
                plan2prods[plan] = []
            plan2prods[plan].append(prod)

    # give a recommandation on each plan
    plan_list = []
    for plan in plan2prods.keys():
        plan_list.append({
            'name':plan,
            'target_size' : plan.split("_")[1],
            'per_stick_size' : plan.split("_")[2],
            'score':score_plan(plan, plan2prods[plan], sys_info),
            'prod_list':plan2prods[plan]})    

    return plan_list

if __name__ == "__main__":
    sys_info = {"mem_list": [{"type": "DDR3", "model": "HMT451R7AFR8C-RD  ", "capacity": 4096, "detail": "Registered ", "speed": 1866}, {"type": "DDR3", "model": "HMT451R7AFR8C-RD  ", "capacity": 4096, "detail": "Registered ", "speed": 1866}], "slots": 8, "productname": " Precision T3610", "maximum_capacity": 128, "manufacturer": " Dell Inc."}
    plan_list = make_suggestion2(sys_info)
    for plan in plan_list:
        print plan