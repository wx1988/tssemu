"""
This file is used to give suggestion based on the current system settings.
"""
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg
prod_col = db.products

from compatible_mem.get_compatmem_by_machine import get_cm_list_mp

########
# global interface
########
def make_suggestion( sys_info ):
    """
    The total RAM capacity must be larger than the existing one.
    """
    pass

########
# Suggestion based on the memory vendors
########
def get_suggestion_mem_vendor(sys_info):
    # get by machine model
    mem_list = get_cm_list_mp(sys_info['manufacturer'], sys_info['productname'])
    
    # TODO?
    # for each memory, check weather in crucial_mem collection    

    # TODO, integrate crucial database with other database.
    # for each memory, step 1, check whether have this item

    # TODO, summary the specification here

########
# two modes of upgrading
########
def find_same_model(sys_info):
    """
    """
    match_ram_list = []
    if sys_info.has_key('mem_list') and len(sys_info['mem_list']) > 0:
        mem_model_list = [mem['model'] for mem in sys_info['mem_list']]
        for mem_model in mem_model_list:
            obj = prod_col.find_one( { 'model': mem_model } )
            # TODO, if not in the system, need to
            match_ram_list.append(obj)
    return match_ram_list


def find_same_spec(sys_info):
    """
    Form Factor SODIMM
    Type Detail: Synchronous
    """
    pass


def keep_old_suggestion( sys_info ):
    """
    First try to identify memory of the same model
    Then find all memory with the same specification.
    """
    pass


def full_replace_suggestion( sys_info ):
    """
    Full replace the old one.
    If of the same size, fully replace the old one only if the kit price is cheaper than the price of upgrading.
    Could replace with larger size per stick
    """
    pass


########
# the internal assistant function
########
def get_mem_by_spec( spec_info ):
    """
    spec_info : a dictionary
    """
    pass

