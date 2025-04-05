

#  Python Standard Libraries
import argparse
import configparser
import logging
import os

def valid_file( p ):

    if not os.path.exists( p ):
        raise Exception( f'Config file does not exist at {p}' )
    return p


class Options:
    '''
    Application configuration
    '''
    def __init__( self, cmd_args, cfg_args ):
        self.cmd_args = cmd_args
        self.cfg_args = cfg_args

        self.init_logging()


    def init_logging(self):

        logging.basicConfig( level = self.cmd_args.log_level )
        
        return logging.getLogger( 'trackgen' )

    @staticmethod
    def parse_command_line():

        #  create parser
        parser = argparse.ArgumentParser( description = 'Generate synthetic missile tracks.' )

        #  Configuration file
        parser.add_argument( '-c','--config',
                             dest = 'config_path',
                             required = True,
                             type = valid_file,
                             help = 'Path to configuration file.' )

        #  Generate config-file from scratch
        parser.add_argument( '-g', '--gen-config',
                             dest = 'gen_config',
                             default = False,
                             action = 'store_true',
                             required = False,
                             help = 'Generate config-file at -c path.' )

        #  Verbose logging
        parser.add_argument( '-v', '--verbose',
                             dest = 'log_level',
                             default = logging.INFO,
                             action = 'store_const',
                             const = logging.DEBUG,
                             help = 'Use verbose logging.' )
        
        return parser.parse_args()
    
    @staticmethod
    def parse_config_file( config_path ):

        parser = configparser.ConfigParser()

        parser.read( config_path )

        return parser
    
    @staticmethod
    def parse():

        cmd_args = Options.parse_command_line()

        if cmd_args.gen_config:
            Options.generate_config( cmd_args.config_path )
            exit(0)
        
        cfg_args = Options.parse_config_file( cmd_args.config_path )

        return Options( cmd_args,
                        cfg_args )
    
    @staticmethod
    def generate_config( config_path ):

        with open( config_path, 'w' ) as fout:

            fout.write( '# General Settings\n' )
            fout.write( '[general]\n' )
            fout.write( '\n' )
            fout.write( '#  Base path (no extension) for output files\n' )
            fout.write( 'output_base=demo.01\n' )
            fout.write( '#  Number of missile events\n' )
            fout.write( 'number_missiles=1\n' )
            fout.write( '\n' )
            fout.write( '#  Timing Characteristics\n' )
            fout.write( 'start_time_unix=0\n' )
            fout.write( 'simulation_time_secs=500\n' )
            fout.write( 'step_time_ms=500\n' )
            fout.write( '\n' )

            #  Write missile event
            fout.write( '# First missile event\n' )
            fout.write( '[missile_1]\n' )
            fout.write( '\n' )
            fout.write( '# ID Value\n' )
            fout.write( 'id=1\n' )
            fout.write( '\n' )
            fout.write( '#  Motion Model\n' )
            fout.write( 'motion_type=straight\n' )
            fout.write( '\n' )
            fout.write( '#  Launch Position\n' )
            fout.write( 'launch_position_latitude=39.545218\n')
            fout.write( 'launch_position_longitude=-104.844892\n')
            fout.write( 'launch_position_elevation=1806\n')
            fout.write( '\n' )
            fout.write( '# Missile Characteristics\n' )
            fout.write( 'missile_mass_kg=900\n' )
            fout.write( 'missile_radius_m=0.25\n' )
            fout.write( 'missile_thrust_kN=107873.15\n' )
            fout.write( 'missile_drag_coefficient=0.05\n' )
            fout.write( 'air_mass_density=1.2\n' )
            fout.write( '\n' )
            fout.write( '# Launch Characteristics\n' )
            fout.write( 'launch_pitch_degrees=60\n' )
            fout.write( 'launch_yaw_degrees=-45\n' )
            fout.write( 'start_time_offset_sec=10\n' )
            fout.write( 'burn_time_sec=60\n' )
            fout.write( '\n' )
