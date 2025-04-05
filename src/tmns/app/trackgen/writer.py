
#  Python Standard Libraries
from collections import namedtuple
from pathlib import Path

#  Project Libraries
import tmns.io.kml as kml

Missile_Entry = namedtuple( 'Missile_Entry', [ 'position' ] )

class Track_Writer:

    def __init__(self, output_base: str ):
        self.output_base = output_base

        self.missiles = {}

    def add_missile_entry( self,
                           midx: str,
                           unix_time: float,
                           position ):
        
        if not midx in self.missiles.keys():
            self.missiles[midx] = {}
        
        self.missiles[midx][unix_time] = Missile_Entry( position )
        


    def write_all(self):

        self.write_kml()
    
    def write_kml(self):

        #  Create KML writer
        writer = kml.Writer()

        #  Append all launch nodes
        missiles_dir = kml.Folder( 'missiles' )

        for midx in self.missiles.keys():
            
            missile_folder = kml.Folder( f'Missile: {midx}' )

            for unix_time in self.missiles[midx].keys():

                coord = kml.Point( lon      = self.missiles[midx][unix_time].position[0],
                                   lat      = self.missiles[midx][unix_time].position[1],
                                   elev     = self.missiles[midx][unix_time].position[2],
                                   alt_mode = kml.Altitude_Mode.ABSOLUTE )
                
                point = kml.Placemark( f'Time: {unix_time}',
                                       geometry = coord )
                missile_folder.append_node( point )

            missiles_dir.append_node( missile_folder )
                

        writer.add_node( missiles_dir )

        writer.write( self.output_base )