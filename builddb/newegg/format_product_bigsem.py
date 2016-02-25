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
volt_reg = "(\d.\d+)V"
ecc_reg = "Yes|No"
buf_reg = "Buffered|Unbuffered"
kit_reg = "\w+"
heat_reg = "Yes|No"

from format_product_free import get_capacity, get_typefreq

def format_complete_prod(prod_md):
    if not prod_md['newegg_product'].has_key("specifications_table"):
        return {}

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
    if kv.has_key("Model"):
        prod_info['model'] = kv["Model"]

    # number * capacity
    if kv.has_key('Capacity'):
        cap_dic = get_capacity(kv['Capacity'])
        prod_info = dict(prod_info.items() + cap_dic.items())
        """
        #print cap
        if cap.count("(") == 0 and cap.count("[") == 0:
            prod_info['capacity'] = float(cap[:-2])
            prod_info['number'] = 1
        else:
            cap_reg = "\d+G[B]* [\(|\[](\d)\s*x (\d+)G[B]*[\)|\]]"
            m = re.match(cap_reg, cap, re.IGNORECASE)
            print m
            print m.groups()
            prod_info['capacity'] = float(m.group(2))
            prod_info['number'] = int(m.group(1))
        """

    if kv.has_key('Speed'):
        tf_dic = get_typefreq(kv['Speed'])
        prod_info = dict(prod_info.items() + tf_dic.items())
        """
        prod_info['type'] = kv['Type'].split(" ")[1]
        prod_info['pin'] = int( kv['Type'].split(" ")[0].split('-')[0] )
        prod_info['freq'] = int( kv['Speed'].split(" ")[1])
        """

    # ECC
    if kv.has_key('ECC'):
        if kv['ECC'] == "Yes":
            prod_info['ecc'] = True
        if kv['ECC'] == "No":
            prod_info['ecc'] = False

    # registered
    br = "Buffered/Registered"
    if kv.has_key(br):
        prod_info["reg"] = kv[br]

    # TODO, possible two voltage
    if kv.has_key("Voltage"):
        m = re.search(volt_reg, kv['Voltage'])
        prod_info['voltage'] = float(m.group(1))

    #print prod_info
    return prod_info

def test_complete():
    pid = "N82E16820148166"
    pid = "9SIA0ZX2M46757"
    pid = "N82E16820231569" # kit
    pid = "N82E16820148959"
    prod_md = json.load(open("metadata/%s.json"%(pid)))
    format_complete_prod(prod_md)


if __name__ == "__main__":
    test_complete()

