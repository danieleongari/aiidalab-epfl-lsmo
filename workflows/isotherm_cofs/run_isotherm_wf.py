import os
import numpy as np
from aiida.common.example_helpers import test_and_get_code  # noqa
from aiida.orm import CalculationFactory, DataFactory
from aiida.orm.data.base import Float, Str
from aiida.work.run import submit

from ase.io import read
from workflows.isotherm_cofs import Isotherm

from glob import glob
from os import path

# data objects
ArrayData = DataFactory('array')
ParameterData = DataFactory('parameter')
CifData = DataFactory('cif')

#cp2k_code = test_and_get_code('cp2k-5.1@fidis-debug', expected_code_type='cp2k')
cp2k_code = test_and_get_code('cp2k-5.1@fidis', expected_code_type='cp2k')
#ddec_code = test_and_get_code('ddec@fidis-debug', expected_code_type='ddec')
ddec_code = test_and_get_code('ddec@fidis', expected_code_type='ddec')
zeopp_code = test_and_get_code('zeopp@deneb', expected_code_type='zeopp.network')
raspa_code = test_and_get_code('raspa@deneb', expected_code_type='raspa')

cp2k_options = {
    "resources": {
        "num_machines": 2,
    },
    "max_wallclock_seconds": 24 * 60 * 60,
    }

ddec_options = {
    "resources": {
        "num_machines": 1,
    },
    "max_wallclock_seconds": 5 * 60 * 60,
    "withmpi": False,
    }

zr_options = {
    "resources": {
        "num_machines": 1,
        "tot_num_mpiprocs": 1,
    },
    "max_wallclock_seconds": 72 * 60 * 60,
    "withmpi": False,
    }

raspa_parameters = ParameterData(dict={
        "GeneralSettings":
        {
        "SimulationType"                   : "MonteCarlo",
        "NumberOfCycles"                   : 100000,
        "NumberOfInitializationCycles"     : 10000,

        "PrintEvery"                       : 1000,

        "ChargeMethod"                     : "None", #switched on if _usecharges=True
        "CutOff"                           : 12.0,
        "Forcefield"                       : "LSMO_UFF-TraPPE",

        "Framework"                        : 0,
        "UnitCells"                        : "1 1 1", #this will be expanded according to CutOff 
        "HeliumVoidFraction"               : 0.0, #will be changed with POAV

        "ExternalTemperature"              : 298.0,
        "ExternalPressure"                 : 0.0, #modified to compute isotherms
        },
        "Component":
        [{
        "MoleculeName"                     : "CO2",
        "MoleculeDefinition"               : "TraPPE",
        "TranslationProbability"           : 0.5,
        "RotationProbability"              : 0.5,
        "ReinsertionProbability"           : 0.5,
        "SwapProbability"                  : 1.0,
        "CreateNumberOfMolecules"          : 0,
        }],
        })

pressures = ArrayData()
pressures.set_array("pressures", np.array([0.01e5, 0.05e5, 0.1e5, 0.15e5, 0.2e5]))

all_structures = glob(path.abspath("/home/daniele/Programs/aiida-database/frameworks/corecofs/13*N.cif"))
for s in all_structures:
    structure = CifData(file=s)
    structure.label = s.split('/')[-1].split('.')[0] #label = cifname
    structure.store()

    submit(Isotherm,
        structure=structure,
        probe_molecule=ParameterData(dict={"sigma":1.525}),
        pressures=pressures,
        min_cell_size=Float(10.0), 
        cp2k_code=cp2k_code,
        _cp2k_options=cp2k_options,
        ddec_code=ddec_code,
        _ddec_options=ddec_options,
        zeopp_code=zeopp_code,
        _zeopp_options=zr_options,
        raspa_code=raspa_code,
        raspa_parameters=raspa_parameters,
        _raspa_options=zr_options,
        _usecharges=True,
        _guess_multiplicity=True,
        _label='Isotherm',
        )
