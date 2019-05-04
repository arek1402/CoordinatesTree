from c_Position import *
from c_Orientation import *
from c_Link import *
from c_Result import *
from c_Record import *
import numpy as np
import numpy.linalg as nplg
import pyquaternion as pq
import yaml
from pathlib import Path


#Parsowanie pliku YAML z danymi
def read_yaml_file(path):
    with open(path, 'r') as stream:  
        x = yaml.safe_load(stream)
        return x

#Pobiera ostatnie 5 znaków z podanej ścieżki
def get_file_extension(path):
    length = len(path)
    result = path[(length)-5:lenght]
    return result

#Sprawdza czy wprowadzona ściezka nie zawiera błędów"
def check_file_path(path):
    if(len(path) == 0):
        print('Nie wprowadzono ścieżki do pliku. \n')
        return False
    elif(path[1] != ':' or path[2] != '\\' ):
        print('Wprowadzono niepoprawny format ścieżki dostępu do pliku źródłowego \n')
        return False
    elif(len(path) > 5 and (get_file_extension(path) == ".YAML" or get_file_extension == ".yaml")):
        return True

#Sprawdza czy plik w podanej lokalizacji znajduje sie na dysku

def check_that_file_exists(path):
    temp_path = Path(path)
    if(temp_path.is_file()):
        return True
    else:
        return False


# Wyodrębnianie danych ze struktury sparsowanego  rekordu pliku YAML
def extract_data_from_record(record): 
    link = c_Link()
    link.name = record['Name']
    link.id = float(record['ID'])
    link.master_id = float(record['Master_ID'])
    link.inverted = float(record['Inverted'])
    link.position.x = float(record['Position']['X'])
    link.position.y = float(record['Position']['Y'])
    link.position.z = float(record['Position']['Z'])
    link.orientation.scalar = float(record['Orientation']['Scalar'])
    link.orientation.rotx = float(record['Orientation']['RotX'])
    link.orientation.roty = float(record['Orientation']['RotY'])
    link.orientation.rotz = float(record['Orientation']['RotZ'])

    return link


# Główna funkcja agregująca dane odczytane ze sparsowanego pliku YAML - podział na układ bazowy i tablicę układów zależnych
def agregate_parsed_data(data):
   base_link = c_Link()
   other_link = c_Link()
   all_other_links = []
   i = 0
   
   for record in data:
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