import os
import re
import json
import subprocess
import sys
import urllib
import webbrowser

def execute_cmd(cmd):
    """execute a command line command
    and get the output

    Returns output strings
    """
    p = subprocess.Popen(cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out, _ = p.communicate()
    out = out.replace("\r\n", "\n")
    return out


def get_memory_str():
    """
    """
    sys_info = {}
    dmidecode_path = ""
    if os.path.isfile("./dmidecode.exe"):
        dmidecode_path = "./dmidecode.exe"
    elif os.path.isfile("./dist/dmidecode.exe"):
        dmidecode_path = "./dist/dmidecode.exe"
    else:
        raise Exception("dmidecode not found")
    print "detected dmidecode", dmidecode_path
        
    # machine model
    dmidecode_cmd = [dmidecode_path, "-t", "system"]
    output = execute_cmd(dmidecode_cmd)
    lines = [line.strip() for line in output.split("\n")]
    for line in lines:
        if line.startswith("Manufacturer"):
            sys_info['manufacturer'] = line[line.index(":")+1:]
        if line.startswith("Product Name"):
            sys_info['productname'] = line[line.index(":")+1:]

    # some system info
    dmidecode_cmd = [dmidecode_path, "-t", "16"]
    output = execute_cmd( dmidecode_cmd )
    lines = [line.strip() for line in output.split("\n")]
    for line in lines:
        ws = line.split(':')
        if line.startswith("Max"):
            mc = int(ws[1].strip().split(' ')[0])
            sys_info['maximum_capacity'] = mc
        if line.startswith("Num"):
            sys_info['slots'] = int( ws[1])

    # get existing memories
    dmidecode_cmd = [dmidecode_path, "-t", "17"]
    output = execute_cmd( dmidecode_cmd )
    lines = [line.strip() for line in output.split("\n")]
    #print output

    # 1. size
    size_re = re.compile("Size: (\d+) MB")
    # 2. type
    type_re = re.compile("Type: ([\s\S]*?)\n")
    typed_re = re.compile("Type Detail: ([\w ]+)")
    # 3. speed
    speed_re = re.compile("Speed: (\d+) MHz")
    # 4. Part number
    pn_re = re.compile("Part Number: ([\s|\S]*?)\n")

    sys_info['mem_list'] = []
    mem_list = output.split('\n\n')
    for mem in mem_list:
        mem = mem.strip()
        #print '0', mem[0]
        if mem == "":
            continue
        if mem.startswith("Handle"):
            print 'Mem', mem
            try:
                size_str = size_re.search( mem ).group(1)
                print 'size'
                type_str = type_re.search( mem ).group(1)
                print 'type'
                typed_str = typed_re.search( mem ).group(1)
                print 'speed'
                speed_str = speed_re.search( mem ).group(1)
                print 'pn'
                pn_str = pn_re.search( mem ).group(1)
                mem_info = {
                        'capacity':int(size_str),
                        'type':type_str,
                        'detail':typed_str.strip(),
                        'speed':int(speed_str),
                        'model': pn_str.strip()
                        }
                sys_info['mem_list'].append( mem_info )
            except Exception as e:
                # empty slots
                print e
                pass
    return sys_info

if __name__ == "__main__":
    sys_info =  get_memory_str()
    print sys_info
    #print sys_info

    url_tpl = "http://rtds9.cse.tamu.edu:8080/suggest?sys_info=%s"
    json_str = json.dumps(sys_info)

    the_url = url_tpl%(urllib.quote_plus(json.dumps(sys_info)))

    print the_url
    #the_url.replace("")
    #os.system("explorer %s"%(the_url))

    webbrowser.open(the_url)
