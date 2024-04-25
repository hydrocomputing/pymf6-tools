from pymf6.mf6 import MF6
from pymf6.api import States
import os 
from pathlib import Path 

dir = os.getcwd()
model_name = "example_1"
model_path = os.path.abspath(os.path.join(dir, 'models', model_name))
print(model_path)
nam_file = os.path.join(model_path, 'mfsim.nam')
nam_file

def run_model(nam_file):
    print('xpx')
    # Initialize the MF6 model using the provided nam file 
    mf6 = MF6(nam_file=nam_file)
    print('xzx')
    # Set tolerance and head limit values for control 
    tolerance = 0.01
    head_limit = 0.5
    lower_limit = head_limit - tolerance
    upper_limit = head_limit + tolerance
    
    # Variable to track if the watre level has been below the lower limit 
    been_below = False
    
    # List of wells with coordinates (layer, row, col)
    well_coords_list = [(0, 8, 4), (0, 13, 8), (0, 3, 9), (0, 9, 9), (0, 12, 7) ,(0, 3, 4)]
    
    # Dictionary to store information about each well 
    wells_info = {coords: {'been_below': False} for coords in well_coords_list}
    
    print('xx')
    # Main simulation loop 
    for sim, state in mf6.loop:
        print('xy')
        # Check if the start of a new time step 
        if state == States.timestep_start:
            # Get the model object 
            ml = sim.get_model()
            
            # Check if stress period (kper == 2)
            if ml.kper == 2:
                # Iteration over each well 
                for wel_coords, well_info in wells_info.items():
                    # Retrieve pumping rate and well head information
                    pumping = ml.wel.stress_period_data["flux"]
                    wel_head = ml.X.__getitem__(wel_coords)
                    wel_bc = ml.wel.stress_period_data

                    # Adjust pumping rtae if the well head is below the lower limit 
                    if wel_head <= lower_limit:
                        wel_bc["flux"] = pumping * 0.9
                        been_below = True
                    # Adjust pumping rate if the well head is above the limit 
                    elif been_below and wel_head >= upper_limit:
                        wel_bc["flux"] = pumping * 1.1

if __name__ == '__main__':
    run_model(model_path)
    print('done')
