import os
import json

from builddb.format_product_free import format_incomplete_prod, get_capacity, get_typefreq
from tsse_common import bb_memory_folder
debug = 0
def extract_spec(skuid):
    #print skuid
    ram_md_folder = bb_memory_folder
    prod_md_str = open("%s/%s.json"%(ram_md_folder,skuid)).read()
    if debug:
        print prod_md_str
    spec = format_incomplete_prod(prod_md_str)

    # in field features or details
    # capacity
    obj = json.loads(prod_md_str)
    if obj.has_key('salePrice'):
        spec['price'] = obj['salePrice']

    # mem model
    if obj.has_key('manufacturer'):
        spec['brand'] = obj['manufacturer']
    if obj.has_key('modelNumber'):
        spec['model'] = obj['modelNumber']
    #print "before", spec

    #print "features", obj['features']
    feature_dic = {}
    if obj.has_key('features'):
        for feature in obj['features']:
            if feature['feature'].count(':') == 0:
                continue
            ws = feature['feature'].split(":")
            feature_dic[ws[0].strip()] = ws[1].strip()
    if debug:
        print feature_dic
    # TODO, enhance the specification extraction
    # capacity, ,
    cap_key1 = "Number of Modules"
    cap_key2 = "Memory Size"
    if feature_dic.has_key(cap_key1):
        cap_dic = get_capacity(feature_dic[cap_key1])
        #print "num modules", cap_dic, "'%s'"%(feature_dic[cap_key1])
    elif feature_dic.has_key(cap_key2):
        cap_dic = get_capacity(feature_dic[cap_key2])
        #print 'memory size', cap_dic
    else:
        #raise Exception("best buy capacity")
        cap_dic = {}
    spec = dict(spec.items()+cap_dic.items())

    # formfactor
    #"Form Factor: DIMM"
    ff_key1 = "Form Factor"
    if feature_dic.has_key(ff_key1):
        spec['formfactor'] = feature_dic[ff_key1]
    return spec

def test_extract_spec():
    """
    TODO, these are with bugs
    bad 3604232
bad 3604214
bad 6307695
bad 4737987
bad 4418039
bad 4418048
bad 6656759
bad 3604287
bad 4648295
bad 3961084
bad 5404724
bad 4418454
bad 3332468
bad 1201174
bad 4533189
bad 9918884
bad 4132581
bad 5421731
bad 8724767
bad 7644178
bad 4737978
bad 6000911
bad 7203242
bad 3604223
bad 4254900
bad 4417831
bad 3769006
bad 8724847
bad 3946359
bad 6714102
bad 4771586
bad 4417482
bad 4678769
bad 4495655
bad 6531734
bad 5958868
bad 5251606
bad 9150553
bad 3946377
bad 9663668
bad 4771629
bad 4771674
bad 4438961
bad 3740693
bad 4809701
bad 4418084
bad 4417859
bad 3352134
bad 4648286
bad 8020036
bad 3739591
bad 5987873
bad 8020054
bad 4117564
bad 4358295
bad 3332699
bad 8643569

    """
    skuid="3352143"
    skuid="6526314"
    skuid="4396991"
    skuid="3352143"
    skuid = "6485622"
    print extract_spec(skuid)

if __name__ == '__main__':
    test_extract_spec()
