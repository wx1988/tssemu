"""
the must have property are
type, freq, capacity

optional are:
ecc, reg, pin,

Enumerate all products, get the file that doesn't pass,
fix the regex.
"""
import os
import json

from format_product_bigsem import format_complete_prod
from format_product_free import format_incomplete_prod

nece_list = ['type', 'freq', 'capacity']

def check_ok(prod_info):
    for k in nece_list:
        if not prod_info.has_key(k):
            print 'missing', k
            return False
    return True

def check():
    ignore_list = [
        "9SIA8H53HE0050.json",
        "9SIA8H53HD6014.json",
        "N82E16820120052.json",
        "9SIA6ZP3R88366.json",
        "9SIA85V3R92208.json",
        "9SIA25V1GB7057.json",
        "9SIA8H53HD1618.json",
        "9SIA24G3RH4813.json",
        "9SIA70F3H87208.json",
        "9SIA4CP1GF9691.json",
        "9SIA6ZP3R86397.json",
        "9SIA86Y3P66595.json",
        "9SIA4HM2B16154.json",
        # computer based
        "9SIA70F3H87003.json",
        "9SIA6ZP3R86331.json",
        "9SIA86Y3P66828.json",
        "9SIA86Y3P66954.json",
        "9SIA70F3H86916.json",
        # wrong information
        "N82E16820120070.json",
        "9SIA24G3RH5874.json",
        "9SIA98C3RC7818.json",
        "9SIA85V3R92140.json",
        "9SIA86Y3P66772.json",
        "9SIA86Y3P66742.json",
        "9SIA8H53HD5276.json",
        "9SIA86Y3P66745.json",
        "9SIA86Y3P66875.json",
        "9SIA17P3KE7064.json",
        "9SIA85V3R91887.json",
        "9SIA8H53HD7613.json",
        "9SIA86Y3P66887.json",
        "9SIA8H53HD4362.json",
        "9SIA2E11681062.json",
        "9SIA8H53HD5924.json"

        ]
    todo_list = [
        #  PC3L
        "9SIA8UC3RA0528.json",
        "N82E16820104583.json",
        "N82E16820226787.json",
        "9SIA7253N23165.json",
        "9SIA85V3R92537.json",
        "9SIA85V3R92317.json",
        "N82E16820231733.json",
        "N82E16820231466.json",
        # pc100, # pc2100
        "9SIA70F3H87330.json"
        "9SIA70F3H87385.json",
        "9SIA4UB3TD3552.json",
        "9SIA70F3HT7634.json",
        "9SIA1K624N0752.json",
        "9SIA7S62VZ7601.json",
        "9SIA70F3HT7685.json",
        "9SIA70F3HT7702.json",
        "9SIA85V3R91843.json",
        # unit missing
        "9SIA86Y3P66748.json",
        "9SIA86Y3P66747.json",
        # TODO
        "9SIA70F3H87120.json",
        "9SIA24G2HZ2332.json",
        "9SIA86Y3P66711.json",
        "9SIA7S62VZ7633.json",
        "9SIA86Y3P66842.json",
        "9SIA7S62VZ7584.json",
        "9SIA5752CZ1519.json",
        "N82E16820516309.json",
        "9SIA67S3T49574.json",
        "9SIA8BU3PC9858.json",
        "9SIA70F3HT7740.json",
        "9SIA70F3HT7783.json",
        "9SIA85V3RB1833.json",
        "9SIA67S3T48863.json",
        "9SIAA443S22485.json",
        "9SIA6ZP3R87639.json",
        "N82E16820224064.json",
        "9SIA86Y3P66891.json",
        "9SIA8H53HD4883.json",
        # unknown type
        "9SIA85V3R95134.json",
        "9SIA7S62VZ7944.json",
        "9SIA67S3T49550.json",
        "9SIA7S62VZ7611.json",
        "9SIA70F3H87119.json",
        "9SIA24G3SW5108.json",
        "9SIA4UB1UJ9934.json",
        # obvious wrong
        "9SIA5751PV1922.json",
        "9SIA6UM2C46488.json",
        "9SIA70F3HT7643.json",
        "9SIA5753KG5842.json",
        "9SIA70F3HT7833.json",
        "9SIA8BU3RA6910.json",
        "9SIA70F3HT7775.json",
        # need voting
        "9SIA24G1GC6355.json",
        "9SIA70F3H87075.json",
        "9SIA70F3J47809.json",
        "9SIA70F3H87159.json",
        "9SIA70F3H87023.json",
        "9SIA70F3H87088.json",
        "9SIA70F3H86931.json",
        "9SIA8R03U35487.json",
        "9SIAA443S21648.json",
        "9SIA70F3H87016.json",
        "9SIA70F3H87308.json",
        "9SIA70F3HT7757.json",
        ]
    meta_dir = "metadata"

    gc = 0
    bc = 0
    start_index = 0
    for i, fname in enumerate( os.listdir(meta_dir) ):
        if not fname.endswith("json"):
            continue
        if fname in ignore_list:
            continue
        if fname in todo_list:
            continue
        if i < start_index:
            continue

        print "##################"
        print i,fname
        prod_md_str = open("%s/%s"%(meta_dir,fname)).read()
        prod_md = json.loads(prod_md_str)
        if prod_md_str.lower().count("mushkin") > 0:
            continue
        computer_models = ['apple','macbook','hp']
        for_cm = False
        for cm in computer_models:
            if prod_md_str.lower().count(cm) > 0:
                for_cm = True
                break
        if for_cm:
            continue

        p1 = format_complete_prod(prod_md)
        ok1 = check_ok(p1)
        if ok1:
            continue

        p2 = format_incomplete_prod(prod_md_str)
        ok2 = check_ok(p2)
        if not ok2:
            print "=========Good %d==========="%(i)
            print fname
            print prod_md_str
            print p2
            #raise Exception("")
            bc += 1
            #exit(1)
        """
        except Exception as e:
            print "===================="
            print e
            print fname
            print prod_md_str
            exit(1)
        """
        gc += 1
    print gc, bc



if __name__ == "__main__":
    check()


