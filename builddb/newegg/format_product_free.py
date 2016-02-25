import re
import json

###############
# general regex for general text
###############
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
    },
    2:{
        5300:667,
        6400:800,
    }
}

g_ddr_reg = "(DDR\d)"
g_freq_reg = "(\d)+[ ]*Mhz"
g_pin_reg = "(\d+)[- ]*Pin"
g_kitsize_reg = "(\d+)\s*[x](\d+)\s*GB"
g_size_reg = "(\d+)\s*+GB"
g_pc_reg = "PC(\d)[- ]*(\d+)"
g_volt_reg = "(\d.\d)V"
g_timing_reg = "(\d+)-(\d+)-(\d+)-(\d+)"

def format_incomplete_prod(prod_md_str):
    """
    test cases
    kit capacity: 9SIA8R03P79648, 9SIA85V3R92386
    """
    prod_info = {}
    # capacity
    m = re.search(g_kitsize_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['capacity'] = int(m.group(2))
        prod_info['number'] = int(m.group(1))
    else:
        # try to search single memory
        m = re.search(g_size_reg, prod_md_str, re.IGNORECASE)
        if not m:
            raise Exception("no capacity")
        prod_info['capacity'] = int(m.group(1))
        prod_info['number'] = 1

    # freq, first check PC*...
    m = re.search(g_pc_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = "DDR"+m.group(1)
        prod_info['freq'] = pc2freq[int(m.group(1))][int(m.group(2))]
    else:
        m = re.search(g_freq_reg, prod_md_str, re.IGNORECASE)
        if not m:
            raise Exception("no freq")
        prod_info['freq'] = int(m.group(1))

    # ddr type
    m = re.search(g_ddr_reg, prod_md_str, re.IGNORECASE)
    if m:
        prod_info['type'] = m.group(0)

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

    print prod_info

def test_unstructured():
    pid = "9SIA85V3R92072"
    pid = "9SIA8R03P79648"
    pid = "9SIA85V3R92386"
    prod_md_str = open("metadata/%s.json"%(pid)).read()
    format_incomplete_prod(prod_md_str)

if __name__ == "__main__":
    #test_incomplete()

