

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
            fout.write( '#  Number of missile events\n' )
            fout.write( 'number_missiles=1\n' )
            fout.write( '\n' )

            #  Write missile event
            fout.write( '# First missile event\n' )
            fout.write( '[missile_1]\n' )
            fout.write( '\n' )
            fout.write( '# ID Value\n' )
            fout.write( 'id=1\n' )
            fout.write( '\n' )
            fout.write( '#  Launch Position\n' )
            fout.write( 'launch_position_latitude=39.545218\n')
            fout.write( 'launch_position_longitude=-104.844892\n')
            fout.write( 'launch_position_elevation=1806\n')
            fout.write( '\n' )