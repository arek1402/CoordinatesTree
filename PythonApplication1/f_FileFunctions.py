from c_Position import *
from c_Orientation import *
from c_Link import *
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
    result = path[((length)-5):]
    return result

#Sprawdza czy wprowadzona ściezka nie zawiera błędów"
def check_file_path(path):
    if(len(path) == 0):
        print('Nie wprowadzono ścieżki do pliku. \n')
        return False
    elif(len(path) > 5):
        ext = get_file_extension(path)
        if(ext == ".yaml" or ext == ".YAML"):
            return True
    else:
        return False

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
    link.name = str(record['Name'])
    link.master = str(record['Master'])
    link.inverted = int(record['Inverted'])
    link.position.assingn_data(record['Position'])
    link.orientation.assingn_data(record['Orientation'])

    return link


# Główna funkcja agregująca dane odczytane ze sparsowanego pliku YAML - podział na układ bazowy i tablicę układów zależnych
def agregate_parsed_data(data):
   base_link = c_Link()
   other_link = c_Link()
   all_other_links = []
   i = 1
   j = 0
   
   
   for record in data:
       temp_link_name = 'Link' + str(j)
       row = record[temp_link_name]
       if (row['Master'] == ''):
            base_link = extract_data_from_record(row)         
            base_link.set_id(0)
            base_link.get_coordinate_system()
       else:
            other_link = extract_data_from_record(row)
            other_link.set_id(i)
            other_link.get_coordinate_system()
            all_other_links.append(other_link)
            i = i+1
       j += 1
   final_input_data = make_data_consistent(base_link, all_other_links)
   return final_input_data



# Składa wszystkie układy do jednego wektora danych, gdzie układ bazowy jest na pierwszym miejscu
def make_data_consistent(base_link, other_links):
    result = []
    result.append(base_link)
    for i in other_links:
        result.append(i)

    return result

#Sprawdza czy wczytane dane mają tylko jeden układ główny (pole master_id = -1)
def check_master_link_id(data):
    number_of_roots = 0
    for i in data:
        if(i.master == ''):
            number_of_roots += 1
    if(number_of_roots == 1):
        return True
    else:
        return False

#Sprawdza czy dane ID nie powtarza sie w danych wejściowych dla dwóch różnych układów
def check_multiple_id(data):
    current_name = 'empty'
    number_of_current_name = 0

    for i in data:
        current_name = i.name
        number_of_current_name = 0
        for j in data:
            if(current_name == j.name):
                number_of_current_name += 1
        
        if(number_of_current_name > 1):
            return False

    return True


def save_result_to_yaml(path, data):
    
    stream = open(path, "w")
    
    for i in data:
        record = c_Record()
        record.prepare_data_to_save(i)
        rec_data = record.generate_record_to_save(i.id)
        yaml.dump(rec_data, stream,default_flow_style=False, sort_keys=False )
