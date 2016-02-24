"""
desktop memory
http://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-100?cm_sp=cat_memory_1-_-VisNav-_-desktop-memory

laptop memory
http://www.newegg.com/Laptop-Memory/SubCategory/ID-381/Page-100

"""
import os
import time

time_lag = 30

def download_desktop_mem():
    for i in range(1,101):
        url = "http://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-%d?cm_sp=cat_memory_1-_-VisNav-_-desktop-memory"%(i)
        cmd = 'wget "%s" -O download/desktop%i.html'%(url, i)
        print cmd
        os.system(cmd)
        time.sleep(10)

def download_laptop_mem():
    for i in range(1,101):
        url = "http://www.newegg.com/Laptop-Memory/SubCategory/ID-381/Page-%d"%(i)
        cmd = 'wget "%s" -O download/laptop%i.html'%(url, i)
        print cmd
        os.system(cmd)
        time.sleep(time_lag)

def download_mac_mem():
    for i in range(1,18):
        url = "http://www.newegg.com/Laptop-Memory/SubCategory/ID-551/Page-%d"%(i)
        cmd = 'wget "%s" -O download/mac%i.html'%(url, i)
        print cmd
        os.system(cmd)
        time.sleep(time_lag)

def download_server_mem():
    for i in range(1,101):
        url = "http://www.newegg.com/Laptop-Memory/SubCategory/ID-541/Page-%d"%(i)
        cmd = 'wget "%s" -O download/server%i.html'%(url, i)
        print cmd
        os.system(cmd)
        time.sleep(time_lag)

if __name__ == "__main__":
    #download_desktop_mem()
    download_laptop_mem()
    download_mac_mem()
    download_server_mem()
