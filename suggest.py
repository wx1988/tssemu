"""
This file is used to give suggestion based on the current system settings.
"""
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg
prod_col = db.products

import copy

from builddb.crucial.get_compatmem_by_machine import get_cm_list_mp
from product_api import get_match_prod

########
# global interface
########
def make_suggestion( sys_info ):
    """
    The total RAM capacity must be larger than the existing one.
    """
    mem_list, _ = get_match_prod( sys_info )

    for mem in mem_list:
        print mem['model'], mem['metadata']['capacity']*mem['metadata']['number']

    # keep old plans
    ko_plans = keep_old_suggestion(sys_info, mem_list)
    #print len(ko_plans), ko_plans
    #print '\n\n\n\n\n\n'

    # full replace plans
    fr_plans = full_replace_suggestion(sys_info, mem_list)
    #print len(fr_plans), fr_plans

    return {'keep_old':ko_plans, 'full_replace': fr_plans}


########
# internal function
########
def get_current_size(sys_info):
    """
    """
    s = 0
    for mem in sys_info['mem_list']:
        s += mem['capacity'] / 1024
    return s

debug = 1
########
# two modes of upgrading
########
def keep_old_suggestion( sys_info, mem_list ):
    """
    First try to identify memory of the same model
    Then find all memory with the same specification.
    """
    ts2plan_list = {}
    current_size = get_current_size(sys_info)
    if debug:
        print "Current Size", current_size
    target_size_list = [2,4,8,16,32]
    for ts in target_size_list:
        plan_list = []
        if ts <= current_size:
            continue
        for i,mem in enumerate(mem_list):
            try:
                mem_tmp = copy.copy(mem)
                mem_size = mem_tmp['metadata']['capacity'] * mem_tmp['metadata']['number']
                print mem_tmp['model'], ts, current_size, mem_size
                if (ts - current_size) % mem_size == 0:
                    mem_tmp['buy_number'] = (ts - current_size) / mem_size
                    min_unit_price = min([ web_info['price'] for web_info in mem['websites'] ])
                    mem_tmp['min_price'] = mem_tmp['buy_number'] * min_unit_price
                    plan_list.append(mem_tmp)

            except Exception as e:
                print e
        if len(plan_list) > 0:
            ts2plan_list[ts] = plan_list

    return ts2plan_list

def full_replace_suggestion( sys_info, mem_list ):
    """
    Full replace the old one.
    If of the same size, fully replace the old one -
    only if the kit price is cheaper than the price of upgrading.
    Could replace with larger size per stick
    """
    ts2plan_list = {}
    target_size_list = [2,4,8,16,32]
    current_size = get_current_size(sys_info)
    for ts in target_size_list:
        plan_list = []
        if ts <= current_size:
            continue

        for i,mem in enumerate(mem_list):
            try:
                mem_tmp = copy.copy(mem)
                mem_size = mem_tmp['metadata']['capacity'] * mem_tmp['metadata']['number']
                print mem_tmp['model'], ts, current_size, mem_size
                if (ts - current_size) % mem_size == 0:
                    mem_tmp['buy_number'] = (ts) / mem_size
                    min_unit_price = min([ web_info['price'] for web_info in mem['websites'] ])
                    mem_tmp['min_price'] = mem_tmp['buy_number'] * min_unit_price
                    plan_list.append(mem_tmp)
            except Exception as e:
                print e
        if len(plan_list) > 0:
            ts2plan_list[ts] = plan_list
    return ts2plan_list

def test_make_suggestion():
    #sys_info = {u'mem_list': [{u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other', u'detail': u'Synchronous', u'speed': 2133}, {u'capacity': 4096, u'model': u'HMA 451R7MFR8N-TF ', u'type': u'Other', u'detail': u'Synchronous', u'speed': 2133}, {u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other', u'detail': u'Synchronous', u'speed': 2133}, {u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other ', u'detail': u'Synchronous', u'speed': 2133}], u'manufacturer': u' Dell Inc.', u'slots': 8, u'maximum_capacity': 256, u'productname': u' Precision Tower 5810'}
    sys_info = {"mem_list": [{"type": "DDR3", "model": "HMT451R7AFR8C-RD  ", "capacity": 4096, "detail": "Registered ", "speed": 1866}, {"type": "DDR3", "model": "HMT451R7AFR8C-RD  ", "capacity": 4096, "detail": "Registered ", "speed": 1866}], "slots": 8, "productname": " Precision T3610", "maximum_capacity": 128, "manufacturer": " Dell Inc."}
    make_suggestion(sys_info)

if __name__ == "__main__":
    test_make_suggestion()
