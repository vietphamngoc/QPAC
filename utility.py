import numpy as np
import pickle
import random
import os


def ones_to_str(ones: set, n: int)->str:
    """
    Function to transform the set of positions of '1's into the corresponding binary string.

    Arguments:
        - ones: set, the set of positions
        - n: int, the length of the resulting binary string

    Returns:
        The binary string of length n where the '1's are at the positions collected in ones
    """
    binary = ["0" for i in range(n)]
    for i in ones:
        binary[i] = "1"
    return("".join(binary))


def str_to_ones(string: str)->set:
    """
    Function to transform a binary string into a set collecting the positions of the '1's.

    Arguments:
        - string: str, the binary string

    Returns:
        The set collecting the positions of the '1's in string
    """
    ones = [i for i in range(len(string)) if string[i] == "1"]
    return(set(ones))


def get_custom_params(n: int, u: str, angle: float)->list:
    """
    Function to generate custom parameters for the oracle.

    Arguments:
        - n: int, the dimension of the input space
        - u: str, the string controlling the placement of the specified angle
        - angle: float, the custom angle

    Returns:
        - A list containing angles to build the amplitudes in the oracle
    """
    if len(u) != n:
        raise ValueError(f"Length of u is not {n}")
    params = []
    for i in range(n):
        if u[i] == "1":
            params.append(angle)
        else:
            params.append(np.pi/2)
    return(params)


def get_parameters(n: int):
    """
    Function to save parameters in a file, if this file exists, retrieve the saved parameters.

    Arguments:
        - n: int, the dimension of the input space

    Returns:
        - A list containing angles to build the amplitudes in the oracle
    """
    directory = f"{os.getcwd()}/parameters"

    if not os.path.exists(directory):
        os.makedirs(directory)

    file = f"{directory}/parameters_{n}.txt"

    if os.path.exists(file):
        with open(file, "rb") as f:
            params = pickle.load(f)

    else :
        params = []
        for i in range(n):
            params.append(random.random()*np.pi)
        with open(file, "wb") as f:
            pickle.dump(params, f)

    return(params)


def get_functions(n: int, number: int=0):
    """
    Function to save a set of target concepts in a file, if this file exists, retrieve the functions.

    Arguments:
        - n: int, the dimension of the input space
        - number: int (default=0), the number of functions in the set. If 0, then it is the whole class of concepts

    Returns:
        - A list containing the functions
    """
    if number > 2**n:
        raise ValueError(f"number should not be greater than {2**n}")

    directory = f"{os.getcwd()}/functions"

    if not os.path.exists(directory):
        os.makedirs(directory)

    file = f"{directory}/functions_{n}_{number}.txt"

    if os.path.exists(file):
        with open(file, "rb") as f:
            U = pickle.load(f)

    else:
        U = []
        if number == 0:
            for i in range(2**n):
                U.append(np.binary_repr(i, n))
        else:
            for i in range(number):
                u = random.randint(0, 2**n-1)
                while u in U:
                    u = random.randint(0, 2**n-1)
                U.append(np.binary_repr(u, n))

        with open(file, "wb") as f:
            pickle.dump(U, f)

    return(U)
