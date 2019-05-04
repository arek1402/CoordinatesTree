from c_Position import *
from c_Orientation import *
from c_Link import *
from c_Result import *
from c_Record import *
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
    link.master_id = record['Master_ID']
    link.inverted = record['Inverted']
    link.position.x = record['Position']['X']
    link.position.y = record['Position']['Y']
    link.position.z = record['Position']['Z']
    link.orientation.scalar = record['Orientation']['Scalar']
    link.orientation.rotx = record['Orientation']['RotX']
    link.orientation.roty = record['Orientation']['RotY']
    link.orientation.rotz = record['Orientation']['RotZ']

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
       else:
            other_link = extract_data_from_record(row)         
            other_link.get_coordinate_system()
            all_other_links.append(other_link)
       i = i+1
   
   final_input_data = make_data_consistent(base_link, all_other_links)
   return final_input_data

def agregate_parsed_data2(data):
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
       else:
            other_link = extract_data_from_record(row)         
            other_link.get_coordinate_system()
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

def save_result_to_yaml(path, data):
    
    stream = open(path, "w")
    
    for i in data:
        record = c_Record()
        record.prepare_data_to_save(i)
        rec_data = record.generate_record_to_save()
        yaml.dump(rec_data, stream,default_flow_style=False, sort_keys=False )
        #yaml.dump(record2, stream)