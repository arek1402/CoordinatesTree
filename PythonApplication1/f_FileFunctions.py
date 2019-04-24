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
            base_link.get_translation_matrix()
            base_link.get_rotation_matrix()
            base_link.rad2deg()
            base_link.get_coordinate_system()
            #print(base_link.coordinate_system)
       else:
            #print(row)
            other_link = extract_data_from_record(row)
            other_link.get_translation_matrix()
            other_link.get_rotation_matrix()
            other_link.rad2deg()
            other_link.get_coordinate_system()
            all_other_links.append(other_link)
       i = i+1
   
   return base_link, all_other_links

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
    cords_data['X'] = link.coordinates.x
    cords_data['Y'] = link.coordinates.y
    cords_data['Z'] = link.coordinates.z
    cords_data['scalar'] = link.coordinates.scalar
    cords_data['RotX'] = link.coordinates.rotx
    cords_data['RotY'] = link.coordinates.roty
    cords_data['RotZ'] = link.coordinates.rotz
    ret_data['Name'] = link.name
    ret_data['ID'] = link.id
    ret_data['Master_link'] = 0
    ret_data['Cords'] = cords_data


    return ret_data


def agregate_data_to_save(base_link, other_links):
    ag_data = []
    i = 0
    bl = record_injection(base_link)
    ag_data.append(bl)

    for i in other_links:
        ol = record_injection(i)
        ag_data.append(ol)

    #print(ag_data)
    return ag_data

def save_result_to_yaml(path, data):
    
    dictionary = dict(data)
    with open(path, 'w') as outfile:
        yaml.dump(dictionary,outfile,default_flow_style =False)