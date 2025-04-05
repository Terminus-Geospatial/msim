

#  Pyproj
from pyproj import Transformer

#  Numerical Python
import numpy as np

def geographic_to_ecf( coord = None,
                       lat = None,
                       lon = None,
                       elev = None ):

    if coord is None:
        coord = [lon, lat, elev]

    transformer = Transformer.from_crs( { 'proj':  'latlong', 
                                          'ellps': 'WGS84',
                                          'datum': 'WGS84' },
                                        { 'proj':  'geocent', 
                                          'ellps': 'WGS84',
                                          'datum': 'WGS84' },
                                        always_xy = True )
    
    x, y, z = transformer.transform( coord[0], coord[1], coord[2] )

    return np.array( [[x],[y],[z]], dtype = np.float64 )

def ecf_to_geographic( coord = None,
                       x = None,
                       y = None,
                       z = None ):
    
    if coord == None:
        coord = [x, y, z]

    transformer = Transformer.from_crs( { 'proj':  'geocent', 
                                          'ellps': 'WGS84',
                                          'datum': 'WGS84' },
                                        { 'proj':  'latlong', 
                                          'ellps': 'WGS84',
                                          'datum': 'WGS84' },
                                        always_xy = True )
    
    x, y, z = transformer.transform( coord[0], coord[1], coord[2] )

    return np.array( [[x],[y],[z]], dtype = np.float64 )

def get_ecf_forward_vector( point1_lla, forward_axis_lla ):

    #  Convert lla to ECF
    point1_ecf = geographic_to_ecf( point1_lla )

    #  Create 2nd point
    point2_lla = point1_lla + forward_axis_lla
    point2_ecf = geographic_to_ecf( point2_lla )

    return point2_ecf - point1_ecf
