import yaml
import numpy as np
import pyquaternion as pq
from c_Coordinates import *
from c_Link import *
from c_Childs import *
from f_Functions import *

#Deklaracja zmiennych globalnych


data = read_yaml_file("dane.yaml")
base_link, other_links = agregate_parsed_data(data)
print(base_link.id)
print('\n')
all_data = make_data_consistent(base_link, other_links)
#pr_data = agregate_data_to_save(Base_link, Other_links)
temp = find_dependencies(all_data)
for i in temp:
    for j in i.childs:
        print(i.name)
        print('\n')
        print(j.id)
        print('\n')

#save_result_to_yaml("gowno.yaml",pr_data)
