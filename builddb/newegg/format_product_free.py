import re
import json

###############
# general regex for general text
###############
pc2freq = {
    4: {
        17000:2133,
        19200:2400,
        21300:2666,
        22400:2800,
        24000:3000,
        25600:3200,
        26600:3333,
        26400:3300,
        27200:3400,
        27700:3466,
        28000:3600,
        28800:3600,
        30000:3866,
        30900:3866,
    },
    3:{
        6400:800,
        8500:1066,
        10600:1333,
        10666:1333,
        12800:1600,
        14900:1866,
        17000:2133,
        19200:2400,
        22400:2800,
        24000:3000
    },
    2:{
        8500:1066,
        6400:800,
        5400:667,
        5300:667,
        5200:667,
        4200:533,
        3200:400
    },
    1:{
        1600:200,
        2100:266,
        2700:333,
        3200:400,
        4200:533,
        8500:1066,
    }
}

g_ddr_reg = "(DDR\d)"
g_freq_reg = "(\d+)\s*Mhz"
g_ddrfreq_reg = "DDR\d[-\s]*(\d+)"
g_pin_reg = "(\d+)[-\s]*Pin"

g_kitsize_reg = "(\d+)\s*[x](\d+)\s*GB"
g_size_reg = "(\d+)\s*GB"
g_size_mb_reg = "(\d+)\s*MB"

g_pc_reg = "PC(\d)[-\s]*(\d+)"
g_pc1_reg = "PC[-\s]*(\d+)"
g_pc3l_reg = "PC3L\s*(\d+)"

g_volt_reg = "(\d.\d+)V"
g_timing_reg = "(\d+)-(\d+)-(\d+)-(\d+)"

def get_capacity(prod_md_str):
    print "in function get_capacity", prod_md_str
    prod_info ={}
    m = re.search(g_kitsize_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = int(m.group(2))
        prod_info['number'] = int(m.group(1))
        return prod_info

    # try to search single memory
    m = re.search(g_size_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = int(m.group(1))
        prod_info['number'] = 1
        return prod_info

    m = re.search(g_size_mb_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = float(m.group(1))/ 1024
        prod_info['number'] = 1
        return prod_info

    #raise Exception("no capacity")
    return {}

def get_typefreq(prod_md_str):
    print "in function typefreq", prod_md_str
    prod_info = {}
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

def format_incomplete_prod(prod_md_str):
    """
    test cases
    kit capacity: 9SIA8R03P79648, 9SIA85V3R92386
    """
    prod_info = {}

    # capacity
    print prod_md_str

    cap_dic = get_capacity(prod_md_str)
    prod_info = dict(prod_info.items() + cap_dic.items())

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
    # TODO NonECC

    # voltage
    m = re.search(g_volt_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['voltage'] = float(m.group(1))

    #print prod_info
    return prod_info

def test_unstructured():
    pid = "9SIA85V3R92072"
    pid = "9SIA8R03P79648"
    pid = "9SIA85V3R92386"
    prod_md_str = open("metadata/%s.json"%(pid)).read()
    format_incomplete_prod(prod_md_str)

if __name__ == "__main__":
    #test_incomplete()
    pass
