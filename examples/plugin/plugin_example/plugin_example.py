import utils
import numpy as np

def example_func(a, b):
    """Function to calculate (a+b) + (a*b) then return as numpy array

    Args:
        a (_type_): _description_
        b (_type_): _description_
    """
    return np.array(utils.add(utils.add(a, b), utils.mul(a, b)))
