import struct
import numpy as np

# Reading Functions
def read_half(binary_file):
    s = binary_file.read(2)
    return struct.unpack('>h',s)[0]

def read_half_unsigned(binary_file):
    s = binary_file.read(2)
    return struct.unpack('>H',s)[0]

def read_word(binary_file):
    s = binary_file.read(4)
    return struct.unpack('>i',s)[0]

def read_byte(binary_file):
    return struct.unpack('B',binary_file.read(1))[0]

# Auxiliary function to map polar data to a cartesian plane
def polar_to_cart(polar_data, ini_theta, theta_step, range_step, x, y, order=3):

    from scipy.ndimage.interpolation import map_coordinates as mp

    # "x" and "y" are numpy arrays with the desired cartesian coordinates
    # we make a meshgrid with them
    X, Y = np.meshgrid(x, y)

    # Now that we have the X and Y coordinates of each point in the output plane
    # we can calculate their corresponding theta and range
    Tc = 180-np.degrees(np.arctan2(Y, X)).ravel() - ini_theta
    Rc = (np.sqrt(X**2 + Y**2)).ravel()

    # Negative angles are corrected
    Tc[Tc < 0] = 360 + Tc[Tc < 0]

    # Using the known theta and range steps, the coordinates are mapped to
    # those of the data grid
    Tc = Tc / theta_step
    Rc = Rc / range_step

    # An array of polar coordinates is created stacking the previous arrays
    coords = np.vstack((Tc, Rc))

    # To avoid holes in the 360 - 0 boundary, the last column of the data
    # copied in the begining
    polar_data = np.vstack((polar_data, polar_data[-1,:]))

    # The data is mapped to the new coordinates
    # Values outside range are substituted with 0s
    cart_data = mp(polar_data, coords, order=order, mode='constant', cval=0)

    # The data is reshaped and returned
    return(cart_data.reshape(len(y), len(x)).T)