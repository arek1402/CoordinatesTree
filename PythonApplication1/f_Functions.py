
from c_Position import *
from c_Orientation import *
from c_Link import *
from c_Result import *
from f_FileFunctions import *
from c_Record import *
import numpy as np
import numpy.linalg as nplg
import pyquaternion as pq
import yaml

all_links = []
result_links = []
current_transformation = np.eye(4)
result_tab = []
current_link_id = -1


#Pobiera z listy układów cLink układ o zadanym ID
def get_cLink(cLink_id):
    global all_links
    result = 0
    for i in all_links:
        if i.id == cLink_id:
            result = i
            return result

def get_cLink_name(cLink_id): #Zwraca nazwe ukladu o zadanym ID
    global all_links
    result = ''
    for i in all_links:
        if i.id == cLink_id:
            result = i.name
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
        temp = get_cLink(i)
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

# Zwraca identyfikator układu bazowego
def get_base_link_id():
    global all_links
    for i in all_links:
        if(i.master_id == -1):
            return i.id

# Wykonuje operacje mnożenia macierzowego celem uzyskania nowego przekształcenia
def make_transformation(master_link_transformation, slave_link_transformation, inverted):
      
    if(inverted == 0):
        result = np.matmul(master_link_transformation, slave_link_transformation)
        return result
   
    else:
        temp_matrix = nplg.inv(master_link_transformation)
        result_inv = np.matmul(temp_matrix, slave_link_transformation)
        return result_inv


   #Główna funkcja analizująca drzewo
def analyze_tree(link_id, link_transformation):
    global all_links
    global result_tab
    global current_link_id
    global current_transformation

    childs = [] #Tablica przechowujaca identyfikatory potomków danego układu
    number_of_childs = [] #Liczba potomkow danego ukladu
    childs_status = False #Flaga - informacja czy wszyscy potomkowie danego układu zostali już sprawdzeni
    current_link_id = link_id
    current_transformation = link_transformation

    if(check_end_condition(all_links) == True):  #Sprawdz warunek zakonczenia pracy algorytmu
        return True

    number_of_childs, childs = find_childs(current_link_id) #Wyszukuje potomków danego układu

    if(len(childs) > 0): #Jesli znaleziono potomków danego układu to sprawdza ich status 
        childs_status = check_childs_status(childs, all_links)

    if(number_of_childs == 0 or childs_status == True): #Jesli dany uklad nie ma potomkow to zapisz aktualne przekształcenie do bazy wynikow

       temp_result = c_Result() #Obiekt klasy c_Result przechowujący informacje o ID układu i jego przekształcenia względnem układu bazowego 
       temp_result.id = link_id
       temp_result.transform = current_transformation
       result_tab.append(temp_result) #Dopisanie wyniku przekształcenia do tablicy wynikow

       change_status(current_link_id) #Zmienia status danego ukladu na sprawdzony

       current_transformation = np.eye(4)
       current_link_id = get_base_link_id() #Wyszukuje w bazie układ bazowy i pobiera jego ID
       analyze_tree(current_link_id, current_transformation)

    else:

        first_child_id = get_first_child_id(childs) #Pobiera pierwszy uklad z bazy, który jest dzieckiem danego układu i nie ma statusu "Checked"
        child_link = get_cLink(first_child_id) #Pobiera ID potomka

        current_transformation = make_transformation(current_transformation, child_link.coordinate_system, child_link.inverted) #Wyznaczanie transformacji do nowego układu
        current_link_id = child_link.id #Przypisanie danych nowego układu
        analyze_tree(current_link_id, current_transformation) #Rekurencyjne wywołanie funkcji analyze_tree z nowymi danymi


#Przekształca dane z formatu wynikowego do formatu wejściowego dla zapisu do pliku
def organize_results_to_cLink(result_tab): 

    organised_result = []

    if(len(result_tab) > 0):

        for i in result_tab:
            old_cLink = get_cLink(i.id)
            new_cLink = old_cLink
            new_cLink.master_id = get_base_link_id()
            new_cLink.coordinate_system = i.transform
            new_cLink.get_quaternion_from_matrix()
            new_cLink.round_floats(5)
            organised_result.append(new_cLink)


    return organised_result

#Sortowanie tablicy z wynikami
def bubble_sort_organised_results(org_res): 

    i = 0
    j = 0
    k = len(org_res)
    data = org_res
    for i in range(k-1):
        for j in range(k-1):
            cLink1 = data[j]
            cLink2 = data[j+1]
            if(cLink1.id > cLink2.id):
                data[j+1] = cLink1
                data[j] = cLink2
                
    return data



def main_function():
    global all_links
    global current_transformation
    global result_tab
    global current_link_id

    data = read_yaml_file("results.yaml")
    all_links = agregate_parsed_data(data)

    start_id = get_base_link_id()
    start_transformation = np.eye(4)

    analyze_tree(start_id, start_transformation)
    new_tab = organize_results_to_cLink(result_tab)

    new_tab2 = bubble_sort_organised_results(new_tab)

    #result = prepare_data_to_save(new_tab2)
    save_result_to_yaml('results.yaml',new_tab2)
    #print(result)
    
def main_program():

    global all_links
    global current_transformation
    global result_tab
    global current_link_id

    state_number = 0

    print('Witaj w aplikacji CoordinatesTree. Aby rozpocząć pracę wskaż lokalizację pliku źródłowego YAML podając jego BEZWZGLĘDNĄ ścieżkę.')
    state_number = 1
    source_file_path = ''
    dest_file_path = ''

    try:
        while(1):
            if(state_number == 1):
                source_file_path = input('Lokalizacja: ')
                state_number = 2

            if(state_number == 2):
                path_ok = check_file_path()
                if(path_ok == True):
                    exist = check_that_file_exists(source_file_path)
                    if(exist):
                        state_number = 3
                    else:
                        print('Plik o podanej ścieżce nie istnieje. Wprowadz sciezke ponownie. \n')
                        state_number = 1
                else:
                    print('Wprowadzona ścieżka do pliku ma nieprawidłowy format. Wprowadz ją ponownie zwracając uwagę na rozszerzenie. \n')
                    state_number = 1

            if(state_number == 3):
                print('Odczytywanie danych... \n')
                try:
                    data = read_yaml_file(source_file_path)
                    all_links = agregate_parsed_data(data)
                    state_number = 4
                except:
                    print('Bład odczytu danych. Sprawdź zawartość pliku źródłowego i spróbuj ponownie. \n')
                    state_number = -1

            if(state_number == 4):
                print('Wprowadź lokalizację pliku docelowego \n')
                dest_file_path = input('Lokalizacja:')
                state_number = 5

            if(state_number == 5):
                #Sprawdz poprawnosc sciezki docelowej
                pass




