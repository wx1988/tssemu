import re

"""
Item=N82E16833127685&
"""
p = re.compile("Item=(\w+)&")
tmp_str = open("download/desktop1.html").read()
#for m in p.finadll( tmp_str):
for m in re.findall("Item=(\w+)[&\"]", tmp_str):
    #print m.group(1)
    print m

"""
Use this API to extract the meta data information
http://ecology-service.cs.tamu.edu/BigSemanticsService/metadata.json?url=http://www.newegg.com/Product/Product.aspx?Item=N82E16820148770
"""
