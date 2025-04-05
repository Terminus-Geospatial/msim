
#  Python Standard Libraries
import logging

#  Pyproj
from pyproj import CRS
from pyproj import Transformer
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

#  Numerical Python
import numpy as np


def geographic_to_ecf( coord = None,
                       lat = None,
                       lon = None,
                       elev = None ):

    if coord is None:
        coord = np.array( [lon, lat, elev], dtype = np.float64 )

    #  Force array to be a single array
    coord = coord.flatten()

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
    
    if coord is None:
        coord = [x, y, z]
    
    # force single dimension array
    coord = coord.flatten()

    transformer = Transformer.from_crs( { 'proj':  'geocent', 
                                          'ellps': 'WGS84',
                                          'datum': 'WGS84' },
                                        { 'proj':  'latlong', 
                                          'ellps': 'WGS84',
                                          'datum': 'WGS84' } )
    
    x, y, z = transformer.transform( coord[0], coord[1], coord[2], radians = False )

    return np.array( [[x],[y],[z]], dtype = np.float64 )

def get_ecf_forward_vector( point1_lla, forward_axis_lla ):

    #  Convert lla to ECF
    point1_ecf = geographic_to_ecf( point1_lla.reshape(3) )

    #  Create 2nd point
    point2_lla = point1_lla.reshape(3) + forward_axis_lla.reshape(3)
    point2_ecf = geographic_to_ecf( point2_lla.reshape(3) )

    return (point2_ecf - point1_ecf).reshape((3,1))


def utm_grid_zone( lla_coord ):
    
    lla_coord = lla_coord.flatten()
    print( list( lla_coord ) )
    utm_crs_list = query_utm_crs_info(
          datum_name       = "WGS 84",
          area_of_interest = AreaOfInterest(
              west_lon_degree  = lla_coord[0],
              south_lat_degree = lla_coord[1],
              east_lon_degree  = lla_coord[0],
              north_lat_degree = lla_coord[1],
          ),
    )
    print( 'AAAAAA: ', utm_crs_list )
    utm_crs = CRS.from_epsg(utm_crs_list[0].code)
    print( f'VALUE: ', utm_crs )
