from __future__ import print_function
from aiida.orm.data.cif import CifData
from aiida.orm.calculation.work import WorkCalculation
import sys
sys.path.append('/home/daniele/Programs/cp2k_utils/parse_steps')
from parser_utils import print_header, print_steps

from contextlib import contextmanager
@contextmanager
def redirect_stdout(target):
    original = sys.stdout
    sys.stdout = target
    yield
    sys.stdout = original

#seairch for the path for the 4 steps: energy, md, geo_opt, cell_opt. Store them.
step_path = ['','','','']
step_info = ['ENERGY','MD_NVT','GEO_OPT','CELL_OPT']
last = 0 #select the Nth last result in time
with open('cif_list.txt') as finp:
 labels=finp.read().splitlines()
for label in labels:
 step_done = [False,False,False,False]
 #1 energy   
 qb = QueryBuilder()
 qb.append(CifData, filters={'label': {'==':label}}, tag='init_structure')
 qb.append(WorkCalculation, filters={'label':{'==':'Isotherm'}}, output_of='init_structure', tag='isotherm')
 qb.append(WorkCalculation, filters={'label':{'==':'Cp2kRobustGeoOptWorkChain'}}, output_of='isotherm', tag='robustgeoopt')
 qb.append(WorkCalculation, filters={'label':{'==':'Cp2kDftBaseWorkChain'}}, output_of='robustgeoopt', tag='dftbase')
 qb.append(JobCalculation,output_of='dftbase',tag='calc')
 qb.order_by({WorkCalculation:{'ctime':'desc'}})
 if len(qb.all()) > 0:
  step_path[0] =  qb.all()[last][0].out.retrieved.get_abs_path()+'/path/aiida.out'
  step_done[0] = True
 #2 md
 if step_done[0]:
  qb = QueryBuilder()
  qb.append(CifData, filters={'label': {'==':label}}, tag='init_structure')
  qb.append(WorkCalculation, filters={'label':{'==':'Isotherm'}}, output_of='init_structure', tag='isotherm')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kRobustGeoOptWorkChain'}}, output_of='isotherm', tag='robustgeoopt')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kMdWorkChain'}}, output_of='robustgeoopt', tag='md')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kDftBaseWorkChain'}}, output_of='md', tag='dftbase')
  qb.append(JobCalculation,output_of='dftbase',tag='calc')
  qb.order_by({WorkCalculation:{'ctime':'desc'}})
  if len(qb.all()) > 0:
   step_path[1] =  qb.all()[last][0].out.retrieved.get_abs_path()+'/path/aiida.out'
   step_done[1] = True
 #3 geo_opt 
 if step_done[1]:
  qb = QueryBuilder()
  qb.append(CifData, filters={'label': {'==':label}}, tag='init_structure')
  qb.append(WorkCalculation, filters={'label':{'==':'Isotherm'}}, output_of='init_structure', tag='isotherm')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kRobustGeoOptWorkChain'}}, output_of='isotherm', tag='robustgeoopt')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kGeoOptWorkChain'}}, output_of='robustgeoopt', tag='geoopt')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kDftBaseWorkChain'}}, output_of='geoopt', tag='dftbase')
  qb.append(JobCalculation,output_of='dftbase',tag='calc')
  qb.order_by({WorkCalculation:{'ctime':'desc'}})
  if len(qb.all()) > 0:
   step_path[2] =  qb.all()[last][0].out.retrieved.get_abs_path()+'/path/aiida.out'
   step_done[2] = True
 #4 cell_opt
 if step_done[2]:
  qb = QueryBuilder()
  qb.append(CifData, filters={'label': {'==':label}}, tag='init_structure')
  qb.append(WorkCalculation, filters={'label':{'==':'Isotherm'}}, output_of='init_structure', tag='isotherm')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kRobustGeoOptWorkChain'}}, output_of='isotherm', tag='robustgeoopt')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kCellOptWorkChain'}}, output_of='robustgeoopt', tag='cellopt')
  qb.append(WorkCalculation, filters={'label':{'==':'Cp2kDftBaseWorkChain'}}, output_of='cellopt', tag='dftbase')
  qb.append(JobCalculation,output_of='dftbase',tag='calc')
  qb.order_by({WorkCalculation:{'ctime':'desc'}})
  if len(qb.all()) > 0:
   step_path[3] =  qb.all()[last][0].out.retrieved.get_abs_path()+'/path/aiida.out'
   step_done[3] = True
 #print folders:
 if True:
    print('*** label = %s ***' %label)
    for i in range(4):
        if step_done[i]:
            print('%d) %s:\t%s' %(i,step_info[i],step_path[i]))
        else:
            print('%d) %s:\tINCOMPLETE' %(i,step_info[i]))

 #print stuff
 with open('parse_dftopt_'+label+'.out', 'w+') as fout:
  if step_done[3]:
   with redirect_stdout(fout):
    print_header()
    for i in step_path:
     print_steps(i)
