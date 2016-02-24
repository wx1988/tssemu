"""
For the products with all fields pass the regex matching, could easily transform to predefined format.

For the products only passing partial regex matching, try to use regex to extract information.
"""
import re
import json

##############
# newegg specific regex
##############
model_reg = "[\w-\/]+"
cap_reg = "\d+GB\(\d x \d+GB\)"
type_reg = "(\d+)-Pin (DDR\d) (\w+)"
speed_reg = "(DDR\d) (\d+) \((PC\d) (\d+)\)"
cas_reg = "\d+"
timing_reg = "\d-\d-\d"
#timing_reg = "\d-\d-\d", possible with four measure
volt_reg = "\d.\dV"
ecc_reg = "Yes|No"
buf_reg = "Buffered|Unbuffered"
kit_reg = "\w+"
heat_reg = "Yes|No"

def format_complete_prod(prod_md):
    st = prod_md['newegg_product']['specifications_table']
    # key-value extraction
    kv = {}
    for ss in st:
        for s in ss['specifications']:
            kv[s['name']] = s['value']
    print kv

    prod_info = {}
    if kv.has_key("Brand"):
        prod_info['brand'] = kv['Brand']
    prod_info['model'] = kv["Model"]
    prod_info['voltage'] = float(kv['Voltage'][:-1])

    # number * capacity
    cap = kv['Capacity']
    if cap.count("(") == 0:
        prod_info['capacity'] = float(cap[:-2])
        prod_info['number'] = 1
    else:
        cap_reg = "\d+GB \((\d) x (\d+)GB\)"
        m = re.match(cap_reg, cap)
        print m
        print m.groups()
        prod_info['capacity'] = float(m.group(2))
        prod_info['number'] = int(m.group(1))

    prod_info['type'] = kv['Type'].split(" ")[1]
    prod_info['pin'] = int( kv['Type'].split(" ")[0].split('-')[0] )
    prod_info['speed'] = int( kv['Speed'].split(" ")[1])
    if kv['ECC'] == "Yes":
        prod_info['ecc'] = True
    if kv['ECC'] == "No":
        prod_info['ecc'] = False

    #print prod_info
    return prod_info


###############
# general regex for general text
###############
g_ddr_reg = "(DDR\d)"
g_freq_reg = "\d+[ ]+Mhz"
g_pin_reg = "\d+[- ][Pp]in"
g_kitsize_reg = "\(\s*(\d+)\s*[xX](\d+)\s*GB\)"
g_size_reg = "\d+[ ]+GB"
g_pc_reg = "(PC\d)([- ]+\d+)"
g_volt_reg = "(\d.\d)V"

pc2freq = {
    4: {
        19200:2400,
        21300:2666,
        22400:2800,
        24000:3000,
        17000:2133,
        25600:3200,
        26400:3300,
        },
    3:{
        6400:800,
        8500:1066,
        10600:1333,
        12800:1600
    }
    2:{
        5300:667,
    }
}

def format_incomplete_prod(prod_md_str):
    """
    PC4-21300 (2666Mhz) - PC4-22400 (28000Mhz) PC4-19200 (2400Mhz) - PC4-24000 (3000MHz) - PC4-17000 (2133 MHZ) - PC4-25600 (3200MHz) - PC4-26400 (3300MHz)
    pc3-6400 = 800MHz - pc3-8500 = 1066MHz - pc3-10600 = 1333MHz - pc3-12800 = 1600MHz
    pc2-5300 = 667
    """
    prod_info = {}
    m = re.search(g_kitsize_reg, prod_md_str, re.IGNORECASE)
    if m:
        print m, m.groups()
        prod_info['capacity'] = int(m.group(2))
        prod_info['number'] = int(m.group(1))

    # TODO NonECC
    m = re.search(g_ddr_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = m.group(0)

    # voltage
    m = re.search(g_volt_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['voltage'] = float(m.group(1))

    print prod_info


###############
# Begin of test codes
###############
def test_complete():
    pid = "N82E16820148166"
    pid = "9SIA0ZX2M46757"
    pid = "N82E16820231569" # kit
    prod_md = json.load(open("metadata/%s.json"%(pid)))
    format_complete_prod(prod_md)

def test_incomplete():
    pid = "9SIA85V3R92072"
    pid = "9SIA8R03P79648"
    prod_md_str = open("metadata/%s.json"%(pid)).read()
    format_incomplete_prod(prod_md_str)

if __name__ == "__main__":
    #test_complete()
    test_incomplete()
