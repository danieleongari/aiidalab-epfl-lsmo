from aiida.common.example_helpers import test_and_get_code  # noqa
from aiida.orm.data.structure import StructureData  # noqa
from aiida.orm.data.parameter import ParameterData  # noqa
from aiida.orm.data.base import Str
from aiida.orm import DataFactory
from aiida.work.run import submit

from ase.io import read
from workflows.charges import DdecCp2kChargesWorkChain
# data objects
ArrayData = DataFactory('array')
ParameterData = DataFactory('parameter')
StructureData = DataFactory('structure')

f = read('/home/daniele/Programs/aiida-database/frameworks/corecofs/13150N.cif')
structure = StructureData(ase=f)
structure.label='13150N'
structure.store()

cp2k_options = {
    "resources": {
        "num_machines": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,
    }

ddec_options = {
    "resources": {
        "num_machines": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,
    "withmpi": False,
    }
<<<<<<< HEAD
cp2k_code = test_and_get_code('cp2k-5.1@fidis-debug', expected_code_type='cp2k')
ddec_code = test_and_get_code('ddec@fidis-debug', expected_code_type='ddec')
submit(DdecCp2kChargesWorkChain,
        structure=structure,
        cp2k_code=cp2k_code,
        _cp2k_options=cp2k_options,
#        cp2k_parent_folder=load_node(5337),
        ddec_code=ddec_code,
        _ddec_options=ddec_options,
        ) 
