import yaml
import numpy as np
import pyquaternion as pq
import sys
from c_Position import *
from c_Orientation import *
from c_Link import *
from f_Functions import *

arguments = []
arguments.append('')
arguments.append('wynik.yaml')
arguments.append('wynik2.yaml')
main_program(arguments)
