import re
import json


###############
# general regex for general text
###############
pc2freq = {
    4: {
        17000:2133,
        17060:2133,
        19200:2400,
        21300:2666,
        22400:2800,
        24000:3000,
        25600:3200,
        26600:3333,
        26400:3300,
        27200:3400,
        27700:3466,
        27730:3466,
        28000:3600,
        28800:3600,
        29800:3733,
        30000:3866,
        30900:3866,
        32000:4000,
        33000:4133,
        33600:4200,
    },
    3:{
        6400:800,
        8500:1066,
        10600:1333,
        10660:1333,
        10666:1333,
        12600:1600,
        12800:1600,
        14900:1866,
        15000:1866,
        16000:2000,
        17000:2133,
        17060:2133,
        19200:2400,
        21300:2666,
        22400:2800,
        23400:2933,
        24000:3000,
        24800:3100,
    },
    2:{
        8500:1066,
        6400:800,
        5400:667,
        5300:667,
        5200:667,
        4200:533,
        4300:533,
        3200:400
    },
    1:{
        100:100,
        133:133,
        1600:200,
        2100:266,
        2700:333,
        3200:400,
        3500:433,
        4200:533,
        5300:667,
        8500:1066,
    }
}

g_ddr_reg = "(DDR\d)"
g_freq_reg = "(\d+)\s*Mhz"
g_ddrfreq_reg = "DDR\d[-\s]*(\d+)"
g_pin_reg = "(\d+)[-\s]*Pin"

g_kitsize_reg = "(\d+)\s*x\s*(\d+)\s*GB"
g_kitsize_reg2 = "(\d+)\s*GB\s*x\s*(\d+)"
g_size_reg = "(\d+)\s*GB"
g_size_mb_reg = "(\d+)\s*MB"

g_pc_reg = "PC(\d)[-\s]*(\d+)"
g_pc1_reg = "PC[-\s]*(\d+)"
g_pc3l_reg = "PC3L[-\s]*(\d+)"

g_volt_reg = "(\d\.\d+)\s*V"
g_timing_reg = "(\d+)-(\d+)-(\d+)-(\d+)"

debug = 0

