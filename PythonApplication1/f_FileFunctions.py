from c_Coordinates import *
from c_Link import *
from c_Result import *
import numpy as np
import numpy.linalg as nplg
import pyquaternion as pq
import yaml



#Parsowanie pliku YAML z danymi
def read_yaml_file(path):
    with open(path, 'r') as stream:  
        x = yaml.safe_load(stream)
        return x

# Wyodrębnianie danych ze struktury sparsowanego  rekordu pliku YAML
def extract_data_from_record(record): 
    link = c_Link()
    link.name = record['Name']
    link.id = record['ID']
    link.master_id = record['Master_link']
    link.inverted = record['Inverted']
    link.coordinates.x = record['Cords']['X']
    link.coordinates.y = record['Cords']['Y']
    link.coordinates.z = record['Cords']['Z']
    link.coordinates.scalar = record['Cords']['Scalar']
    link.coordinates.rotx = record['Cords']['RotX']
    link.coordinates.roty = record['Cords']['RotY']
    link.coordinates.rotz = record['Cords']['RotZ']

    return link

# Generowanie numeru nagłówka do odczytu danych 
def generate_link_number(number):
    return 'Link' + str(number)

# Główna funkcja agregująca dane odczytane ze sparsowanego pliku YAML - podział na układ bazowy i tablicę układów zależnych
def agregate_parsed_data(data):
   base_link = c_Link()
   other_link = c_Link()
   all_other_links = []
   i = 0
   
   for record in data:
       header = generate_link_number(i)
       row = data[record]
       if i==0:
            base_link = extract_data_from_record(row)           
            base_link.get_coordinate_system()
            #base_link.rad2deg()
       else:
            other_link = extract_data_from_record(row)         
            other_link.get_coordinate_system()
            #other_link.rad2deg()
            all_other_links.append(other_link)
       i = i+1
   
   final_input_data = make_data_consistent(base_link, all_other_links)
   return final_input_data

# Składa wszystkie układy do jednego wektora danych, gdzie układ bazowy jest na pierwszym miejscu
def make_data_consistent(base_link, other_links):
    result = []
    result.append(base_link)
    for i in other_links:
        result.append(i)

    return result

def record_injection(record):
    link = record
    ret_data = {}
    cords_data = {}
    cords_data['X'] = str(link.coordinates.x)
    cords_data['Y'] = str(link.coordinates.y)
    cords_data['Z'] = str(link.coordinates.z)
    cords_data['scalar'] = str(link.coordinates.scalar)
    cords_data['RotX'] = str(link.coordinates.rotx)
    cords_data['RotY'] = str(link.coordinates.roty)
    cords_data['RotZ'] = str(link.coordinates.rotz)
    ret_data['Name'] = link.name
    ret_data['ID'] = str(link.id)
    ret_data['Master_link'] = str(0)
    ret_data['Cords'] = str(cords_data)


    return ret_data


def agregate_data_to_save(all_data):
    ag_data = []
    for i in all_data:
        ol = record_injection(i)
        ag_data.append(ol)

    #print(ag_data)
    return ag_data

def save_result_to_yaml(path, data):
    
    #dictionary = dict(data)
    #with open(path, 'w') as outfile:
    
    stream = open(path, "w")
    yaml.dump(data,stream)
    print(yaml.dump(data))