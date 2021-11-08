class OFI:
    def __init__(self, bc_file_location):
        self.bc_file_location = bc_file_location

    # Write the boundary conditions to the boundary conditions text file
    # The variable names can be rewritten to anything you would like, as long as the order stays the same. If you need to add an extra variable, let me know.
    def write_bc(self, inlet_temp: float, mid_temp: float, outlet_temp: float, inlet_press:float, mid_press:float, outlet_press:float):
        pass

    # Start the case using the boundary conditions currently written in the BC file (I'm assuming this would be done with a command line)
    def start_case(self):
        pass

    # Returns a bool of whether the solution has converged yet or not. (In other words, should the mass flow valve be set to the mdot from get_mdot() )
    def solution_has_converged(self):
        has_converged = False


        return has_converged
    
    # Returns (1 - (mdot_new - mdot_old)/mdot_new) This will be displayed on OpenFOAM progress plot.
    def get_solver_progress(self):
        solver_progress = 0
        return solver_progress

    # Parses the results file from OpenFOAM and returns the mdot. I think if you wanted to save other values from the OpenFOAM results file, this would be the method to do that.
    def get_mdot(self):
        mdot = 0

        return mdot