def get_capacity(prod_md_str):
    if debug:
        print "in function get_capacity", prod_md_str

    prod_info ={}
    if debug:
        print "step 1"
    # gb kit 1
    m = re.search(g_kitsize_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = int(m.group(2))
        prod_info['number'] = int(m.group(1))
        return prod_info
    if debug:
        print "step 2"
    # gb kit 2
    m = re.search(g_kitsize_reg2, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = int(m.group(1))
        prod_info['number'] = int(m.group(2))
        return prod_info
    if debug:
        print "step 3"
    # try to search single memory
    m = re.search(g_size_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = int(m.group(1))
        prod_info['number'] = 1
        return prod_info
    if debug:
        print "step 4"
    # search mb size memory
    m = re.search(g_size_mb_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = float(m.group(1))/ 1024
        prod_info['number'] = 1
        return prod_info

    #raise Exception("no capacity")
    return {}

def get_typefreq(prod_md_str):
    #print "in function typefreq", prod_md_str
    prod_info = {}
    # PC1
    ddr1_list = ['PC'+str(t) for t in pc2freq[1]]
    for t in ddr1_list:
        if prod_md_str.count( t ) > 0:
            prod_info['type'] = "DDR1"
            prod_info['freq'] = pc2freq[1][int(t[2:])]
            return prod_info

    # DDR3L
    m = re.search(g_pc3l_reg , prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = "DDR3"
        prod_info['freq'] = pc2freq[3][int(m.group(1))]
        return prod_info

    # freq, first check PC*...
    m = re.search(g_pc_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = "DDR"+m.group(1)
        prod_info['freq'] = pc2freq[int(m.group(1))][int(m.group(2))]
        return prod_info

    m = re.search(g_pc1_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = "DDR1"
        prod_info['freq'] = pc2freq[1][int(m.group(1))]
        return prod_info

    # ddr type
    m = re.search(g_ddr_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = m.group(0)

        m = re.search(g_freq_reg, prod_md_str, re.IGNORECASE)
        if m:
            prod_info['freq'] = int(m.group(1))
        else:
            m = re.search(g_ddrfreq_reg, prod_md_str, re.IGNORECASE)
            if not m:
                #raise Exception("no freq")
                return {}
            prod_info['freq'] = int(m.group(1))
    return prod_info

def get_ecc(prod_md_str):
    """
    TODO, get the specification part
    Non-ECC
    nonecc
    """
    prod_info = {}
    if prod_md_str.lower().count("nonecc") > 0:
        prod_info['ecc'] = False
    if prod_md_str.lower().count("non-ecc") > 0:
        prod_info['ecc'] = False
    if prod_info.has_key('ecc'):
        return prod_info
    if prod_md_str.lower().count("ecc") > 0:
        prod_info['ecc'] = True
    return prod_info

def get_reg(prod_md_str):
    """
    TODO, not very acuurate
    Registered
    """
    prod_info = {}
    if prod_md_str.lower().count("unbuffered") > 0:
        prod_info['reg'] = False
    if prod_md_str.lower().count("unregistered") > 0:
        prod_info['reg'] = False
    if debug:
        print "debug registered",
        print prod_md_str.lower().count("unbuffered"),
        print prod_md_str.lower().count("unregistered")
    if prod_info.has_key('reg'):
        return prod_info

    if prod_md_str.lower().count("registered") > 0:
        prod_info['reg'] = True
    if prod_md_str.lower().count("fully buffered") > 0:
        prod_info['reg'] = True
    return prod_info

def get_form_factor(prod_md_str):
    prod_info = {}
    if prod_md_str.lower().count('sodimm') > 0:
        prod_info['formfactor'] = 'SODIMM'
    if prod_md_str.lower().count('so dimm') > 0:
        prod_info['formfactor'] = 'SODIMM'
    if prod_md_str.lower().count('so-dimm') > 0:
        prod_info['formfactor'] = 'SODIMM'
    if prod_info.has_key('formfactor'):
        return prod_info

    if prod_md_str.lower().count('dimm') > 0:
        prod_info['formfactor'] = 'DIMM'
    return prod_info

def format_incomplete_prod(prod_md_str):
    """
    test cases
    kit capacity: 9SIA8R03P79648, 9SIA85V3R92386
    """
    prod_info = {}

    # capacity
    cap_dic = get_capacity(prod_md_str)
    prod_info = dict(prod_info.items() + cap_dic.items())

    # type and frequency
    tf_dic = get_typefreq(prod_md_str)
    prod_info = dict(prod_info.items() + tf_dic.items())

    #  pin num
    m = re.search(g_pin_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['pin'] = int( m.group(1) )

    # timing
    m = re.search(g_timing_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['timing'] = [int(m.group(i)) for i in range(1,5)]

    # check DIMM?
    ff_dic = get_form_factor(prod_md_str)
    prod_info = dict(prod_info.items() + ff_dic.items())
    # NonECC, registerd
    reg_dic = get_reg(prod_md_str)
    prod_info = dict(prod_info.items() + reg_dic.items())
    ecc_dic = get_ecc(prod_md_str)
    prod_info = dict(prod_info.items() + ecc_dic.items())

    # voltage
    m = re.search(g_volt_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['voltage'] = float(m.group(1))

    #print prod_info
    return prod_info

def test_unstructured():
    from tsse_common import newegg_folder
    pid = "9SIA85V3R92072"
    pid = "9SIA8R03P79648"
    pid = "9SIA85V3R92386"
    fpath = "%s/metadata/%s.json"%(newegg_folder,pid)
    prod_md_str = open( fpath ).read()
    format_incomplete_prod(prod_md_str)

def test_ecc_reg():
    """
    TODO, create a folder contain these test files, rather than using DB
    """
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.ram
    az_col = db.amazon

    client = MongoClient()

    # non-ecc
    asin = "B00005AP5R"

    # ecc
    asin = "B00005B409"

    # unbuffer non-ecc
    asin = "B0000665TS"

    # reg ecc
    asin = "B00006HRXV"

    # unbuffer non-ecc
    asin = "B00006HVM4"

    m = az_col.find_one({'asin':asin})
    prod_str = ""
    if m.has_key('title'):
        prod_str += m['title'] + ' '
    if m.has_key("description"):
        prod_str += m['description'] + ' '
    print prod_str
    print get_reg(prod_str), get_ecc(prod_str)


if __name__ == "__main__":
    #test_incomplete()
    test_ecc_reg()
