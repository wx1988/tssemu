"""
This file is used to give suggestion based on the current system settings. 
"""
from pymongo import MongoClient
db = client.ram
newegg_col = db.newegg

client = MongoClient('localhost', 27017)

########
# global interface
########
def make_suggestion( sys_info ):
    """
    The total RAM capacity must be larger than the existing one. 
    """
    pass


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
            obj = newegg_col.find_one( { 'model': mem_model } )
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

