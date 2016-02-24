"""
For the products with all fields pass the regex matching, could easily transform to predefined format. 

For the products only passing partial regex matching, try to use regex to extract information. 

"""
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


###############
# general regex for general text
###############
g_ddr_reg = "DDR\d"
g_freq_reg = "\d+[ ]+Mhz"
g_pin_reg = "\d+[- ][Pp]in"
g_kitsize_reg = "\d+ x \d+ GB"
g_size_reg = "\d+[ ]+GB"
g_pc_reg = "PC\d \d+"
