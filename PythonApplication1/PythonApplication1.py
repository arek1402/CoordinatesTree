import yaml
import numpy as np
import pyquaternion as pq
from c_Coordinates import *
from c_Link import *
from f_Functions import *

#Deklaracja zmiennych globalnych

Base_link = c_Link()
Other_links = []

data = read_yaml_file("dane.yaml")
Base_link, Other_links = agregate_parsed_data(data)
pr_data = agregate_data_to_save(Base_link, Other_links)
#save_result_to_yaml("gowno.yaml",pr_data)



