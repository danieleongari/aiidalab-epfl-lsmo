from __future__ import print_function
from aiida.orm.data.cif import CifData
from aiida.orm.calculation.work import WorkCalculation
import sys
from aiida.orm.data.parameter import ParameterData

print('#label POAV(cm^3/g) ASA(m^2/g) H(mol/kg/Pa) err uptake_p1(cm3stp/gr) p2 p3 p4 p5 err_p1 err_p2 err_p3 err_p4 err_p5')

with open('cif_list.txt') as finp:
 labels=finp.read().splitlines()
for label in labels:
     #Parse ZeoppBlockPocketsWorkChain.POAV_cm^3/g
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'ZeoppBlockPocketsWorkChain'}},
               output_of='isotherm',
               tag='zeopp')
     qb.append(ParameterData,
               output_of='zeopp',
               project=['attributes.POAV_cm^3/g'])
     POAV=qb.all()[0][0]

     #Parse ZeoppBlockPocketsWorkChain.ASA_m^2/g
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'ZeoppBlockPocketsWorkChain'}},
               output_of='isotherm',
               tag='zeopp')
     qb.append(ParameterData,
               output_of='zeopp',
               project=['attributes.ASA_m^2/g'])
     ASA=qb.all()[0][0]

     #Parse RaspaConvergeWorkChain.henry_coefficient_average
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'RaspaConvergeWorkChain'}},
               output_of='isotherm',
               tag='raspa')
     qb.append(ParameterData,
               output_of='raspa',
               project=['attributes.henry_coefficient_average'])
     H=qb.all()[0][0]

     #Parse RaspaConvergeWorkChain.henry_coefficient_dev
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'RaspaConvergeWorkChain'}},
               output_of='isotherm',
               tag='raspa')
     qb.append(ParameterData,
               output_of='raspa',
               project=['attributes.henry_coefficient_dev'])
     H_err=qb.all()[0][0]

     #Parse RaspaConvergeWorkChain.conversion_factor_molec_uc_to_cm3stp_gr
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'RaspaConvergeWorkChain'}},
               output_of='isotherm',
               tag='raspa')
     qb.append(ParameterData,
               output_of='raspa',
               project=['attributes.conversion_factor_molec_uc_to_cm3stp_gr'])
     conv_molecUC_cm3g=qb.all()[0][0]

     #Parse run_loading_raspa.loading_absolute_average
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'run_loading_raspa'}},
               output_of='isotherm',
               tag='raspa')
     qb.order_by({WorkCalculation:{'ctime':'asc'}})
     qb.append(ParameterData,
               output_of='raspa',
               project=['attributes.loading_absolute_average'])
     up_p1=qb.all()[4][0]*conv_molecUC_cm3g
     up_p2=qb.all()[3][0]*conv_molecUC_cm3g
     up_p3=qb.all()[2][0]*conv_molecUC_cm3g
     up_p4=qb.all()[1][0]*conv_molecUC_cm3g
     up_p5=qb.all()[0][0]*conv_molecUC_cm3g

     #Parse run_loading_raspa.loading_absolute_dev
     qb = QueryBuilder()
     qb.append(CifData,
               filters={'label': {'==':label}},
               tag='init_structure')
     qb.append(WorkCalculation,
               filters={'label':{'==':'Isotherm'}},
               output_of='init_structure',
               tag='isotherm')
     qb.append(WorkCalculation,
               filters={'label':{'==':'run_loading_raspa'}},
               output_of='isotherm',
               tag='raspa')
     qb.order_by({WorkCalculation:{'ctime':'asc'}})
     qb.append(ParameterData,
               output_of='raspa',
               project=['attributes.loading_absolute_dev'])
     up_p1_err=qb.all()[4][0]*conv_molecUC_cm3g
     up_p2_err=qb.all()[3][0]*conv_molecUC_cm3g
     up_p3_err=qb.all()[2][0]*conv_molecUC_cm3g
     up_p4_err=qb.all()[1][0]*conv_molecUC_cm3g
     up_p5_err=qb.all()[0][0]*conv_molecUC_cm3g

     print('%s %f %f %E %E %f %f %f %f %f %f %f %f %f %f'
           %(label,POAV,ASA,H,H_err,
             up_p1,up_p2,up_p3,up_p4,up_p5,
             up_p1_err,up_p2_err,up_p3_err,up_p4_err,up_p5_err))
