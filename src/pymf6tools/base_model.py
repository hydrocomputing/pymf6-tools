"""Base model data.

Data for a basic flow model build with `flopy`.
Changing the data allows to quickly create a modified model.
Note: Not all packages are supported, yet.

Assumptions:

1. The first stress period is steady state.
2. Currently, only CHD boundary conditions are supported.
3. For all not supplied values `flopy` default values will be used.
"""


import sys
import numpy as np
from copy import deepcopy


# Function to calculate the constant heads automatically  
# def add_chd_to_dict(base_model_data):
#     chd_value_left = base_model_data.get('chd_value_left')
#     chd_value_right = base_model_data.get('chd_value_right')
#     # Loop to reproduce the matrix for the CHD package 
#     chd = []
#     for col, chd_value in zip([0, base_model_data['ncol']], [chd_value_left, chd_value_right]):
#         for lay in range(base_model_data['nlay']):
#             for row in range(0, base_model_data['nrow'] - 1):
#                 chd.append([(lay, row, col), chd_value])
#     return chd

# Function to calculate the heads automatically for transport package
# def add_chd_to_dict_transp(base_transport_model_data, base_model_data):
#     chd_value_left = base_model_data.get('chd_value_left')
#     chd_value_right = base_model_data.get('chd_value_right')
#     cnc_left = base_transport_model_data.get('concentration_source_wall')
#     cnc_right = 0 
#     # Loop to reproduce the matrix for the CHD package
#     chd = []
#     for col, chd_value, cnc in zip([0, base_model_data['ncol']],
#                                     [chd_value_left, chd_value_right], 
#                                     [cnc_left, cnc_right]):
#         for lay in range(base_model_data['nlay']):
#             for row in range(0, base_model_data['nrow'] - 1):
#                 chd.append([(lay, row, col), chd_value, cnc])

BASE_MODEL_DATA = {
    #  flopy.mf6.ModflowTdis
    'times': (
        10.0,  # perlen (double) is the length of a stress period.
        120,   # nstp (integer) is the number of time steps in a stress period.
        1.0,   # tsmult (double) is the multiplier for the length of successive
               # time steps.
    ),
    'time_units': 'DAYS',
    'length_units': 'meters',
    'repeat_times': 3,  # nper = repeat_times + 1
    #  flopy.mf6.ModflowGwfdis
    'nrow': 30,
    'ncol': 20,
    'nlay': 3,
    'delr': 5.0,
    'delc': 5.0,
    'top': 15.0,
    'botm': [-5.0, -10.0, -15.0],
    #  flopy.mf6.ModflowGwfnpf
    'k': [0.5, 0.000006, 0.5],  # initial value of k
    'k33': [0.1, 0.002, 0.3],  # vertical anisotropy
    #  flopy.mf6.ModflowGwfsto
    'sy': 0.2,
    'ss': 0.000001,
    'initial_head': 10.0,
    # flopy.mf6.ModflowGwfchd
    # default values if function not running  
    'chd_value_left': 10,
    'chd_value_right': 12,
    'chd': [
       [(0, 0, 0), 10.],
       [(0, 1, 0), 10.],
       [(0, 2, 0), 10.],
       [(0, 3, 0), 10.],
       [(0, 4, 0), 10.],
       [(0, 5, 0), 10.],
       [(0, 6, 0), 10.],
       [(0, 7, 0), 10.],
       [(0, 8, 0), 10.],
       [(0, 9, 0), 10.],
       [(0, 10, 0), 10.],
       [(0, 11, 0), 10.],
       [(0, 12, 0), 10.],
       [(0, 13, 0), 10.],
       [(0, 14, 0), 10.],
       [(0, 15, 0), 10.],
       [(0, 16, 0), 10.],
       [(0, 17, 0), 10.],
       [(0, 18, 0), 10.],
       [(0, 19, 0), 10.],
       [(0, 20, 0), 10.],
       [(0, 21, 0), 10.],
       [(0, 22, 0), 10.],
       [(0, 23, 0), 10.],
       [(0, 24, 0), 10.],
       [(0, 25, 0), 10.],
       [(0, 26, 0), 10.],
       [(0, 27, 0), 10.],
       [(0, 28, 0), 10.],
       [(0, 29, 0), 10.],
       [(0, 0, 19), 10.5],
       [(0, 1, 19), 10.5],
       [(0, 2, 19), 10.5],
       [(0, 3, 19), 10.5],
       [(0, 4, 19), 10.5],
       [(0, 5, 19), 10.5],
       [(0, 6, 19), 10.5],
       [(0, 7, 19), 10.5],
       [(0, 8, 19), 10.5],
       [(0, 9, 19), 10.5],
       [(0, 10, 19), 10.5],
       [(0, 11, 19), 10.5],
       [(0, 12, 19), 10.5],
       [(0, 13, 19), 10.5],
       [(0, 14, 19), 10.5],
       [(0, 15, 19), 10.5],
       [(0, 16, 19), 10.5],
       [(0, 17, 19), 10.5],
       [(0, 18, 19), 10.5],
       [(0, 19, 19), 10.5],
       [(0, 20, 19), 10.5],
       [(0, 21, 19), 10.5],
       [(0, 22, 19), 10.5],
       [(0, 23, 19), 10.5],
       [(0, 24, 19), 10.5],
       [(0, 25, 19), 10.5],
       [(0, 26, 19), 10.5],
       [(0, 27, 19), 10.5],
       [(0, 28, 19), 10.5],
       [(0, 29, 19), 10.5],
        ],
    #, 
    'transport': False,
    'river': False,
} 

