import yaml
import numpy as np
import pyquaternion as pq
from c_Coordinates import *
from c_Link import *
from c_Childs import *
from f_Functions import *
from c_Result import*

#Deklaracja zmiennych globalnych


data = read_yaml_file("dane.yaml")
base_link, other_links = agregate_parsed_data(data)
print(base_link.id)
print('\n')
all_data = make_data_consistent(base_link, other_links)

for i in all_data:
    print('\n')
    print(i.name)
    print('\n')
    print(i.coordinate_system)

a = input('Czekaj')



#pr_data = agregate_data_to_save(Base_link, Other_links)
temp = find_dependencies(all_data)
result_matrix = []

for i in all_data:
    temp = None
    temp = analzye_tree(i, all_data)
    if temp != None:
        result_matrix.append(temp)


for j in result_matrix:
    print('Znalezione:',j.id, '\n')




#save_result_to_yaml("gowno.yaml",pr_data)
