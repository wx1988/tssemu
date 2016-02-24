"""
This file is used to give suggestion based on the current system settings. 
"""


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

