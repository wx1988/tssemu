import os
import json

from builddb.newegg.format_product_free import format_incomplete_prod

def extract_spec(skuid):
    ram_md_folder = "memory"
    prod_md_str = open("%s/%s.json"%(ram_md_folder,skuid)).read()
    spec = format_incomplete_prod(prod_md_str)

    # in field features or details
    # capacity
    obj = json.loads(prod_md_str)
    spec['price'] = obj['salePrice']

    # mem model
    spec['brand'] = obj['manufacturer']
    spec['model'] = obj['modelNumber']

    # TODO, enhance the specification extraction

    # the error checking
    #"Error Checking: ECC"

    # buffered
    #"Signal Processing: Registered"

    # formfactor
    #"Form Factor: DIMM"

    return spec


def test_extract_spec():
    skuid="3352143"
    skuid="6526314"
    skuid="4396991"
    print extract_spec(skuid)

if __name__ == '__main__':
    test_extract_spec()
