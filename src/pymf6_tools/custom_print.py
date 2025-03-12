"""
Custom print function.

Prints MF6 output line "in place".
"""


class CustomPrint:
    """
    Custom print of MF6 output.

    This prints the line containing 'Solving:' in place, i.e. creating
    an up-counting effect for number for the time step. The last time
    step in each stress period will remain and the print for the next
    stress period will continue on the next line.
    """

    def __init__(self, show_each_stress_period=True):
        self.show_each_stress_period = show_each_stress_period
        self.one_line_mode = False
        self.last_stress_period = 0

    def __call__(self, line):
        """Callable used by flopy for printing."""
        if 'executable' in line:
            return
        if 'Solving:' in line:
            if self.show_each_stress_period:
                stress_period = int(line.split('Stress period:',)[1].split()[0])
                if stress_period > self.last_stress_period:
                    self.last_stress_period += 1
                    print()
            # don't add a line break to create up-counting number effect
            print(line, end='\r')
            self.one_line_mode = True
        else:
            if self.one_line_mode:
                self.one_line_mode = False
                # add line break
                print()
            print(line)