#BASE_MODEL_DATA['chd'] = add_chd_to_dict(BASE_MODEL_DATA)

BASE_TRANSPORT_MODEL_DATA = {
    'wells':{},
    'initial_concentration': 1,
    'concentration_source_wall':0,
    'cnc': [
        [(0, 15, 4), 100.],
        [(0, 16, 4), 100.], 
        [(1, 15, 4), 100.],
        [(1, 16, 4), 100.] # cell_id, conc (const)
    ],
    'scheme': 'UPSTREAM', #'TVD',  # or 'UPSTREAM'
    'longitudinal_dispersivity': 1.0,
    # Ratio of transverse to longitudinal dispersitivity
    'dispersivity_ratio': 1.0,
    'porosity': 0.35,
    'obs': None,
    'nrow': 30,
    'ncol': 20,
    'nlay': 3,
    # default values if function not running
    'chd': [
       [(0, 0, 0), 10., 1.],
       [(0, 1, 0), 10., 1.],
       [(0, 2, 0), 10., 1.],
       [(0, 3, 0), 10., 1.],
       [(0, 4, 0), 10., 1.],
       [(0, 5, 0), 10., 1.],
       [(0, 6, 0), 10., 1.],
       [(0, 7, 0), 10., 1.],
       [(0, 8, 0), 10., 1.],
       [(0, 9, 0), 10., 1.],
       [(0, 10, 0), 10., 1.],
       [(0, 11, 0), 10., 1.],
       [(0, 12, 0), 10., 1.],
       [(0, 13, 0), 10., 1.],
       [(0, 14, 0), 10., 1.],
       [(0, 15, 0), 10., 1.],
       [(0, 16, 0), 10., 1.],
       [(0, 17, 0), 10., 1.],
       [(0, 18, 0), 10., 1.],
       [(0, 19, 0), 10., 1.],
       [(0, 20, 0), 10., 1.],
       [(0, 21, 0), 10., 1.],
       [(0, 22, 0), 10., 1.],
       [(0, 23, 0), 10., 1.],
       [(0, 24, 0), 10., 1.],
       [(0, 25, 0), 10., 1.],
       [(0, 26, 0), 10., 1.],
       [(0, 27, 0), 10., 1.],
       [(0, 28, 0), 10., 1.],
       [(0, 29, 0), 10., 1.],
       [(0, 0, 19), 10.5, 1.],
       [(0, 1, 19), 10.5, 1.],
       [(0, 2, 19), 10.5, 1.],
       [(0, 3, 19), 10.5, 1.],
       [(0, 4, 19), 10.5, 1.],
       [(0, 5, 19), 10.5, 1.],
       [(0, 6, 19), 10.5, 1.],
       [(0, 7, 19), 10.5, 1.],
       [(0, 8, 19), 10.5, 1.],
       [(0, 9, 19), 10.5, 1.],
       [(0, 10, 19), 10.5, 1.],
       [(0, 11, 19), 10.5, 1.],
       [(0, 12, 19), 10.5, 1.],
       [(0, 13, 19), 10.5, 1.],
       [(0, 14, 19), 10.5, 1.],
       [(0, 15, 19), 10.5, 1.],
       [(0, 16, 19), 10.5, 1.],
       [(0, 17, 19), 10.5, 1.],
       [(0, 18, 19), 10.5, 1.],
       [(0, 19, 19), 10.5, 1.],
       [(0, 20, 19), 10.5, 1.],
       [(0, 21, 19), 10.5, 1.],
       [(0, 22, 19), 10.5, 1.],
       [(0, 23, 19), 10.5, 1.],
       [(0, 24, 19), 10.5, 1.],
       [(0, 25, 19), 10.5, 1.],
       [(0, 26, 19), 10.5, 1.],
       [(0, 27, 19), 10.5, 1.],
       [(0, 28, 19), 10.5, 1.],
       [(0, 29, 19), 10.5, 1.],
        ],

}

