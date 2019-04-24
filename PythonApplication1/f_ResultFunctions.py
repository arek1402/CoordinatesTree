from c_Coordinates import *
from c_Childs import *
from c_Link import *
from c_Result import *
import numpy as np
from f_Functions import *

def organize_results_to_cLink(result_tab): #Przekształca dane z formatu wynikowego do formatu wejściowego dla zapisu do pliku

    global all_links
    organised_result = []

    if(len(result_tab) > 0):
        bl_id = get_base_link_id()
        bl = get_cLink(bl_id)
        bl.coordinate_system = np.eye(4)
        organised_result.append(bl)
        for i in result_tab:
            temp = c_Link()
            temp.id = i.id
            temp.coordinate_system = i.transform
            temp.master_link = bl_id
            temp.name = get_cLink_name(i.id)
            organised_result.append(temp)

            #Dokonczyc funkcje
    organised_result.sort()
    return organised_result

def bubble_sort_organised_results(org_res): #Sortowanie tablicy z wynikami
   
  pass
