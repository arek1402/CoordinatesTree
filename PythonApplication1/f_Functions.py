
from c_Coordinates import *
from c_Childs import *
from c_Link import *
from c_Result import *
import numpy as np
import pyquaternion as pq
import yaml


all_links = []
current_transformation = np.eye(4)
result_tab = []
current_link_id = -1
result_tab.append(1)


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

# Konwersja ze stopni na radiany
def deg2rad(number_in_degrees):
    return number_in_degrees * np.pi / 180.0
# Konwersja z radianów na stopnie
def rad2deg(number_in_radians):
    return number_in_radians * 180.0 / np.pi

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


#Pobiera z listy układów cLink układ o zadanym ID
def get_cLink(cLink_id):
    global all_links
    result = 0
    for i in all_links:
        if i.id == cLink_id:
            result = i
            return result
    

#Znajduje potomków układu o zadanym ID
def find_childs(link_id):
    global all_links
    tab_of_childs = []
    number_of_childs = 0 

    for i in all_links:
        if(i.master_id == link_id):
            tab_of_childs.append(i.id)
            number_of_childs += 1

    return number_of_childs, tab_of_childs

#Sprawdź czy potomkowie układu zostali już przetworzeni przez algorytm - True - tak, wszystkie układy sprawdzone, False - jeden lub kilka układów jest niesprawdzonych
def check_childs_status(tab_of_childs, all_data):
    number_of_childs = len(tab_of_childs)
    number_of_checked = 0
    for i in tab_of_childs:
        temp = get_cLink(i,all_data)
        if (temp.checked == True):
            number_of_checked += 1 

    if (number_of_checked == number_of_childs):
        return True
    else:
        return False

    #Zwraca pierwszy wolny identyfikator niesprawdzonego układu
def get_first_child_id(tab_of_childs):

    for i in tab_of_childs:
        temp = get_cLink(i)
        if(temp.checked == False):
            return temp.id

 #zmienia status układu na "Checked"
def change_status(link_id):
    global all_links

    new_data = []
    for i in all_links:
        if(i.id == link_id):
            i.checked = True
        new_data.append(i)

    all_links = new_data

 #Sprawdza warunek koncowy pracy algorytmu przeszukiwania drzewa
def check_end_condition(all_data):
    number_of_checked = 0
    for i in all_data:
        if(i.checked == True):
            number_of_checked += 1

    if (number_of_checked == len(all_data)):
        return True
    else:
        return False

   #Główna funkcja analizująca drzewo
def analyze_tree(link_id, link_transformation, all_data):

    childs = [] #Tablica przechowujaca identyfikatory potomków danego układu
    number_of_childs = [] #Liczba potomkow danego ukladu
    childs_status = False #Flaga - informacja czy wszyscy potomkowie danego układu zostali już sprawdzeni
  
    if(check_end_condition(all_data) == True):  #Sprawdz warunek zakonczenia pracy algorytmu
        return True

    number_of_childs, childs = find_childs(link_id, all_data) #Wyszukuje potomków danego układu

    if(len(childs) > 0): #Jesli znaleziono potomków danego układu to sprawdza ich status 
        childs_status = check_childs_status(childs, all_data)

    if(number_of_childs == 0 or childs_status == True): #Jesli dany uklad nie ma potomkow to zapisz aktualne przekształcenie do bazy wynikow
       temp_result = c_Result()
       temp_result.id = link_id
       temp_result.transform = current_transformation
       result_tab.append(temp_result)





    if(number_of_childs == 0):
        pass

    else:
        pass


def main_function():
    global all_links
    global current_transformation
    global result_tab
    global current_link_id

    data = read_yaml_file("dane.yaml")
    base_link, other_links = agregate_parsed_data(data)
    print(base_link.id)
    print('\n')
    all_links = make_data_consistent(base_link, other_links)

    temp1,temp2 = find_childs(3)
    temp3 = get_first_child_id(temp2)
    change_status(2)
    w = get_cLink(2)
    x = get_cLink(3)
    y = get_cLink(4)

    pass