#BASE_TRANSPORT_MODEL_DATA['chd'] = add_chd_to_dict_transp(BASE_TRANSPORT_MODEL_DATA, BASE_MODEL_DATA)

# Set the number of river cells in the model 
NRIV = 27

BASE_RIVER_MODEL_DATA = {
    'river_spd': { 
        'rivlay': [0] * NRIV,
        'rivrow': [1, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 7, 8, 8, 9, 10, 11, 11, 12, 13, 11, 14, 14, 14, 15, 16, 17],
        'rivcol': [0, 2, 1, 2, 3, 3, 4, 5, 6, 7, 7, 8, 9, 9, 10, 11, 12, 11, 13, 14, 12, 15, 16, 17, 18, 19, 19],
        'rivstg': np.linspace(13, 14, NRIV), 
        'rivbot': np.linspace(7, 10, NRIV), 
        'rivcnd': [0.05] * NRIV  
        } , 
                     
    'river_boundnames': None, 
    'obs_dict': None, # dict, 
    'tsdict': None, # dict,
    'cond': None, 
}         

BASE_WELL_MODEL_DATA = {
    'wells': {
        'wel_out': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 10, 4)},
        'wel_out1': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 12, 5)},
        'wel_out2': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 14, 6)},
              },

}

EXAMPLE_1_DATA = {
    'wells': {
        'wel_out': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 8, 4)},
        'wel_out1': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 13, 8)},
        'wel_out2': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 3, 9)},
        'wel_out3': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 9, 9)},
        'wel_out4': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 12, 7)},
        'wel_out5': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 3, 4)},
              },

}

EXAMPLE_3_DATA = {
    'wells': {
        'wel_out': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 10, 4)},
        'wel_out1': {'q': (-0.05, -0.5, -0.05), 'coords': (2, 12, 5)},
        'wel_out2': {'q': (-0.05, -0.5, -0.05), 'coords': (0, 14, 6)},
              },

}

def make_model_data(
        specific_model_data,
        base_model_data=BASE_MODEL_DATA,
        base_transport_model_data=BASE_TRANSPORT_MODEL_DATA,
        base_river_model_data=BASE_RIVER_MODEL_DATA, 
        base_well_model_data=BASE_WELL_MODEL_DATA, 
        example_1_data=EXAMPLE_1_DATA, 
        example_3_data=EXAMPLE_3_DATA
    ):

    """Make model data.

    specific_model_data - dictionary with data specific for the current model
                          will merged with `base_model_data`
                          existing keys in `base_model_data` will be overridden
    base_model_data - dictionary with basic model data defaults to
                      `BASE_MODEL_DATA`
    """
    base_model_data=deepcopy(base_model_data)
    base_river_model_data=deepcopy(base_river_model_data)
    base_transport_model_data=deepcopy(base_transport_model_data)
    base_well_model_data=deepcopy(base_well_model_data)
    example_1_data=deepcopy(example_1_data)
    example_3_data=deepcopy(example_3_data)
    
    
    if specific_model_data['transport']:
        base_model_data.update(base_transport_model_data)
    if specific_model_data['river_active']:
        base_model_data.update(base_river_model_data)
    if specific_model_data['wells_active']:
        base_model_data.update(base_well_model_data)
    if specific_model_data['example_1_data']:
        base_model_data.update(example_1_data)
    if specific_model_data['example_3_data']:
        base_model_data.update(example_3_data)


    # old way up to Python 3.8
    if sys.version_info[:2] < (3, 9):
        return {**base_model_data, **specific_model_data}
    # new way starting from Python 3.9
    return base_model_data | specific_model_data
